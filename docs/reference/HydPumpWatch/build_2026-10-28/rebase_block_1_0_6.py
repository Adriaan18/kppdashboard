# ------------------------------------------------------------------------------------------------ rebase (1.0.5, 1.0.6)
# After pressure transmitters were swapped between pumps (or a pump was changed) the long check reads the step as wear.
# rebase() finds the pumps whose level moved and gives each that stepped a reference from the day after its step.
MOVE_P = 8.0          # bar - running pressure this far from the reference has moved (the long check's WATCH size)
MOVE_T = 4.0          # degC - the same for the temperature over its tank
NOW_DAYS = 14         # "now" in rebase(): the judged windows of the last NOW_DAYS days
DAY_MIN_N = 16        # a day counts in the step search with 4 h of steady running
STEP_SHARP = 0.6      # a step: this share of the move or more between the week before the day and the week from it
RB_CHUNK_DAYS = 30    # rebase() reads the table a month at a time (1.0.6)
RB_TRIES = 3          # each read tried up to 3 times, 3 s apart (1.0.6)
REBASE_NOTE = "sensor swap or pump change - its level since the step (rebase)"
BAND_TXT = {-1: "--", 0: "NORMAL", 1: "WATCH", 2: "HOT"}


def _pday(day):
	"""Local midnight of a 'yyyy-MM-dd' day, ms."""
	return long(system.date.parse(day, "yyyy-MM-dd").getTime())


def _rb_try(fn, *args):
	"""fn(*args), tried RB_TRIES times 3 s apart - the Designer gives up on a read that sends nothing for 60 s."""
	for i in range(RB_TRIES):
		try:
			return fn(*args)
		except (Exception, Throwable):
			if i == RB_TRIES - 1:
				raise
			Thread.sleep(3000)


def _rb_load(key, t0, t1):
	"""{w: rec} of one pump for [t0, t1), RB_CHUNK_DAYS a read (1.0.6: 1.0.5 read a pump's whole history in one - on site
	28 Oct the Designer timed out on DB P2's after 60 s)."""
	out = {}
	a = long(t0)
	while a < t1:
		b = min(long(t1), a + RB_CHUNK_DAYS * DAY_MS)
		out.update(_rb_try(_load, a, b, key)[key])
		a = b
	return out


def _rb_why(e):
	"""An error in one line: a Java error's root cause (the time-out, not the query text)."""
	try:
		t = e
		while getattr(t, "getCause", None) is not None and t.getCause() is not None:
			t = t.getCause()
		return _a(t)[:200]
	except:
		return _a(e)[:200]


def _rb_days(J, i):
	"""[(day 'yyyy-MM-dd', median)] of one number of the judged windows (1 P, 3 T), the days with DAY_MIN_N or more."""
	by = {}
	for j in J:
		if j[i] is not None:
			by.setdefault(_fmt(j[0], "yyyy-MM-dd"), []).append(j[i])
	return [(d, _med(v)) for d, v in sorted(by.items()) if len(v) >= DAY_MIN_N]


def _rb_step(days, ref, cur):
	"""The day the level moved from ref to cur: (its first day at the new level, median of the week before, median of the
	week from it, sharp). The new level holds from that day on - nine days in ten, six of its first seven; sharp: the
	move across that day is STEP_SHARP of the whole or more (a swap, a change - not a slow drift). None: no such day, or
	the pump was never at the old level in the table."""
	if ref is None or cur is None or len(days) < 8:
		return None
	like = [abs(m - cur) < abs(m - ref) for d, m in days]
	n = len(days)
	best = None
	tail = 0
	for i in range(n - 1, -1, -1):
		if like[i]:
			tail += 1
			wk = like[i:i + 7]
			if tail >= 0.9 * (n - i) and len([x for x in wk if x]) >= len(wk) - 1:
				best = i
	if best is None or best == 0:
		return None
	b0 = _med([m for d, m in days[max(0, best - 7):best]])
	b1 = _med([m for d, m in days[best:best + 7]])
	gap = abs(cur - ref)
	return days[best][0], b0, b1, gap > 0 and abs(b1 - b0) >= STEP_SHARP * gap


def _rb_months(J, i, pat):
	"""One number's median by month: 'Apr 129.6 | May 130.1 | ...'."""
	by = {}
	for j in J:
		if j[i] is not None:
			by.setdefault(_fmt(j[0], "yyyy-MM"), []).append(j[i])
	return " | ".join(["%s %s" % (_fmt(_pday(m + "-01"), "MMM"), pat % _med(v)) for m, v in sorted(by.items())]) or "-"


def _rb_verdict(r):
	"""The card's verdict for a pump - band, index, value - as analyse() gives it (no held band)."""
	if not r:
		return "-"
	return "%s %d  %s" % (BAND_TXT.get(r.get("band", -1), "--"), int(round(r.get("score", -1))), r.get("v", ""))


def _rb_keys(x):
	"""(pump keys, names not known) from keys or short names - one name or a list."""
	if x is None:
		return set(), []
	if isinstance(x, basestring):
		x = [x]
	got, bad = set(), []
	for y in x:
		k = [p[0] for p in PUMPS if y in (p[0], p[5], p[8])]
		if k:
			got.add(k[0])
		else:
			bad.append(y)
	return got, bad


def _rb_pump(p, c):
	"""One pump of rebase(): prints its block; adds to c["plan"], c["drift"], c["steps"]. Raises on a database read that
	fails RB_TRIES times - rebase() says so and goes on with the next pump."""
	key, label, short = p[0], p[4], p[5]
	now, today = c["now"], c["today"]
	f = _rb_try(_first_window, key)
	if f is None:
		print "%-7s %s - never ran at pressure in the table" % (short, label)
		return
	wins = _rb_load(key, f - (SETTLE_W + 1) * W_MS, now + W_MS)
	J, x = _judged(wins, c["spans"], _prun(wins), f, now + W_MS)
	man = c["refs"].get(key)
	ra, rb, rnote = _rb_try(_ref_span, key, man)
	ref = _stats([j for j in J if ra <= j[0] < rb], ra, rb) if ra is not None else None
	ref_ok = ref is not None and ref["n"] >= REF_MIN_N
	ref_used = ref_ok and rb <= now - LONG_GAP_DAYS * DAY_MS
	b0, b1 = _base_span(now, man)
	base = _stats([j for j in J if b0 <= j[0] < b1], b0, b1)
	cur = _stats([j for j in J if j[0] >= now - NOW_DAYS * DAY_MS], now - NOW_DAYS * DAY_MS, now)
	recent = dict((w, r) for w, r in wins.items() if w >= now - KEEP_DAYS * DAY_MS - W_MS)
	_S["band"] = {}
	r0 = analyse(key, recent, base, ref if ref_used else None, c["spans"], c["live"].get(key), now)
	print "%-7s %s - %d judged windows since %s" % (short, label, len(J), _fmt(f, "d MMM"))
	print "        P by month  %s" % _rb_months(J, 1, "%.1f")
	if ra is None:
		print "        reference   none yet - its first %d windows of running at pressure" % REF_RUN_N
	else:
		print "        reference   %s to %s  n %4d  P %s  T %s  %s%s" % (_fmt(ra, "d MMM"), _fmt(rb, "d MMM"), ref["n"],
			_n(ref["P"]["med"]), _n(ref["T"]["med"], "%+.1f"), "in use" if ref_used else ("too few windows" if not ref_ok else
			"used from %s" % _fmt(rb + LONG_GAP_DAYS * DAY_MS, "d MMM")), (" - set by hand: %s" % rnote) if man is not None else "")
	print "        8 weeks     n %4d  P %s  T %s    last %d days  n %4d  P %s  T %s" % (base["n"], _n(base["P"]["med"]),
		_n(base["T"]["med"], "%+.1f"), NOW_DAYS, cur["n"], _n(cur["P"]["med"]), _n(cur["T"]["med"], "%+.1f"))
	dP = dT = sP = sT = None
	if ref_ok and cur["n"] >= BASE_MIN_N:
		dP = cur["P"]["med"] - ref["P"]["med"]
		if cur["T"]["med"] is not None and ref["T"]["med"] is not None:
			dT = cur["T"]["med"] - ref["T"]["med"]
		if abs(dP) >= MOVE_P:
			sP = _rb_step(_rb_days(J, 1), ref["P"]["med"], cur["P"]["med"])
		if dT is not None and abs(dT) >= MOVE_T:
			sT = _rb_step(_rb_days(J, 3), ref["T"]["med"], cur["T"]["med"])
	movedP = dP is not None and abs(dP) >= MOVE_P
	movedT = dT is not None and abs(dT) >= MOVE_T
	if dP is not None:
		mv = "P %+.1f bar, T %s against the reference" % (dP, ("%+.1f degC" % dT) if dT is not None else "-")
		for nm, moved, s in (("P", movedP, sP), ("T", movedT, sT)):
			if not moved:
				continue
			if s is None:
				mv += "; %s moved, no day it changed" % nm
			else:
				mv += "; %s %s on %s (week before %.1f, from it %.1f)" % (nm, "steps" if s[3] else "drifts", _fmt(_pday(s[0]),
					"EEE d MMM"), s[1], s[2])
				if s[3]:
					c["steps"].append((s[0], short, "%s %+.1f" % (nm, s[2] - s[1])))
		print "        moved       %s" % mv
	elif not ref_ok:
		print "        moved       - no reference to judge it against yet"
	else:
		print "        moved       - too little steady running in the last %d days (n %d)" % (NOW_DAYS, cur["n"])
	sharp = [s for s in (sP, sT) if s is not None and s[3]]
	if key in c["sk"]:
		print "        card        %s  (skipped)" % _rb_verdict(r0)
		return
	if sharp:
		a = _pday(max([s[0] for s in sharp])) + DAY_MS
	elif key in c["fk"]:
		a = today - REF_DAYS * DAY_MS
	elif movedP or movedT:
		c["drift"].append(short)
		print "        card        %s  - DRIFT: moved slowly, not rebased (it may be wear)" % _rb_verdict(r0)
		return
	else:
		print "        card        %s" % _rb_verdict(r0)
		return
	b = min(a + REF_DAYS * DAY_MS, today)
	nj = [j for j in J if a <= j[0] < b]
	if b <= a or len(nj) < REF_MIN_N:
		print "        card        %s  - too little running since the step to rebase (%d windows of %d) - run again in a few days" % (
			_rb_verdict(r0), len(nj), REF_MIN_N)
		return
	new = _stats(nj, a, b)
	new_used = b <= now - LONG_GAP_DAYS * DAY_MS
	nb0, nb1 = _base_span(now, (a, b, REBASE_NOTE, None))
	nbase = _stats([j for j in J if nb0 <= j[0] < nb1], nb0, nb1)
	_S["band"] = {}
	r1 = analyse(key, recent, nbase, new if new_used else None, c["spans"], c["live"].get(key), now)
	c["plan"].append((key, short, a, b))
	print "        new ref     %s to %s  n %4d  P %s  T %s  - %s; 8 weeks %s" % (_fmt(a, "d MMM"), _fmt(b, "d MMM"), new["n"],
		_n(new["P"]["med"]), _n(new["T"]["med"], "%+.1f"), "in use at once" if new_used else "long check from %s" % _fmt(
		b + LONG_GAP_DAYS * DAY_MS, "d MMM"), ("from %s" % _fmt(nb0, "d MMM")) if nb0 > now - BASE_DAYS * DAY_MS else "as before")
	print "        card        now %s  ->  rebased %s" % (_rb_verdict(r0), _rb_verdict(r1))


def rebase(dry=True, force=None, skip=None, only=None):
	"""Console, after pressure transmitters were swapped between pumps (or a pump was changed). Every pump against its
	long reference: its running pressure by month, its reference, its 8 weeks, its last NOW_DAYS days, the day its level
	moved and what its card shows - now and rebased. A pump that moved MOVE_P bar or MOVE_T degC or more, either way (a
	swapped sensor can read high or low), in a step gets a new reference from the day after the step, REF_DAYS long (to
	today at most): its level since the step as its normal. A slow drift is listed and left alone - it may be wear.
	rebase() prints only. rebase(False) writes the references (set_reference); the gateway takes them at its next
	refresh. force / skip: keys or short names ("DB P6") to rebase whatever the check says (no step found: its last
	REF_DAYS days) / never to rebase. only: just these pumps (1.0.6 - e.g. one that was not read). A pump whose table
	read fails RB_TRIES times is listed NOT READ and the others go on; nothing is written for it."""
	_init()
	now = _now()
	today = long(system.date.midnight(Date(long(now))).getTime())
	fk, fbad = _rb_keys(force)
	sk, sbad = _rb_keys(skip)
	ok, obad = _rb_keys(only)
	print "forensics.hydPump v%s  rebase  %s  %s" % (SCRIPT_VERSION, _fmt(now, "EEE d MMM HH:mm"),
		"DRY RUN - nothing written" if dry else "LIVE - writes the new references")
	print "  moved = the last %d days %.0f bar or %.0f degC or more from the reference, either way; step = most of it across one day" % (
		NOW_DAYS, MOVE_P, MOVE_T)
	if fbad or sbad or obad:
		print "  not pumps: %s - use keys (SDB_U2P2) or short names (DB P6)" % ", ".join(fbad + sbad + obad)
		if only is not None and not ok:
			return None
	c = {"now": now, "today": today, "fk": fk, "sk": sk, "plan": [], "drift": [], "steps": [], "failed": []}
	c["refs"] = _rb_try(_ref_rows)
	ds = _rb_try(system.db.runQuery, "SELECT min(win_start) FROM hydraulics.pump_window WHERE %s" % RUNNING_SQL, DB)
	first = _ms(ds.getValueAt(0, 0)) if ds.getRowCount() and ds.getValueAt(0, 0) is not None else None
	if first is None:
		print "  no running windows stored - run backfill() first"
		return None
	c["spans"], snote = _spans(first - DAY_MS, now + W_MS)
	if snote:
		print "  note: %s" % snote
	try:
		c["live"] = _live()
	except (Exception, Throwable):
		c["live"] = {}
	saved = dict(_S.get("band") or {})
	try:
		for p in PUMPS:
			if only is not None and p[0] not in ok:
				continue
			print ""
			try:
				_rb_pump(p, c)
			except (Exception, Throwable) as e:
				c["failed"].append(p[5])
				print "%-7s %s - NOT READ after %d tries (%s): nothing written for it" % (p[5], p[4], RB_TRIES, _rb_why(e))
	finally:
		_S["band"] = saved
	plan, failed = c["plan"], c["failed"]
	print ""
	print "SUMMARY"
	print "  rebase: %s" % (", ".join(["%s from %s" % (s, _fmt(a, "d MMM")) for k, s, a, b in plan]) or "none")
	print "  drift - moved slowly, left alone (may be wear; force=[...] to rebase): %s" % (", ".join(c["drift"]) or "none")
	if failed:
		print "  NOT READ: %s - run it again for them: rebase(%sonly=[%s])" % (", ".join(failed), "" if dry else "False, ",
			", ".join(['"%s"' % x for x in failed]))
	if c["steps"]:
		print "  steps by day (a swap between two pumps steps both the same day):"
		for d in sorted(set([x[0] for x in c["steps"]])):
			print "    %s  %s" % (_fmt(_pday(d), "EEE d MMM yyyy"), ", ".join(["%s %s" % (x[1], x[2]) for x in c["steps"] if x[0] == d]))
	if dry:
		print "DRY RUN - nothing written. rebase(False) writes these references (force / skip change the list)."
		return None
	if not plan:
		print "nothing to write"
		return None
	for k, s, a, b in plan:
		set_reference(k, _fmt(a, "yyyy-MM-dd"), _fmt(b, "yyyy-MM-dd"), REBASE_NOTE)
	print "written - the gateway takes them at its next refresh (within 15 min) and judges these pumps afresh"
	return None
