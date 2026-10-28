# =============================================================================
# forensics_alarmHistory_v1_0_0.py
# Project library script:  forensics.alarmHistory     (package forensics = plain folder)
# Author:   Adriaan
# Version:  1.0.0  (2026-10-28)
# Truth test (Script Console):  print forensics.alarmHistory.VERSION   -> 1.0.0
#                               forensics.alarmHistory.install()        -> schema, tables, view (safe to re-run)
#                               forensics.alarmHistory.check()          -> rows by kind, engine heartbeat, last rows
#
# HMI alarm history - what the plant HMIs showed, kept 30 days, for the booth Alarms popup (HISTORY tab) and for
# the AI box to read. One table, alarm.hmi_history (KPP_production), one row per:
#   kind 'alarm'   Ignition alarm occurrence (every provider): active time, value, cleared, acknowledged, by whom
#   kind 'safety'  isolation group change, from the GroupTags of every IG with Ignition tags:
#                  ENERGIZED (a reset was done - by the HMI user when an HMI reset did it), DE-ENERGIZED (why),
#                  FAULT (why), FAULT CLEARED (reset held 3 s), ISOLATED (which isolator), ISOLATION OFF
#   kind 'reset'   RESET ALL IGs pressed on an HMI (booth.safetyreset): who, where, what came back
#   kind 'msgack'  MESSAGE ACK / Fault Reset pressed on a booth (Application/Booth/Components/MessageAckButton)
# The booth popup filters on display_path the same way the live alarm table does ('SDB,HOG' = either word anywhere);
# safety, reset and msgack rows carry '<area>/Safety/<IG>' and '<area>/HMI/...' so they land on the right booths.
# View alarm.v_history adds NZ local times for the AI box; every column has a COMMENT in the database.
#
# Engine - gateway timer "AlarmHistory_FixedDelay", fixed delay 1000 ms, dedicated thread, body:
#     forensics.alarmHistory.tick()
#   - one system.alarm.queryStatus a second, diffed by event id against the last one. The alarm's own active, clear
#     and ack times are stored, not the poll time. An alarm that cleared and was acknowledged between two polls
#     leaves the status list: after 3 polls without it, it is closed at the first poll that missed it
#     (clear_est = true, within a second). If it comes back (a provider restart), its row takes the alarm's state
#     again - reopened, or its real clear time.
#   - one readBlocking of the IG flags (GroupEn, GroupFaultActive, GroupIsolated) a second; a change gets its why
#     from booth.safety (the Safety Diagnostics popup's own rules), read only when something changed.
#   - the database is touched only on a change (200 rows a statement), plus a heartbeat row in alarm.engine_status
#     once a minute. A row the database refuses is left out and logged, the rest are written. With the database
#     down the engine keeps its last state and writes the changes when the database answers again (an alarm that
#     came and went in the outage is not seen; one that ended in it gets an estimated clear time).
#   - state lives in the gateway globals, so a project save does not re-read everything. After a gateway restart
#     the first tick re-reads the status list (event_id is unique - nothing doubles); 2 minutes later, with the
#     alarm providers up, the occurrences still open in the table and not in the status list are closed - they
#     ended while the engine was off (clear_est = true, clear time = the engine start, detail says so).
#   - an alarm that went active more than 30 days ago is followed in memory, not written.
# Retention: shared.purge job "HMI alarm history" (keep 30 days) - the one purge owner. Nothing here deletes.
# tick(), logAction() and rows() never raise.
#
# Changelog (newest first):
#   1.0.0  2026-10-28  First issue.
# =============================================================================

import re
from java.lang import Throwable, System
from java.util import Date

VERSION = '1.0.0'
LOGGER = 'forensics.alarmHistory'
DB = 'KPP_production'
TABLE = 'alarm.hmi_history'
ENGINE = 'hmi_history'
KEEP_DAYS = 30            # shown on the HMI; shared.purge owns the delete
BATCH = 200               # rows per statement
BEAT_MS = 60000           # heartbeat row
DDL_RETRY_MS = 60000
VANISH_POLLS = 3          # polls an alarm must be missing from the status list before it is closed
RECONCILE_MS = 120000     # after a (re)start: wait for the alarm providers before closing what ended while off
TAG_TIMEOUT_MS = 5000
ROWS_MAX = 400            # rows the popup shows
_KEY = 'forensics.alarmHistory:' + VERSION
IG_FLAGS = ('GroupEn', 'GroupFaultActive', 'GroupIsolated')
NOTE_OFF = u'[ended while the history engine was off - clear time unknown, set to the engine start]'

# area from the alarm source (tag folder) first, then from the display path
AREA_BY_PATH = (('/STEMDB/', 'SDB'), ('/GRADER/', 'GRA'), ('/COS/', 'COS'), ('/TNB/', 'TNB'), ('/SORTLINE/', 'STL'),
	('/CHIPPERS/', 'CHP'), ('/PULPDECK/', 'CHP'), ('/HOG/', 'HOG'), ('/DRUMDB/', 'DDB'))
AREA_BY_WORD = (('DRUM DEBARKER', 'DDB'), ('DRUMDB', 'DDB'), ('DDB', 'DDB'), ('SDB', 'SDB'), ('DEBARKER', 'SDB'),
	('SEQDECK', 'GRA'), ('GRA', 'GRA'), ('COS', 'COS'), ('T&B', 'TNB'), ('TNB', 'TNB'), ('SORTLINE', 'STL'),
	('PULPDECK', 'CHP'), ('CHIP', 'CHP'), ('HOG', 'HOG'))
# the word each area's rows carry in display_path - the booth panels' filters match these
AREA_WORD = {'SDB': 'SDB', 'GRA': 'GRA', 'COS': 'COS', 'TNB': 'TnB', 'STL': 'Sortline', 'CHP': 'CHP', 'HOG': 'HOG',
	'DDB': 'DDB', 'GEN': 'Plant'}
KIND_WORD = {'alarm': 'ALARM', 'safety': 'SAFETY', 'reset': 'RESET', 'msgack': 'MSG ACK'}
HMI_WORD = {'reset': 'Reset all IGs', 'msgack': 'Message ack'}

COLS = ('event_ts', 'kind', 'area', 'display_path', 'label', 'priority', 'source', 'event_id', 'value', 'clear_ts',
	'clear_est', 'ack_ts', 'ack_user', 'duration_s', 'who', 'station', 'detail')

# what the engine needs
DDL = [
	"CREATE SCHEMA IF NOT EXISTS alarm",
	"""CREATE TABLE IF NOT EXISTS alarm.hmi_history (
		id            bigserial PRIMARY KEY,
		event_ts      timestamptz NOT NULL,
		kind          text        NOT NULL,
		area          text,
		display_path  text,
		label         text,
		priority      text,
		source        text,
		event_id      text,
		value         text,
		clear_ts      timestamptz,
		clear_est     boolean     NOT NULL DEFAULT false,
		ack_ts        timestamptz,
		ack_user      text,
		duration_s    double precision,
		who           text,
		station       text,
		detail        text,
		logged_ts     timestamptz NOT NULL DEFAULT now()
	)""",
	"CREATE UNIQUE INDEX IF NOT EXISTS hmi_history_event_id_uq ON alarm.hmi_history (event_id)",
	"CREATE INDEX IF NOT EXISTS hmi_history_ts_idx ON alarm.hmi_history (event_ts DESC)",
	"CREATE INDEX IF NOT EXISTS hmi_history_kind_ts_idx ON alarm.hmi_history (kind, event_ts DESC)",
	"CREATE INDEX IF NOT EXISTS hmi_history_open_idx ON alarm.hmi_history (event_ts) WHERE kind = 'alarm' AND clear_ts IS NULL",
	"""CREATE TABLE IF NOT EXISTS alarm.engine_status (
		engine        text PRIMARY KEY,
		beat_ts       timestamptz NOT NULL DEFAULT now(),
		started_ts    timestamptz,
		version       text,
		alarms_open   integer,
		groups_read   integer,
		rows_written  bigint,
		last_error    text,
		last_error_ts timestamptz
	)""",
]
# for people and the AI box - written by install() and at engine start, never blocking the engine
DDL_DOC = [
	"""CREATE OR REPLACE VIEW alarm.v_history AS
	SELECT h.id, h.event_ts, (h.event_ts AT TIME ZONE 'Pacific/Auckland') AS event_local, h.kind, h.area, h.label,
	       h.value, h.display_path, h.priority, h.clear_ts, (h.clear_ts AT TIME ZONE 'Pacific/Auckland') AS clear_local,
	       h.clear_est, h.duration_s, h.ack_ts, h.ack_user, h.who, h.station, h.detail, h.source, h.event_id
	FROM alarm.hmi_history h""",
	"COMMENT ON TABLE alarm.hmi_history IS 'KPP HMI alarm history, last 30 days (purged nightly by shared.purge). One row per Ignition alarm occurrence (kind alarm) or per HMI or safety event (kind safety, reset, msgack). Written by forensics.alarmHistory, gateway timer AlarmHistory_FixedDelay, 1 s.'",
	"COMMENT ON COLUMN alarm.hmi_history.event_ts IS 'When it happened: the alarm went active, the safety change was seen, the HMI button was pressed.'",
	"COMMENT ON COLUMN alarm.hmi_history.kind IS 'alarm = Ignition alarm occurrence; safety = isolation group change (ENERGIZED means a reset was done); reset = RESET ALL IGs pressed on an HMI; msgack = MESSAGE ACK or Fault Reset pressed on a booth.'",
	"COMMENT ON COLUMN alarm.hmi_history.area IS 'SDB stem debarker, GRA grading, COS cut off saw, TNB tag and brand, STL sortline, CHP chippers, HOG hogger and refuse, DDB drum debarker, GEN not an area.'",
	"COMMENT ON COLUMN alarm.hmi_history.display_path IS 'Alarm display path (the booth panels filter on it). Safety rows: <area>/Safety/<IG>. HMI rows: <area>/HMI/<button>.'",
	"COMMENT ON COLUMN alarm.hmi_history.label IS 'What it is, in words: the alarm label, or the group and its new state.'",
	"COMMENT ON COLUMN alarm.hmi_history.value IS 'Alarm: the value that raised it. Safety: ENERGIZED, DE-ENERGIZED, FAULT, FAULT CLEARED, ISOLATED or ISOLATION OFF. Reset: DONE, PARTIAL or FAILED. Msgack: SENT.'",
	"COMMENT ON COLUMN alarm.hmi_history.clear_ts IS 'Alarm cleared. NULL = still active.'",
	"COMMENT ON COLUMN alarm.hmi_history.clear_est IS 'true = clear_ts is when the engine saw the alarm gone (it cleared and was acknowledged between two 1 s polls, or ended while the engine was off), not the alarm own clear time.'",
	"COMMENT ON COLUMN alarm.hmi_history.duration_s IS 'Seconds the alarm was active (set when it clears).'",
	"COMMENT ON COLUMN alarm.hmi_history.ack_user IS 'Who acknowledged the alarm (Ignition user), when known.'",
	"COMMENT ON COLUMN alarm.hmi_history.who IS 'HMI user for reset and msgack rows; on a safety ENERGIZED or FAULT CLEARED row, the HMI user when an HMI reset did it.'",
	"COMMENT ON COLUMN alarm.hmi_history.station IS 'The screen the HMI action came from.'",
	"COMMENT ON COLUMN alarm.hmi_history.detail IS 'Why: for safety rows the devices holding the group off or the reset that did it; for reset rows what came back.'",
	"COMMENT ON COLUMN alarm.hmi_history.event_id IS 'Ignition alarm event id (alarm rows only, unique).'",
	"COMMENT ON TABLE alarm.engine_status IS 'Heartbeat of the history engine (one row per engine, updated every minute). beat_ts more than 2 minutes old = the history has a gap.'",
	"COMMENT ON VIEW alarm.v_history IS 'alarm.hmi_history with event and clear times in NZ local time - the easiest read for reports and the AI box.'",
]


def _log():
	return system.util.getLogger(LOGGER)


def _now():
	return System.currentTimeMillis()


def _s(v):
	if v is None:
		return u''
	try:
		return u'%s' % (v,)
	except:
		return u''


def _clean(v, n):
	"""Text for the database: NUL characters out (PostgreSQL refuses them), cut to n; None when empty."""
	v = _s(v)
	if not v:
		return None
	if u'\x00' in v:
		v = v.replace(u'\x00', u'')
	return v[:n] or None


def _g():
	"""Engine state - gateway globals, so a project save keeps it (new version = new key = fresh state)."""
	import system
	try:
		gl = system.util.globals
	except:
		gl = system.util.getGlobals()
	st = gl.get(_KEY)
	if st is None:
		st = gl.setdefault(_KEY, {})
	return st


def _date(ms):
	return None if ms is None else Date(long(ms))


# ---------------------------------------------------------------- schema
def _ensure(g, now):
	import system
	if g.get('ready'):
		return True
	if now - g.get('ddlFailAt', 0) < DDL_RETRY_MS:
		return False
	try:
		for sql in DDL:
			system.db.runUpdateQuery(sql, DB)
	except Exception as e:
		g['ddlFailAt'] = now
		_log().warn('schema: %s' % e)
		return False
	except Throwable as t:
		g['ddlFailAt'] = now
		_log().warn('schema: %s' % t)
		return False
	for sql in DDL_DOC:
		try:
			system.db.runUpdateQuery(sql, DB)
		except Exception as e:
			_log().info('schema (view / comment - not needed by the engine): %s' % e)
		except Throwable as t:
			_log().info('schema (view / comment - not needed by the engine): %s' % t)
	g['ready'] = True
	return True


def install():
	"""Script Console: create the schema, tables, view and comments (IF NOT EXISTS - safe to re-run), then check()."""
	import system
	n = 0
	for sql in DDL + DDL_DOC:
		try:
			system.db.runUpdateQuery(sql, DB)
			n += 1
		except Exception as e:
			print 'FAILED: %s | %s' % (sql.split('\n')[0][:80], str(e)[:300])
		except Throwable as t:
			print 'FAILED: %s | %s' % (sql.split('\n')[0][:80], str(t)[:300])
	print 'install v%s: %d of %d statements OK' % (VERSION, n, len(DDL) + len(DDL_DOC))
	check()


# ---------------------------------------------------------------- writing
def _dbUp():
	import system
	try:
		system.db.runScalarQuery('SELECT 1', DB)
		return True
	except Exception:
		return False
	except Throwable:
		return False


def _chunks(fn, items, what):
	"""fn(chunk) for every BATCH items; returns the rows changed. A chunk the database refuses is tried again one item
	at a time - a bad row is left out (logged) instead of stopping the engine. With the database not answering it
	raises: the caller keeps its state and the change is written on a later tick."""
	n = 0
	for i in range(0, len(items), BATCH):
		chunk = items[i:i + BATCH]
		err = None
		try:
			n += fn(chunk)
			continue
		except Exception as e:
			err = e
		except Throwable as t:
			err = t
		if not _dbUp():
			raise IOError(u'%s: database %s not answering - %s' % (what, DB, _s(err)[:300]))
		for one in chunk:
			try:
				n += fn([one])
			except Exception as e:
				err = e
			except Throwable as t:
				err = t
			else:
				continue
			if not _dbUp():
				raise IOError(u'%s: database %s not answering - %s' % (what, DB, _s(err)[:300]))
			_log().warn(u'%s: one row left out - %s | %s' % (what, _s(err)[:300], _s(one)[:300]))
	return n


def _insertChunk(chunk):
	import system
	one = '(' + ','.join(['?'] * len(COLS)) + ')'
	args = []
	for r in chunk:
		args.extend(r)
	sql = ('INSERT INTO %s AS h (%s) VALUES %s ON CONFLICT (event_id) DO UPDATE SET clear_ts = EXCLUDED.clear_ts, '
		'clear_est = EXCLUDED.clear_est, duration_s = EXCLUDED.duration_s, ack_ts = EXCLUDED.ack_ts, '
		'ack_user = EXCLUDED.ack_user, detail = EXCLUDED.detail WHERE h.clear_est'
		% (TABLE, ', '.join(COLS), ', '.join([one] * len(chunk))))
	return system.db.runPrepUpdate(sql, args, DB)


def _insert(rows):
	"""New rows, 200 a statement. An alarm row already there (a restart, a new library version) is left as it is,
	unless its clear was only estimated - then it takes the alarm's state from the status list again."""
	return _chunks(_insertChunk, rows, 'insert')


def _row(ts, kind, area, dp, label, priority=None, source=None, eventId=None, value=None, clearTs=None, clearEst=False,
		ackTs=None, ackUser=None, dur=None, who=None, station=None, detail=None):
	return [ts, kind, area, _clean(dp, 400), _clean(label, 400), _clean(priority, 20), _clean(source, 400), eventId,
		_clean(value, 200), clearTs, bool(clearEst), ackTs, _clean(ackUser, 120), dur, _clean(who, 120),
		_clean(station, 200), _clean(detail, 1000)]


def logAction(kind, area, label, value='', who='', station='', detail='', source='', ts=None):
	"""One HMI action row (kind 'reset' or 'msgack'). Called by booth.safetyreset and the booth MESSAGE ACK button.
	ts = epoch ms of the press (default now). Returns True when written. Never raises."""
	try:
		g = _g()
		now = _now()
		if not _ensure(g, now):
			return False
		a = _s(area).strip().upper() or 'GEN'
		dp = u'%s/HMI/%s' % (AREA_WORD.get(a, a), HMI_WORD.get(kind, kind))
		row = _row(_date(ts or now), kind, a, dp, label, source=source, value=value, who=who, station=station,
			detail=detail)
		return _insert([row]) == 1
	except Exception as e:
		_log().warn('logAction(%s, %s): %s' % (kind, area, e))
	except Throwable as t:
		_log().warn('logAction(%s, %s): %s' % (kind, area, t))
	return False


# ---------------------------------------------------------------- alarms
def _ms(data):
	"""EventData timestamp -> epoch ms (a Date on this gateway; a long is handled too)."""
	if data is None:
		return None
	try:
		ts = data.getTimestamp()
	except:
		return None
	if ts is None:
		return None
	try:
		return long(ts.getTime())
	except AttributeError:
		try:
			return long(ts)
		except:
			return None


def _flag(fn):
	try:
		return bool(fn())
	except:
		return False


def _clearMs(e):
	if not _flag(e.isCleared):
		return None
	try:
		return _ms(e.getClearedData())
	except:
		return None


def _ackMs(e):
	if not _flag(e.isAcked):
		return None
	try:
		return _ms(e.getAckData())
	except:
		return None


def _prop(data, names):
	try:
		from com.inductiveautomation.ignition.common.alarming.config import CommonAlarmProperties as P
	except:
		return None
	if data is None:
		return None
	for n in names:
		try:
			v = data.get(getattr(P, n))
			if v is not None and _s(v):
				return v
		except:
			pass
	return None


def _ackUser(e):
	try:
		v = _s(_prop(e.getAckData(), ('AckUserName', 'AckUser')))
	except:
		return None
	if not v:
		return None
	if '/usr:' in v:
		v = v.split('/usr:')[-1]
	return v


def _value(e):
	try:
		v = _prop(e.getActiveData(), ('EventValue',))
		return None if v is None else _s(v)
	except:
		return None


def areaOf(source, displayPath=''):
	"""Area code from an alarm's source path (tag folder), else from its display path; GEN when neither says."""
	s = _s(source).upper()
	for key, code in AREA_BY_PATH:
		if key in s:
			return code
	d = _s(displayPath).upper()
	for key, code in AREA_BY_WORD:
		if key in d:
			return code
	return 'GEN'


def _alarmRow(eid, e, now):
	act = None
	try:
		act = _ms(e.getActiveData())
	except:
		act = None
	if act is None:
		act = now
	clr = _clearMs(e)
	ak = _ackMs(e)
	src = _s(e.getSource())
	dp = _s(e.getDisplayPath())
	if not dp:
		# no display path: the tag path, readable ('KPP/StemDB/.../Alarm')
		dp = src
		if ':/tag:' in dp:
			dp = dp.split(':/tag:')[-1].replace(':/alm:', '/')
	label = _s(e.getLabel()) or _s(e.getName())
	dur = None if clr is None else max(0.0, (clr - act) / 1000.0)
	return _row(_date(act), 'alarm', areaOf(src, dp), dp, label, priority=_s(e.getPriority()), source=src, eventId=eid,
		value=_value(e), clearTs=_date(clr), ackTs=_date(ak), ackUser=_ackUser(e) if ak else None, dur=dur)


def _closeRows(items):
	"""items: (event_id, clear_ms, estimated). Sets clear_ts and duration on rows still open, and puts a real clear
	time over an estimated one - 200 a statement."""
	import system
	one = '(CAST(? AS text), CAST(? AS timestamptz), CAST(? AS boolean))'

	def fn(chunk):
		args = []
		for eid, ms, est in chunk:
			args.extend([eid, _date(ms), bool(est)])
		sql = ('UPDATE %s h SET clear_ts = v.ts, clear_est = v.est, duration_s = GREATEST(0, EXTRACT(EPOCH FROM (v.ts - '
			'h.event_ts))), detail = CASE WHEN h.clear_ts IS NULL THEN h.detail ELSE NULL END FROM (VALUES %s) AS '
			'v(eid, ts, est) WHERE h.event_id = v.eid AND (h.clear_ts IS NULL OR (h.clear_est AND NOT v.est))'
			% (TABLE, ', '.join([one] * len(chunk))))
		return system.db.runPrepUpdate(sql, args, DB)
	return _chunks(fn, items, 'clear')


def _ackRows(items):
	"""items: (event_id, ack_ms, user) - 200 a statement."""
	import system
	one = '(CAST(? AS text), CAST(? AS timestamptz), CAST(? AS text))'

	def fn(chunk):
		args = []
		for eid, ms, user in chunk:
			args.extend([eid, _date(ms), _clean(user, 120)])
		sql = ('UPDATE %s h SET ack_ts = v.ts, ack_user = COALESCE(v.u, h.ack_user) FROM (VALUES %s) AS v(eid, ts, u) '
			'WHERE h.event_id = v.eid AND h.ack_ts IS NULL' % (TABLE, ', '.join([one] * len(chunk))))
		return system.db.runPrepUpdate(sql, args, DB)
	return _chunks(fn, items, 'ack')


def _reconcile(g, seen):
	"""Once, RECONCILE_MS after a (re)start: close the occurrences still open in the table that the engine has not
	seen in the status list since it started - they ended while it was off."""
	import system
	ds = system.db.runQuery("SELECT event_id FROM %s WHERE kind = 'alarm' AND clear_ts IS NULL AND event_id IS NOT NULL"
		% TABLE, DB)
	gone = []
	for r in range(ds.getRowCount()):
		eid = _s(ds.getValueAt(r, 0))
		if eid and eid not in seen:
			gone.append(eid)
	if not gone:
		return 0
	start = _date(g.get('started') or _now())

	def fn(chunk):
		sql = ("UPDATE %s SET clear_ts = CAST(? AS timestamptz), clear_est = true, duration_s = GREATEST(0, EXTRACT(EPOCH "
			"FROM (CAST(? AS timestamptz) - event_ts))), detail = CAST(? AS text) WHERE kind = 'alarm' AND clear_ts IS NULL "
			"AND event_id IN (%s)" % (TABLE, ', '.join(['?'] * len(chunk))))
		return system.db.runPrepUpdate(sql, [start, start, NOTE_OFF] + list(chunk), DB)
	n = _chunks(fn, gone, 'reconcile')
	if n:
		_log().info('start: closed %d alarm occurrences that ended while the engine was off' % n)
	return n


def _tickAlarms(g, now):
	import system
	try:
		evs = system.alarm.queryStatus(includeShelved=True)
	except TypeError:
		evs = system.alarm.queryStatus()
	cur = {}
	for e in evs:
		try:
			cur[_s(e.getId())] = e
		except:
			pass
	known = g.get('known')
	if known is None:
		known = {}
	oldest = now - KEEP_DAYS * 86400000
	ins, clr, ack = [], [], []
	state = {}           # event id -> (cleared, acked, event, polls missing, first poll missing)
	for eid, e in cur.items():
		cl, ak = _flag(e.isCleared), _flag(e.isAcked)
		state[eid] = (cl, ak, e, 0, 0)
		k = known.get(eid)
		if k is None:
			row = _alarmRow(eid, e, now)
			if row[0].getTime() < oldest:
				continue          # older than the history keeps: followed in memory only
			ins.append(row)
			# the row may be there already (a restart, a new library version): bring it up to date
			if cl:
				ms = _clearMs(e)
				clr.append((eid, ms or now, ms is None))
			if ak:
				ms = _ackMs(e)
				ack.append((eid, ms or now, _ackUser(e)))
		else:
			if cl and not k[0]:
				ms = _clearMs(e)
				clr.append((eid, ms or now, ms is None))
			if ak and not k[1]:
				ms = _ackMs(e)
				ack.append((eid, ms or now, _ackUser(e)))
	for eid, k in known.items():
		if eid in cur:
			continue
		miss, first = k[3] + 1, k[4] or now
		if miss < VANISH_POLLS:
			state[eid] = (k[0], k[1], k[2], miss, first)      # one poll without it is not an end yet
			continue
		# missing 3 polls running: it cleared and was acknowledged at about the first poll without it
		e = k[2]
		if not k[0]:
			ms = _clearMs(e)
			clr.append((eid, ms or first, ms is None))
		if not k[1]:
			ms = _ackMs(e)
			ack.append((eid, ms or first, _ackUser(e)))
	n = 0
	if ins:
		n += _insert(ins)
	if clr:
		n += _closeRows(clr)
	if ack:
		n += _ackRows(ack)
	g['known'] = state
	g['open'] = len([1 for v in state.values() if not v[0]])
	if not g.get('reconciled') and now - g.get('started', now) >= RECONCILE_MS:
		n += _reconcile(g, state)
		g['reconciled'] = True
	return n


# ---------------------------------------------------------------- isolation groups
def _resetPlaces(grp):
	places = []
	for r in grp.get('resets', []):
		p = booth.safety.RESET_AT.get(r, r)
		if r[:3] != grp['area'] and not (grp['area'] == 'TNB' and r[:3] == 'STL'):
			p = r[:3] + ' ' + p
		if p not in places:
			places.append(p)
	if not places:
		return u'a reset button'
	if len(places) == 1:
		return u'the reset button at %s' % places[0]
	return u'a reset button (%s)' % u', '.join(places)


def _igRow(ig, flag, on, qts, vals, now):
	grp = booth.safety.GROUPS[ig]
	area, no, name = grp['area'], grp['no'], grp['name']
	if flag == 'GroupEn':
		word = 'ENERGIZED' if on else 'DE-ENERGIZED'
	elif flag == 'GroupFaultActive':
		word = 'FAULT' if on else 'FAULT CLEARED'
	else:
		word = 'ISOLATED' if on else 'ISOLATION OFF'
	who = station = None
	detail = u''
	if word in ('ENERGIZED', 'FAULT CLEARED'):
		r = None
		try:
			r = booth.safetyreset.recent(ig, 8000)
		except:
			r = None
		if r:
			who, station = r[0] or None, r[1] or None
			detail = u'HMI reset (RESET ALL IGs) by %s' % (r[0] or 'no login')
		else:
			detail = _resetPlaces(grp)
		if word == 'FAULT CLEARED':
			detail = u'fault reset (reset held 3 s) - ' + detail
		else:
			detail = u'reset - ' + detail
	elif word != 'ISOLATION OFF':
		try:
			v = vals.get(area)
			if v is None:
				v = booth.safety.Values(booth.safety._read(booth.safety._paths(area, booth.safety._structure(area))))
				vals[area] = v
			t, w, why, hint = booth.safety.groupState(v, ig)
			detail = w + ((u': ' + booth.safety._whyText(why, 6)) if why else u'')
		except Exception as e:
			detail = u'(why not read: %s)' % _s(e)
		except Throwable as t:
			detail = u'(why not read: %s)' % _s(t)
	ms = None
	try:
		ms = long(qts.getTime())
	except:
		ms = None
	if ms is None or ms > now + 5000 or ms < now - 120000:
		ms = now
	label = u'%s IG%d %s - %s' % (area, no, name, word)
	dp = u'%s/Safety/%s' % (AREA_WORD.get(area, area), ig)
	return _row(_date(ms), 'safety', area, dp, label, source=booth.safety.groupPath(ig, 'GroupTags/' + flag), value=word,
		who=who, station=station, detail=detail)


def _tickSafety(g, now):
	import system
	try:
		groups = booth.safety.GROUPS
	except:
		return 0
	igs = g.get('igs')
	if igs is None:
		igs = sorted([ig for ig in groups if groups[ig].get('tags')])
		g['igs'] = igs
	paths = []
	for ig in igs:
		for f in IG_FLAGS:
			paths.append(booth.safety.groupPath(ig, 'GroupTags/' + f))
	qvs = system.tag.readBlocking(paths, TAG_TIMEOUT_MS)
	prev = g.get('ig')
	cur = {}
	rows = []
	vals = {}
	for i, ig in enumerate(igs):
		q = qvs[3 * i:3 * i + 3]
		good = True
		for x in q:
			try:
				if not x.quality.isGood():
					good = False
			except:
				good = False
		if not good:
			if prev and ig in prev:
				cur[ig] = prev[ig]
			continue
		st = tuple([bool(x.value) for x in q])
		cur[ig] = st
		p = prev.get(ig) if prev else None
		if p is None:
			continue
		for j in range(len(IG_FLAGS)):
			if st[j] != p[j]:
				rows.append(_igRow(ig, IG_FLAGS[j], st[j], q[j].timestamp, vals, now))
	n = _insert(rows) if rows else 0       # first: with the database down the old state stays, the change is seen again
	g['ig'] = cur
	return n


# ---------------------------------------------------------------- the timer
def _beat(g, now):
	import system
	err = g.get('err') or (None, 0)
	system.db.runPrepUpdate("INSERT INTO alarm.engine_status (engine, beat_ts, started_ts, version, alarms_open, "
		"groups_read, rows_written, last_error, last_error_ts) VALUES (?, now(), ?, ?, ?, ?, ?, ?, ?) "
		"ON CONFLICT (engine) DO UPDATE SET beat_ts = now(), started_ts = EXCLUDED.started_ts, version = EXCLUDED.version, "
		"alarms_open = EXCLUDED.alarms_open, groups_read = EXCLUDED.groups_read, rows_written = EXCLUDED.rows_written, "
		"last_error = EXCLUDED.last_error, last_error_ts = EXCLUDED.last_error_ts",
		[ENGINE, _date(g.get('started')), VERSION, int(g.get('open', 0)), len(g.get('ig') or {}),
		long(g.get('rows', 0)), _clean(err[0], 400), _date(err[1]) if err[1] else None], DB)
	g['beat'] = now


def _err(g, now, msg):
	"""The last error goes to the heartbeat row; each distinct message is logged at most once a minute."""
	m = _s(msg)[:400]
	g['err'] = (m, now)
	seen = g.setdefault('errLogged', {})
	if now - seen.get(m, 0) > 60000:
		if len(seen) > 50:
			for k in [k for k, t in seen.items() if now - t > 60000]:
				del seen[k]
		seen[m] = now
		_log().warn(u'tick: %s' % m)


def tick():
	"""Gateway timer body (fixed delay 1000 ms). Never raises."""
	g = _g()
	now = _now()
	try:
		if not _ensure(g, now):
			return
		if not g.get('started'):
			g['started'] = now
		n = 0
		try:
			n += _tickAlarms(g, now)
		except Exception as e:
			_err(g, now, u'alarms: %s' % _s(e))
		except Throwable as t:
			_err(g, now, u'alarms: %s' % _s(t))
		try:
			n += _tickSafety(g, now)
		except Exception as e:
			_err(g, now, u'safety: %s' % _s(e))
		except Throwable as t:
			_err(g, now, u'safety: %s' % _s(t))
		g['rows'] = g.get('rows', 0) + n
		if now - g.get('beat', 0) >= BEAT_MS:
			_beat(g, now)
	except Exception as e:
		_err(g, now, _s(e))
	except Throwable as t:
		_err(g, now, _s(t))


# ---------------------------------------------------------------- the booth popup
def _like(text):
	return _s(text).replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_')


def _dur(sec):
	if sec is None:
		return u''
	s = int(round(float(sec)))
	if s < 60:
		return u'%d s' % s
	if s < 3600:
		return u'%d min %02d s' % (s // 60, s % 60)
	if s < 86400:
		return u'%d h %02d min' % (s // 3600, (s % 3600) // 60)
	return u'%d d %d h' % (s // 86400, (s % 86400) // 3600)


def _tone(kind, value, active, priority):
	"""(colour, weight) of a row on the light booth popup."""
	v = _s(value).upper()
	if kind == 'alarm':
		if active:
			return '#C02026', 700
		if _s(priority) in ('Diagnostic', 'Low'):
			return '#5F696B', 400
		return '#242E30', 400
	if kind == 'safety':
		return {'ENERGIZED': ('#0A733A', 700), 'FAULT': ('#C02026', 700), 'DE-ENERGIZED': ('#B4560F', 600),
			'ISOLATED': ('#8A6100', 600), 'FAULT CLEARED': ('#004063', 600)}.get(v, ('#4A5558', 400))
	if kind == 'reset':
		return {'DONE': ('#004063', 700), 'PARTIAL': ('#B4560F', 700), 'FAILED': ('#C02026', 700)}.get(v, ('#004063', 700))
	return '#004063', 600


def rows(filterText='', hours=24, mode='all', search='', limit=ROWS_MAX):
	"""The HISTORY tab of Application/Booth/Popups/Alarms: newest first.
	filterText = the booth's display path filter ('SDB,HOG' - either word anywhere, as the live table);
	hours 1..720; mode 'all' | 'alarms' | 'safety' (safety changes, resets and message acks); search = any text.
	Returns {'rows': [table rows of {value, style} cells], 'info': text, 'infoColor': colour}. Never raises."""
	import system
	out = {'rows': [], 'info': '', 'infoColor': '#5F696B'}
	try:
		try:
			h = int(hours or 24)
		except:
			h = 24
		h = max(1, min(24 * KEEP_DAYS, h))
		now = _now()
		where = ['event_ts >= ?']
		args = [Date(long(now - h * 3600000))]
		m = _s(mode).lower()
		if m == 'alarms':
			where.append("kind = 'alarm'")
		elif m == 'safety':
			where.append("kind <> 'alarm'")
		parts = [p.strip() for p in _s(filterText).split(',') if p.strip()]
		if parts:
			where.append('(' + ' OR '.join(['display_path ILIKE ?'] * len(parts)) + ')')
			args.extend([u'%' + _like(p) + u'%' for p in parts])
		q = _s(search).strip()
		if q:
			where.append('(label ILIKE ? OR display_path ILIKE ? OR detail ILIKE ? OR value ILIKE ? OR who ILIKE ? '
				'OR ack_user ILIKE ?)')
			args.extend([u'%' + _like(q) + u'%'] * 6)
		lim = max(10, min(2000, int(limit)))
		sql = ('SELECT event_ts, kind, label, display_path, value, clear_ts, clear_est, duration_s, ack_user, who, detail, '
			'priority FROM %s WHERE %s ORDER BY event_ts DESC, id DESC LIMIT %d' % (TABLE, ' AND '.join(where), lim + 1))
		ds = system.db.runPrepQuery(sql, args, DB)
		n = ds.getRowCount()
		for r in range(min(n, lim)):
			ts = ds.getValueAt(r, 0)
			kind = _s(ds.getValueAt(r, 1))
			label = _s(ds.getValueAt(r, 2))
			dp = _s(ds.getValueAt(r, 3))
			value = _s(ds.getValueAt(r, 4))
			clr = ds.getValueAt(r, 5)
			est = bool(ds.getValueAt(r, 6))
			dur = ds.getValueAt(r, 7)
			ackUser = _s(ds.getValueAt(r, 8))
			who = _s(ds.getValueAt(r, 9))
			detail = _s(ds.getValueAt(r, 10))
			pri = _s(ds.getValueAt(r, 11))
			active = kind == 'alarm' and clr is None
			if kind == 'alarm':
				state = u'ACTIVE' if active else (u'CLEARED %s%s' % ('~' if est else '', system.date.format(clr, 'HH:mm:ss')))
				if active:
					lasted = u'for ' + _dur((now - ts.getTime()) / 1000.0)
				else:
					lasted = _dur(dur)
				det = dp
				by = (u'ack ' + ackUser) if ackUser else u''
			elif kind == 'msgack':
				state, lasted, det, by = value or u'SENT', u'', detail, who
			else:
				state, lasted, det, by = value, u'', detail, who
				if kind == 'safety' and value and label.endswith(u' - ' + value):
					label = label[:-len(u' - ' + value)]
			col, fw = _tone(kind, value, active, pri)
			cells = {'when': system.date.format(ts, 'EEE dd/MM HH:mm:ss'), 'type': KIND_WORD.get(kind, kind.upper()),
				'what': label, 'detail': det, 'state': state, 'lasted': lasted, 'by': by}
			row = {}
			for k, v in cells.items():
				st = {'color': col, 'fontWeight': fw if k in ('what', 'state', 'type') else 400}
				if k == 'when':
					st['color'] = '#4A5558'
				row[k] = {'value': v, 'style': st}
			out['rows'].append(row)
		span = (u'%d h' % h) if h < 48 else (u'%d days' % (h // 24))
		what = {'alarms': u'alarms', 'safety': u'safety changes and resets'}.get(m, u'events')
		if n > lim:
			out['info'] = u'newest %d %s in the last %s - narrow the range or search' % (lim, what, span)
		elif n:
			out['info'] = u'%d %s in the last %s - newest first' % (n, what, span)
		else:
			out['info'] = u'no %s in the last %s' % (what, span)
	except Exception as e:
		out['info'], out['infoColor'] = u'history not readable: %s' % _s(e)[:200], '#C02026'
		_log().warn('rows: %s' % e)
	except Throwable as t:
		out['info'], out['infoColor'] = u'history not readable: %s' % _s(t)[:200], '#C02026'
		_log().warn('rows: %s' % t)
	return out


# ---------------------------------------------------------------- console
def check(last=8):
	"""Script Console, read only: rows by kind (24 h / 30 days), open alarms, the engine heartbeat, the newest rows."""
	import system
	try:
		ds = system.db.runQuery("SELECT kind, count(*) FILTER (WHERE event_ts > now() - interval '24 hours'), count(*), "
			"min(event_ts) FROM %s GROUP BY kind ORDER BY kind" % TABLE, DB)
		print 'forensics.alarmHistory v%s - %s' % (VERSION, TABLE)
		for r in range(ds.getRowCount()):
			line = '  %-7s 24 h %6s | all %7s | oldest %s' % (ds.getValueAt(r, 0), ds.getValueAt(r, 1), ds.getValueAt(r, 2),
				ds.getValueAt(r, 3))
			print line
		ds = system.db.runQuery("SELECT count(*) FROM %s WHERE kind = 'alarm' AND clear_ts IS NULL" % TABLE, DB)
		print '  open alarm occurrences: %s' % ds.getValueAt(0, 0)
		ds = system.db.runQuery("SELECT engine, beat_ts, round(EXTRACT(EPOCH FROM (now() - beat_ts))), version, "
			"alarms_open, groups_read, rows_written, last_error, last_error_ts FROM alarm.engine_status", DB)
		if ds.getRowCount() == 0:
			print '  engine: no heartbeat yet - is the timer AlarmHistory_FixedDelay enabled and saved?'
		for r in range(ds.getRowCount()):
			line = '  engine %s v%s: beat %s s ago | open %s | groups %s | rows %s | last error %s %s' % (
				ds.getValueAt(r, 0), ds.getValueAt(r, 3), ds.getValueAt(r, 2), ds.getValueAt(r, 4), ds.getValueAt(r, 5),
				ds.getValueAt(r, 6), ds.getValueAt(r, 7), ds.getValueAt(r, 8))
			print line
		ds = system.db.runQuery("SELECT event_ts, kind, area, label, value, who, detail FROM %s ORDER BY event_ts DESC, id "
			"DESC LIMIT %d" % (TABLE, max(1, min(50, int(last)))), DB)
		for r in range(ds.getRowCount()):
			line = '  %s %-7s %-4s %s | %s | %s | %s' % (ds.getValueAt(r, 0), ds.getValueAt(r, 1), ds.getValueAt(r, 2),
				_s(ds.getValueAt(r, 3))[:70], ds.getValueAt(r, 4), ds.getValueAt(r, 5), _s(ds.getValueAt(r, 6))[:80])
			print line
	except Exception as e:
		print 'check failed: %s' % str(e)[:300]
	except Throwable as t:
		print 'check failed: %s' % str(t)[:300]
