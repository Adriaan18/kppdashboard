# forensics.hydPump 1.0.5 off the gateway: a simulated plant of 18 pumps (Apr - 28 Oct 2026) with the site's facts -
# DB P6 stepped down 25 Sep (135 -> 111), GRA P1 down 1 May (116.5 -> 52.5), TNB P2 up 10 Aug (115 -> 169: a swap the
# card never raised), COS3 P1 temperature +5.7 from 1 Oct, COS3 P2 a slow drift 124 -> 114 (wear - must stay raised),
# TNB P1 (Big John) only since 19 Oct. Gateway refresh before / after rebase, the console rebase dry and live, the
# first refresh after a reload, replay, the updated-column fallback, set_reference's guard, 1.0.4 regression.
import sys, io, contextlib, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness as H

OUT = '/home/claude/out/'
SRC104 = '/tmp/claude-0/-home-claude/093166e4-91e7-5882-8ec5-a1a53ea7875b/scratchpad/hyd/hydPump_1_0_4.py'
fails = 0


def expect(c, m):
    global fails
    if not c:
        fails += 1
        print('  FAIL:', m)


# stubs the library reaches
class NS(object):
    pass

pj = NS()
pj.shut_spans = lambda t0, t1: []
H.forensics.peWatchJudge = pj
hd = NS()
hd.PUMPS = []
hd.BASE = ''
H.forensics.hyddiag = hd


def _a3(s):
    if s is None:
        return ''
    return str(s).encode('ascii', 'replace').decode('ascii')


def load(path, name):
    m = H.load(path, name)
    m.__dict__['_a'] = _a3          # Jython's unicode handling, as plain str under CPython
    return m


db = H.SYSTEM.db
q = lambda sql: [[ds.getValueAt(r, c) for c in range(ds.getColumnCount())] for ds in [db.runQuery(sql)] for r in range(ds.getRowCount())]

# ---------------------------------------------------------------- tables and the simulated plant
db.runUpdateQuery("DROP SCHEMA IF EXISTS hydraulics CASCADE")
db.runUpdateQuery("""CREATE SCHEMA hydraulics;
CREATE TABLE hydraulics.pump_window (pump text NOT NULL, win_start timestamptz NOT NULL, p_avg double precision, p_min double precision,
  p_max double precision, t_avg double precision, t_min double precision, t_max double precision, run double precision, run_src text,
  ref_t double precision, ref_src text, dt double precision, sm double precision, src text, updated timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (pump, win_start));
CREATE INDEX ON hydraulics.pump_window (win_start);
CREATE TABLE hydraulics.pump_band (pump text PRIMARY KEY, band integer NOT NULL, since timestamptz, updated timestamptz NOT NULL DEFAULT now());
CREATE TABLE hydraulics.pump_ref (pump text PRIMARY KEY, ref_from timestamptz NOT NULL, ref_to timestamptz, note text,
  updated timestamptz NOT NULL DEFAULT now())""")


def step(day, a, b):
    return "CASE WHEN lt < TIMESTAMP '%s' THEN %s ELSE %s END" % (day, a, b)

SIM = {
    'SDB_U1P1': ('2026-04-16 08:00', '138.0', '-0.7', 'tank'),
    'SDB_U1P2': ('2026-04-16 08:00', '137.0', '-2.2', 'tank'),
    'SDB_U1P3': ('2026-04-16 08:00', '138.0', '-4.7', 'tank'),
    'SDB_U1P4': ('2026-04-16 08:00', '130.0', '-1.0', 'tank'),
    'SDB_U2P1': ('2026-04-16 08:00', '110.0', '2.5', 'peer'),
    'SDB_U2P2': ('2026-04-16 08:00', step('2026-09-25 09:00', '135.0', '111.0'), '-2.5', 'peer'),
    'GRA_U1P1': ('2026-04-09 08:00', "CASE WHEN lt < TIMESTAMP '2026-05-01' THEN 116.5 WHEN lt < TIMESTAMP '2026-09-01' THEN 52.5 ELSE 54.5 END", '0.0', 'tank'),
    'GRA_U1P2': ('2026-04-09 08:00', '127.0', '-1.5', 'tank'),
    'GRA_U1P3': ('2026-04-09 08:00', '129.0', '0.1', 'tank'),
    'COS_U1P1': ('2026-04-16 08:00', '114.0', '-2.2', 'tank'),
    'COS_U1P2': ('2026-04-16 08:00', '115.0', '-3.0', 'tank'),
    'COS_U1P3': ('2026-04-16 08:00', '114.0', '0.5', 'tank'),
    'COS_U3P1': ('2026-04-16 08:00', '114.0', step('2026-10-01 00:00', '0.2', '5.9'), 'tank'),
    'COS_U3P2': ('2026-04-16 08:00', "124.0 - 10.0 * LEAST(1.0, GREATEST(0.0, EXTRACT(EPOCH FROM (lt - TIMESTAMP '2026-06-01')) / "
                 "EXTRACT(EPOCH FROM INTERVAL '136 days')))", '2.2', 'tank'),
    'TNB_U4P1': ('2026-10-19 10:30', '168.0', '-0.1', 'tank'),
    'TNB_U4P2': ('2026-04-16 08:00', step('2026-08-10 09:00', '115.0', '169.0'), '5.6', 'tank'),
    'TNB_U4P3': ('2026-04-16 08:00', '115.0', '-0.4', 'tank'),
    'TNB_U4P4': ('2026-04-16 08:00', '115.0', '-1.6', 'tank'),
}
db.runUpdateQuery("SELECT setseed(0.42)")
for key, (start, lvl, toff, rsrc) in SIM.items():
    db.runUpdateQuery("""INSERT INTO hydraulics.pump_window (pump, win_start, p_avg, p_min, p_max, t_avg, t_min, t_max, run, run_src, ref_t,
  ref_src, dt, sm, src)
WITH g AS (
  SELECT ts, lt, (lt >= TIMESTAMP '%(start)s') AS on_,
    (EXTRACT(isodow FROM lt) <= 5 AND EXTRACT(hour FROM lt) >= 6 AND EXTRACT(hour FROM lt) < 22) AS run_,
    (%(lvl)s)::float8 AS lvl, (%(toff)s)::float8 AS toff, random() AS r1, random() AS r2, random() AS r3,
    45 + 2 * sin(EXTRACT(epoch FROM ts) / 86400.0 * 2 * pi() / 7) AS tank
  FROM (SELECT ts, ts AT TIME ZONE 'Pacific/Auckland' AS lt
        FROM generate_series(TIMESTAMP '2026-04-05 00:00' AT TIME ZONE 'Pacific/Auckland',
                             TIMESTAMP '2026-10-28 14:30' AT TIME ZONE 'Pacific/Auckland', interval '15 minutes') ts) s
), v AS (
  SELECT ts, on_, run_, tank, r3,
    CASE WHEN NOT on_ THEN 0.0 WHEN run_ THEN lvl + (r1 - 0.5) * 1.6 ELSE 1.5 + r1 END AS p,
    CASE WHEN NOT on_ THEN 0.0 WHEN run_ THEN tank + toff + (r2 - 0.5) * 0.6 ELSE tank + (r2 - 0.5) END AS t
  FROM g
)
SELECT '%(key)s', ts, p, CASE WHEN run_ AND on_ THEN p - 4 - r3 * 2 ELSE p * 0.5 END, CASE WHEN run_ AND on_ THEN p + 3 ELSE p * 1.5 END,
  t, t - 0.3, t + 0.3, CASE WHEN run_ THEN 1.0 ELSE 0.0 END, 'tag', tank, '%(rsrc)s', 0.0, 0.0, 'test'
FROM v""" % {'key': key, 'start': start, 'lvl': lvl, 'toff': toff, 'rsrc': rsrc})
print('windows:', q("SELECT count(*), count(DISTINCT pump), min(win_start), max(win_start) FROM hydraulics.pump_window")[0])
NOW = H.CLOCK.now()
db.runPrepUpdate("INSERT INTO hydraulics.pump_band (pump, band, since) VALUES ('SDB_U2P2', 2, ?), ('GRA_U1P1', 2, ?), ('COS_U3P2', 1, ?)",
                 [H.Date(NOW - 1200000), H.Date(NOW - 1200000), H.Date(NOW - 1200000)])


def gateway(mod, now, fresh=True):
    """One gateway refresh: as _refresh after a (re)load (bands and windows from the tables), then _calc."""
    if fresh:
        mod._S.clear()
        mod._init()
        got = mod._band_read()
        mod._S["band"].update(got)
        mod._S["band_saved"].update(got)
        mod._S["band_loaded"] = True
        w = mod._load(now - mod.KEEP_DAYS * mod.DAY_MS)
        for k in w:
            mod._S["win"][k] = w[k]
        mod._S["loaded"] = True
    mod._calc(now)
    return mod._S["res"]


def show(res, keys=None):
    for p in G.PUMPS:
        if keys and p[0] not in keys:
            continue
        r = res[p[0]]
        print('   %-7s %-9s band %2s score %5.1f  %s' % (p[5], r.get('st'), r.get('band'), r.get('score', -1), r.get('v')))


def cap(fn, *a, **k):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn(*a, **k)
    return buf.getvalue()

# ---------------------------------------------------------------- 1. 1.0.4 and 1.0.5 agree with no reference set by hand
print('== 1. regression: 1.0.4 vs 1.0.5, no reference set by hand')
OLD = load(SRC104, 'forensics.hydPump104')
G = load(OUT + 'forensics_hydPump_v1_0_5.py', 'forensics.hydPump')
H.forensics.hydPump = G
r4 = gateway(OLD, NOW)
r5 = gateway(G, NOW)
diff = [k for k in r4 if (r4[k].get('v'), r4[k].get('band'), round(r4[k].get('score', 0), 6)) != (r5[k].get('v'), r5[k].get('band'), round(r5[k].get('score', 0), 6))]
expect(not diff, '1.0.4 and 1.0.5 differ without references: %s' % diff)
show(r5)
expect(r5['SDB_U2P2']['band'] == 2 and 'since Apr' in r5['SDB_U2P2']['v'], 'DB P6 HOT "since Apr" as on site')
expect(r5['GRA_U1P1']['band'] == 2 and 'since Apr' in r5['GRA_U1P1']['v'], 'GRA P1 HOT "since Apr" as on site')
expect(r5['TNB_U4P2']['band'] == 0, 'TNB P2 up step not raised by the card (only the bad direction)')
expect(r5['COS_U3P2']['band'] >= 1, 'COS3 P2 drift raised')

# ---------------------------------------------------------------- 2. console rebase(), dry
print('== 2. rebase() dry')
C = load(OUT + 'forensics_hydPump_v1_0_5.py', 'forensics.hydPump.console')
out = cap(C.rebase)
print(out)
expect('DRY RUN' in out and q("SELECT count(*) FROM hydraulics.pump_ref")[0][0] == 0, 'dry run writes nothing')
summ = out.split('SUMMARY')[1]
reb = summ.split('rebase:')[1].split('\n')[0]
for want in ('DB P6 from 26 Sep', 'GRA P1 from 2 May', 'TNB P2 from 11 Aug', 'COS3 P1 from 2 Oct'):
    expect(want in reb, 'rebase plan has %s: %s' % (want, reb))
expect('COS3 P2' in summ.split('drift')[1].split('\n')[0] and 'COS3 P2' not in reb, 'COS3 P2 drift left alone')
for k in ('DB P1', 'DB P5', 'GRA P2', 'COS1 P1', 'TNB P1', 'TNB P3'):
    expect(k not in reb, '%s not rebased' % k)

# ---------------------------------------------------------------- 3. rebase(False) and the running gateway's next refresh
print('== 3. rebase(False), then the running gateway refreshes 15 min later')
out = cap(C.rebase, False)
print('\n'.join([l for l in out.splitlines() if 'reference 2026' in l or 'written' in l]))
refs = q("SELECT pump, to_char(ref_from, 'YYYY-MM-DD'), to_char(ref_to, 'YYYY-MM-DD'), note, updated IS NOT NULL FROM hydraulics.pump_ref ORDER BY pump")
print('   pump_ref:', refs)
expect([r[:3] for r in refs] == [['COS_U3P1', '2026-10-02', '2026-10-28'], ['GRA_U1P1', '2026-05-02', '2026-05-30'],
                                 ['SDB_U2P2', '2026-09-26', '2026-10-24'], ['TNB_U4P2', '2026-08-11', '2026-09-08']], 'the four references')
expect(all(r[4] for r in refs), 'rows stamped')
H.Logger.LINES[:] = []
r6 = gateway(G, NOW + 900000, fresh=False)
show(r6)
for k in ('SDB_U2P2', 'GRA_U1P1', 'TNB_U4P2', 'COS_U3P1'):
    expect(r6[k]['band'] == 0 and r6[k]['v'] == 'normal', '%s normal after the rebase (got %s %s)' % (k, r6[k]['band'], r6[k]['v']))
expect(r6['COS_U3P2']['band'] >= 1, 'COS3 P2 (wear) still raised')
expect(len([l for l in H.Logger.LINES if 'judged afresh' in l[2]]) == 4, 'four "judged afresh" lines')
bands = dict((r[0], r[1]) for r in q("SELECT pump, band FROM hydraulics.pump_band"))
print('   pump_band:', bands)
expect(bands.get('SDB_U2P2') == 0 and bands.get('GRA_U1P1') == 0, 'held HOT bands let go in the table')
expect(G._S['ref'].get('GRA_U1P1')[1] is not None and G._S['ref'].get('SDB_U2P2')[1] is None, 'GRA P1 new reference in use, DB P6 not until Dec')
b = G._S['base']['SDB_U2P2'][1]
print('   DB P6 baseline from', H.Date(b['from']), 'n', b['n'], 'P', round(b['P']['med'], 1))
expect(abs(b['P']['med'] - 111.0) < 1.0 and H.Date(b['from']).dt().strftime('%Y-%m-%d') == '2026-09-26', 'DB P6 8 weeks from 26 Sep at its new level')
r7 = gateway(G, NOW + 1800000, fresh=False)
expect(all(r7[k]['band'] == r6[k]['band'] for k in r6), 'the next refresh: nothing changes again')

# ---------------------------------------------------------------- 4. a reload after the rebase: held bands older than the reference go
print('== 4. reload after the rebase (bands in the table from before it)')
db.runPrepUpdate("UPDATE hydraulics.pump_band SET band = 2, since = ? WHERE pump = 'SDB_U2P2'", [H.Date(NOW - 3600000)])
db.runPrepUpdate("UPDATE hydraulics.pump_ref SET updated = ?", [H.Date(NOW + 600000)])     # written 15:10 (virtual clock)
db.runPrepUpdate("UPDATE hydraulics.pump_band SET band = 2, since = ? WHERE pump = 'GRA_U1P1'", [H.Date(NOW + 1800000)])
G2 = load(OUT + 'forensics_hydPump_v1_0_5.py', 'forensics.hydPump.reload')
H.CLOCK.t = NOW + 2700000
r8 = gateway(G2, NOW + 2700000)
H.CLOCK.t = NOW
print('   DB P6:', r8['SDB_U2P2']['band'], r8['SDB_U2P2']['v'], '| GRA P1:', r8['GRA_U1P1']['band'], r8['GRA_U1P1']['v'])
expect(r8['SDB_U2P2']['band'] == 0 and r8['SDB_U2P2']['v'] == 'normal', 'band from before the reference dropped at the first refresh')
expect(r8['GRA_U1P1']['band'] == 2 and 'held' in r8['GRA_U1P1']['v'], 'band confirmed after the reference kept (held, now normal)')

# ---------------------------------------------------------------- 5. replay, fallbacks, guards
print('== 5. replay, the updated-column fallback, set_reference guard, force / skip')
out = cap(C.replay, 3, 6, 'SDB_U2P2')
print('\n'.join(out.splitlines()[-4:]))
expect('baseline at the end: n' in out and 'share:' in out, 'replay runs')
db.runUpdateQuery("ALTER TABLE hydraulics.pump_ref RENAME COLUMN updated TO upd_x")
rr = G._ref_rows()
expect(len(rr) == 4 and all(v[3] is None for v in rr.values()), 'reference rows read without the updated column')
db.runUpdateQuery("ALTER TABLE hydraulics.pump_ref RENAME COLUMN upd_x TO updated")
out = cap(C.set_reference, 'COS_U1P1', '2026-10-10', '2026-10-01', 'x')
expect('not written' in out and q("SELECT count(*) FROM hydraulics.pump_ref WHERE pump = 'COS_U1P1'")[0][0] == 0, 'to before from refused')
db.runUpdateQuery("DELETE FROM hydraulics.pump_ref")
out = cap(C.rebase, True, ['DB P1', 'nonsense'], 'GRA P1')
reb = out.split('SUMMARY')[1].split('rebase:')[1].split('\n')[0]
print('   force DB P1, skip GRA P1:', reb)
expect('DB P1 from' in reb and 'GRA P1' not in reb and 'not pumps: nonsense' in out, 'force and skip')
expect('(skipped)' in out, 'skip printed')
H.SYSTEM.db.runUpdateQuery("DELETE FROM hydraulics.pump_band")
print('\nFAILS: %d' % fails)
