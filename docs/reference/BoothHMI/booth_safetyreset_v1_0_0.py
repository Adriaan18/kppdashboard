# =============================================================================
# booth_safetyreset_v1_0_0.py
# Project library script:  booth.safetyreset     (package booth = plain folder)
# Author:   Adriaan
# Version:  1.0.0  (2026-10-28)
# Truth test (Script Console):  print booth.safetyreset.VERSION   -> 1.0.0
#                               booth.safetyreset.check()          -> one line per area (read only)
#
# RESET ALL IGs in ONE press, with no change to the safety program (KPP_COS_V20T, safety locked).
# What the safety PLC does with an area's HMI reset bit <X>_ToSafetyMap.<X>_HMI_RB (mapped to <X>_SafetyMap):
#   - held 3 s     -> tFaultResetTON (3000 ms) -> FaultResetPulse (TOF) clears GroupFaultActive and the device faults
#   - released     -> the falling edge is the group reset (GroupResetONS) - IGNORED while FaultResetPulse is on
#   - held 5 s     -> the standard routine _099_HMI_RB_Timeout clears the bit (the PLC's own stuck-bit guard)
# press() does both steps from a gateway thread, so the HMI button is a plain tap:
#     hold 3.5 s  ->  release  ->  wait out the fault-reset pulse  ->  tap 0.2 s  ->  release  ->  read the groups back
# The FaultResetPulse TOF is 500 ms on every group EXCEPT Grading (GRA_IG1-3: 2000 ms). A tap inside the pulse is
# ignored, so the wait is per area: the tap starts no earlier than 3.0 s + pulse + 0.8 s after the hold began
# (Grading 2.3 s gap, every other area 1.0 s). Whether the 3.5 s release lands just inside or just after a 500 ms
# pulse does not matter - either way the groups end up reset (a second reset on an energized group does nothing).
# The reset can only do what the reset buttons do: an open gate (local gate reset), an activated isolator, a
# pressed E-stop or a fault that is still there keeps its group off - the read-back says which.
# Which groups each HMI reset reaches is the PLC's own wiring (REACH below, read from KPP_COS_V20T 27 Oct 2026):
# the COS reset also resets T&B IG1-5 and Chippers IG7. DDB has no HMI reset in the PLC - monitoring only.
# Guards: one sequence per area at a time (lock in system.util.globals - a second press is refused, never taken
# over while the first can still be writing); a True is written once and never retried, and every way out writes
# False; the hold is abandoned if another screen releases the bit (the old Zone / MapCards press-and-hold buttons
# write the same tag); tag reads and writes have short timeouts, so a sequence cannot outlive its lock.
#
# Used by:
#   Application/Safety/Components/AreaSafetyCard   RESET ALL IGs button (Diag view)    press() / state()
#   Application/Booth/Popups/SafetyDiag             RESET ALL IGs button (popup)        press() / state()
#   forensics.alarmHistory                           recent() - an IG energized during an HMI reset names who
# Every press is written to the HMI alarm history (forensics.alarmHistory.logAction, kind 'reset') when that
# library is installed; without it the reset still works.
#
# Changelog (newest first):
#   1.0.0  2026-10-28  First issue.
# =============================================================================

from java.lang import Throwable, System, Thread

VERSION = '1.0.0'
LOGGER = 'booth.safetyreset'
PROV = '[TL-KPPWS01-01]KPP/'

# area -> the Ignition tag of <X>_ToSafetyMap.<X>_HMI_RB (the tags the old reset buttons write)
RB_TAG = {
	'SDB': PROV + 'StemDB/Data/Safety/SDB_HMI_RB',
	'GRA': PROV + 'Grader/Data/Safety/GRA_HMI_RB',
	'COS': PROV + 'COS/Area/Data/Safety/COS_HMI_RB',
	'TNB': PROV + 'TnB/Data/Safety/TNB_HMI_RB',
	'CHP': PROV + 'Chippers/Data/Safety/CHP_HMI_RB',
	'HOG': PROV + 'HOG/Data/Safety/HOG_HMI_RB',
}
AREA_NAME = {'SDB': 'Stem Debarker', 'GRA': 'Grading', 'COS': 'Cut Off Saw', 'TNB': 'T&B + Sortline',
	'CHP': 'Chippers', 'HOG': 'Hog + refuse', 'DDB': 'Drum debarker'}

# isolation groups whose GroupResetONS and fault-reset rungs carry the area's HMI reset bit (KPP_COS_V20T)
REACH = {
	'SDB': ['SDB_IG1', 'SDB_IG2', 'SDB_IG3', 'SDB_IG4'],
	'GRA': ['GRA_IG1', 'GRA_IG2', 'GRA_IG3'],
	'COS': ['COS_IG1', 'COS_IG2', 'TNB_IG1', 'TNB_IG2', 'TNB_IG3', 'TNB_IG4', 'TNB_IG5', 'CHP_IG7'],
	'TNB': ['TNB_IG1', 'TNB_IG2', 'TNB_IG3', 'TNB_IG4', 'TNB_IG5'],
	'CHP': ['CHP_IG1', 'CHP_IG2', 'CHP_IG3', 'CHP_IG4', 'CHP_IG5', 'CHP_IG6', 'CHP_IG7'],
	'HOG': ['HOG_IG1', 'HOG_IG2', 'HOG_IG3', 'HOG_IG4', 'HOG_IG5'],
}
REACH_TEXT = {
	'SDB': u'SDB IG1-4',
	'GRA': u'GRA IG1-3',
	'COS': u'COS IG1-2 + T&B IG1-5 + CHP IG7',
	'TNB': u'T&B IG1-5',
	'CHP': u'CHP IG1-7',
	'HOG': u'HOG IG1-5',
}

# timing (ms) - the PLC side: tFaultResetTON.PRE 3000 on every group, tFaultResetPulse.PRE 500 (Grading 2000),
# safety task 50 ms, HMI reset timeout 5000 ms
HOLD_MS = 3500           # the fault-reset hold (the asked 3.5 s): 0.5 s over the PLC's 3 s
TAP_MS = 200             # the group-reset tap (4 safety-task scans)
TON_MS = 3000
PULSE_MS = {'GRA': 2000}
PULSE_DEFAULT_MS = 500
MARGIN_MS = 800          # after the pulse ends, before the tap starts
GAP_MIN_MS = 1000
WATCH_MS = 250           # how often the hold checks that nobody else released the bit
CHECK_MS = (1200, 1000)  # read the groups back 1.2 s after the tap, once more 1 s later if any is not energized
READ_TIMEOUT_MS = 2000
WATCH_READ_MS = 300      # the hold's watch reads must not stretch the hold
WRITE_TIMEOUT_MS = 3000
SHOW_MS = 12000          # the result stays on the buttons
STALE_MS = 120000        # a lock this old has no live thread (a sequence is bounded well under a minute)

RUNNING = ('start', 'hold', 'gap', 'tap', 'check')
_KEY = 'booth.safetyreset'


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


def _area(area):
	a = _s(area).strip().upper()
	if a in ('T&B', 'TNB', 'SORT', 'STL'):
		return 'TNB'
	return a


def gapMs(area):
	"""Release-to-tap wait for an area: the tap must start after the fault-reset pulse has ended."""
	pulse = PULSE_MS.get(_area(area), PULSE_DEFAULT_MS)
	return max(GAP_MIN_MS, TON_MS + pulse + MARGIN_MS - HOLD_MS)


def _store():
	"""Gateway-wide map (survives a project save, so a running reset keeps its lock)."""
	import system
	try:
		g = system.util.globals
	except:
		g = system.util.getGlobals()
	m = g.get(_KEY)
	if m is None:
		from java.util.concurrent import ConcurrentHashMap
		m = g.setdefault(_KEY, ConcurrentHashMap())
	return m


# ---------------------------------------------------------------- tags
def _readOne(path, timeout=READ_TIMEOUT_MS):
	"""(value, good)"""
	import system
	try:
		q = system.tag.readBlocking([path], timeout)[0]
		return q.value, bool(q.quality.isGood())
	except Exception as e:
		_log().warn('read %s: %s' % (path, e))
	except Throwable as t:
		_log().warn('read %s: %s' % (path, t))
	return None, False


def _write(path, value, tries=1):
	"""True when the write came back Good. A True is written once (a retry could add edges); False may be retried -
	it is idempotent, and the PLC clears a stuck True after 5 s anyway."""
	import system
	last = ''
	for i in range(tries):
		try:
			q = system.tag.writeBlocking([path], [value], WRITE_TIMEOUT_MS)[0]
			if q.isGood():
				return True
			last = _s(q)
		except Exception as e:
			last = _s(e)
		except Throwable as t:
			last = _s(t)
		if i < tries - 1:
			Thread.sleep(100)
	_log().warn('write %s = %s failed: %s' % (path, value, last))
	return False


def _groupWords(igs):
	"""{ig: (tone, word)} for the groups with Ignition tags - the popup's own state rules (booth.safety._quick)."""
	out = {}
	try:
		have = [ig for ig in igs if ig in booth.safety.GROUPS and booth.safety.GROUPS[ig]['tags']]
		paths = []
		for ig in have:
			for f in booth.safety.CORE_FLAGS:
				paths.append(booth.safety.groupPath(ig, 'GroupTags/' + f))
		vals = booth.safety.Values(booth.safety._read(paths))
		for ig in have:
			t, w, _why, _h = booth.safety._quick(vals, ig)
			out[ig] = (t, w)
	except Exception as e:
		_log().warn('groupWords: %s' % e)
	except Throwable as t:
		_log().warn('groupWords: %s' % t)
	return out


def _short(ig):
	try:
		g = booth.safety.GROUPS.get(ig)
		if g:
			return u'%s IG%d' % ('T&B' if g['area'] == 'TNB' else g['area'], g['no'])
	except:
		pass
	return _s(ig).replace('_', ' ')


def _summary(words):
	"""'2 of 2 energized' or '5 of 7 energized - T&B IG2 isolated, CHP IG3 fault'."""
	if not words:
		return u'no group data to read back', False
	order = sorted(words.keys())
	on = [ig for ig in order if words[ig][1] == 'ENERGIZED']
	off = [ig for ig in order if words[ig][1] != 'ENERGIZED']
	text = u'%d of %d energized' % (len(on), len(order))
	if off:
		text += u' - ' + u', '.join(u'%s %s' % (_short(ig), words[ig][1].lower()) for ig in off[:4])
		if len(off) > 4:
			text += u' +%d more' % (len(off) - 4)
	return text, not off


# ---------------------------------------------------------------- the sequence
def press(area, who='', station=''):
	"""RESET ALL IGs for one area: starts the hold-and-tap sequence on a gateway thread and returns at once.
	Returns 'started', 'busy' (a reset of this area is running), 'no reset' (no HMI reset for the area) or 'error'."""
	import system
	a = _area(area)
	if a not in RB_TAG:
		return 'no reset'
	m = _store()
	lockKey = 'lock:' + a
	now = _now()
	token = '%d-%s' % (now, id(m))
	held = m.putIfAbsent(lockKey, token)
	if held is not None:
		try:
			age = now - long(_s(held).split('-')[0])
		except:
			age = 0
		# the running thread always frees its own lock; only a lock far older than any sequence is taken over
		if age < STALE_MS or not m.replace(lockKey, held, token):
			return 'busy'
		_log().warn('press(%s): took over a lock %d s old' % (a, age // 1000))
	rec = {'area': a, 'token': token, 'step': 'start', 'started': now, 'stepEnd': now, 'ended': 0, 'tapAt': 0,
		'who': _s(who) or u'no login', 'station': _s(station), 'msg': u'', 'ok': False, 'gap': gapMs(a), 'words': {}}
	m.put('rec:' + a, rec)

	def job(a=a, rec=rec, token=token, lockKey=lockKey):
		try:
			_run(a, rec)
		finally:
			try:
				_store().remove(lockKey, token)
			except:
				pass
	try:
		system.util.invokeAsynchronous(job)
		return 'started'
	except Exception as e:
		rec['step'], rec['msg'], rec['ended'] = 'failed', u'could not start: %s' % _s(e), _now()
		m.remove(lockKey, token)
	except Throwable as t:
		rec['step'], rec['msg'], rec['ended'] = 'failed', u'could not start: %s' % _s(t), _now()
		m.remove(lockKey, token)
	return 'error'


def _sleepUntil(t):
	d = t - _now()
	if d > 0:
		Thread.sleep(d)


def _holdUntil(path, t):
	"""Sleep to t, checking every WATCH_MS that nobody else released the bit. False if it went True -> False."""
	seen = False
	while True:
		d = t - _now()
		if d <= 0:
			return True
		Thread.sleep(min(d, WATCH_MS))
		if _now() >= t:
			return True
		v, good = _readOne(path, WATCH_READ_MS)
		if good and v:
			seen = True
		elif good and seen and not v:
			return False


def _run(a, rec):
	"""The sequence. Never raises; the record carries the outcome."""
	import system
	path = RB_TAG[a]
	wroteTrue = False
	try:
		v, good = _readOne(path)
		if not good:
			raise ValueError(u'the reset tag cannot be read (%s)' % path)
		if v:
			raise ValueError(u'the reset is held from another screen - try again in 5 s')

		# 1. hold - fault reset (FaultResetPulse after 3 s)
		rec['step'] = 'hold'
		wroteTrue = True                  # from here every way out writes False, even if this write reports Bad
		if not _write(path, True):
			raise ValueError(u'the PLC did not confirm the reset - check the groups, then press again')
		t1 = _now()
		rec['stepEnd'] = t1 + HOLD_MS
		if not _holdUntil(path, t1 + HOLD_MS):
			raise ValueError(u'another screen released the reset during the hold - press again')
		if not _write(path, False, 3):
			raise ValueError(u'the reset could not be released - the PLC clears it after 5 s; press again then')
		wroteTrue = False

		# 2. wait out the fault-reset pulse (a tap inside it is ignored by the PLC)
		rec['step'] = 'gap'
		tapStart = max(_now() + GAP_MIN_MS, t1 + TON_MS + PULSE_MS.get(a, PULSE_DEFAULT_MS) + MARGIN_MS)
		rec['stepEnd'] = tapStart
		_sleepUntil(tapStart)

		# 3. tap - its falling edge is the group reset
		rec['step'] = 'tap'
		wroteTrue = True
		if not _write(path, True):
			raise ValueError(u'the PLC did not confirm the group reset tap - check the groups')
		t2 = _now()
		rec['stepEnd'] = t2 + TAP_MS
		_sleepUntil(t2 + TAP_MS)
		if not _write(path, False, 3):
			raise ValueError(u'the tap could not be released - the PLC clears it after 5 s')
		wroteTrue = False
		rec['tapAt'] = _now()

		# 4. read the groups back
		rec['step'] = 'check'
		rec['stepEnd'] = _now() + sum(CHECK_MS)
		Thread.sleep(CHECK_MS[0])
		words = _groupWords(REACH[a])
		if [w for w in words.values() if w[1] != 'ENERGIZED']:
			Thread.sleep(CHECK_MS[1])
			words = _groupWords(REACH[a])
		text, ok = _summary(words)
		rec['words'] = dict((k, w[1]) for k, w in words.items())
		rec['msg'], rec['ok'] = text, ok
		rec['step'] = 'done'
	except ValueError as e:
		rec['step'], rec['msg'] = 'failed', _s(e)
	except Exception as e:
		rec['step'], rec['msg'] = 'failed', u'error: %s' % _s(e)
		_log().warn('press(%s): %s' % (a, e))
	except Throwable as t:
		rec['step'], rec['msg'] = 'failed', u'error: %s' % _s(t)
		_log().warn('press(%s): %s' % (a, t))
	finally:
		if wroteTrue:
			_write(path, False, 5)
		rec['ended'] = _now()
	secs = (rec['ended'] - rec['started']) / 1000.0
	line = u'RESET ALL IGs %s by %s (%s): %s - %s (%.1f s, gap %d ms)' % (a, rec['who'], rec['station'],
		rec['step'].upper(), rec['msg'], secs, rec['gap'])
	if rec['step'] == 'done':
		_log().info(line)
	else:
		_log().warn(line)
	_history(a, rec, secs)


def _history(a, rec, secs):
	"""One row in the HMI alarm history (forensics.alarmHistory), stamped at the press - optional, never raises."""
	try:
		value = 'DONE' if rec['step'] == 'done' and rec['ok'] else ('PARTIAL' if rec['step'] == 'done' else 'FAILED')
		detail = u'%s - reaches %s - %.1f s (hold %.1f s, gap %.1f s, tap %.1f s)' % (rec['msg'], REACH_TEXT.get(a, a),
			secs, HOLD_MS / 1000.0, rec['gap'] / 1000.0, TAP_MS / 1000.0)
		forensics.alarmHistory.logAction('reset', a, u'RESET ALL IGs - %s (HMI)' % AREA_NAME.get(a, a), value=value,
			who=rec['who'], station=rec['station'], detail=detail, source=RB_TAG.get(a, ''), ts=rec['started'])
	except Exception as e:
		_log().debug('history: %s' % e)
	except Throwable as t:
		_log().debug('history: %s' % t)


# ---------------------------------------------------------------- views
def state(area):
	"""The RESET ALL IGs button for an area (polled by the views every 500 ms). Never raises.
	Light popup: text, sub, note, bg, fg, border. Dark Diag card: cls (the glass gold class when idle - it wins over
	inline colours - else ''), cardBg, cardFg. Plus can, busy, tip."""
	import system
	a = _area(area)
	out = {'can': False, 'busy': False, 'text': 'RESET ALL IGs', 'sub': '', 'note': '', 'bg': '#DEBF7A',
		'fg': '#242E30', 'border': '#D4A863', 'cls': 'gbtn gbtn-gold', 'cardBg': '', 'cardFg': '#F6E6B8', 'tip': '',
		'area': a}
	try:
		if a not in RB_TAG:
			out.update({'text': 'MONITORING ONLY', 'bg': '#DDE1E1', 'fg': '#5F696B', 'border': '#C5CBCC', 'cls': '',
				'cardBg': 'rgba(255,255,255,0.05)', 'cardFg': '#80878A',
				'sub': u'no HMI reset for %s in the safety PLC' % a,
				'tip': u'%s has no HMI reset in the safety PLC - reset at the panel' % AREA_NAME.get(a, a)})
			return out
		reach = REACH_TEXT.get(a, a)
		out['can'] = True
		out['sub'] = u'%s - one press' % reach
		out['tip'] = (u'One press = hold the %s reset %.1f s (clears a safety fault), then a %.1f s tap (resets the '
			u'groups). Reaches %s. A gate, isolator or E-stop that is still open keeps its group off.' % (a,
			HOLD_MS / 1000.0, TAP_MS / 1000.0, reach))
		rec = _store().get('rec:' + a)
		if rec is None:
			return out
		now = _now()
		step = rec.get('step')
		left = max(0.0, (rec.get('stepEnd', now) - now) / 1000.0)
		if step in RUNNING:
			out.update({'busy': True, 'can': False, 'bg': '#EBC452', 'border': '#D4A863', 'cls': '', 'cardBg': '#EBC452',
				'cardFg': '#242E30'})
			if step in ('start', 'hold'):
				out['text'] = u'FAULT RESET %.1f s' % left
				out['note'] = u'holding the reset (clears a safety fault)'
			elif step == 'gap':
				out['text'] = u'GROUP RESET IN %.1f s' % left
				out['note'] = u'fault reset done - waiting for the PLC'
			elif step == 'tap':
				out['text'] = u'GROUP RESET'
				out['note'] = u'resetting the groups'
			else:
				out['text'] = u'CHECKING'
				out['note'] = u'reading the groups back'
			out['note'] += u' - %s' % rec.get('who', '')
			return out
		ended = rec.get('ended') or now        # 0 while the last False writes are still going: the result shows at once
		when = system.date.format(system.date.fromMillis(ended), 'HH:mm:ss')
		if step == 'done':
			msg = rec.get('msg', '')
			if now - ended < SHOW_MS:
				if rec.get('ok'):
					out.update({'text': 'RESET DONE', 'bg': '#0A733A', 'fg': '#FFFFFF', 'border': '#0A733A',
						'cls': '', 'cardBg': '#0A733A', 'cardFg': '#FFFFFF'})
				else:
					out.update({'text': 'RESET SENT', 'bg': '#DC7323', 'fg': '#FFFFFF', 'border': '#DC7323',
						'cls': '', 'cardBg': '#B4560F', 'cardFg': '#FFFFFF'})
			out['note'] = u'Last %s by %s - %s' % (when, rec.get('who', ''), msg)
		elif step == 'failed':
			if now - ended < SHOW_MS:
				out.update({'text': 'RESET FAILED', 'bg': '#C02026', 'fg': '#FFFFFF', 'border': '#8E1A1E', 'cls': '',
					'cardBg': '#C02026', 'cardFg': '#FFFFFF'})
			out['note'] = u'Failed %s - %s' % (when, rec.get('msg', ''))
		return out
	except Exception as e:
		out['note'] = u'state error: %s' % _s(e)
	except Throwable as t:
		out['note'] = u'state error: %s' % _s(t)
	return out


def recent(ig, withinMs=8000):
	"""(who, station) of an HMI reset that reaches this group and is running now or ended within withinMs, else None
	(forensics.alarmHistory names the HMI user on an ENERGIZED or FAULT CLEARED row)."""
	try:
		m = _store()
		now = _now()
		for a, igs in REACH.items():
			if ig not in igs:
				continue
			rec = m.get('rec:' + a)
			if rec is None:
				continue
			start = rec.get('started') or 0
			end = rec.get('ended') or 0
			if start and now >= start - 1000 and (not end or now <= end + withinMs):
				return (rec.get('who', ''), rec.get('station', ''))
	except Exception as e:
		_log().debug('recent: %s' % e)
	except Throwable as t:
		_log().debug('recent: %s' % t)
	return None


# ---------------------------------------------------------------- console
def check():
	"""Script Console, read only: each area's reset tag, its value, the groups it reaches and the timing."""
	for a in ('SDB', 'GRA', 'COS', 'TNB', 'CHP', 'HOG', 'DDB'):
		if a not in RB_TAG:
			print '%-4s no HMI reset in the safety PLC - monitoring only' % a
			continue
		v, good = _readOne(RB_TAG[a])
		line = '%-4s %-5s %-6s reaches %-34s hold %d ms, gap %d ms, tap %d ms | %s' % (a, 'GOOD' if good else 'BAD',
			_s(v), REACH_TEXT[a], HOLD_MS, gapMs(a), TAP_MS, RB_TAG[a])
		print line
