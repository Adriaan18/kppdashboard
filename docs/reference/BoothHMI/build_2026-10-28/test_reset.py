import sys, random, copy
sys.path.insert(0, '.')
import harness as H, plcsim
H.load_all()
sr = H.booth.safetyreset
LOGGED = []
class FakeHist(object):
    def logAction(self, *a, **k):
        LOGGED.append((a, k)); return True
real_hist = H.forensics.alarmHistory

def run(area, setup, latency=(20, 150), phase=None, pulse_override=None, pre=None, hist=True, who='tester', during=None):
    H.TAGS.clear(); H.WRITES.clear(); H.GLOBALS.clear(); H.CLOCK.listeners[:] = []; H.WRITE_FAIL.clear()
    H.WRITE_LIE.clear(); LOGGED[:] = []
    H.forensics.alarmHistory = FakeHist() if hist else real_hist
    igs = sr.REACH[area]
    plc = plcsim.PLC(igs, {area: sr.RB_TAG[area]}, phase)
    for ig, kw in setup.items():
        plc.igs[ig].setup(**kw)
    plc.publish()
    H.WRITE_LATENCY = list(latency)
    saved = dict(sr.PULSE_MS)
    if pulse_override is not None:
        sr.PULSE_MS.clear(); sr.PULSE_MS.update(pulse_override)
    if pre:
        pre(plc)
    t0 = H.CLOCK.now()
    if during:
        H.CLOCK.listeners.append(lambda t: during(t - t0))
    res = sr.press(area, who, 'test-station')
    dt = H.CLOCK.now() - t0
    sr.PULSE_MS.clear(); sr.PULSE_MS.update(saved)
    rec = H.GLOBALS[sr._KEY].get('rec:' + area)
    H.CLOCK.advance(1500)
    plc.stop()
    return plc, rec, res, dt

def states(plc):
    return dict((n, ('EN' if g.en else ('FLT' if g.fault else ('ISO' if g.iso else 'off')))) for n, g in plc.igs.items())

fails = 0
def expect(cond, msg):
    global fails
    if not cond:
        fails += 1
        print('  FAIL:', msg)

# --- 1. one run per area, mixed starting states
cases = {
    'SDB': {'SDB_IG1': dict(fault=True), 'SDB_IG2': dict(), 'SDB_IG3': dict(en=True), 'SDB_IG4': dict(isolator=True)},
    'GRA': {'GRA_IG1': dict(fault=True), 'GRA_IG2': dict(), 'GRA_IG3': dict(isolator=True)},
    'COS': {'COS_IG1': dict(fault=True), 'COS_IG2': dict(), 'TNB_IG1': dict(en=True), 'TNB_IG2': dict(fault=True),
            'TNB_IG3': dict(), 'TNB_IG4': dict(), 'TNB_IG5': dict(), 'CHP_IG7': dict()},
    'TNB': {'TNB_IG1': dict(fault=True), 'TNB_IG2': dict(), 'TNB_IG3': dict(), 'TNB_IG4': dict(gates=False), 'TNB_IG5': dict()},
    'CHP': {'CHP_IG1': dict(fault=True), 'CHP_IG2': dict(), 'CHP_IG3': dict(), 'CHP_IG4': dict(), 'CHP_IG5': dict(),
            'CHP_IG6': dict(), 'CHP_IG7': dict()},
    'HOG': {'HOG_IG1': dict(fault=True), 'HOG_IG2': dict(), 'HOG_IG3': dict(), 'HOG_IG4': dict(), 'HOG_IG5': dict(cause=True)},
}
blocked = {'SDB': {'SDB_IG4': 'ISO'}, 'GRA': {'GRA_IG3': 'ISO'}, 'TNB': {'TNB_IG4': 'off'}, 'HOG': {'HOG_IG5': 'FLT'}}
print('== 1. one press per area')
for area, setup in cases.items():
    plc, rec, res, dt = run(area, setup)
    st = states(plc)
    print('%-4s %-7s %-5s %.1f s  %s  | %s' % (area, res, rec['step'], dt / 1000.0, rec['msg'], st))
    for ig, s in st.items():
        want = blocked.get(area, {}).get(ig, 'EN')
        expect(s == want, '%s %s: %s, want %s' % (area, ig, s, want))
    expect(plc.timeouts == 0, '%s: PLC 5 s timeout fired' % area)
    expect(H.TAGS[sr.RB_TAG[area]][0] is False, '%s: reset bit left on' % area)
    expect(len(LOGGED) >= 1, 'history row logged')

# --- 2. Grading with a fixed 1.0 s gap (the 2.0 s pulse ignored) - the tap must be lost (control)
print('== 2. control: GRA with a 0.5 s pulse assumed (gap 1.0 s)')
lost = 0
random.seed(3)
for i in range(100):
    plc, rec, res, dt = run('GRA', {'GRA_IG1': dict(), 'GRA_IG2': dict(), 'GRA_IG3': dict()}, pulse_override={})
    if states(plc)['GRA_IG2'] != 'EN':
        lost += 1
print('GRA with a 1.0 s gap: the group reset was lost in %d of 100 presses (per-area gap: 0 of 150 below)' % lost)
expect(lost > 0, 'control: a 1.0 s gap should lose GRA resets')

# --- 3. fault cause still there
print('== 3. fault cause still present (COS_IG1)')
plc, rec, res, dt = run('COS', {'COS_IG1': dict(fault=True, cause=True)})
print('cause present:', rec['msg'], states(plc))
expect(states(plc)['COS_IG1'] == 'FLT' and not rec['ok'], 'fault with cause must stay')

# --- 4. reset bit already held elsewhere / write failure / DDB / busy / stale lock
print('== 4. guards')
plc, rec, res, dt = run('SDB', {}, pre=lambda p: H.TAGS.__setitem__(sr.RB_TAG['SDB'], [True, H.CLOCK.now()]))
print('held elsewhere:', res, rec['step'], rec['msg'])
expect(rec['step'] == 'failed' and 'another screen' in rec['msg'], 'held elsewhere refused')
expect(H.TAGS[sr.RB_TAG['SDB']][0] is True or plc.timeouts == 1, 'did not touch a bit it did not set')

plc, rec, res, dt = run('SDB', {}, pre=lambda p: H.WRITE_FAIL.add(sr.RB_TAG['SDB']))
print('write fails:', res, rec['step'], rec['msg'])
expect(rec['step'] == 'failed', 'write failure reported')

print('DDB:', sr.press('DDB', 'x', 'y'), sr.state('DDB')['text'])
expect(sr.press('DDB') == 'no reset', 'DDB has no reset')

H.GLOBALS.clear()
m = sr._store()
m.put('lock:COS', '%d-1' % H.CLOCK.now())
expect(sr.press('COS', 'x', 'y') == 'busy', 'live lock -> busy')
m.put('lock:COS', '%d-1' % (H.CLOCK.now() - 60000))
expect(sr.press('COS', 'x', 'y') == 'busy', 'a 60 s old lock is still live (STALE_MS 120 s) -> busy')
m.put('lock:COS', '%d-1' % (H.CLOCK.now() - 130000))
H.CLOCK.listeners[:] = []
plcx = plcsim.PLC(sr.REACH['COS'], {'COS': sr.RB_TAG['COS']})
r = sr.press('COS', 'x', 'y')
plcx.stop()
expect(r == 'started', 'stale lock (130 s) replaced -> started (got %s)' % r)
expect('lock:COS' not in m, 'lock released after the run')

# --- 4b. review fixes: another screen releases during the hold; a True write that reports Bad; who None; row time
print('== 4b. review fixes')
def release_mid_hold(dt):
    if 1500 <= dt < 1510:
        H.TAGS[sr.RB_TAG['SDB']] = [False, H.CLOCK.now()]
plc, rec, res, dt = run('SDB', {'SDB_IG1': dict(fault=True), 'SDB_IG2': dict()}, during=release_mid_hold)
print('released by another screen mid-hold:', rec['step'], '|', rec['msg'], '| %.1f s' % (dt / 1000.0), states(plc))
expect(rec['step'] == 'failed' and 'another screen released' in rec['msg'], 'hold abandoned when another screen releases')
expect(dt < 2500, 'abandoned at once (%.1f s)' % (dt / 1000.0))
expect(H.TAGS[sr.RB_TAG['SDB']][0] is False and plc.timeouts == 0, 'bit left False')
w = [x for x in H.WRITES if x[2] is True]
expect(len(w) == 1, 'one True write only (got %d)' % len(w))

plc, rec, res, dt = run('GRA', {'GRA_IG1': dict()}, pre=lambda p: H.WRITE_LIE.add(sr.RB_TAG['GRA']))
print('True write reached the PLC but came back Bad:', rec['step'], '|', rec['msg'])
expect(rec['step'] == 'failed', 'Bad True write -> failed')
expect(H.TAGS[sr.RB_TAG['GRA']][0] is False, 'the bit is written False after a Bad True write')
expect(plc.timeouts == 0, 'no 5 s PLC timeout needed')
expect(len([x for x in H.WRITES if x[2] is True]) == 1, 'the True is not retried')

plc, rec, res, dt = run('HOG', {'HOG_IG1': dict()}, who=None)
print('who None ->', repr(rec['who']), '| history ts = press:', LOGGED[-1][1].get('ts') == rec['started'])
expect(rec['who'] == 'no login', "who None -> 'no login' (got %r)" % rec['who'])
expect(LOGGED and LOGGED[-1][1].get('ts') == rec['started'], 'history row stamped at the press')
expect(LOGGED[-1][1].get('who') == 'no login', 'history who')

# state() card fields
H.GLOBALS.clear()
st = sr.state('COS')
expect(st['cls'] == 'gbtn gbtn-gold' and st['can'], 'idle: glass gold')
st = sr.state('DDB')
expect(st['cls'] == '' and st['text'] == 'MONITORING ONLY' and not st['can'], 'DDB: monitoring only, no class')

# --- 5. state() text through a run (busy texts) - poll it from a clock listener
print('== 5. state() while running')
seen = []
TICKS = [0]
def spy(t):
    TICKS[0] += 1
    if TICKS[0] % 25 == 0:
        s = sr.state('GRA')
        if not seen or seen[-1] != s['text'].split(' ')[0] + ' ' + str(s['busy']):
            seen.append(s['text'].split(' ')[0] + ' ' + str(s['busy']))
H.CLOCK.listeners[:] = []
H.GLOBALS.clear()
plc = plcsim.PLC(sr.REACH['GRA'], {'GRA': sr.RB_TAG['GRA']})
H.CLOCK.listeners.append(spy)
sr.press('GRA', 'shane', 'Booth GRA')
plc.stop(); H.CLOCK.listeners[:] = []
print('states seen:', seen)
CARD = []
def spy2(t):
    TICKS[0] += 1
    if TICKS[0] % 25 == 0:
        s = sr.state('SDB')
        k = (s['text'].split(' ')[0], s['cls'], s['cardBg'], s['cardFg'])
        if not CARD or CARD[-1] != k:
            CARD.append(k)
after = sr.state('GRA')
print('after:', after)
expect(after['text'] == 'RESET DONE' and after['cls'] == '' and after['cardBg'] == '#0A733A', 'done: solid green on the card')
H.CLOCK.listeners[:] = []
plc2 = plcsim.PLC(sr.REACH['SDB'], {'SDB': sr.RB_TAG['SDB']})
H.WRITE_FAIL.add(sr.RB_TAG['SDB'])
H.CLOCK.listeners.append(spy2)
sr.press('SDB', 'shane', 'Booth SDB')
H.CLOCK.advance(200)
plc2.stop(); H.CLOCK.listeners[:] = []; H.WRITE_FAIL.clear()
print('card states (SDB, write failing):', CARD)
fs = sr.state('SDB')
expect(fs['text'] == 'RESET FAILED' and fs['cls'] == '' and fs['cardBg'] == '#C02026', 'failed: red on the card')
H.CLOCK.advance(sr.SHOW_MS + 100)
print('after SHOW_MS:', sr.state('GRA')['text'], '|', sr.state('GRA')['note'])
print('recent(GRA_IG2):', sr.recent('GRA_IG2', 60000), ' recent(SDB_IG1):', sr.recent('SDB_IG1', 60000))

# --- 5b. COS_IG2 shares ONSAux[0].7 between the COS HMI reset and CHP_RB_08: count reset pulses while held
print('== 5b. dup ONS on COS_IG2')
H.CLOCK.listeners[:] = []
H.GLOBALS.clear()
plc = plcsim.PLC(sr.REACH['COS'], {'COS': sr.RB_TAG['COS']}, 0)
print('COS_IG2 reset branches:', plc.igs['COS_IG2'].reset)
H.TAGS[sr.RB_TAG['COS']] = [True, H.CLOCK.now()]
H.CLOCK.advance(1000)
print('held 1 s: COS_IG1 reset scans %d, COS_IG2 reset scans %d' % (plc.igs['COS_IG1'].resets, plc.igs['COS_IG2'].resets))
H.TAGS[sr.RB_TAG['COS']] = [False, H.CLOCK.now()]
H.CLOCK.advance(500)
print('released: COS_IG1 reset scans %d, COS_IG2 reset scans %d' % (plc.igs['COS_IG1'].resets, plc.igs['COS_IG2'].resets))
plc.stop()

# --- 6. Monte Carlo: random latency 10-400 ms, random safety-task phase
print('== 6. Monte Carlo')
random.seed(7)
for area in ['SDB', 'GRA', 'COS', 'TNB', 'CHP', 'HOG']:
    bad = 0
    for i in range(150):
        setup = {}
        for ig in sr.REACH[area]:
            setup[ig] = random.choice([dict(), dict(fault=True), dict(en=True)])
        lat = (random.randint(5, 60), random.randint(80, 400))
        plc, rec, res, dt = run(area, setup, latency=lat)
        st = states(plc)
        if [s for s in st.values() if s != 'EN'] or plc.timeouts or rec['step'] != 'done':
            bad += 1
            if bad < 3:
                print('  bad run', area, lat, rec['msg'], st)
    print('%-4s 150 runs, %d not all energized' % (area, bad))
    expect(bad == 0, '%s Monte Carlo' % area)

print('\nFAILS: %d' % fails)
