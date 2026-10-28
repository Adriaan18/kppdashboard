import sys, random
sys.path.insert(0, '.')
import harness as H, plcsim
H.load_all()
ah = H.forensics.alarmHistory
sr = H.booth.safetyreset
bs = H.booth.safety
H.Logger.LINES[:] = []
fails = 0
def expect(c, m):
    global fails
    if not c:
        fails += 1; print('  FAIL:', m)
def q(sql):
    ds = H.SYSTEM.db.runQuery(sql)
    return [[ds.getValueAt(r, c) for c in range(ds.getColumnCount())] for r in range(ds.getRowCount())]

H.SYSTEM.db.runUpdateQuery("DROP SCHEMA IF EXISTS alarm CASCADE")
H.SYSTEM.db.runUpdateQuery("DROP TABLE IF EXISTS public.purge_log")
print('== install')
ah.install()

# PLC model for every IG with tags (all areas), all energized
igs = sorted([ig for ig in bs.GROUPS if bs.GROUPS[ig]['tags']])
H.CLOCK.listeners[:] = []
plc = plcsim.PLC(igs, dict(sr.RB_TAG), 0)
for ig in igs:
    plc.igs[ig].setup(en=True)
plc.publish()
# a few device tags so the why text has something to read
for dev in ['COS_GS_01', 'COS_IS_01', 'GRA_IS_01']:
    for m in bs.MEMBERS[bs.DEVICES[dev][0]]:
        H.TAGS[bs.devPath(dev, m)] = [True if m in ('InputOkay', 'InputStatus') else False, H.CLOCK.now()]
for e in bs.ESTOP_CHAIN:
    for m in bs.MEMBERS['ES']:
        H.TAGS[bs.devPath(e, m)] = [m in ('InputOkay', 'InputStatus'), H.CLOCK.now()]

now = H.CLOCK.now
A = H.FakeEvent('aaaaaaaa-0000-0000-0000-000000000001', 'prov:TL-KPPWS01-01:/tag:KPP/StemDB/Devices/Motors/Feed:/alm:Fault',
                'SDB/Debarker/Feed motor', 'Feed motor fault', 'High', act=now() - 5000, value=3)
C = H.FakeEvent('cccccccc-0000-0000-0000-000000000003', 'prov:TL-KPPWS01-01:/tag:KPP/Grader/Devices/Hyd/Pump2:/alm:Low',
                '', 'Pump 2 low pressure', 'Low', act=now() - 2 * 86400000, clr=now() - 1 * 86400000)
OLD = H.FakeEvent('99999999-0000-0000-0000-000000000009', 'prov:TL-KPPWS01-01:/tag:KPP/COS/Area/Old:/alm:A', 'COS/Old',
                  'Forty days old', 'Low', act=now() - 40 * 86400000, clr=now() - 39 * 86400000)
H.ALARMS[:] = [A, C, OLD]
print('== tick 1 (baseline + 2 alarms)')
ah.tick()
rows = q("SELECT kind, area, label, display_path, value, clear_ts IS NOT NULL, clear_est, duration_s FROM alarm.hmi_history ORDER BY id")
for r in rows: print('  ', r)
expect(len(rows) == 2, 'two alarm rows after tick 1')
expect(rows[0][1] == 'SDB' and rows[1][1] == 'GRA', 'areas from the tag folder')
expect(rows[1][3] == 'KPP/Grader/Devices/Hyd/Pump2/Low', 'display path from source when blank: %s' % rows[1][3])
expect(not [r for r in rows if r[2] == 'Forty days old'], 'an alarm older than 30 days is not written')

print('== tick 2 (A acked)')
H.CLOCK.advance(1000)
A.ack = now(); A.ackUser = 'usr-prov:default:/usr:shane'
ah.tick()
r = q("SELECT ack_ts IS NOT NULL, ack_user FROM alarm.hmi_history WHERE event_id = '%s'" % A.eid)[0]
print('  ', r); expect(r == [True, 'shane'], 'ack user parsed')

print('== tick 3 (A cleared and acked -> leaves the list; B appears)')
H.CLOCK.advance(1000)
A.clr = now() - 300
B = H.FakeEvent('bbbbbbbb-0000-0000-0000-000000000002', 'prov:TL-KPPWS01-01:/tag:KPP/COS/Area/Devices/Saw:/alm:Stall',
                'COS/Saws/A saw stall', 'A saw stalled', 'High', act=now() - 200)
H.ALARMS[:] = [C, B, OLD]
ah.tick()
r = q("SELECT clear_ts IS NULL FROM alarm.hmi_history WHERE event_id = '%s'" % A.eid)[0]
print('   A after 1 poll without it:', r); expect(r == [True], 'A not closed after one missed poll')

print('== tick 4 (B gone between polls), ticks 5-6: closed only after 3 polls without them')
H.CLOCK.advance(1000)
H.ALARMS[:] = [C, OLD]
tB = now()
ah.tick()
r = q("SELECT clear_ts IS NULL FROM alarm.hmi_history WHERE event_id = '%s'" % B.eid)[0]
expect(r == [True], 'B open after 1 missed poll')
H.CLOCK.advance(1000); ah.tick()
r = q("SELECT clear_est, round(duration_s::numeric,1) FROM alarm.hmi_history WHERE event_id = '%s'" % A.eid)[0]
print('   A after 3 polls:', r); expect(r[0] is False and abs(r[1] - 6.7) < 0.3, 'A closed at its own clear time')
r = q("SELECT clear_ts IS NULL FROM alarm.hmi_history WHERE event_id = '%s'" % B.eid)[0]
expect(r == [True], 'B open after 2 missed polls')
H.CLOCK.advance(1000); ah.tick()
r = q("SELECT clear_est, clear_ts, ack_ts IS NOT NULL FROM alarm.hmi_history WHERE event_id = '%s'" % B.eid)[0]
print('   B after 3 polls:', r)
expect(r[0] is True and r[1].getTime() == tB and r[2] is True, 'B closed at the first poll without it, estimated, acked')

print('== blip: an active alarm missing from 2 polls comes back - never closed')
E = H.FakeEvent('eeeeeeee-0000-0000-0000-000000000005', 'prov:TL-KPPWS01-01:/tag:KPP/HOG/Devices/Conv:/alm:Stop',
                'HOG/Hog conveyor', 'Hog conveyor stopped', 'Medium', act=now() - 100)
H.ALARMS[:] = [C, OLD, E]; H.CLOCK.advance(1000); ah.tick()
H.ALARMS[:] = [C, OLD]; H.CLOCK.advance(1000); ah.tick(); H.CLOCK.advance(1000); ah.tick()
H.ALARMS[:] = [C, OLD, E]; H.CLOCK.advance(1000); ah.tick()
H.CLOCK.advance(1000); ah.tick()
r = q("SELECT clear_ts IS NULL, clear_est FROM alarm.hmi_history WHERE event_id = '%s'" % E.eid)[0]
print('   E:', r); expect(r == [True, False], 'a 2-poll blip does not close the occurrence')

print('== reopen: E missing 3 polls (closed, estimated) then back still active; then its real clear')
H.ALARMS[:] = [C, OLD]
for i in range(3):
    H.CLOCK.advance(1000); ah.tick()
r = q("SELECT clear_ts IS NULL, clear_est FROM alarm.hmi_history WHERE event_id = '%s'" % E.eid)[0]
expect(r == [False, True], 'E closed by estimate after 3 polls')
H.ALARMS[:] = [C, OLD, E]; H.CLOCK.advance(1000); ah.tick()
r = q("SELECT clear_ts IS NULL, clear_est, duration_s FROM alarm.hmi_history WHERE event_id = '%s'" % E.eid)[0]
print('   E back:', r); expect(r == [True, False, None], 'E reopened when it came back active')
E.clr = now() - 100
H.CLOCK.advance(1000); ah.tick()
r = q("SELECT clear_est, clear_ts FROM alarm.hmi_history WHERE event_id = '%s'" % E.eid)[0]
expect(r[0] is False and r[1].getTime() == E.clr, 'E real clear time')
F = H.FakeEvent('ffffffff-0000-0000-0000-000000000006', 'prov:TL-KPPWS01-01:/tag:KPP/Chippers/Devices/C1:/alm:Jam',
                'CHP/Chipper 1', 'Chipper 1 jam', 'High', act=now() - 500)
H.ALARMS[:] = [C, OLD, F]; H.CLOCK.advance(1000); ah.tick()
H.ALARMS[:] = [C, OLD]
for i in range(3):
    H.CLOCK.advance(1000); ah.tick()
F.clr = now() - 2500
H.ALARMS[:] = [C, OLD, F]; H.CLOCK.advance(1000); ah.tick()
r = q("SELECT clear_est, clear_ts, round(duration_s::numeric,1) FROM alarm.hmi_history WHERE event_id = '%s'" % F.eid)[0]
print('   F back cleared:', r)
expect(r[0] is False and r[1].getTime() == F.clr, 'a real clear time replaces the estimate')

print('== a row the database refuses is left out, the rest are written, the engine goes on; NUL text cleaned')
H.SYSTEM.db.runUpdateQuery("ALTER TABLE alarm.hmi_history ADD CONSTRAINT t_no_bad CHECK (label IS DISTINCT FROM 'BAD ROW')")
G1 = H.FakeEvent('11111111-0000-0000-0000-000000000007', 'prov:x:/tag:KPP/COS/Area/X:/alm:A', 'COS/X', 'BAD ROW', 'High', act=now() - 50)
G2 = H.FakeEvent('22222222-0000-0000-0000-000000000008', 'prov:x:/tag:KPP/COS/Area/Y:/alm:A', 'COS/Y', 'Good row', 'High', act=now() - 50)
G3 = H.FakeEvent('33333333-0000-0000-0000-000000000009', 'prov:x:/tag:KPP/COS/Area/Z:/alm:A', 'COS/Z', u'Nul\x00in label', 'High', act=now() - 50)
H.Logger.LINES[:] = []
H.ALARMS[:] = [C, OLD, G1, G2, G3]; H.CLOCK.advance(1000); ah.tick()
got = q("SELECT label FROM alarm.hmi_history WHERE event_id IN ('%s', '%s', '%s') ORDER BY label" % (G1.eid, G2.eid, G3.eid))
print('   written:', got, '| warns:', [l[2][:90] for l in H.Logger.LINES if l[0] == 'WARN'])
expect(got == [['Good row'], ['Nulin label']], 'bad row left out, good rows written, NUL removed')
n0 = len(H.SQL_LOG)
H.CLOCK.advance(1000); ah.tick()
expect(not [x for x in H.SQL_LOG[n0:] if x.startswith('INSERT INTO alarm.hmi_history AS h')], 'no retry of the bad row')
expect(ah._g().get('err') is None or 'insert' not in (ah._g()['err'][0] or ''), 'engine not in error')
H.SYSTEM.db.runUpdateQuery("ALTER TABLE alarm.hmi_history DROP CONSTRAINT t_no_bad")

print('== database down: nothing advances; written when it answers again')
D2 = H.FakeEvent('44444444-0000-0000-0000-000000000010', 'prov:x:/tag:KPP/TnB/Devices/K:/alm:A', 'TnB/Kicker 3', 'Kicker 3 stuck', 'High', act=now())
H.DB_DOWN[0] = True
H.ALARMS[:] = [C, OLD, G2, G3, D2]
plc.igs['COS_IG2'].gates = False
for i in range(3):
    H.CLOCK.advance(1000); ah.tick()
print('   err while down:', ah._g().get('err'))
expect(ah._g().get('err') and 'not answering' in ah._g()['err'][0], 'error recorded while the database is down')
H.DB_DOWN[0] = False
H.CLOCK.advance(1000); ah.tick()
r = q("SELECT count(*) FROM alarm.hmi_history WHERE event_id = '%s'" % D2.eid)[0][0]
r2 = q("SELECT value FROM alarm.hmi_history WHERE kind = 'safety' AND display_path = 'COS/Safety/COS_IG2' ORDER BY id DESC LIMIT 1")
print('   after:', r, r2)
expect(r == 1 and r2 == [['DE-ENERGIZED']], 'alarm and safety change written when the database is back')
plc.igs['COS_IG2'].gates = True

print('== tick 5 (safety: COS IG1 de-energized by COS_GS_01 open, GRA IG1 fault, then HMI reset energizes)')
H.CLOCK.advance(1000)
g = plc.igs['COS_IG1']; g.gates = False
H.TAGS[bs.devPath('COS_GS_01', 'InputOkay')] = [False, now()]
gg = plc.igs['GRA_IG1']; gg.dev_cause = True
H.CLOCK.advance(200)
ah.tick()
H.CLOCK.advance(1000)
gg.dev_cause = False
g.gates = True
H.TAGS[bs.devPath('COS_GS_01', 'InputOkay')] = [True, now()]
# HMI reset of COS through booth.safetyreset (real sequence on the PLC model) while the engine ticks every second
H.SYSTEM.util.INLINE = True
_orig = H.CLOCK.listeners[:]
TK = [0]
def ticker(t):
    TK[0] += 1
    if TK[0] % 100 == 0:
        ah.tick()
H.CLOCK.listeners.append(ticker)
print('   press COS:', sr.press('COS', 'shane', 'Booth COS'))
print('   press GRA:', sr.press('GRA', 'mike', 'Diag view'))
H.CLOCK.advance(3000)
H.CLOCK.listeners.remove(ticker)
ah.tick()
rows = q("SELECT kind, area, label, value, who, detail FROM alarm.hmi_history WHERE kind <> 'alarm' ORDER BY event_ts, id")
for r in rows: print('  ', r)
kinds = [(r[0], r[1], r[3]) for r in rows]
expect(('safety', 'COS', 'DE-ENERGIZED') in kinds, 'COS IG1 de-energized row')
expect(('safety', 'GRA', 'FAULT') in kinds, 'GRA IG1 fault row')
expect(('reset', 'COS', 'DONE') in kinds and ('reset', 'GRA', 'DONE') in kinds, 'reset rows DONE')
en = [r for r in rows if r[0] == 'safety' and r[3] == 'ENERGIZED' and r[1] == 'COS']
expect(en and en[0][4] == 'shane', 'COS ENERGIZED row names the HMI user')
fc = [r for r in rows if r[0] == 'safety' and r[3] == 'FAULT CLEARED']
expect(fc and fc[0][4] == 'mike', 'GRA FAULT CLEARED names the HMI user')

print('== restart: new globals; an open row in the table is not in the status list any more')
H.SYSTEM.db.runUpdateQuery("INSERT INTO alarm.hmi_history (event_ts, kind, area, label, event_id) VALUES (now() - interval '2 hours', 'alarm', 'COS', 'Old open', 'dddddddd-0000-0000-0000-000000000004')")
J = H.FakeEvent('55555555-0000-0000-0000-000000000011', 'prov:x:/tag:KPP/Grader/Devices/Q:/alm:A', 'GRA/Q', 'Still active over the restart', 'High', act=now() - 1000)
H.ALARMS[:] = [C, J]; H.CLOCK.advance(1000); ah.tick()
H.GLOBALS.clear()
ah.tick()
tS = now()
H.CLOCK.advance(60000); ah.tick()
r = q("SELECT clear_ts IS NULL FROM alarm.hmi_history WHERE event_id = 'dddddddd-0000-0000-0000-000000000004'")[0]
expect(r == [True], 'not closed in the first 2 minutes after a start')
H.CLOCK.advance(61000); ah.tick()
r = q("SELECT clear_est, detail, clear_ts FROM alarm.hmi_history WHERE event_id = 'dddddddd-0000-0000-0000-000000000004'")[0]
print('  ', r); expect(r[0] is True and 'engine was off' in r[1] and r[2].getTime() == tS, 'reconcile closes it, at the engine start')
r = q("SELECT clear_ts IS NULL FROM alarm.hmi_history WHERE event_id = '%s'" % J.eid)[0]
expect(r == [True], 'J (still in the status list after the restart) not reconciled')
r = q("SELECT clear_ts IS NULL, clear_est FROM alarm.hmi_history WHERE event_id = '%s'" % E.eid)[0]
expect(r == [False, False], 'a real clear is never reopened')
n = q("SELECT count(*) FROM alarm.hmi_history WHERE event_id = '%s'" % C.eid)[0][0]
expect(n == 1, 'no duplicate after restart')

print('== logAction msgack + rows()')
print('  ', ah.logAction('msgack', 'SDB', u'MESSAGE ACK - Debarker', value='SENT', who='kenny', station='/Debarker/Overview', detail='(I:70/17) Message Acknowledge', source='[x]MessageAck'))
for f, mode, srch in [('SDB,HOG', 'all', ''), ('COS,TnB,Sortline,PulpDeck,T&B', 'all', ''), ('GRA, SeqDeck', 'safety', ''),
                      ('COS,TnB,Sortline,PulpDeck,T&B', 'alarms', ''), ('', 'all', 'shane'), ('SDB,HOG', 'all', "50%_x'")]:
    res = ah.rows(f, 24 * 60, mode, srch)
    print('  rows(%r, %s, %r): %d | %s' % (f, mode, srch, len(res['rows']), res['info']))
    for row in res['rows'][:3]:
        print('     ', ' | '.join('%s' % row[k]['value'] for k in ('when', 'type', 'what', 'detail', 'state', 'lasted', 'by')))
res = ah.rows('SDB,HOG', 1, 'all', '')
print('  1 h:', res['info'])
res = ah.rows('SDB,HOG', 24 * 60, 'all', '', limit=1)
print('  limit:', res['info'])
expect('newest' in res['info'] or len(res['rows']) <= 10, 'limit text')

print('== check()')
ah.check()

print('== purge 1.2.0')
H.SYSTEM.db.runUpdateQuery("INSERT INTO alarm.hmi_history (event_ts, kind, area, label) VALUES (now() - interval '31 days', 'safety', 'SDB', 'old'), (now() - interval '29 days', 'safety', 'SDB', 'keep')")
out = H.shared.purge.run(dry=True)
mine = [o for o in out if o['job'] == 'HMI alarm history'][0]
print('   dry:', mine)
out = H.shared.purge.run()
mine = [o for o in out if o['job'] == 'HMI alarm history'][0]
print('   live:', mine)
left = q("SELECT label FROM alarm.hmi_history WHERE label IN ('old', 'keep')")
print('   left:', left)
expect(left == [['keep']], 'purge keeps 30 days')
expect(q("SELECT count(*) FROM alarm.hmi_history WHERE event_id = '%s'" % C.eid)[0][0] == 1, 'C (2 days old) kept')

print('== view alarm.v_history and comments')
print('  ', q("SELECT event_local, kind, label FROM alarm.v_history ORDER BY event_ts DESC LIMIT 2"))
print('  ', q("SELECT count(*) FROM pg_description d JOIN pg_class c ON c.oid = d.objoid JOIN pg_namespace n ON n.oid = c.relnamespace WHERE n.nspname = 'alarm'"))
print('engine_status:', q("SELECT engine, version, alarms_open, groups_read, rows_written, last_error FROM alarm.engine_status"))
warns = [l for l in H.Logger.LINES if l[0] == 'WARN']
print('WARN lines:', len(warns))
for w in warns[:10]: print('   ', w)
print('\nFAILS: %d' % fails)
plc.stop()
