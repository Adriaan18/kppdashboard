# builds forensics_hydPump_v1_0_5.py from the 1.0.4 in the 28 Oct 14:22 export - exact replacements, each asserted once
import sys
src = open('hydPump_1_0_4.py', encoding='utf-8').read()
s = src


def rep(old, new, cnt=1):
    global s
    n = s.count(old)
    assert n == cnt, (n, old[:120])
    s = s.replace(old, new)


# ---- header
rep("# Version: 1.0.4  (2026-10-19)", "# Version: 1.0.5  (2026-10-28)")
rep("#          Script Console (check, backfill, replay, status, trend, set_reference). Reads the tag historian (each pump's",
    "#          Script Console (check, backfill, replay, status, trend, set_reference, rebase). Reads the tag historian (each pump's")
rep("# Design:  KPP_HydPumpWatch_Design_v1_0_0.md", "# Design:  KPP_HydPumpWatch_Design_v1_2_0.md")
rep("""#            BASELINE  per number, the judged windows of the last BASE_DAYS ending GUARD_DAYS ago: median and spread
#                      (1.4826 x MAD, at least FLOOR); BASE_MIN_N windows at least, else learning. Every BASE_EVERY_MS""",
    """#            BASELINE  per number, the judged windows of the last BASE_DAYS ending GUARD_DAYS ago: median and spread
#                      (1.4826 x MAD, at least FLOOR); BASE_MIN_N windows at least, else learning. Every BASE_EVERY_MS.
#                      From the start of a reference set by hand on, when it is inside them (a swapped sensor or a
#                      changed pump - the windows before it are not this pump's normal)""")
rep("""#            REFERENCE from the first window the pump ran at pressure, its first REF_RUN_N such windows (about two weeks
#                      of running - the sensors' early months), or the period set with set_reference() after a pump change -
#                      used once it ended LONG_GAP_DAYS ago: slow wear the rolling baseline would learn in""",
    """#            REFERENCE from the first window the pump ran at pressure, its first REF_RUN_N such windows (about two weeks
#                      of running - the sensors' early months), or the period set with set_reference() / rebase() after a
#                      pump change or a sensor swap - used once it ended LONG_GAP_DAYS ago: slow wear the rolling baseline
#                      would learn in. A reference set or cleared by hand is taken at the next refresh: the pump's cached
#                      reference and baseline go and a band it holds is let go - judged afresh""")
rep("""#          forensics.hydPump.set_reference("COS_U1P2", "2026-11-02", "2026-11-30", "new pump")  the long reference for
#                                                 a pump after it is changed; set_reference(key, None) clears it
#          The console writes the table; the gateway reads the new windows within 15 min (a learning pump's baseline is
#          worked out again every window, a judged one every 6 h).""",
    """#          forensics.hydPump.set_reference("COS_U1P2", "2026-11-02", "2026-11-30", "new pump")  the long reference for
#                                                 a pump after it is changed; set_reference(key, None) clears it
#          forensics.hydPump.rebase()           READ-ONLY - every pump against its long reference: its pressure by
#                                                 month, the day its level moved, step (a swapped sensor, a changed
#                                                 pump) or drift (wear), what its card shows now and rebased;
#                                                 rebase(False) writes a new reference for each pump that stepped
#                                                 (force=["DB P6"] / skip=[...] to change the list)
#          The console writes the table; the gateway reads the new windows within 15 min (a learning pump's baseline is
#          worked out again every window, a judged one every 6 h) and a new reference at its next refresh.""")
rep("""# History
#   1.0.4  detail(code):""", """# History
#   1.0.5  A sensor swap or a pump change, said once (28 Oct: pressure transmitters swapped between pumps - DB P6 "-18 bar
#          since Apr" and GRA P1 "-62 bar since Apr" were swaps, not wear). rebase(): every pump against its long
#          reference - its running pressure by month, its reference, its 8 weeks, its last NOW_DAYS days, the day its
#          level moved and whether it stepped (STEP_SHARP of the move or more across that day: a swap, a change) or
#          drifted (wear - listed, left alone), what its card shows now and rebased. Each pump that stepped MOVE_P bar or
#          MOVE_T degC or more, either way (a swapped sensor can read high or low), gets a reference from the day after
#          the step, REF_DAYS long (to today at most): its level since the step as its normal. rebase() prints only,
#          rebase(False) writes (set_reference). A reference set or cleared by hand is taken at the gateway's next
#          refresh - the pump's cached reference and baseline go and a band it holds is let go, so it is judged afresh
#          within 15 min (1.0.4 read the references every 24 h and held a band up to 6 h more); at the first refresh after
#          a (re)load a held band last confirmed before the pump's reference row was written goes too. The rolling
#          baseline starts at a reference set by hand when that start is inside its BASE_DAYS - a pump that stepped in the
#          last weeks is not judged against the windows before its step (it learns again from BASE_MIN_N windows after
#          it). replay() follows the same baseline rule. set_reference() stamps the row's updated time and refuses a "to"
#          not after its "from".
#   1.0.4  detail(code):""")
rep('SCRIPT_VERSION = "1.0.4"', 'SCRIPT_VERSION = "1.0.5"')

# ---- the references set by hand: the row's updated time too
rep('''def _ref_rows():
	"""{pump: (from ms, to ms or None, note)} - the long references set by hand (set_reference)."""
	ds = system.db.runQuery("SELECT pump, ref_from, ref_to, COALESCE(note, '') FROM hydraulics.pump_ref", DB)
	out = {}
	for r in range(ds.getRowCount()):
		out[_a(ds.getValueAt(r, 0))] = (_ms(ds.getValueAt(r, 1)), _ms(ds.getValueAt(r, 2)), _a(ds.getValueAt(r, 3)))
	return out''', '''def _ref_rows():
	"""{pump: (from ms, to ms or None, note, written ms or None)} - the long references set by hand (set_reference,
	rebase). 'written' is the row's updated time (1.0.5); None where the table has no such column."""
	try:
		ds = system.db.runQuery("SELECT pump, ref_from, ref_to, COALESCE(note, ''), updated FROM hydraulics.pump_ref", DB)
		upd = True
	except (Exception, Throwable):
		ds = system.db.runQuery("SELECT pump, ref_from, ref_to, COALESCE(note, '') FROM hydraulics.pump_ref", DB)
		upd = False
	out = {}
	for r in range(ds.getRowCount()):
		out[_a(ds.getValueAt(r, 0))] = (_ms(ds.getValueAt(r, 1)), _ms(ds.getValueAt(r, 2)), _a(ds.getValueAt(r, 3)),
			_ms(ds.getValueAt(r, 4)) if upd else None)
	return out


def _ref_changes(refs, now):
	"""A reference set or cleared from the console (set_reference, rebase) is taken at the next refresh (1.0.5): the
	pump's cached reference and baseline go and a band it holds is let go, so it is judged afresh. At the first refresh
	after a (re)load, a held band last confirmed before the pump's reference row was written goes the same way."""
	seen = _S.get("refs_seen")
	changed = []
	if seen is None:
		for k, v in refs.items():
			b = (_S.get("band") or {}).get(k)
			if v[3] is not None and b is not None and b[0] >= 1 and b[1] is not None and b[1] < v[3]:
				changed.append(k)
	else:
		for k in set(seen.keys()) | set(refs.keys()):
			if seen.get(k) != refs.get(k):
				changed.append(k)
	for k in sorted(changed):
		_S["ref"].pop(k, None)
		_S["base"].pop(k, None)
		b = _S["band"].get(k)
		if b is not None and b[0] >= 1:
			_S["band"][k] = (0, now)
		_log.info("%s: reference %s - judged afresh" % (k, "set" if k in refs else "cleared"))
	_S["refs_seen"] = dict(refs)
	return changed''')

# ---- the rolling baseline from a reference set by hand
rep('''def _baseline(key, now, spans_cache):
	"""The rolling baseline from the table - cached BASE_EVERY_MS, a learning one only one window (a backfill from the
	console shows within 15 min). On a database error the cached one stands."""
	hit = _S["base"].get(key)
	if hit is not None and now - hit[0] < (BASE_EVERY_MS if hit[1]["n"] >= BASE_MIN_N else W_MS):
		return hit[1]
	t1 = now - GUARD_DAYS * DAY_MS
	t0 = now - BASE_DAYS * DAY_MS
	try:
		wins = _load(t0 - (SETTLE_W + 1) * W_MS, t1, key)[key]
		if "base" not in spans_cache:
			spans_cache["base"] = _spans(t0 - DAY_MS, t1)[0]''', '''def _base_span(now, man):
	"""[t0, t1) of the rolling baseline: the last BASE_DAYS ending GUARD_DAYS before now - from the start of a reference
	set by hand on, when that start is inside them (1.0.5: after a sensor swap or a pump change the windows before it are
	not this pump's normal; it learns again from its first BASE_MIN_N windows after it)."""
	t1 = now - GUARD_DAYS * DAY_MS
	t0 = now - BASE_DAYS * DAY_MS
	if man is not None and man[0] is not None and t0 < man[0] <= now:
		t0 = min(long(man[0]), t1)
	return t0, t1


def _baseline(key, now, spans_cache, man=None):
	"""The rolling baseline from the table - cached BASE_EVERY_MS, a learning one only one window (a backfill from the
	console shows within 15 min). man: the pump's reference set by hand (_base_span). On a database error the cached one
	stands."""
	hit = _S["base"].get(key)
	if hit is not None and now - hit[0] < (BASE_EVERY_MS if hit[1]["n"] >= BASE_MIN_N else W_MS):
		return hit[1]
	t0, t1 = _base_span(now, man)
	try:
		wins = _load(t0 - (SETTLE_W + 1) * W_MS, t1, key)[key]
		if "base" not in spans_cache:
			spans_cache["base"] = _spans(now - BASE_DAYS * DAY_MS - DAY_MS, t1)[0]''')

# ---- the refresh: references read every refresh, changes taken at once, the baseline from a hand-set start
rep('''	try:
		refs = _ref_rows()
	except (Exception, Throwable) as e:
		refs = {}
		_err("reference table read", e)
	cache = {}
	res = {}
	for p in PUMPS:
		k = p[0]
		try:
			base = _baseline(k, now, cache)''', '''	try:
		refs = _ref_rows()
		_ref_changes(refs, now)
	except (Exception, Throwable) as e:
		# the last references read stand (1.0.4 fell back to none - the old April references for a refresh)
		refs = _S.get("refs_seen") or {}
		_err("reference table read", e)
	cache = {}
	res = {}
	for p in PUMPS:
		k = p[0]
		try:
			base = _baseline(k, now, cache, refs.get(k))''')

# ---- replay: the same baseline rule
rep('''			if base_at is None or e - base_at >= BASE_EVERY_MS:
				b0 = e - BASE_DAYS * DAY_MS
				b1 = e - GUARD_DAYS * DAY_MS
				base = _stats(J[bisect.bisect_left(ws, b0):bisect.bisect_left(ws, b1)], b0, b1)''', '''			if base_at is None or e - base_at >= BASE_EVERY_MS:
				b0, b1 = _base_span(e, refs.get(p[0]))
				base = _stats(J[bisect.bisect_left(ws, b0):bisect.bisect_left(ws, b1)], b0, b1)''')

# ---- set_reference: the row stamped, "to" after "from", the gateway's pickup said
rep('''	if date_from is None:
		system.db.runPrepUpdate("DELETE FROM hydraulics.pump_ref WHERE pump = ?", [key], DB)
		print "%s: reference cleared - its first %d windows of running again" % (p[4], REF_RUN_N)
	else:
		a = system.date.parse(date_from, "yyyy-MM-dd")
		b = system.date.parse(date_to, "yyyy-MM-dd") if date_to else None
		system.db.runPrepUpdate("INSERT INTO hydraulics.pump_ref (pump, ref_from, ref_to, note) VALUES (?, ?, ?, ?) ON CONFLICT (pump) "
			"DO UPDATE SET ref_from = EXCLUDED.ref_from, ref_to = EXCLUDED.ref_to, note = EXCLUDED.note, updated = now()", [key, a, b, note], DB)
		print "%s: reference %s to %s%s - used from %d days after its end" % (p[4], date_from, date_to or ("+%d days" % REF_DAYS),
			(" (%s)" % note) if note else "", LONG_GAP_DAYS)''', '''	if date_from is None:
		system.db.runPrepUpdate("DELETE FROM hydraulics.pump_ref WHERE pump = ?", [key], DB)
		print "%s: reference cleared - its first %d windows of running again; the gateway takes it at its next refresh" % (p[4],
			REF_RUN_N)
	else:
		a = system.date.parse(date_from, "yyyy-MM-dd")
		b = system.date.parse(date_to, "yyyy-MM-dd") if date_to else None
		if b is not None and b.getTime() <= a.getTime():
			print "%s: not written - the reference must end after it starts (%s to %s)" % (p[4], date_from, date_to)
			return None
		system.db.runPrepUpdate("INSERT INTO hydraulics.pump_ref (pump, ref_from, ref_to, note, updated) VALUES (?, ?, ?, ?, now()) "
			"ON CONFLICT (pump) DO UPDATE SET ref_from = EXCLUDED.ref_from, ref_to = EXCLUDED.ref_to, note = EXCLUDED.note, updated = now()",
			[key, a, b, note], DB)
		print "%s: reference %s to %s%s - used from %d days after its end; the gateway takes it at its next refresh" % (p[4],
			date_from, date_to or ("+%d days" % REF_DAYS), (" (%s)" % note) if note else "", LONG_GAP_DAYS)''')

# ---- rebase(): appended
s = s.rstrip('\n') + '\n' + open('rebase_block.py', encoding='utf-8').read()
open('/home/claude/out/forensics_hydPump_v1_0_5.py', 'w', encoding='utf-8').write(s)
print('written', len(s))
