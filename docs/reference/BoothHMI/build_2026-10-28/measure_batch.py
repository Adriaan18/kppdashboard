# statement counts of the history engine with 1,500 alarms (re-measured after the review fixes)
import sys
sys.path.insert(0, '.')
import harness as H
H.load_all()
ah = H.forensics.alarmHistory
H.SYSTEM.db.runUpdateQuery("DROP SCHEMA IF EXISTS alarm CASCADE")
import io, contextlib
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    ah.install()
print([l for l in buf.getvalue().splitlines() if l.startswith('install')][0], '| DDL', len(ah.DDL), 'DOC', len(ah.DDL_DOC))
now = H.CLOCK.now
evs = []
for i in range(1500):
    e = H.FakeEvent('%08d-0000-0000-0000-%012d' % (i, i), 'prov:x:/tag:KPP/COS/Area/D%d:/alm:A' % i, 'COS/D%d' % i, 'Alarm %d' % i,
                    'High', act=now() - 60000 - i, clr=(now() - 1000) if i % 3 == 0 else None, ack=(now() - 500) if i % 2 == 0 else None,
                    ackUser='usr-prov:default:/usr:op')
    evs.append(e)
H.ALARMS[:] = evs
H.GLOBALS.clear()
n0 = len(H.SQL_LOG)
ah.tick()
first = H.SQL_LOG[n0:]
print('first tick: %d statements (%s)' % (len(first), ', '.join(sorted(set(s.split(' ')[0] + ' ' + s.split(' ')[1] for s in first)))))
H.CLOCK.advance(1000); ah.tick()
open_ = [e for e in evs if e.clr is None][:300]
for e in open_:
    e.clr = now() - 100
H.CLOCK.advance(1000)
n0 = len(H.SQL_LOG)
ah.tick()
print('300 clearing at once: %d statements' % len([s for s in H.SQL_LOG[n0:] if 'alarm.hmi_history' in s]))
r = H.SYSTEM.db.runQuery("SELECT count(*), count(clear_ts), count(ack_ts) FROM alarm.hmi_history")
print('rows', [r.getValueAt(0, c) for c in range(3)])
