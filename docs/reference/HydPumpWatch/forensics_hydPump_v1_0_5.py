# forensics.hydPump
# Author:  Adriaan
# Version: 1.0.5  (2026-10-28)
# Scope:   Project Library forensics/hydPump (a script in the plain-folder package forensics). Gateway - called by
#          forensics.anomalyWatch 1.15.0 (poll() on its slow pass, rows() every pass) and by the hydraulics diagnostics
#          cards (card(), view HydraulicsDiagnosticsCard 1.7.0; detail(), its DETAILS popup HydPumpWatchDetail 1.0.0) - and
#          Script Console (check, backfill, replay, status, trend, set_reference, rebase). Reads the tag historian (each pump's
#          IO-Link pressure and temperature, its motor's run state, the five tank temperatures LEAK WATCH reads, plant
#          downtime and smoko), hydraulics.pump_events (the forensics.hyddiag start / stop capture) and the Shut Plan
#          (forensics.peWatchJudge 1.5.0 shut_spans). Writes only its own tables hydraulics.pump_window,
#          hydraulics.pump_band and hydraulics.pump_ref (KPP_HydPump_schema_apply_v1_0_0.py). Read-only on the plant - no
#          PLC change, no new tag.
# Design:  KPP_HydPumpWatch_Design_v1_2_0.md
# Purpose: the hydraulic PUMP WATCH - pump leakage from the pressure and temperature sensors at each of the 18 sensored
#          pumps (17 from 1.0.0, the Big John crane's power pack from 1.0.3). The PLC trips on fixed limits (250 bar /
#          75 degC high alarms); a pump that starts leaking inside stays well within them for weeks. A worn pump loses flow
#          inside: its running pressure sags, the dips under load get deeper, and the oil it forces back across the
#          pressure drop turns to heat (about 0.06 degC per bar), so it runs hotter than the oil it draws. Each pump is
#          judged against its own normal:
#            WINDOWS   every 15 minutes the closed window's pressure (average, minimum, maximum), temperature (average,
#                      minimum, maximum), the share of it the motor ran, the reference temperature (its tank's - only SDB
#                      HydUnit2, which has no tank sensor, takes the median of its other running pump) and the plant's
#                      downtime and smoko shares go into hydraulics.pump_window - three historian reads for all pumps, 3 min
#                      after the window closes; gaps of the last KEEP_DAYS filled one per refresh, 6 h at a time
#            JUDGED    a window counts when the pump ran all of it under pressure (its run state, and its pressure over
#                      P_RUN_MIN all window) and the two windows before it (the oil is warm), the plant was not down or on
#                      smoko for half of it, not in a Shut Plan shift and not within SETTLE_MS after one, and it has a
#                      pressure. Its numbers: P running pressure (average), D dip depth (average - minimum), T temperature
#                      over the oil it works (average - reference)
#            BASELINE  per number, the judged windows of the last BASE_DAYS ending GUARD_DAYS ago: median and spread
#                      (1.4826 x MAD, at least FLOOR); BASE_MIN_N windows at least, else learning. Every BASE_EVERY_MS.
#                      From the start of a reference set by hand on, when it is inside them (a swapped sensor or a
#                      changed pump - the windows before it are not this pump's normal)
#            REFERENCE from the first window the pump ran at pressure, its first REF_RUN_N such windows (about two weeks
#                      of running - the sensors' early months), or the period set with set_reference() / rebase() after a
#                      pump change or a sensor swap - used once it ended LONG_GAP_DAYS ago: slow wear the rolling baseline
#                      would learn in. A reference set or cleared by hand is taken at the next refresh: the pump's cached
#                      reference and baseline go and a band it holds is let go - judged afresh
#            RECENT    the median of the judged windows of the last RECENT_H; RECENT_MIN_N at least
#            CHECKS    PRESSURE LOW (baseline P - recent P), DIPS DEEPER (recent D - baseline D), RUNS HOTTER (recent T -
#                      baseline T), and against the reference PRESSURE LOW and RUNS HOTTER; each scored on the smaller of
#                      its significance (z: 2 -> 0, 3.5 -> WATCH 60, 5 -> HOT 80) and its size (ABS_* bar / degC). SENSOR:
#                      flat through the newest FLAT_N judged windows where it normally moves, or out of range -> WATCH. The
#                      pump's score is its worst check, capped at HOT - the PLC limits are the alarms
#            BANDS     a raised band holds while its score stays at its keep level (KEEP_WATCH, KEEP_HOT) and drops HOLD_MS
#                      after the last pass there; through standby, measuring and a shut it holds up to HOLD_IDLE_MS. Kept
#                      in hydraulics.pump_band - a project save or a gateway restart does not drop a held band
#            NOT JUDGED plant shut, sensor bypassed (its protection bypassed in the PLC), runs with no pressure (its motor ran
#                      NOPRESS_N whole windows of production in the last 2 h and its pressure stayed under NOPRESS_P all
#                      that time - the transmitter is not connected or not reading), standby (not running), measuring
#                      (running, under RECENT_MIN_N judged windows - or it runs on and off), learning (baseline short), no
#                      data (no window for NODATA_MS)
#          Anomaly Watch shows the pumps in the Hydraulics row beside the tanks (DEBARKER SDB, GRADING GRA, COS COS and
#          T&B); the worst pump leads. rows(area) -> (row, assets); state() -> every pump's result; card(code) -> the
#          PUMP WATCH section of a hydraulics card (SDB, GRA, COS, TNB); detail(code) -> the same section read in full (the
#          card's DETAILS popup); poll() starts a background refresh when a window is due and returns at once. Never raises
#          out of poll(), rows(), state(), card() or detail().
# Console: forensics.hydPump.check()            READ-ONLY - paths, live values, history configuration and coverage,
#                                                 the running sources, a 2 h historian read, then a preview of the
#                                                 analysis on the last 3 days straight from the historian
#          forensics.hydPump.backfill(30)       writes the windows of the last 30 days (12 h per historian read) and
#                                                 prints the rows and the pumps with a pressure per day;
#                                                 backfill(30, 30) writes the 30 days before that; backfill(30, 0, 6)
#                                                 reads 6 h at a time if a read times out
#          forensics.hydPump.replay(14)         READ-ONLY - the analysis every 6 h over the stored windows: what it
#                                                 would have raised per pump - set the limits from this
#          forensics.hydPump.status()           READ-ONLY - what the Hydraulics rows and the cards show now
#          forensics.hydPump.trend()            READ-ONLY - monthly medians per pump (wear since the sensors went in)
#          forensics.hydPump.set_reference("COS_U1P2", "2026-11-02", "2026-11-30", "new pump")  the long reference for
#                                                 a pump after it is changed; set_reference(key, None) clears it
#          forensics.hydPump.rebase()           READ-ONLY - every pump against its long reference: its pressure by
#                                                 month, the day its level moved, step (a swapped sensor, a changed
#                                                 pump) or drift (wear), what its card shows now and rebased;
#                                                 rebase(False) writes a new reference for each pump that stepped
#                                                 (force=["DB P6"] / skip=[...] to change the list)
#          The console writes the table; the gateway reads the new windows within 15 min (a learning pump's baseline is
#          worked out again every window, a judged one every 6 h) and a new reference at its next refresh.
#
# History
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
#   1.0.4  detail(code): the PUMP WATCH section read in full, for the DETAILS button of HydraulicsDiagnosticsCard 1.7.0
#          (popup HydPumpWatchDetail 1.0.0) - the card's hover text held every pump's full text in one block and covered
#          the cards. One block per pump: its verdict chip; for a judged pump three gauges - pressure, dips under load,
#          temperature over the oil it draws - each with the number now, its normal and its reference; for one not judged
#          its live values; then its full text. The sheet is an SVG like the card's, as tall as its pumps need. Nothing
#          else changes - the analysis, the tables and card() are as 1.0.3 (card() still returns "tip"; 1.7.0 shows none).
#   1.0.3  The long reference starts at the first window the pump ran at pressure and takes its first REF_RUN_N such
#          windows. 1.0.2 took the first REF_DAYS of the table: the backfill reached back to 21 Jan, months before the
#          sensors (the pumps first ran at pressure 9 Apr GRA, 16 Apr the rest), so every reference held no judged window
#          and the two long checks never ran (replay 19 Oct). Expect them to speak once a reference has ended
#          LONG_GAP_DAYS ago - GRA P1 (April median 116 bar, the last 28 days 53) and DB P6 (25 Sep step) among them.
#          TNB P1 - the Big John crane's power pack, HydUnit4 Pump 1 (TnB_Area.Pumps[0], motor
#          Program:Chippers.MCC.HydUnit4Pump1) - from the tags KPP/TnB/Devices/Pumps/HydUnit4Pump1
#          (KPP_HydPump_BigJohn_Tags_v1_0_0.py); its history starts when they are made. New state "runs, no pressure":
#          a pump whose motor runs through production while its pressure reads zero (under NOPRESS_P) read "standby"
#          before (19 Oct: TnB_Area.Pumps[0] read 0.0 bar while the Big John pump ran). A pump idling unloaded at a few
#          bar is not caught by it.
#   1.0.2  Short names by area on the card and the Hydraulics row: DB P1-P6, GRA P1-P3, COS1 P1-P3, COS3 P1-P2, TNB P2-P4
#          (T&B by its physical pumps, as the PLC motors are named); the labels follow - "Debarker Pump 5 (HydUnit2
#          Pump 1)", "Grading Pump 1 (drive)", "T&B Pump 2 (star loader)". The card's name column is wider. Names only -
#          the pump keys, the tables and the analysis are as 1.0.1.
#   1.0.1  The house-tree paths as check() found them on site (18 Oct): the SDB HydUnit2 pumps are the HydUnit1 folder's
#          Pump 5 and Pump 6 (SDB_General.HydraulicPumps[5], [6]); the T&B HydUnit4 folder numbers its pumps 1-3 by
#          the PLC array (TnB_Area.Pumps[1]-[3]) - its Pump 1 is the star loader, physical Pump 2 (the same stream as the
#          old kpp/tnb/devices/pumps/hydunit4pump2), Pump 2 is physical 3, Pump 3 is physical 4. 1.0.0 read the T&B
#          physical 3 and 4 as 2 and 3 and found no data for SDB HydUnit2 and T&B 4: backfill again after 1.0.1 (it
#          rewrites the rows). The diagnostics folder for the bypass is found by the PLC reference
#          (forensics.hyddiag.PUMPS), not by the faceplate's path numbering. backfill() prints how many pumps had a
#          pressure each day - the sensors' start is where it drops.
#   1.0.0  first issue.

from java.lang import System, Throwable
from java.util import Date
import base64
import bisect
import math

SCRIPT_VERSION = "1.0.5"
DB = "KPP_production"
PROV = "[TL-KPPWS01-01]"
HP = "histprov:KPP_production:/drv:ignition-tl-kppws01:tl-kppws01-01:/tag:"

# key, Anomaly Watch area, card, unit, label, short (card), house-tree pump path, forensics.hyddiag plc_ref, row name.
# Short names (1.0.2): DB P1-P6 as the debarker station's faceplate numbers them (5 and 6 are the PLC's HydUnit2 Pump 1-2,
# in the house tree's HydUnit1 folder), GRA P1-P3, COS1 / COS3 by the station, TNB P2-P4 by the physical pump - the T&B
# folder numbers them 1-3 by the PLC array (1.0.1). TNB P1 (1.0.3) is the Big John crane's power pack, HydUnit4 Pump 1: the
# array's element 0, which the T&B station folder does not show - its own tags under KPP/TnB/Devices/Pumps.
PUMPS = [
	("SDB_U1P1", "DEBARKER", "SDB", "SDB_U1", "Debarker Pump 1", "DB P1", "KPP/StemDB/Devices/Hydraulic Stations/HydUnit1/Pumps/Pump 1", "SDB_General.HydraulicPumps[1]", "DB P1"),
	("SDB_U1P2", "DEBARKER", "SDB", "SDB_U1", "Debarker Pump 2", "DB P2", "KPP/StemDB/Devices/Hydraulic Stations/HydUnit1/Pumps/Pump 2", "SDB_General.HydraulicPumps[2]", "DB P2"),
	("SDB_U1P3", "DEBARKER", "SDB", "SDB_U1", "Debarker Pump 3", "DB P3", "KPP/StemDB/Devices/Hydraulic Stations/HydUnit1/Pumps/Pump 3", "SDB_General.HydraulicPumps[3]", "DB P3"),
	("SDB_U1P4", "DEBARKER", "SDB", "SDB_U1", "Debarker Pump 4", "DB P4", "KPP/StemDB/Devices/Hydraulic Stations/HydUnit1/Pumps/Pump 4", "SDB_General.HydraulicPumps[4]", "DB P4"),
	("SDB_U2P1", "DEBARKER", "SDB", "SDB_U2", "Debarker Pump 5 (HydUnit2 Pump 1)", "DB P5", "KPP/StemDB/Devices/Hydraulic Stations/HydUnit1/Pumps/Pump 5", "SDB_General.HydraulicPumps[5]", "DB P5"),
	("SDB_U2P2", "DEBARKER", "SDB", "SDB_U2", "Debarker Pump 6 (HydUnit2 Pump 2)", "DB P6", "KPP/StemDB/Devices/Hydraulic Stations/HydUnit1/Pumps/Pump 6", "SDB_General.HydraulicPumps[6]", "DB P6"),
	("GRA_U1P1", "GRADING", "GRA", "GRA_U1", "Grading Pump 1 (drive)", "GRA P1", "KPP/Grader/Devices/Hydraulic Stations/HydUnit1/Pumps/Pump 1", "GRA_General.HydraulicPumps[1]", "GRA P1"),
	("GRA_U1P2", "GRADING", "GRA", "GRA_U1", "Grading Pump 2 (cylinder)", "GRA P2", "KPP/Grader/Devices/Hydraulic Stations/HydUnit1/Pumps/Pump 2", "GRA_General.HydraulicPumps[2]", "GRA P2"),
	("GRA_U1P3", "GRADING", "GRA", "GRA_U1", "Grading Pump 3 (cylinder)", "GRA P3", "KPP/Grader/Devices/Hydraulic Stations/HydUnit1/Pumps/Pump 3", "GRA_General.HydraulicPumps[3]", "GRA P3"),
	("COS_U1P1", "COS", "COS", "COS_U1", "COS HydUnit1 Pump 1", "COS1 P1", "KPP/COS/Area/Devices/Hydraulic Stations/HydUnit1/Pumps/Pump 1", "COS_Area.HydUnit1_Pumps[1]", "COS1 P1"),
	("COS_U1P2", "COS", "COS", "COS_U1", "COS HydUnit1 Pump 2", "COS1 P2", "KPP/COS/Area/Devices/Hydraulic Stations/HydUnit1/Pumps/Pump 2", "COS_Area.HydUnit1_Pumps[2]", "COS1 P2"),
	("COS_U1P3", "COS", "COS", "COS_U1", "COS HydUnit1 Pump 3", "COS1 P3", "KPP/COS/Area/Devices/Hydraulic Stations/HydUnit1/Pumps/Pump 3", "COS_Area.HydUnit1_Pumps[3]", "COS1 P3"),
	("COS_U3P1", "COS", "COS", "COS_U3", "COS HydUnit3 Pump 1", "COS3 P1", "KPP/COS/Area/Devices/Hydraulic Stations/HydUnit3/Pumps/Pump 1", "COS_Area.HydUnit3_Pumps[1]", "COS3 P1"),
	("COS_U3P2", "COS", "COS", "COS_U3", "COS HydUnit3 Pump 2", "COS3 P2", "KPP/COS/Area/Devices/Hydraulic Stations/HydUnit3/Pumps/Pump 2", "COS_Area.HydUnit3_Pumps[2]", "COS3 P2"),
	("TNB_U4P1", "COS", "TNB", "TNB_U4", "T&B Pump 1 (Big John crane)", "TNB P1", "KPP/TnB/Devices/Pumps/HydUnit4Pump1", "TnB_Area.Pumps[0]", "TNB P1"),
	("TNB_U4P2", "COS", "TNB", "TNB_U4", "T&B Pump 2 (star loader)", "TNB P2", "KPP/TnB/Devices/Hydraulic Stations/HydUnit4/Pumps/Pump 1", "TnB_Area.Pumps[1]", "TNB P2"),
	("TNB_U4P3", "COS", "TNB", "TNB_U4", "T&B Pump 3", "TNB P3", "KPP/TnB/Devices/Hydraulic Stations/HydUnit4/Pumps/Pump 2", "TnB_Area.Pumps[2]", "TNB P3"),
	("TNB_U4P4", "COS", "TNB", "TNB_U4", "T&B Pump 4", "TNB P4", "KPP/TnB/Devices/Hydraulic Stations/HydUnit4/Pumps/Pump 3", "TnB_Area.Pumps[3]", "TNB P4"),
]
# the tank temperatures LEAK WATCH reads (forensics.hydLeak TANKS - the Hydraulic Stations chart's history folders);
# SDB HydUnit2 has no tank sensor - its pumps are judged against each other
TANK_T = [("COS_U1", "timberlands/plant/COS1/hydraulics/hydraulicunitno1"), ("COS_U3", "timberlands/plant/COS1/hydraulics/hydraulicunitno2"),
	("TNB_U4", "timberlands/plant/COS2/hydraulics/hydraulicunitno1"), ("GRA_U1", "timberlands/plant/Grading/hydraulics/hydraulicunitno1"),
	("SDB_U1", "timberlands/plant/debarking/hydraulics/hydraulicunitno1")]
DT_REL = "kpp/general/data/downtimeactive"
SM_REL = "kpp/general/derived/smokoactive"

W_MS = 900000
W_MIN = 15
DAY_MS = 86400000
LAG_MS = 180000
KEEP_DAYS = 3
CHUNK_MS = 6 * 3600000
BF_CHUNK_H = 12
HIST_TIMEOUT_MS = 45000
BUSY_MAX_MS = 1800000
NODATA_MS = 2 * 3600000
DEAD_RETRY_MS = 6 * 3600000
EV_LOOKBACK_MS = 14 * DAY_MS
# judged windows
RUN_MIN = 0.95
SETTLE_W = 2
SETTLE_MS = 30 * 60000
DT_MAX = 0.5
SM_MAX = 0.5
P_RUN_FRAC = 0.4
P_RUN_MIN = 10.0
P_OK = (-1.0, 400.0)
T_OK = (-30.0, 130.0)
# baseline, reference, recent
BASE_DAYS = 56
GUARD_DAYS = 2
BASE_MIN_N = 96
BASE_EVERY_MS = 6 * 3600000
REF_DAYS = 28
REF_RUN_N = 1344
REF_MIN_N = 96
LONG_GAP_DAYS = 42
REF_EVERY_MS = 24 * 3600000
REF_RETRY_MS = 3600000
RECENT_H = 12
RECENT_MIN_N = 16
FLOOR = {"P": 1.0, "D": 1.5, "T": 0.5}
MAD_K = 1.4826
# checks: z ref / watch / hot, and the sizes ref / watch / hot (bar, bar, degC)
Z_REF = 2.0
Z_WATCH = 3.5
Z_HOT = 5.0
ABS_P = (2.0, 5.0, 10.0)
ABS_D = (3.0, 8.0, 15.0)
ABS_T = (1.0, 3.0, 6.0)
ABS_P_LONG = (3.0, 8.0, 15.0)
ABS_T_LONG = (1.5, 4.0, 8.0)
FLAT_P = 0.05
FLAT_T = 0.05
FLAT_P_BASE = 1.0
FLAT_T_BASE = 0.3
FLAT_N = 20
# bands
WATCH = 60
HOT = 80
KEEP_WATCH = 30.0
KEEP_HOT = 70.0
HOLD_MS = 6 * 3600000
NOPRESS_N = 4
NOPRESS_P = 1.0
HOLD_IDLE_MS = 72 * 3600000
AREAS = ["DEBARKER", "GRADING", "COS"]
GROUPS_AVG = ["p", "t", "r", "k", "x"]
GROUPS_MM = ["p", "t"]
FORM0 = {"p": "tag", "t": "tag", "r": "tag", "k": "hist", "x": "hist"}
ST_WORD = {"learning": "learning", "standby": "standby", "measuring": "measuring", "shut": "plant shut", "nodata": "no data",
	"nopress": "runs, no pressure",
	"bypass": "sensor bypassed", "error": "error", "stale": "stale"}

_log = system.util.getLogger("HydPump")
_S = {}


# ------------------------------------------------------------------------------------------------ small helpers
def _now():
	return long(System.currentTimeMillis())


def _fmt(ms, pat):
	return system.date.format(Date(long(ms)), pat)


def _f(v):
	"""float or None (None, NaN, text that is not a number)."""
	try:
		if v is None:
			return None
		x = float(v)
		if x != x:
			return None
		return x
	except:
		return None


def _ms(v):
	if v is None:
		return None
	if hasattr(v, "getTime"):
		return long(v.getTime())
	return long(float(v) * 1000)


def _a(s):
	"""Plain ASCII text of anything - a Java message or a note with a dash or a macron must not stop a refresh."""
	try:
		if s is None:
			return ""
		if isinstance(s, unicode):
			return s.encode("ascii", "replace")
		return str(s)
	except:
		try:
			return unicode(s).encode("ascii", "replace")
		except:
			return "?"


def _med(xs):
	s = sorted(xs)
	n = len(s)
	if n == 0:
		return None
	if n % 2:
		return s[n // 2]
	return 0.5 * (s[n // 2 - 1] + s[n // 2])


def _pct(xs, p):
	"""The p-th percentile (0-100), linear between ranks; None for no values."""
	s = sorted(xs)
	n = len(s)
	if n == 0:
		return None
	if n == 1:
		return s[0]
	r = (n - 1) * p / 100.0
	i = int(math.floor(r))
	if i >= n - 1:
		return s[-1]
	return s[i] + (s[i + 1] - s[i]) * (r - i)


def _h(n):
	"""Windows as whole hours."""
	return int(n * W_MS / 3600000)


def _pump(key):
	for p in PUMPS:
		if p[0] == key:
			return p
	return None


def _err(where, e):
	msg = "%s %s: %s" % (_fmt(_now(), "HH:mm:ss"), where, _a(e)[:240])
	last = _S.setdefault("err_t", {})
	if _now() - last.get(where, 0) > 60000:
		_log.warn(msg)
		last[where] = _now()
	_S["last_error"] = msg


def _init():
	if _S.get("init"):
		return
	_S["win"] = dict((p[0], {}) for p in PUMPS)
	_S["loaded"] = False
	_S["loaded_at"] = 0
	_S["res"] = {}
	_S["band"] = {}
	_S["busy"] = False
	_S["busy_since"] = 0
	_S["calc_at"] = 0
	_S["calc_w"] = None
	_S["last_error"] = ""
	_S["form"] = dict(FORM0)
	_S["dead"] = {}
	_S["band_loaded"] = False
	_S["band_saved"] = {}
	_S["base"] = {}
	_S["ref"] = {}
	_S["tried"] = set()
	_S["init"] = True


def scale(v, ref, amber, red):
	"""The Anomaly Watch colour mapping: ref -> 0, amber -> WATCH 60, red -> HOT 80, one amber-to-red step past red ->
	100. Linear in between."""
	if v is None:
		return None
	if v <= ref:
		return 0.0
	if v <= amber:
		return WATCH * (v - ref) / (amber - ref) if amber > ref else float(WATCH)
	step = red - amber
	if v <= red:
		return WATCH + (HOT - WATCH) * (v - amber) / step if step > 0 else float(HOT)
	if step <= 0:
		return 100.0
	return min(100.0, HOT + (100.0 - HOT) * (v - red) / step)


def _band(score):
	if score is None or score < 0:
		return -1
	if score >= HOT:
		return 2
	if score >= WATCH:
		return 1
	return 0


# ------------------------------------------------------------------------------------------------ the historian
def _gpaths(g, form):
	pre = HP if form == "hist" else PROV
	if g == "p":
		return [pre + p[6] + "/Status/Pressure" for p in PUMPS]
	if g == "t":
		return [pre + p[6] + "/Status/Temperature" for p in PUMPS]
	if g == "r":
		return [pre + p[6] + "/Motor/Status/Running" for p in PUMPS]
	if g == "k":
		return [pre + f + "/Temperature" for u, f in TANK_T]
	return [pre + DT_REL, pre + SM_REL]


def _qth(paths, t0, t1, mode):
	"""One historian read: 15-minute aggregates ('Average' time-weighted, 'Minimum', 'Maximum') over [t0, t1)."""
	kw = {"paths": paths, "startDate": Date(long(t0)), "endDate": Date(long(t1)), "intervalMinutes": W_MIN,
		"aggregationMode": mode, "returnFormat": "Wide"}
	try:
		return system.tag.queryTagHistory(ignoreBadQuality=True, timeout=HIST_TIMEOUT_MS, **kw)
	except TypeError:
		return system.tag.queryTagHistory(**kw)


def _parse(ds, t0, t1, ncol):
	"""{window ms: [value per path]} from a Wide history dataset. Rows stamped at the end of their interval (first row at
	t0 + 15 min) are moved back one window."""
	out = {}
	n = ds.getRowCount()
	if n == 0:
		return out
	first = _ms(ds.getValueAt(0, 0))
	shift = W_MS if (first is not None and abs(first - (t0 + W_MS)) < 2000) else 0
	for r in range(n):
		ts = _ms(ds.getValueAt(r, 0))
		if ts is None:
			continue
		w = ts - shift
		w -= w % W_MS
		if w < t0 or w >= t1:
			continue
		out[w] = [_f(ds.getValueAt(r, 1 + c)) for c in range(ncol)]
	return out


def _has(rows):
	for v in rows.values():
		for x in v:
			if x is not None:
				return True
	return False


def _query(mode, groups, t0, t1):
	"""{group: {w: [values]}} - one read for the groups in their known path form; a group that returns nothing is tried
	once in the other form. Only the motor run state, when it is in the history in neither form while the others answer,
	is left out for DEAD_RETRY_MS (the start / stop events stand in) - a hole in the tank or pump history never is."""
	forms = _S["form"]
	now = _now()
	dead = _S["dead"]
	use = [g for g in groups if now - dead.get((g, mode), 0) > DEAD_RETRY_MS]
	out = dict((g, {}) for g in groups)
	if not use:
		return out
	paths = []
	idx = {}
	for g in use:
		ps = _gpaths(g, forms[g])
		idx[g] = (len(paths), len(ps))
		paths += ps
	rows = _parse(_qth(paths, t0, t1, mode), t0, t1, len(paths))
	for g in use:
		a, n = idx[g]
		out[g] = dict((w, v[a:a + n]) for w, v in rows.items())
	answered = [g for g in use if _has(out[g])]
	for g in use:
		if g in answered:
			continue
		other = "hist" if forms[g] == "tag" else "tag"
		try:
			ps = _gpaths(g, other)
			got = _parse(_qth(ps, t0, t1, mode), t0, t1, len(ps))
		except (Exception, Throwable) as e:
			_err("historian %s %s" % (g, mode), e)
			got = {}
		if _has(got):
			forms[g] = other
			out[g] = got
		elif answered and g == "r":
			# the historian answered for the other groups and has no motor run state in either form
			dead[(g, mode)] = now
	return out


def _events(t0, t1, keys):
	"""{pump key: [(ms, 1 start / 0 stop)]} from hydraulics.pump_events (forensics.hyddiag, every 60 s) - from
	EV_LOOKBACK_MS before t0, so the state at t0 is known."""
	refs = dict((p[7], p[0]) for p in PUMPS if p[0] in keys)
	ds = system.db.runQuery("SELECT plc_ref, event_type, event_time FROM hydraulics.pump_events WHERE event_type IN ('start', 'stop') "
		"AND event_time >= to_timestamp(%d / 1000.0) AND event_time < to_timestamp(%d / 1000.0) ORDER BY event_time"
		% (long(t0) - EV_LOOKBACK_MS, long(t1)), DB)
	out = {}
	for r in range(ds.getRowCount()):
		k = refs.get(_a(ds.getValueAt(r, 0)))
		t = _ms(ds.getValueAt(r, 2))
		if k is None or t is None:
			continue
		out.setdefault(k, []).append((t, 1 if _a(ds.getValueAt(r, 1)) == "start" else 0))
	return out


def _ev_share(ev, w):
	"""The share of [w, w + W_MS) the pump ran by its start / stop events; None when no event says."""
	if not ev:
		return None
	e = w + W_MS
	st = None
	for t, s in ev:
		if t <= w:
			st = s
	if st is None:
		# the first event is after w: the state before it was the other one
		st = 1 - ev[0][1]
	on = 0
	cur = w
	for t, s in ev:
		if t <= w:
			continue
		if t >= e:
			break
		if st:
			on += t - cur
		cur = t
		st = s
	if st:
		on += e - cur
	return on / float(W_MS)


def _hist(t0, t1):
	"""Windows starting in [t0, t1) for every pump from the historian: {(pump, w): rec} with
	rec = [p_avg, p_min, p_max, t_avg, t_min, t_max, run, run_src, ref_t, ref_src, dt, sm]."""
	t0 = long(t0) - long(t0) % W_MS
	t1 = long(t1)
	avg = _query("Average", GROUPS_AVG, t0, t1)
	mn = _query("Minimum", GROUPS_MM, t0, t1)
	mx = _query("Maximum", GROUPS_MM, t0, t1)
	ws = set()
	for g in ("p", "t"):
		ws.update(avg[g].keys())
		ws.update(mn[g].keys())
		ws.update(mx[g].keys())
	ws = sorted(ws)
	n = len(PUMPS)
	none = [None] * n
	recs = {}
	no_run = set()
	for w in ws:
		x = avg["x"].get(w) or [None, None]
		for i in range(n):
			p = PUMPS[i]
			run = (avg["r"].get(w) or none)[i]
			if run is not None:
				run = max(0.0, min(1.0, run))
			else:
				no_run.add(p[0])
			recs[(p[0], w)] = [(avg["p"].get(w) or none)[i], (mn["p"].get(w) or none)[i], (mx["p"].get(w) or none)[i],
				(avg["t"].get(w) or none)[i], (mn["t"].get(w) or none)[i], (mx["t"].get(w) or none)[i],
				run, "tag" if run is not None else None, None, None, x[0], x[1]]
	if no_run:
		try:
			ev = _events(t0, t1, no_run)
			for (k, w), rec in recs.items():
				if rec[6] is None and k in ev:
					s = _ev_share(ev[k], w)
					if s is not None:
						rec[6] = s
						rec[7] = "events"
		except (Exception, Throwable) as e:
			_err("pump events", e)
	tank = {}
	for w in ws:
		k = avg["k"].get(w) or [None] * len(TANK_T)
		for j in range(len(TANK_T)):
			tank[(TANK_T[j][0], w)] = k[j]
	tank_units = set([u for u, f in TANK_T])
	for w in ws:
		for p in PUMPS:
			rec = recs[(p[0], w)]
			tk = tank.get((p[3], w))
			if tk is not None:
				rec[8] = tk
				rec[9] = "tank"
				continue
			if p[3] in tank_units:
				# a unit with a tank sensor is only ever judged against its tank (another zero would mix into its normal):
				# no tank temperature in this window - no temperature over the oil
				continue
			# the unit with no tank sensor: the median of its other pumps that ran all the window (by their run share,
			# or with none known, their pressure never under P_RUN_MIN in it)
			peers = []
			for q in PUMPS:
				if q[3] != p[3] or q[0] == p[0]:
					continue
				o = recs[(q[0], w)]
				ran = (o[6] >= RUN_MIN) if o[6] is not None else (o[1] is not None and o[1] >= P_RUN_MIN)
				if o[3] is not None and ran:
					peers.append(o[3])
			if peers:
				rec[8] = _med(peers)
				rec[9] = "peer"
	return recs


# ------------------------------------------------------------------------------------------------ the tables
WCOLS = "p_avg, p_min, p_max, t_avg, t_min, t_max, run, run_src, ref_t, ref_src, dt, sm"


def _upsert(rows, src):
	"""rows = [(pump, w, rec)] - one statement per 100 rows."""
	for i in range(0, len(rows), 100):
		part = rows[i:i + 100]
		args = []
		for k, w, rec in part:
			args.extend([k, long(w)] + list(rec) + [src])
		system.db.runPrepUpdate("INSERT INTO hydraulics.pump_window (pump, win_start, " + WCOLS + ", src) VALUES "
			+ ", ".join(["(?, to_timestamp(? / 1000.0), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"] * len(part))
			+ " ON CONFLICT (pump, win_start) DO UPDATE SET p_avg = EXCLUDED.p_avg, p_min = EXCLUDED.p_min, p_max = EXCLUDED.p_max, "
			"t_avg = EXCLUDED.t_avg, t_min = EXCLUDED.t_min, t_max = EXCLUDED.t_max, run = EXCLUDED.run, run_src = EXCLUDED.run_src, "
			"ref_t = EXCLUDED.ref_t, ref_src = EXCLUDED.ref_src, dt = EXCLUDED.dt, sm = EXCLUDED.sm, src = EXCLUDED.src, updated = now()",
			args, DB)


def _rec(ds, r, c0):
	out = []
	for j in range(12):
		v = ds.getValueAt(r, c0 + j)
		if j in (7, 9):
			out.append(str(v) if v is not None else None)
		else:
			out.append(_f(v))
	return out


def _load(t0, t1=None, key=None):
	"""{pump: {w: rec}} from hydraulics.pump_window for windows starting in [t0, t1), one pump or all."""
	sql = "SELECT pump, win_start, " + WCOLS + " FROM hydraulics.pump_window WHERE win_start >= to_timestamp(%d / 1000.0)" % long(t0)
	if t1 is not None:
		sql += " AND win_start < to_timestamp(%d / 1000.0)" % long(t1)
	if key is not None:
		sql += " AND pump = '%s'" % str(key).replace("'", "")
	ds = system.db.runQuery(sql + " ORDER BY win_start", DB)
	out = dict((p[0], {}) for p in PUMPS) if key is None else {key: {}}
	for r in range(ds.getRowCount()):
		k = _a(ds.getValueAt(r, 0))
		if k in out:
			out[k][_ms(ds.getValueAt(r, 1))] = _rec(ds, r, 2)
	return out


def _store(found, src, keep=True):
	"""Writes the windows; keep=False (the console backfill) does not hold them in memory as well."""
	rows = []
	for (k, w), rec in sorted(found.items()):
		rows.append((k, w, rec))
		if keep:
			_S["win"].setdefault(k, {})[w] = list(rec)
	if rows:
		_upsert(rows, src)
	return len(rows)


def _closed(now):
	"""Start of the newest window the historian should hold by now."""
	t = long(now) - LAG_MS - W_MS
	return t - t % W_MS


def _band_read():
	ds = system.db.runQuery("SELECT pump, band, since FROM hydraulics.pump_band", DB)
	out = {}
	for r in range(ds.getRowCount()):
		out[_a(ds.getValueAt(r, 0))] = (int(ds.getValueAt(r, 1)), _ms(ds.getValueAt(r, 2)))
	return out


def _band_write(key, band, since):
	system.db.runPrepUpdate("INSERT INTO hydraulics.pump_band (pump, band, since) VALUES (?, ?, to_timestamp(? / 1000.0)) "
		"ON CONFLICT (pump) DO UPDATE SET band = EXCLUDED.band, since = EXCLUDED.since, updated = now()", [key, int(band), long(since)], DB)


def _ref_rows():
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
	return changed


RUNNING_SQL = "p_min >= %s AND (run IS NULL OR run >= %s)" % (P_RUN_MIN, RUN_MIN)


def _first_window(key):
	"""The first window the pump ran at pressure (its run state, and its pressure over P_RUN_MIN all window) - not the
	first row of the table: the backfill reaches back before the sensors (1.0.3)."""
	ds = system.db.runQuery("SELECT min(win_start) FROM hydraulics.pump_window WHERE pump = '%s' AND %s"
		% (str(key).replace("'", ""), RUNNING_SQL), DB)
	if ds.getRowCount() == 0 or ds.getValueAt(0, 0) is None:
		return None
	return _ms(ds.getValueAt(0, 0))


def _ref_end(key, a):
	"""Just after the REF_RUN_N-th window from a that the pump ran at pressure; None while it has run fewer."""
	ds = system.db.runQuery("SELECT win_start FROM hydraulics.pump_window WHERE pump = '%s' AND win_start >= to_timestamp(%d / 1000.0) "
		"AND %s ORDER BY win_start OFFSET %d LIMIT 1" % (str(key).replace("'", ""), long(a), RUNNING_SQL, REF_RUN_N - 1), DB)
	if ds.getRowCount() == 0 or ds.getValueAt(0, 0) is None:
		return None
	return _ms(ds.getValueAt(0, 0)) + W_MS


def _ref_span(key, man):
	"""(from ms, to ms, note) of a pump's long reference: set by hand, else from the first window it ran at pressure its
	first REF_RUN_N such windows - (None, None, "") until it has run that many."""
	if man is not None and man[0] is not None:
		return man[0], (man[1] or (man[0] + REF_DAYS * DAY_MS)), man[2]
	a = _first_window(key)
	if a is None:
		return None, None, ""
	b = _ref_end(key, a)
	if b is None:
		return None, None, ""
	return a, b, ""


def _spans(t0, t1):
	"""(Shut Plan spans [(from ms, to ms, text)], note or None) from forensics.peWatchJudge 1.5.0."""
	fn = getattr(forensics.peWatchJudge, "shut_spans", None)
	if fn is None:
		return [], "PE Watch judge older than 1.5.0 - shuts not known"
	try:
		return [(long(s["from_ms"]), long(s["to_ms"]), _a(s["text"])) for s in fn(t0, t1)], None
	except (Exception, Throwable) as e:
		return [], "Shut Plan unreadable: %s" % _a(e)[:120]


def _diag(p):
	"""The pump's forensics.hyddiag diagnostics folder ('' when not found) - its BypassActive is what the pump popup shows.
	Found by the PLC reference in forensics.hyddiag.PUMPS (1.0.1: the house-tree folders number the T&B pumps by the PLC
	array, the faceplate by the physical pump)."""
	try:
		hd = forensics.hyddiag
		for d in hd.PUMPS:
			if d.get("plc_ref") == p[7]:
				return "%s/%s/%s" % (_a(hd.BASE), _a(d["area"]), _a(d["key"]))
	except (Exception, Throwable):
		pass
	return ""


def _live():
	"""{pump: {"p", "t", "run", "bypass", "pq", "tq"}} - the house-tree values now. bypass: the sensor's protection is
	bypassed (the diagnostics BypassActive, else Setpoints/SensorBypass), as the pump popup reads it."""
	if "diag" not in _S:
		_S["diag"] = dict((p[0], _diag(p)) for p in PUMPS)
	paths = []
	for p in PUMPS:
		dp = _S["diag"].get(p[0]) or ""
		paths += [PROV + p[6] + "/Status/Pressure", PROV + p[6] + "/Status/Temperature", PROV + p[6] + "/Motor/Status/Running",
			PROV + p[6] + "/Setpoints/SensorBypass", (dp + "/BypassActive") if dp else PROV + p[6] + "/Setpoints/SensorBypass"]
	qvs = system.tag.readBlocking(paths)
	out = {}
	for i in range(len(PUMPS)):
		q = [qvs[5 * i + j] for j in range(5)]
		g = [x.quality.isGood() and x.value is not None for x in q]
		byp = bool(q[4].value) if g[4] else (bool(q[3].value) if g[3] else None)
		out[PUMPS[i][0]] = {"p": _f(q[0].value) if g[0] else None, "t": _f(q[1].value) if g[1] else None,
			"run": bool(q[2].value) if g[2] else None, "bypass": byp, "pq": _a(q[0].quality), "tq": _a(q[1].quality)}
	return out


# ------------------------------------------------------------------------------------------------ judged windows
def _prun(wins):
	"""The running pressure threshold for a pump with no run state: P_RUN_FRAC of its usual running pressure."""
	ps = [r[0] for r in wins.values() if r[0] is not None and r[0] > P_RUN_MIN]
	if len(ps) < 8:
		return None
	return max(P_RUN_MIN, P_RUN_FRAC * _pct(ps, 90))


def _runs(rec, prun):
	"""True / False / None - the pump ran all of the window under pressure. With a run state (the motor, or the start /
	stop events) the pressure must also have stayed over P_RUN_MIN all window: a run state left stale (the event capture
	stopped) or a pump running unloaded is not judged. With none, its pressure must have stayed over prun."""
	if rec is None:
		return None
	pm = rec[1] if rec[1] is not None else rec[0]
	if rec[6] is not None:
		return rec[6] >= RUN_MIN and pm is not None and pm >= P_RUN_MIN
	if prun is None or pm is None:
		return None
	return pm >= prun


def _ran_some(rec, prun):
	"""The pump ran at some time in the window - standby or measuring, and 'not running since'. By its run state when
	there is one, with its pressure up at some time in the window (a pump that runs on and off reads measuring, not
	standby; a stale run state does not count); with none, its pressure reached prun."""
	if rec is None:
		return False
	pm = rec[2] if rec[2] is not None else rec[0]
	if rec[6] is not None:
		return rec[6] > 0.05 and pm is not None and pm >= P_RUN_MIN
	return prun is not None and pm is not None and pm >= prun


def _judged(wins, spans, prun, t0, t1):
	"""Judged windows starting in [t0, t1): [(w, P, D, T, prange, trange)] oldest first, and the count left out per
	reason. wins {w: rec} may start earlier (the settle check looks back)."""
	out = []
	skip = {"stopped": 0, "start": 0, "down": 0, "shut": 0, "nodata": 0}
	settle_to = None
	for w in sorted(wins.keys()):
		if w >= t1:
			break
		r = wins[w]
		e = w + W_MS
		shut = False
		for a, b, x in spans:
			if a < e and b > w:
				shut = True
				break
		down = (r[10] is not None and r[10] >= DT_MAX) or (r[11] is not None and r[11] >= SM_MAX)
		if shut or down:
			settle_to = e + SETTLE_MS
		if w < t0:
			continue
		if r[0] is None:
			skip["nodata"] += 1
			continue
		if shut:
			skip["shut"] += 1
			continue
		if down:
			skip["down"] += 1
			continue
		if not _runs(r, prun):
			skip["stopped"] += 1
			continue
		if settle_to is not None and w < settle_to:
			skip["start"] += 1
			continue
		ok = True
		for i in range(1, SETTLE_W + 1):
			if not _runs(wins.get(w - i * W_MS), prun):
				ok = False
				break
		if not ok:
			skip["start"] += 1
			continue
		dd = (r[0] - r[1]) if r[1] is not None else None
		tt = (r[3] - r[8]) if (r[3] is not None and r[8] is not None) else None
		pr = (r[2] - r[1]) if (r[2] is not None and r[1] is not None) else None
		tr = (r[5] - r[4]) if (r[5] is not None and r[4] is not None) else None
		out.append((w, r[0], dd, tt, pr, tr))
	return out, skip


def _stat(vals, floor):
	"""{"med", "spread", "p05", "p95", "n"} - spread = 1.4826 x MAD, at least floor."""
	vs = [v for v in vals if v is not None]
	if not vs:
		return {"med": None, "spread": None, "p05": None, "p95": None, "n": 0}
	m = _med(vs)
	mad = _med([abs(v - m) for v in vs])
	return {"med": m, "spread": max(floor, MAD_K * mad), "p05": _pct(vs, 5), "p95": _pct(vs, 95), "n": len(vs)}


def _stats(J, t0, t1):
	"""Baseline numbers from judged windows: {"n", "P", "D", "T", "prange", "trange", "from", "to"}."""
	return {"n": len(J), "P": _stat([j[1] for j in J], FLOOR["P"]), "D": _stat([j[2] for j in J], FLOOR["D"]),
		"T": _stat([j[3] for j in J], FLOOR["T"]), "prange": _med([j[4] for j in J if j[4] is not None]),
		"trange": _med([j[5] for j in J if j[5] is not None]), "from": t0, "to": t1}


# ------------------------------------------------------------------------------------------------ the analysis
def _chk(x, spread, absr):
	"""(score, z) - the smaller of the significance and the size of a change x (positive = the bad direction)."""
	if x is None or spread is None or spread <= 0:
		return None, None
	z = x / spread
	return min(scale(z, Z_REF, Z_WATCH, Z_HOT), scale(x, absr[0], absr[1], absr[2])), z


def _refname(src):
	return {"tank": "its tank", "peer": "the unit's other pump"}.get(src, "its reference")


def analyse(key, wins, base, ref, spans, live, now, note=None):
	"""One pump at 'now': the result dict Anomaly Watch and the card show. wins {w: rec} (the last KEEP_DAYS - the flat
	check looks back that far), base / ref from _stats (or None), spans [(from, to, text)], live {"p", "t", "run",
	"bypass"} or None."""
	p = _pump(key)
	live = live or {}
	res = {"key": key, "label": p[4], "short": p[5], "row": p[8], "area": p[1], "card": p[2], "ts": now, "st": "ok", "score": -1,
		"band": -1, "v": "", "d": "", "note": note or "", "live": live, "n_recent": 0, "n_base": (base or {}).get("n", 0), "chk": {}}
	for a, b, txt in spans:
		if a <= now < b:
			res["st"] = "shut"
			res["shut_to"] = b
			res["v"] = "plant shut"
			res["d"] = "%s - %s, not judged" % (p[4], txt)
			return _hold_idle(res, now)
	if live.get("bypass"):
		res["st"] = "bypass"
		res["v"] = "sensor bypassed"
		res["d"] = "%s - its sensor protection is bypassed in the PLC, not judged" % p[4]
		return _hold_idle(res, now)
	have = [w for w, r in wins.items() if r[0] is not None]
	newest = max(have) if have else None
	if newest is None or now - (newest + W_MS) > NODATA_MS:
		res["st"] = "nodata"
		res["v"] = "no data"
		res["d"] = "%s - no pressure data%s" % (p[4], (" since %s" % _fmt(newest + W_MS, "EEE HH:mm")) if newest is not None else " in the historian")
		return _hold_idle(res, now)
	prun = _prun(wins)
	t0 = now - RECENT_H * 3600000
	J, skip = _judged(wins, spans, prun, t0, now)
	res["n_recent"] = len(J)
	res["skip"] = skip
	ran = [w for w, r in wins.items() if _ran_some(r, prun)]
	res["last_run"] = (max(ran) + W_MS) if ran else None
	# its motor runs through production but its pressure reads zero: the transmitter is not connected or not reading -
	# not standby (1.0.3). A pump idling unloaded reads a few bar and is not caught here.
	last2 = [r for w, r in wins.items() if now - 2 * 3600000 - W_MS <= w < now]
	prod = [r for r in last2 if r[6] is not None and r[6] >= RUN_MIN and not ((r[10] is not None and r[10] >= DT_MAX) or
		(r[11] is not None and r[11] >= SM_MAX))]
	pz = [(r[2] if r[2] is not None else r[0]) for r in last2 if r[2] is not None or r[0] is not None]
	if len(prod) >= NOPRESS_N and pz and max(pz) < NOPRESS_P:
		res["st"] = "nopress"
		res["v"] = "runs, no pressure"
		res["d"] = "%s - its motor runs but its pressure reads %.1f bar (the most in the last 2 h): the pressure transmitter is " \
			"not connected or not reading, not judged" % (p[4], max(pz))
		return _hold_idle(res, now)
	if base is None or base.get("n", 0) < BASE_MIN_N:
		res["st"] = "learning"
		nb = (base or {}).get("n", 0)
		res["v"] = "learning %d h of %d" % (_h(nb), _h(BASE_MIN_N))
		res["d"] = "%s - learning its normal: %d h of steady running in the last %d days, judged from %d h" % (p[4], _h(nb),
			BASE_DAYS, _h(BASE_MIN_N))
		return _hold_idle(res, now)
	if len(J) < RECENT_MIN_N:
		recent_run = [w for w in ran if w >= now - 2 * 3600000]
		if not recent_run:
			res["st"] = "standby"
			res["v"] = "standby"
			res["d"] = "%s - not running%s, not judged" % (p[4], (" since %s" % _fmt(res["last_run"], "EEE d MMM HH:mm")) if res["last_run"] else "")
		else:
			res["st"] = "measuring"
			res["v"] = "measuring %d h of %d" % (_h(len(J)), _h(RECENT_MIN_N))
			res["d"] = "%s - measuring: %d h of steady running in the last %d h, judged from %d h (left out: %s)" % (p[4],
				_h(len(J)), RECENT_H, _h(RECENT_MIN_N), ", ".join(["%s %d" % (k, v) for k, v in sorted(skip.items()) if v]) or "none")
			if skip.get("stopped", 0) >= 4:
				res["d"] += " - it runs on and off: only whole quarter hours under pressure are judged"
		return _hold_idle(res, now)
	rP = _med([j[1] for j in J])
	Dv = [j[2] for j in J if j[2] is not None]
	rD = _med(Dv) if Dv else None
	Tv = [j[3] for j in J if j[3] is not None]
	rT = _med(Tv) if len(Tv) >= RECENT_MIN_N // 2 else None
	res.update({"rP": rP, "rD": rD, "rT": rT, "ref_src": wins[newest][9]})
	bP, bD, bT = base["P"], base["D"], base["T"]
	chk = {}
	chk["plow"] = _chk(bP["med"] - rP, bP["spread"], ABS_P) + (bP["med"], rP)
	if rD is not None and bD["med"] is not None:
		chk["dips"] = _chk(rD - bD["med"], bD["spread"], ABS_D) + (bD["med"], rD)
	if rT is not None and bT["med"] is not None and bT["n"] >= BASE_MIN_N // 2:
		chk["hot"] = _chk(rT - bT["med"], bT["spread"], ABS_T) + (bT["med"], rT)
	if ref is not None and ref.get("n", 0) >= REF_MIN_N:
		chk["plow_l"] = _chk(ref["P"]["med"] - rP, ref["P"]["spread"], ABS_P_LONG) + (ref["P"]["med"], rP)
		if rT is not None and ref["T"]["med"] is not None and ref["T"]["n"] >= REF_MIN_N // 2:
			chk["hot_l"] = _chk(rT - ref["T"]["med"], ref["T"]["spread"], ABS_T_LONG) + (ref["T"]["med"], rT)
	# the sensors: flat through the newest FLAT_N judged windows of the last KEEP_DAYS where they normally move, or out of
	# range
	sens = []
	JF, x = _judged(wins, spans, prun, now - KEEP_DAYS * DAY_MS, now)
	tail = JF[-FLAT_N:]
	prs = [j[4] for j in tail if j[4] is not None]
	if len(prs) >= FLAT_N and max(prs) < FLAT_P and (base.get("prange") or 0) >= FLAT_P_BASE:
		sens.append("pressure sensor reads flat through the last %d h of running (it normally moves %.1f bar in a window)" % (_h(len(tail)),
			base["prange"]))
	trs = [j[5] for j in tail if j[5] is not None]
	if len(trs) >= FLAT_N and max(trs) < FLAT_T and (base.get("trange") or 0) >= FLAT_T_BASE:
		sens.append("temperature sensor reads flat through the last %d h of running (it normally moves %.1f degC in a window)" % (
			_h(len(tail)), base["trange"]))
	if rP < P_OK[0] or rP > P_OK[1]:
		sens.append("pressure reads %.1f bar - out of range" % rP)
	tv = [wins[j[0]][3] for j in J if wins[j[0]][3] is not None]
	if tv and (_med(tv) < T_OK[0] or _med(tv) > T_OK[1]):
		sens.append("temperature reads %.1f degC - out of range" % _med(tv))
	if sens:
		chk["sensor"] = (float(WATCH), None, None, None)
	res["chk"] = chk
	scored = [(v[0], k) for k, v in chk.items() if v[0] is not None]
	score, lead = max(scored) if scored else (0.0, None)
	score = min(score, float(HOT))
	res["lead"] = lead
	res["score_raw"] = score
	# a raised band holds while its score stays at its keep level; under it the band drops HOLD_MS after the last pass there
	ob, oat = _S.setdefault("band", {}).get(key, (None, 0))
	nb = _band(score)
	if ob is not None and ob >= 1 and nb <= ob:
		keep = score >= (KEEP_HOT if ob >= 2 else KEEP_WATCH)
		if keep or now - oat < HOLD_MS:
			if nb < ob:
				score = float(HOT if ob >= 2 else WATCH)
				nb = ob
			if keep:
				_S["band"][key] = (ob, now)
	res["score"] = score
	res["band"] = nb
	if nb != ob:
		_S["band"][key] = (nb, now)
	_words(res, p, base, ref, sens)
	return res


def _hold_idle(res, now):
	"""A raised band holds through a not-judged state (standby, measuring, learning, a shut, no data) for HOLD_IDLE_MS
	from its last judged pass - a pump taken off line for a suspected leak stays marked until it is judged again."""
	ob, oat = (_S.get("band") or {}).get(res["key"], (None, 0))
	if ob is not None and ob >= 1 and now - oat < HOLD_IDLE_MS:
		bt = "HOT" if ob >= 2 else "WATCH"
		res["band"] = ob
		res["score"] = float(HOT if ob >= 2 else WATCH)
		res["held"] = True
		res["v"] = "%s held, %s" % (bt, res["v"])
		res["d"] += "; %s held from %s - judged again when it runs" % (bt, _fmt(oat, "EEE HH:mm"))
	return res


def _ctext(k, v, res, refsince, refmon):
	"""The words for one check: (short value - the row and the card, about 25 characters at most, long text)."""
	sc, z, b, r = v
	lab = res["label"]
	src = _refname(res.get("ref_src"))
	if k == "plow":
		return ("pressure -%.0f bar" % (b - r), "%s running pressure %.1f bar - %.1f bar under its normal %.1f (z %.1f): it cannot hold "
			"its pressure - internal leakage or the compensator" % (lab, r, b - r, b, z))
	if k == "dips":
		return ("dips %.0f bar deeper" % (r - b), "%s pressure falls %.1f bar under load in a window, normal %.1f (z %.1f): it cannot "
			"make up the flow - internal leakage" % (lab, r, b, z))
	if k == "hot":
		return ("%.1f degC hotter" % (r - b), "%s runs %+.1f degC over %s, normal %+.1f (z %.1f): %.1f degC hotter - oil forced back "
			"through a worn pump turns to heat" % (lab, r, src, b, z, r - b))
	if k == "plow_l":
		return ("-%.0f bar since %s" % (b - r, refmon), "%s running pressure %.1f bar - %.1f bar under its reference %.1f "
			"(the month from %s): wear since then" % (lab, r, b - r, b, refsince))
	if k == "hot_l":
		return ("+%.1f degC since %s" % (r - b, refmon), "%s runs %+.1f degC over %s against %+.1f in its reference (the month "
			"from %s): %.1f degC hotter - wear since then" % (lab, r, src, b, refsince, r - b))
	return ("sensor", lab + " - sensor")


def _words(res, p, base, ref, sens):
	lab = p[4]
	refsince = _fmt(ref["from"], "d MMM") if ref and ref.get("from") else ""
	refmon = _fmt(ref["from"], "MMM") if ref and ref.get("from") else ""
	numbers = "%.1f bar (normal %.1f)" % (res["rP"], base["P"]["med"])
	if res.get("rD") is not None and base["D"]["med"] is not None:
		numbers += ", dips %.1f bar (%.1f)" % (res["rD"], base["D"]["med"])
	if res.get("rT") is not None and base["T"]["med"] is not None:
		numbers += ", %+.1f degC over %s (%+.1f)" % (res["rT"], _refname(res.get("ref_src")), base["T"]["med"])
	span = " - %d h of running against the last %d days" % (_h(res["n_recent"]), BASE_DAYS)
	lead = res.get("lead")
	b = res["band"]
	if lead == "sensor" and b >= 1:
		res["v"] = "sensor"
		res["d"] = "%s %s%s" % (lab, "; ".join(sens), span)
	elif lead is not None and b >= 1 and res["chk"][lead][0] > 0:
		v, d = _ctext(lead, res["chk"][lead], res, refsince, refmon)
		others = [k for k, x in res["chk"].items() if k != lead and x[0] is not None and x[0] >= WATCH]
		res["v"] = v
		res["d"] = d + ((" - also " + ", ".join([_ctext(k, res["chk"][k], res, refsince, refmon)[0] for k in others])) if others else "") + span
	else:
		res["v"] = "normal"
		res["d"] = "%s normal - %s%s" % (lab, numbers, span)
	if b >= 1 and res.get("score_raw", 0) < (HOT if b >= 2 else WATCH):
		bt = "HOT" if b >= 2 else "WATCH"
		res["held"] = True
		res["v"] = "%s held, %s" % (bt, "now normal" if res["v"] == "normal" else res["v"])
		res["d"] += " (%s held - drops %d h after the last pass at %d)" % (bt, HOLD_MS // 3600000, int(KEEP_HOT if b >= 2 else KEEP_WATCH))


# ------------------------------------------------------------------------------------------------ the refresh
def _have():
	have = set()
	for k in _S["win"]:
		have.update(_S["win"][k].keys())
	return have


def _mine(gen):
	return gen is None or _S.get("gen") == gen


def _base_span(now, man):
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
			spans_cache["base"] = _spans(now - BASE_DAYS * DAY_MS - DAY_MS, t1)[0]
		J, skip = _judged(wins, spans_cache["base"], _prun(wins), t0, t1)
		st = _stats(J, t0, t1)
	except (Exception, Throwable) as e:
		_err("baseline %s" % key, e)
		if hit is not None:
			return hit[1]
		raise
	_S["base"][key] = (now, st)
	return st


def _reference(key, now, refs):
	"""The long reference (cached REF_EVERY_MS; none yet is looked at again hourly): set by hand, else the pump's first
	REF_RUN_N windows of running at pressure - used once it ended LONG_GAP_DAYS ago."""
	hit = _S["ref"].get(key)
	if hit is not None and now - hit[0] < (REF_EVERY_MS if hit[1] is not None else REF_RETRY_MS):
		return hit[1]
	st = None
	a, b, note = _ref_span(key, refs.get(key))
	if a is not None and b is not None and b <= now - LONG_GAP_DAYS * DAY_MS:
		wins = _load(a - (SETTLE_W + 1) * W_MS, b, key)[key]
		J, skip = _judged(wins, _spans(a - DAY_MS, b)[0], _prun(wins), a, b)
		st = _stats(J, a, b)
		st["note"] = note
	_S["ref"][key] = (now, st)
	return st


def _refresh(gen=None):
	"""Background: the stored windows (once, then hourly), the due windows from the historian, one older gap, then every
	pump analysed. Each step on its own; never raises."""
	now = _now()
	try:
		if not _S["loaded"] or now - _S.get("loaded_at", 0) > 3600000:
			try:
				got = _load(now - KEEP_DAYS * DAY_MS)
				if not _mine(gen):
					return
				for k in got:
					_S["win"].setdefault(k, {}).update(got[k])
				_S["loaded"] = True
				_S["loaded_at"] = now
			except (Exception, Throwable) as e:
				_err("window table read", e)
		if not _S["band_loaded"]:
			try:
				got = _band_read()
				if not _mine(gen):
					return
				for k in got:
					_S["band"].setdefault(k, got[k])
				_S["band_saved"].update(got)
				_S["band_loaded"] = True
			except (Exception, Throwable) as e:
				_err("band table read", e)
		due = _closed(now)
		have = _have()
		newest = max(have) if have else None
		start = max(newest + W_MS, due - CHUNK_MS + W_MS) if newest is not None else due - CHUNK_MS + W_MS
		if start <= due:
			try:
				got = _hist(start, due + W_MS)
				if not _mine(gen):
					return
				_store(got, "live")
			except (Exception, Throwable) as e:
				_err("historian / store", e)
			have = _have()
		tried = _S["tried"]
		floor = now - KEEP_DAYS * DAY_MS
		floor -= floor % W_MS
		w = due - CHUNK_MS
		while w >= floor:
			if w not in have and w not in tried:
				a = max(floor, w - CHUNK_MS + W_MS)
				for x in range(a, w + W_MS, W_MS):
					tried.add(x)
				try:
					got = _hist(a, w + W_MS)
					if not _mine(gen):
						return
					_store(got, "live")
				except (Exception, Throwable) as e:
					_err("historian gap fill", e)
				break
			w -= W_MS
		if not _mine(gen):
			return
		_calc(now, gen)
	except (Exception, Throwable) as e:
		_err("refresh", e)
	finally:
		if _mine(gen):
			_S["busy"] = False


def _calc(now, gen=None):
	floor = now - KEEP_DAYS * DAY_MS
	for k in _S["win"]:
		for w in [w for w in _S["win"][k] if w < floor - W_MS]:
			del _S["win"][k][w]
	for w in [w for w in _S["tried"] if w < floor - W_MS]:
		_S["tried"].discard(w)
	spans, snote = _spans(now - DAY_MS, now + W_MS)
	try:
		live = _live()
	except (Exception, Throwable) as e:
		live = {}
		_err("live tags", e)
	try:
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
			base = _baseline(k, now, cache, refs.get(k))
			try:
				ref = _reference(k, now, refs)
			except (Exception, Throwable) as e:
				ref = None
				_err("reference %s" % k, e)
			res[k] = analyse(k, _S["win"].get(k) or {}, base, ref, spans, live.get(k), now, snote)
		except (Exception, Throwable) as e:
			res[k] = {"key": k, "label": p[4], "short": p[5], "row": p[8], "area": p[1], "card": p[2], "st": "error", "score": -1,
				"band": -1, "v": "error", "d": "%s - analysis failed: %s" % (p[4], _a(e)[:120]), "live": live.get(k) or {}}
			_err("analyse %s" % k, e)
	if not _mine(gen):
		return
	_S["res"] = res
	_S["calc_at"] = now
	_S["calc_w"] = _closed(now)
	_publish(res, now)
	for k, v in list(_S["band"].items()):
		if _S["band_saved"].get(k) != v:
			try:
				_band_write(k, v[0], v[1])
				_S["band_saved"][k] = v
			except (Exception, Throwable) as e:
				_err("band table write", e)
				break


def poll(now=None):
	"""Anomaly Watch slow pass: start a background refresh when a new window is due, none has run or a shut has just
	ended. Returns at once, never raises."""
	try:
		_init()
		t = long(now) if now is not None else _now()
		if _S["busy"] and t - _S["busy_since"] < BUSY_MAX_MS:
			return False
		if _S["calc_w"] is not None and _S["calc_w"] >= _closed(t) and t - _S["calc_at"] < 2 * W_MS:
			# a shut that has just ended is judged again at once, not at the next window
			if not [1 for r in (_S.get("res") or {}).values() if r.get("st") == "shut" and r.get("shut_to", t + 1) <= t]:
				return False
		_S["busy"] = True
		_S["busy_since"] = t
		gen = _S.get("gen", 0) + 1
		_S["gen"] = gen
		system.util.invokeAsynchronous(lambda: _refresh(gen))
		return True
	except (Exception, Throwable) as e:
		_S["busy"] = False
		_err("poll", e)
		return False


GKEY = "forensics.hydPump"
STALE_MS = 2 * 3600000


def _publish(res, now):
	"""The latest results for every gateway scope (system.util.getGlobals - one per gateway): a Perspective binding
	reaches them even where it does not share this module's state with the Anomaly Watch timer. Never raises."""
	try:
		system.util.getGlobals()[GKEY] = {"res": res, "calc_at": now, "version": SCRIPT_VERSION}
	except (Exception, Throwable):
		pass


def _results():
	"""(results, the time they were worked out): this module's own, else the ones the gateway refresh published."""
	if _S.get("res"):
		return _S["res"], _S.get("calc_at", 0)
	try:
		x = system.util.getGlobals().get(GKEY)
		if x and x.get("res"):
			return x["res"], x.get("calc_at", 0)
	except (Exception, Throwable):
		pass
	return {}, 0


def state():
	"""Every pump's latest result: {"ts", "version", "pumps": {key: result}, "error"}. Never raises."""
	try:
		_init()
		res, cat = _results()
		return {"ts": cat, "version": SCRIPT_VERSION, "pumps": dict(res), "error": _S.get("last_error", "")}
	except (Exception, Throwable) as e:
		return {"ts": 0, "version": SCRIPT_VERSION, "pumps": {}, "error": _a(e)[:160]}


def _rv(r):
	"""A pump's value on the Hydraulics row: its row name and its value."""
	return "%s %s" % (r.get("row") or r.get("short") or r.get("key"), r.get("v") or "")


def _head(r, judged):
	"""The short line under an Anomaly Watch area card's title - two lines at most there."""
	b = int(r.get("band", 0))
	if b >= 1:
		h = "%s - %s" % (r.get("label"), r.get("v"))
	else:
		h = "%d pumps normal" % len(judged)
	up = [x for x in judged if x is not r and int(x.get("band", -1)) >= 1]
	if len(up) == 1:
		h += "; %s %s too" % (up[0].get("label"), "HOT" if int(up[0].get("band", 1)) >= 2 else "WATCH")
	elif up:
		h += "; %d more pumps raised" % len(up)
	if len(h) > 110:
		h = h[:107].rsplit(" ", 1)[0] + "..."
	return h


def rows(area):
	"""(row, assets) for one Anomaly Watch area - the pumps of the Hydraulics row: the worst pump leads. Never raises."""
	try:
		_init()
		pumps = [p for p in PUMPS if p[1] == area]
		if not pumps:
			return None, []
		res0, cat = _results()
		stale = bool(cat) and _now() - cat > STALE_MS
		res = [None if stale else res0.get(p[0]) for p in pumps]
		assets = []
		for p, r in zip(pumps, res):
			b = r.get("band", -1) if r else -1
			assets.append(("pump " + p[4], b if b >= 0 else -2))
		got = [r for r in res if r]
		if not got:
			v = "pumps stale" if stale else "pumps starting"
			txt = ("pump watch not updated since %s" % _fmt(cat, "EEE HH:mm")) if stale else "pump watch starting"
			return {"k": "hyd", "l": "Hydraulics", "v": v, "i": -1, "d": txt, "h": v, "note": v, "cap": 2}, assets
		judged = [r for r in got if r.get("band", -1) >= 0]
		if not judged:
			sts = set([str(r.get("st")) for r in got])
			if len(sts) == 1:
				v = "pumps " + ST_WORD.get(list(sts)[0], "not judged")
			elif sts <= set(["standby", "measuring"]):
				v = "pumps measuring"
			else:
				v = "pumps not judged"
			return {"k": "hyd", "l": "Hydraulics", "v": v, "i": -1, "d": "; ".join([r.get("d", "") for r in got]), "h": v, "note": v,
				"cap": 2}, assets
		wst = max(judged, key=lambda r: (r.get("band", 0), r.get("score", 0)))
		score = wst.get("score", 0)
		if wst.get("band", 0) >= 1:
			v = _rv(wst)
		else:
			idle = len([r for r in got if r.get("st") != "ok"])
			v = "%d pumps OK" % len(judged) + ((", %d idle" % idle) if idle else "")
		more = [r.get("d", "") for r in got if r is not wst and (r.get("band", -1) >= 1 or r.get("st") != "ok")]
		d = wst.get("d", "")
		if more:
			d += "; " + "; ".join(more[:6])
		return {"k": "hyd", "l": "Hydraulics", "v": v, "i": score, "d": d, "h": _head(wst, judged), "cap": 2}, assets
	except (Exception, Throwable) as e:
		_err("rows %s" % area, e)
		return {"k": "hyd", "l": "Hydraulics", "v": "error", "i": -1, "d": "pump watch: %s" % _a(e)[:120]}, []


# ------------------------------------------------------------------------------------------------ the pump card
# The PUMP WATCH section of the hydraulics diagnostics cards (view HydraulicsDiagnosticsCard 1.6.0): one SVG per card for
# an ia.display.image - one line per pump: LED, name, the running pressure and the temperature over the oil it works,
# each as a marker on a gauge against its own normal (the tick in the middle is its median, the green band +-2 spreads,
# the ends +-6), the numbers and the verdict. Not judged: the live values and why.
CARD_PUMPS = {"SDB": ["SDB_U1P1", "SDB_U1P2", "SDB_U1P3", "SDB_U1P4", "SDB_U2P1", "SDB_U2P2"],
	"GRA": ["GRA_U1P1", "GRA_U1P2", "GRA_U1P3"], "COS": ["COS_U1P1", "COS_U1P2", "COS_U1P3", "COS_U3P1", "COS_U3P2"],
	"TNB": ["TNB_U4P1", "TNB_U4P2", "TNB_U4P3", "TNB_U4P4"]}
CARD_W = 400
CARD_H = 92
ROW_H = 15.0
X_NAME = 13
X_PG = 60
X_PV = 116
X_TG = 156
X_TV = 212
G_W = 52
F_NAME = 10
F_VAL = 9
FONT = "Segoe UI, Calibri, Arial, sans-serif"
C_TXT = "#F3EEE7"
C_SUB = "#C2C7C7"
C_MUTE = "#80878A"
C_TRACK = "#3A4448"
C_BAND = "#36664A"
C_LED = {-1: "#80878A", 0: "#7CB342", 1: "#EBC452", 2: "#F08A3C"}
C_MARK = {-1: "#80878A", 0: "#78A699", 1: "#EBC452", 2: "#F08A3C"}
C_BADGE = {"HOT": ("#DC7323", "#F3EEE7"), "WATCH": ("#D4A863", "#242E30"), "OK": ("#36664A", "#F3EEE7")}
C_BADGE_OFF = ("#3A4448", "#C2C7C7")
G_Z = 6.0
CSS = ("text{font-family:%s;}"
	"@keyframes pwPulse{0%%,100%%{opacity:.95}50%%{opacity:.35}}"
	".pl{animation:pwPulse 1.4s ease-in-out infinite}" % FONT)


def _x(s):
	"""Text for the SVG: ASCII, XML-escaped."""
	try:
		if isinstance(s, str):
			s = s.decode("utf-8", "replace")
		elif not isinstance(s, unicode):
			s = unicode(s)
		s = s.encode("ascii", "replace")
	except (Exception, Throwable):
		s = "?"
	return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def _tx(x, y, s, size, fill, anchor="start", weight=400, extra=""):
	return '<text x="%.1f" y="%.1f" font-size="%s" fill="%s" text-anchor="%s" font-weight="%s"%s>%s</text>' % (x, y, size,
		fill, anchor, weight, (" " + extra) if extra else "", _x(s))


def _uri(svg):
	if isinstance(svg, unicode):
		svg = svg.encode("ascii", "xmlcharrefreplace")
	return "data:image/svg+xml;base64," + base64.b64encode(svg)


def _gauge(x0, w, yc, z, band):
	"""A gauge: the track, the normal band (+-2 spreads), the median tick and the marker at z (clamped to +-G_Z)."""
	out = ['<rect x="%.1f" y="%.1f" width="%.1f" height="3" rx="1.5" fill="%s"/>' % (x0, yc - 1.5, w, C_TRACK)]
	bw = w * (2 * Z_REF) / (2 * G_Z)
	out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="3" rx="1.5" fill="%s"/>' % (x0 + (w - bw) / 2.0, yc - 1.5, bw, C_BAND))
	out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="0.8"/>' % (x0 + w / 2.0, yc - 3.5,
		x0 + w / 2.0, yc + 3.5, C_MUTE))
	if z is not None:
		zz = max(-G_Z, min(G_Z, z))
		cx = x0 + w / 2.0 + zz * w / (2 * G_Z)
		out.append('<circle cx="%.1f" cy="%.1f" r="3.1" fill="%s" stroke="#242E30" stroke-width="0.8"%s/>' % (cx, yc,
			C_MARK.get(band, C_MUTE), ' class="pl"' if band >= 2 else ""))
	return out


def _cband(c, keys):
	return _band(max([c[k][0] for k in keys if c.get(k) and c[k][0] is not None] or [0]))


def _cz(c, keys, sign):
	"""The z of the check that scores highest of keys (the gauge follows the check that speaks), signed for the gauge."""
	best = None
	for k in keys:
		x = c.get(k)
		if x is None or x[1] is None:
			continue
		if best is None or (x[0] or 0) > (best[0] or 0):
			best = x
	return sign * best[1] if best is not None else None


def _pline(r, y):
	"""One pump's line of the card."""
	out = []
	if r is None:
		out.append(_tx(X_NAME, y + 10.5, "-", F_NAME, C_MUTE))
		return out
	b = int(r.get("band", -1))
	judged = r.get("st") == "ok" and r.get("rP") is not None
	out.append('<circle cx="6" cy="%.1f" r="3.4" fill="%s"%s/>' % (y + 7.0, C_LED.get(b, C_MUTE), ' class="pl"' if b >= 2 else ""))
	out.append(_tx(X_NAME, y + 10.5, r.get("short") or "", F_NAME, C_TXT if judged else C_SUB, weight=700))
	v = r.get("v") or ST_WORD.get(str(r.get("st")), str(r.get("st")))
	if judged:
		c = r.get("chk") or {}
		out.extend(_gauge(X_PG, G_W, y + 7.0, _cz(c, ("plow", "plow_l"), -1), _cband(c, ("plow", "dips", "plow_l"))))
		out.append(_tx(X_PV, y + 10.5, "%.0f bar" % r["rP"], F_VAL, C_SUB))
		if r.get("rT") is not None:
			out.extend(_gauge(X_TG, G_W, y + 7.0, _cz(c, ("hot", "hot_l"), 1), _cband(c, ("hot", "hot_l"))))
			out.append(_tx(X_TV, y + 10.5, "%+.1f C" % r["rT"], F_VAL, C_SUB))
		else:
			out.append(_tx(X_TG + G_W / 2.0, y + 10.5, "no ref", F_VAL - 1, C_MUTE, "middle"))
		if b == 0:
			v = "normal"
		out.append(_tx(396, y + 10.5, v[:30], F_VAL, C_MARK.get(b, C_SUB) if b >= 1 else C_SUB, "end", 700 if b >= 1 else 400))
	else:
		lv = r.get("live") or {}
		now_txt = []
		if lv.get("p") is not None:
			now_txt.append("%.0f bar" % lv["p"])
		if lv.get("t") is not None:
			now_txt.append("%.0f C" % lv["t"])
		out.append(_tx(X_PG, y + 10.5, "  ".join(now_txt), F_VAL, C_MUTE))
		out.append(_tx(396, y + 10.5, v[:34], F_VAL, C_MARK.get(b, C_MUTE) if b >= 1 else C_MUTE, "end", 700 if b >= 1 else 400))
	return out


def card(code):
	"""The PUMP WATCH section of one hydraulics diagnostics card (code SDB, GRA, COS, TNB): {"svg" (data URI), "badge",
	"badge_bg", "badge_fg", "led", "band", "sub", "tip"}. Results older than STALE_MS show as STALE. Never raises."""
	try:
		_init()
		code = str(code).upper().strip()
		keys = CARD_PUMPS.get(code, [])
		res, cat = _results()
		stale = bool(cat) and _now() - cat > STALE_MS
		cc = _S.setdefault("cards", {})
		hit = cc.get(code)
		if hit is not None and cat and hit[0] == cat and not stale:
			return dict(hit[1])
		rs = [res.get(k) for k in keys]
		got = [r for r in rs if r]
		bands = [int(r.get("band", -1)) for r in got]
		worst = max(bands) if bands and not stale else -1
		sts = [str(r.get("st")) for r in got]
		if not keys:
			badge = "NO PUMPS"
		elif not got:
			badge = "STARTING"
		elif stale:
			badge = "STALE"
		elif worst >= 2:
			badge = "HOT"
		elif worst == 1:
			badge = "WATCH"
		elif worst == 0:
			badge = "OK"
		elif "shut" in sts:
			badge = "SHUT"
		elif all([s == "learning" for s in sts]):
			badge = "LEARNING"
		elif all([s == "nodata" for s in sts]):
			badge = "NO DATA"
		else:
			badge = "IDLE"
		bg, fg = C_BADGE.get(badge, C_BADGE_OFF)
		if stale:
			why = "not updated since %s" % _fmt(cat, "EEE HH:mm")
			rs = [dict(r, st="stale", band=-1, v=why) if r else r for r in rs]
		body = []
		for i in range(len(keys)):
			body.extend(_pline(rs[i], 1 + i * ROW_H))
		if not keys:
			body.append(_tx(CARD_W / 2.0, CARD_H / 2.0, "no sensored pumps on this card", 9, C_MUTE, "middle"))
		svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" preserveAspectRatio="xMidYMin meet">'
			'<style>%s</style>%s</svg>' % (CARD_W, CARD_H, CSS, "".join(body)))
		run = len([r for r in got if r.get("st") == "ok"])
		idle = len([r for r in got if r.get("st") in ("standby", "measuring")])
		if not keys:
			sub = "no sensored pumps on this card"
		elif not got:
			sub = "starting"
		elif stale:
			sub = "not updated since %s" % _fmt(cat, "EEE HH:mm")
		elif badge == "LEARNING":
			sub = "learning each pump's normal"
		elif badge == "SHUT":
			sub = "plant shut - not judged"
		else:
			sub = "%d judged, %d idle - each against its own 8 weeks" % (run, idle)
		tip = "; ".join([str(r.get("d", "")) for r in got]) or "pump watch starting"
		if stale:
			tip = "Pump watch not updated since %s (is the Anomaly Watch timer running?) - last: %s" % (_fmt(cat, "EEE d MMM HH:mm"), tip)
		else:
			tip = ("Each pump against its own normal: pressure (left gauge) and temperature over the oil it draws (right gauge); "
				"the tick is its median, the green band its usual spread. " + tip)
		out = {"svg": _uri(svg), "badge": badge, "badge_bg": bg, "badge_fg": fg, "led": C_LED.get(worst, C_MUTE), "band": worst,
			"sub": sub, "tip": tip[:1200]}
		if cat and not stale:
			cc[code] = (cat, dict(out))
		return out
	except (Exception, Throwable) as e:
		_err("card %s" % code, e)
		return {"svg": "", "badge": "ERROR", "badge_bg": C_BADGE_OFF[0], "badge_fg": C_BADGE_OFF[1], "led": C_MUTE, "band": -1,
			"sub": "pump watch: %s" % _a(e)[:80], "tip": _a(e)[:200]}


# ------------------------------------------------------------------------------------------------ the details popup
# detail(code) (1.0.4): the PUMP WATCH section of one card read in full - the popup HydPumpWatchDetail, opened by the
# DETAILS button of HydraulicsDiagnosticsCard 1.7.0 (it replaces the card's hover text)
DW = 760
D_X = 16
D_COLS = (36, 278, 520)
D_GW = 108
D_WRAP = 128
D_LH = 14.0
D_TOP = 86.0
C_GOLD = "#DEBF7A"
C_BG = "#1F2A2D"
C_LINE = "#34413F"
C_CHIP = {2: C_BADGE["HOT"], 1: C_BADGE["WATCH"], 0: C_BADGE["OK"]}
D_LEGEND = ("Each pump against its own normal - its steady running of the last %d days - and against its reference - its "
	"first %d days of running at pressure, used from %d days after. Gauges: the green band is its usual spread, the tick "
	"its median, the dot where it runs now - pressure lower to the left, dips deeper and temperature hotter to the right."
	% (BASE_DAYS, REF_RUN_N // 96, LONG_GAP_DAYS))


def _wrap(s, n):
	"""Lines of at most n characters, broken at spaces."""
	out = []
	line = ""
	for w in _a(s).split():
		if line and len(line) + 1 + len(w) > n:
			out.append(line)
			line = w
		else:
			line = (line + " " + w) if line else w
	if line:
		out.append(line)
	return out


def _dgauge(x0, w, yc, z, band):
	"""The sheet's gauge - the card's, larger: the track, the normal band (+-2 spreads), the median tick and the marker
	at z (clamped to +-G_Z)."""
	out = ['<rect x="%.1f" y="%.1f" width="%.1f" height="5" rx="2.5" fill="%s"/>' % (x0, yc - 2.5, w, C_TRACK)]
	bw = w * (2 * Z_REF) / (2 * G_Z)
	out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="5" rx="2.5" fill="%s"/>' % (x0 + (w - bw) / 2.0, yc - 2.5, bw, C_BAND))
	out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.2"/>' % (x0 + w / 2.0, yc - 6,
		x0 + w / 2.0, yc + 6, C_SUB))
	if z is not None:
		zz = max(-G_Z, min(G_Z, z))
		cx = x0 + w / 2.0 + zz * w / (2 * G_Z)
		out.append('<circle cx="%.1f" cy="%.1f" r="5.2" fill="%s" stroke="%s" stroke-width="1.5"%s/>' % (cx, yc,
			C_MARK.get(band, C_MUTE), C_BG, ' class="pl"' if band >= 2 else ""))
	return out


def _chip(xr, yb, text, band, judged):
	"""A verdict chip ending at xr, text baseline yb."""
	bg, fg = C_CHIP.get(band, C_BADGE_OFF) if (band >= 1 or (judged and band == 0)) else C_BADGE_OFF
	w = 6.2 * len(text) + 18
	return ['<rect x="%.1f" y="%.1f" width="%.1f" height="20" rx="4" fill="%s"/>' % (xr - w, yb - 14, w, bg),
		_tx(xr - w / 2.0, yb, text, 10.5, fg, "middle", 700, 'letter-spacing="0.3"')]


def _dnorm(c, k, kl, f):
	"""Under a gauge: the medians its checks compare with - 'normal X, reference Y'."""
	out = []
	x = c.get(k)
	if x is not None and x[2] is not None:
		out.append(("normal " + f) % x[2])
	y = c.get(kl) if kl else None
	if y is not None and y[2] is not None:
		out.append(("reference " + f) % y[2])
	return ", ".join(out) or "no normal yet"


def _dtext(p, r):
	"""The pump's full text without its name in front - the block shows the name. A pump judged normal: how much running
	it was judged on (its gauges carry the numbers its text repeats)."""
	if r.get("st") == "ok" and r.get("rP") is not None and int(r.get("band", -1)) == 0:
		return "Normal - %d h of steady running in the last %d h, judged against its last %d days." % (_h(r.get("n_recent", 0)),
			RECENT_H, BASE_DAYS)
	t = _a(r.get("d") or "")
	for lab in (p[4], p[5]):
		if lab and t.startswith(lab):
			t = t[len(lab):].strip()
			break
	if t.startswith("- "):
		t = t[2:]
	return (t[:1].upper() + t[1:]) if t else ""


def _dblock(p, r, y):
	"""One pump's block of the sheet from y: (svg parts, height)."""
	out = ['<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="1"/>' % (D_X, y, DW - D_X, y, C_LINE)]
	ya = y + 25
	if not r:
		out.append(_tx(D_X + 20, ya, p[5], 13.5, C_SUB, weight=700))
		out.append(_tx(D_X + 92, ya, "%s - no result yet" % p[4], 11, C_MUTE))
		return out, 40
	b = int(r.get("band", -1))
	st = str(r.get("st"))
	judged = st == "ok" and r.get("rP") is not None
	out.append('<circle cx="%.1f" cy="%.1f" r="5.5" fill="%s"%s/>' % (D_X + 6, ya - 4.5, C_LED.get(b, C_MUTE),
		' class="pl"' if b >= 2 else ""))
	out.append(_tx(D_X + 20, ya, p[5], 13.5, C_TXT if judged else C_SUB, weight=700))
	out.append(_tx(D_X + 92, ya, p[4], 11, C_SUB))
	v = _a(r.get("v") or ST_WORD.get(st, st))
	if judged and b == 0:
		chip = "NORMAL"
	elif b >= 1 and not (v.startswith("HOT") or v.startswith("WATCH")):
		chip = "%s: %s" % ("HOT" if b >= 2 else "WATCH", v)
	else:
		chip = v
	out.extend(_chip(DW - D_X, ya, chip[:56], b, judged))
	yb = ya + 13
	if judged:
		c = r.get("chk") or {}
		src = {"tank": "OVER ITS TANK", "peer": "OVER THE UNIT'S OTHER PUMP"}.get(r.get("ref_src"), "OVER ITS REFERENCE")
		cols = [("PRESSURE", _cz(c, ("plow", "plow_l"), -1), _cband(c, ("plow", "plow_l")), "%.1f bar" % r["rP"],
				_dnorm(c, "plow", "plow_l", "%.1f")),
			("DIPS UNDER LOAD", _cz(c, ("dips",), 1), _cband(c, ("dips",)),
				("%.1f bar" % r["rD"]) if r.get("rD") is not None else "-", _dnorm(c, "dips", None, "%.1f")),
			("TEMPERATURE " + src, _cz(c, ("hot", "hot_l"), 1), _cband(c, ("hot", "hot_l")),
				("%+.1f C" % r["rT"]) if r.get("rT") is not None else "-", _dnorm(c, "hot", "hot_l", "%+.1f"))]
		for i in range(len(cols)):
			cap, z, cb, val, norm = cols[i]
			x0 = D_COLS[i]
			out.append(_tx(x0, yb + 9, cap, 8.5, C_MUTE, weight=700, extra='letter-spacing="0.6"'))
			out.extend(_dgauge(x0, D_GW, yb + 22, z, cb))
			out.append(_tx(x0 + D_GW + 11, yb + 26.5, val, 12.5, C_MARK.get(cb, C_TXT) if cb >= 1 else C_TXT, weight=700))
			out.append(_tx(x0, yb + 41, norm, 9.5, C_SUB))
		yt = yb + 61
	else:
		lv = r.get("live") or {}
		now = []
		if lv.get("p") is not None:
			now.append("%.1f bar" % lv["p"])
		if lv.get("t") is not None:
			now.append("%.1f C" % lv["t"])
		if lv.get("run") is not None:
			now.append("motor %s" % ("running" if lv["run"] else "stopped"))
		if lv.get("bypass"):
			now.append("sensor bypassed")
		out.append(_tx(D_X + 20, yb + 9, "NOW", 8.5, C_MUTE, weight=700, extra='letter-spacing="0.6"'))
		out.append(_tx(D_X + 50, yb + 9, ", ".join(now) if now else "no live values", 10.5, C_SUB))
		yt = yb + 29
	lines = _wrap(_dtext(p, r), D_WRAP)[:4]
	for i in range(len(lines)):
		out.append(_tx(D_X + 20, yt + i * D_LH, lines[i], 10.5, C_TXT if b >= 1 else C_SUB))
	return out, (yt - y) + max(0, len(lines) - 1) * D_LH + 16


def detail(code):
	"""The PUMP WATCH section of one card read in full (code SDB, GRA, COS, TNB) - the popup HydPumpWatchDetail, the
	card's DETAILS button: {"svg" (data URI), "w", "h" (px), "badge", "badge_bg", "badge_fg", "sub"}. One block per pump:
	its verdict; for a judged pump the pressure, dips and temperature gauges, each with the number now, its normal and
	its reference; for one not judged its live values; then its full text. Never raises."""
	try:
		_init()
		code = str(code).upper().strip()
		keys = CARD_PUMPS.get(code, [])
		res, cat = _results()
		stale = bool(cat) and _now() - cat > STALE_MS
		dc = _S.setdefault("details", {})
		hit = dc.get(code)
		if hit is not None and cat and hit[0] == cat and not stale:
			return dict(hit[1])
		cd = card(code)
		rs = [res.get(k) for k in keys]
		if stale:
			why = "not updated since %s" % _fmt(cat, "EEE HH:mm")
			rs = [dict(r, st="stale", band=-1, v=why) if r else r for r in rs]
		head = [_tx(D_X, 27, "PUMP WATCH", 12, C_GOLD, weight=700, extra='letter-spacing="1.2"'),
			_tx(D_X + 118, 27, cd.get("sub") or "", 11, C_SUB)]
		bb = cd.get("badge") or ""
		bw = 7.2 * len(bb) + 18
		head.append('<rect x="%.1f" y="12" width="%.1f" height="20" rx="4" fill="%s"/>' % (DW - D_X - bw, bw,
			cd.get("badge_bg") or C_BADGE_OFF[0]))
		head.append(_tx(DW - D_X - bw / 2.0, 26, bb, 10.5, cd.get("badge_fg") or C_BADGE_OFF[1], "middle", 700, 'letter-spacing="0.6"'))
		if cat:
			head.append(_tx(DW - D_X - bw - 12, 26, "results of %s" % _fmt(cat, "HH:mm"), 9.5, C_MUTE, "end"))
		leg = _wrap(D_LEGEND, 148)[:3]
		for i in range(len(leg)):
			head.append(_tx(D_X, 48 + i * 12.5, leg[i], 9.5, C_MUTE))
		y = max(D_TOP, 48 + len(leg) * 12.5 + 6)
		body = []
		for i in range(len(keys)):
			parts, h = _dblock(_pump(keys[i]), rs[i], y)
			body.extend(parts)
			y += h
		if not keys:
			body.append(_tx(DW / 2.0, y + 30, "no sensored pumps on this card", 11, C_MUTE, "middle"))
			y += 50
		hh = int(y + 8)
		svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" preserveAspectRatio="xMidYMin meet">'
			'<style>%s</style><rect x="0" y="0" width="%d" height="%d" fill="%s"/>%s</svg>' % (DW, hh, CSS, DW, hh, C_BG,
			"".join(head + body)))
		out = {"svg": _uri(svg), "w": DW, "h": hh, "badge": bb, "badge_bg": cd.get("badge_bg"), "badge_fg": cd.get("badge_fg"),
			"sub": cd.get("sub")}
		if cat and not stale:
			dc[code] = (cat, dict(out))
		return out
	except (Exception, Throwable) as e:
		_err("detail %s" % code, e)
		return {"svg": "", "w": DW, "h": 120, "badge": "ERROR", "badge_bg": C_BADGE_OFF[0], "badge_fg": C_BADGE_OFF[1],
			"sub": "pump watch details: %s" % _a(e)[:80]}


# ------------------------------------------------------------------------------------------------ console
def _line(r):
	if r.get("rP") is None:
		return "%-34s %-9s %s" % (r.get("label"), str(r.get("st")), r.get("v", ""))
	c = r.get("chk") or {}
	parts = []
	for k in ("plow", "dips", "hot", "plow_l", "hot_l", "sensor"):
		x = c.get(k)
		if x is not None and x[0] is not None:
			parts.append("%s %d%s" % (k, int(round(x[0])), (" z%.1f" % x[1]) if x[1] is not None else ""))
	return "%-34s %-9s P %6.1f  D %5.1f  T %s  idx %3d %-6s n %3d  %s  | %s" % (r.get("label"), str(r.get("st")), r["rP"],
		r.get("rD") if r.get("rD") is not None else -1, ("%+5.1f" % r["rT"]) if r.get("rT") is not None else "  -- ",
		int(round(r.get("score", -1))), {-1: "--", 0: "NORMAL", 1: "WATCH", 2: "HOT"}.get(r.get("band", -1)), r.get("n_recent", 0),
		r.get("v", ""), ", ".join(parts))


def _bline(b):
	if not b or not b.get("n"):
		return "no judged windows"
	t = b["T"]
	return "n %4d  P %6.1f +- %4.1f (p05 %.1f)  D %5.1f +- %4.1f  T %s  range P %s T %s" % (b["n"], b["P"]["med"], b["P"]["spread"],
		b["P"]["p05"], b["D"]["med"] if b["D"]["med"] is not None else -1, b["D"]["spread"] or 0,
		("%+5.1f +- %3.1f (n %d)" % (t["med"], t["spread"], t["n"])) if t["med"] is not None else "--",
		("%.2f" % b["prange"]) if b.get("prange") is not None else "--", ("%.2f" % b["trange"]) if b.get("trange") is not None else "--")


def _n(v, pat="%.1f"):
	return (pat % v) if v is not None else "-"


def check(days=3):
	"""READ-ONLY. Paths and live values, the history configuration and coverage, the running sources, a 2 h historian
	read, then a preview of the analysis on the last 'days' straight from the historian (the table is not used). Paste
	the output into the chat if anything reads wrong."""
	_init()
	now = _now()
	print "forensics.hydPump v%s  check  %s  READ-ONLY" % (SCRIPT_VERSION, _fmt(now, "EEE d MMM HH:mm"))
	print ""
	print "LIVE     house tree: pressure, temperature, motor running, sensor bypass"
	try:
		lv = _live()
		for p in PUMPS:
			x = lv.get(p[0]) or {}
			print "         %-34s %-12s %-9s run %-5s bypass %-5s  %s" % (p[4], ("%.1f bar" % x["p"]) if x.get("p") is not None else "BAD " + x.get("pq", "")[:12],
				("%.1f C" % x["t"]) if x.get("t") is not None else "BAD", str(x.get("run")), str(x.get("bypass")), PROV + p[6])
	except (Exception, Throwable) as e:
		print "         FAILED: %s" % _a(e)[-200:]
	print ""
	print "HISTORY  configuration (first pump) and the historian's own record (sqlth_te, sqlth_1_data)"
	try:
		for suf in ("/Status/Pressure", "/Status/Temperature", "/Motor/Status/Running"):
			cfg = system.tag.getConfiguration(PROV + PUMPS[0][6] + suf, False)
			c = cfg[0] if cfg else {}
			keys = ["historyEnabled", "historyProvider", "historicalDeadband", "historicalDeadbandStyle", "sampleMode", "historySampleRate",
				"historySampleRateUnits", "historyMaxAge", "historyMaxAgeUnits", "historyTagGroup"]
			vals = []
			for k in keys:
				try:
					v = c.get(k) if hasattr(c, "get") else c[k]
				except (Exception, Throwable):
					v = None
				if v is not None:
					vals.append("%s=%s" % (k, v))
			print "         %-22s %s" % (suf, ", ".join(vals) or "no history settings returned")
	except (Exception, Throwable) as e:
		print "         configuration: %s" % _a(e)[-160:]
	try:
		ds = system.db.runQuery("SELECT id, tagpath, created, retired FROM sqlth_te WHERE lower(tagpath) LIKE '%pump%' AND (lower(tagpath) LIKE '%pressure' "
			"OR lower(tagpath) LIKE '%temperature' OR lower(tagpath) LIKE '%motor/status/running') ORDER BY tagpath, id LIMIT 120", DB)
		print "         sqlth_te: %d rows (pump pressure / temperature / running)" % ds.getRowCount()
		for r in range(ds.getRowCount()):
			tid = int(ds.getValueAt(r, 0))
			first = last = None
			nh = None
			try:
				a = system.db.runQuery("SELECT t_stamp FROM sqlth_1_data WHERE tagid = %d ORDER BY t_stamp ASC LIMIT 1" % tid, DB)
				b = system.db.runQuery("SELECT t_stamp FROM sqlth_1_data WHERE tagid = %d ORDER BY t_stamp DESC LIMIT 1" % tid, DB)
				c = system.db.runQuery("SELECT count(*) FROM sqlth_1_data WHERE tagid = %d AND t_stamp >= %d" % (tid, now - 3600000), DB)
				first = long(a.getValueAt(0, 0)) if a.getRowCount() else None
				last = long(b.getValueAt(0, 0)) if b.getRowCount() else None
				nh = int(c.getValueAt(0, 0)) if c.getRowCount() else None
			except (Exception, Throwable) as e:
				nh = "?"
			print "         %5d  %-90s %s -> %s  %s samples last hour%s" % (tid, _a(ds.getValueAt(r, 1))[-90:],
				_fmt(first, "d MMM yy") if first else "-", _fmt(last, "d MMM HH:mm") if last else "-", nh,
				"  RETIRED" if ds.getValueAt(r, 3) is not None else "")
	except (Exception, Throwable) as e:
		print "         sqlth_te: %s" % _a(e)[-200:]
	try:
		ds = system.db.runQuery("SELECT column_name FROM information_schema.columns WHERE table_schema = 'hydraulics' AND table_name = 'pump_events' ORDER BY ordinal_position", DB)
		cols = [_a(ds.getValueAt(r, 0)) for r in range(ds.getRowCount())]
		ds = system.db.runQuery("SELECT plc_ref, count(*), min(event_time), max(event_time) FROM hydraulics.pump_events WHERE event_type IN ('start', 'stop') "
			"GROUP BY plc_ref ORDER BY plc_ref", DB)
		print "         hydraulics.pump_events (%s): %d pumps with start / stop events" % (", ".join(cols), ds.getRowCount())
		for r in range(ds.getRowCount()):
			print "           %-34s %6s  %s -> %s" % (ds.getValueAt(r, 0), ds.getValueAt(r, 1), _fmt(_ms(ds.getValueAt(r, 2)), "d MMM yy"),
				_fmt(_ms(ds.getValueAt(r, 3)), "d MMM HH:mm"))
	except (Exception, Throwable) as e:
		print "         hydraulics.pump_events: %s" % _a(e)[-200:]
	print ""
	print "READ     last 2 h, 15-min windows (P avg / min / max bar, T avg degC, run share, reference degC)"
	t1 = _closed(now) + W_MS
	try:
		got = _hist(t1 - 8 * W_MS, t1)
		print "         path forms: %s" % ", ".join(["%s %s" % (g, _S["form"][g]) for g in GROUPS_AVG])
		for p in PUMPS:
			ws = sorted([w for (k, w) in got if k == p[0]])
			if not ws:
				print "         %-34s NO ROWS" % p[4]
				continue
			r = got[(p[0], ws[-1])]
			print "         %-34s %s  P %s / %s / %s  T %s  run %s (%s)  ref %s (%s)" % (p[4], _fmt(ws[-1], "HH:mm"), _n(r[0]), _n(r[1]),
				_n(r[2]), _n(r[3]), _n(r[6], "%.2f"), r[7] or "none", _n(r[8]), r[9] or "none")
	except (Exception, Throwable) as e:
		print "         FAILED: %s" % _a(e)[-300:]
		return None
	print ""
	print "PREVIEW  the last %d days straight from the historian - the baseline here is the days before the last %d h only" % (days, RECENT_H)
	try:
		wins = dict((p[0], {}) for p in PUMPS)
		a = now - int(days * DAY_MS)
		a -= a % W_MS
		while a < t1:
			b = min(t1, a + CHUNK_MS)
			for (k, w), v in _hist(a, b).items():
				wins[k][w] = v
			a = b
		spans, snote = _spans(now - int(days * DAY_MS), now + W_MS)
		print "         shuts: %s" % ("; ".join([s[2] for s in spans]) or "none") + (("  (%s)" % snote) if snote else "")
		saved = dict(_S.get("band") or {})
		_S["band"] = {}
		try:
			lv = _live()
		except (Exception, Throwable):
			lv = {}
		bt1 = now - RECENT_H * 3600000
		bt0 = now - int(days * DAY_MS)
		for p in PUMPS:
			J, skip = _judged(wins[p[0]], spans, _prun(wins[p[0]]), bt0, bt1)
			st = _stats(J, bt0, bt1)
			if st["n"] >= RECENT_MIN_N:
				# a preview: judged on the short baseline it has
				st["n"] = max(st["n"], BASE_MIN_N)
			r = analyse(p[0], wins[p[0]], st, None, spans, lv.get(p[0]), now)
			print "         " + _line(r)
			print "         %-34s base %s  (left out %s)" % ("", _bline(st), ", ".join(["%s %d" % (k, v) for k, v in sorted(skip.items()) if v]) or "none")
		_S["band"] = saved
	except (Exception, Throwable) as e:
		print "         FAILED: %s" % _a(e)[-300:]
	print ""
	print "Next: forensics.hydPump.backfill(30), backfill(30, 30), backfill(30, 60) ... back to the sensors' start (the day"
	print "      lines show the pumps with a pressure), then forensics.hydPump.replay(60)."
	return None


def backfill(days=14, skip_days=0, chunk_h=BF_CHUNK_H):
	"""Writes the windows of the 'days' before the last 'skip_days' into hydraulics.pump_window, chunk_h hours per
	historian read (three reads), oldest first."""
	_init()
	now = _now()
	step = int(chunk_h * 3600000)
	t1 = (_closed(now) + W_MS) - int(skip_days * DAY_MS)
	a = t1 - int(days * DAY_MS)
	a -= a % W_MS
	total = 0
	day = None
	n_day = 0
	p_day = set()
	fails = 0
	print "forensics.hydPump v%s  backfill %d days%s, %d h a read  %s" % (SCRIPT_VERSION, days, (" before the last %d" % skip_days) if skip_days else "",
		chunk_h, _fmt(now, "EEE d MMM HH:mm"))
	while a < t1:
		b = min(t1, a + step)
		_S["dead"] = {}
		d = _fmt(a, "EEE d MMM")
		if d != day:
			if day is not None:
				print "  %s  %5d rows, %2d pumps with a pressure" % (day, n_day, len(p_day))
			day = d
			n_day = 0
			p_day = set()
		try:
			got = _hist(a, b)
			p_day.update([k for (k, w), rec in got.items() if rec[0] is not None])
			n = _store(got, "backfill", False)
		except (Exception, Throwable) as e:
			print "  %s - %s  FAILED: %s" % (_fmt(a, "EEE d MMM HH:mm"), _fmt(b, "HH:mm"), _a(e)[-200:])
			n = 0
			fails += 1
		n_day += n
		total += n
		a = b
	if day is not None:
		print "  %s  %5d rows, %2d pumps with a pressure" % (day, n_day, len(p_day))
	print "done - %d rows (%d pumps x 15-min windows)%s; path forms %s" % (total, len(PUMPS), (", %d reads FAILED - run that stretch again, "
		"smaller chunk_h" % fails) if fails else "", ", ".join(["%s %s" % (g, _S["form"][g]) for g in GROUPS_AVG]))
	_S["loaded"] = False
	_S["base"] = {}
	_S["ref"] = {}
	return total


def replay(days=14, every_h=6, key=None):
	"""READ-ONLY. The analysis every 'every_h' hours over the stored windows of the last 'days' (the baseline as it stood
	then, worked out every BASE_EVERY_MS): what each pump would have shown. Run backfill() first."""
	_init()
	now = _now()
	t0 = now - int(days * DAY_MS)
	step = int(every_h * 3600000)
	print "forensics.hydPump v%s  replay %d days every %d h  %s  READ-ONLY" % (SCRIPT_VERSION, days, every_h, _fmt(now, "EEE d MMM HH:mm"))
	spans, snote = _spans(t0 - (BASE_DAYS + 1) * DAY_MS, now + W_MS)
	if snote:
		print "  note: %s" % snote
	try:
		refs = _ref_rows()
	except (Exception, Throwable):
		refs = {}
	saved = dict(_S.get("band") or {})
	for p in PUMPS:
		if key is not None and p[0] != key:
			continue
		_S["band"] = {}
		allw = _load(t0 - (BASE_DAYS + 1) * DAY_MS, now + W_MS, p[0])[p[0]]
		ks = sorted(allw.keys())
		prun = _prun(allw)
		# the judged windows of the whole stretch once; each baseline is a slice of them
		J, skip = _judged(allw, spans, prun, t0 - BASE_DAYS * DAY_MS, now + W_MS)
		ws = [j[0] for j in J]
		ref = None
		ra, rb, rnote = _ref_span(p[0], refs.get(p[0]))
		if ra is not None:
			rw = _load(ra - (SETTLE_W + 1) * W_MS, rb, p[0])[p[0]]
			rj, x = _judged(rw, _spans(ra - DAY_MS, rb)[0], _prun(rw), ra, rb)
			ref = _stats(rj, ra, rb)
		print ""
		print "%s  (%d windows stored, %d judged; reference %s)" % (p[4], len(allw), len(J), ("%s - %s, n %d, used from %s" % (_fmt(ra, "d MMM"),
			_fmt(rb, "d MMM"), ref["n"], _fmt(rb + LONG_GAP_DAYS * DAY_MS, "d MMM"))) if ref else "none")
		bands = {}
		e = t0 - t0 % step + step
		base = None
		base_at = None
		while e <= now:
			if base_at is None or e - base_at >= BASE_EVERY_MS:
				b0, b1 = _base_span(e, refs.get(p[0]))
				base = _stats(J[bisect.bisect_left(ws, b0):bisect.bisect_left(ws, b1)], b0, b1)
				base_at = e
			use_ref = ref if (ref is not None and ref["to"] <= e - LONG_GAP_DAYS * DAY_MS) else None
			i0 = bisect.bisect_left(ks, e - KEEP_DAYS * DAY_MS)
			i1 = bisect.bisect_right(ks, e - W_MS)
			recent = dict((w, allw[w]) for w in ks[i0:i1])
			r = analyse(p[0], recent, base, use_ref, spans, None, e)
			bands[r.get("band", -1)] = bands.get(r.get("band", -1), 0) + 1
			if r.get("band", -1) >= 1 or r.get("st") not in ("ok", "standby"):
				print "  %s  %s" % (_fmt(e, "EEE dd MMM HH:mm"), _line(r)[35:])
			e += step
		tot = float(sum(bands.values())) or 1.0
		print "  share: normal %d %%  watch %d %%  hot %d %%  not judged %d %%   (normal and standby passes not listed)" % (
			100 * bands.get(0, 0) / tot, 100 * bands.get(1, 0) / tot, 100 * bands.get(2, 0) / tot, 100 * bands.get(-1, 0) / tot)
		print "  baseline at the end: %s" % _bline(base)
	_S["band"] = saved
	return None


def status():
	"""READ-ONLY. What the Hydraulics rows and the cards show now."""
	s = state()
	print "forensics.hydPump v%s  results of %s  last error: %s" % (SCRIPT_VERSION, _fmt(s["ts"], "HH:mm:ss") if s["ts"] else "never", s.get("error") or "none")
	for p in PUMPS:
		r = s["pumps"].get(p[0])
		print "  " + (_line(r) if r else "%-34s no result yet" % p[4])
	for a in AREAS:
		row, assets = rows(a)
		print "  %-9s %s  [%s]" % (a, (row or {}).get("v"), (row or {}).get("i"))
	for c in sorted(CARD_PUMPS.keys()):
		x = card(c)
		print "  card %-4s %-9s %s  (svg %d chars)" % (c, x.get("badge"), x.get("sub"), len(x.get("svg") or ""))
	return None


def trend(key=None):
	"""READ-ONLY. Per pump and month: judged windows, median running pressure, dip depth and temperature over its
	reference - wear since the sensors went in."""
	_init()
	now = _now()
	print "forensics.hydPump v%s  trend  %s  READ-ONLY" % (SCRIPT_VERSION, _fmt(now, "EEE d MMM HH:mm"))
	ds = system.db.runQuery("SELECT min(win_start) FROM hydraulics.pump_window", DB)
	first = _ms(ds.getValueAt(0, 0)) if ds.getRowCount() else None
	if first is None:
		print "  no windows stored - run backfill() first"
		return None
	spans, snote = _spans(first, now + W_MS)
	for p in PUMPS:
		if key is not None and p[0] != key:
			continue
		allw = _load(first, now + W_MS, p[0])[p[0]]
		J, skip = _judged(allw, spans, _prun(allw), first, now + W_MS)
		by = {}
		for j in J:
			by.setdefault(_fmt(j[0], "yyyy-MM"), []).append(j)
		print ""
		print "%s" % p[4]
		for m in sorted(by.keys()):
			x = by[m]
			tv = [j[3] for j in x if j[3] is not None]
			dv = [j[2] for j in x if j[2] is not None]
			print "  %s  n %4d  P %6.1f  D %s  T %s" % (m, len(x), _med([j[1] for j in x]), ("%5.1f" % _med(dv)) if dv else "  -- ",
				("%+5.1f" % _med(tv)) if tv else "  -- ")
	return None


def set_reference(key, date_from, date_to=None, note=""):
	"""The long reference period for one pump (after a pump change): dates as 'yyyy-MM-dd'. date_from None clears it -
	the reference goes back to the pump's first REF_RUN_N windows of running at pressure. Writes hydraulics.pump_ref."""
	p = _pump(key)
	if p is None:
		print "no pump %s - one of: %s" % (key, ", ".join([x[0] for x in PUMPS]))
		return None
	note = _a(note)[:200]
	if date_from is None:
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
			date_from, date_to or ("+%d days" % REF_DAYS), (" (%s)" % note) if note else "", LONG_GAP_DAYS)
	_init()
	_S["ref"] = {}
	return None


# ------------------------------------------------------------------------------------------------ rebase (1.0.5)
# After pressure transmitters were swapped between pumps (or a pump was changed) the long check reads the step as wear.
# rebase() finds the pumps whose level moved and gives each that stepped a reference from the day after its step.
MOVE_P = 8.0          # bar - running pressure this far from the reference has moved (the long check's WATCH size)
MOVE_T = 4.0          # degC - the same for the temperature over its tank
NOW_DAYS = 14         # "now" in rebase(): the judged windows of the last NOW_DAYS days
DAY_MIN_N = 16        # a day counts in the step search with 4 h of steady running
STEP_SHARP = 0.6      # a step: this share of the move or more between the week before the day and the week from it
REBASE_NOTE = "sensor swap or pump change - its level since the step (rebase)"
BAND_TXT = {-1: "--", 0: "NORMAL", 1: "WATCH", 2: "HOT"}


def _pday(day):
	"""Local midnight of a 'yyyy-MM-dd' day, ms."""
	return long(system.date.parse(day, "yyyy-MM-dd").getTime())


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


def rebase(dry=True, force=None, skip=None):
	"""Console, after pressure transmitters were swapped between pumps (or a pump was changed). Every pump against its
	long reference: its running pressure by month, its reference, its 8 weeks, its last NOW_DAYS days, the day its level
	moved and what its card shows - now and rebased. A pump that moved MOVE_P bar or MOVE_T degC or more, either way (a
	swapped sensor can read high or low), in a step gets a new reference from the day after the step, REF_DAYS long (to
	today at most): its level since the step as its normal. A slow drift is listed and left alone - it may be wear.
	rebase() prints only. rebase(False) writes the references (set_reference); the gateway takes them at its next
	refresh. force / skip: keys or short names ("DB P6") to rebase whatever the check says (no step found: its last
	REF_DAYS days) / never to rebase."""
	_init()
	now = _now()
	today = long(system.date.midnight(Date(long(now))).getTime())
	fk, fbad = _rb_keys(force)
	sk, sbad = _rb_keys(skip)
	print "forensics.hydPump v%s  rebase  %s  %s" % (SCRIPT_VERSION, _fmt(now, "EEE d MMM HH:mm"),
		"DRY RUN - nothing written" if dry else "LIVE - writes the new references")
	print "  moved = the last %d days %.0f bar or %.0f degC or more from the reference, either way; step = most of it across one day" % (
		NOW_DAYS, MOVE_P, MOVE_T)
	if fbad or sbad:
		print "  not pumps: %s - use keys (SDB_U2P2) or short names (DB P6)" % ", ".join(fbad + sbad)
	refs = _ref_rows()
	ds = system.db.runQuery("SELECT min(win_start) FROM hydraulics.pump_window WHERE %s" % RUNNING_SQL, DB)
	first = _ms(ds.getValueAt(0, 0)) if ds.getRowCount() and ds.getValueAt(0, 0) is not None else None
	if first is None:
		print "  no running windows stored - run backfill() first"
		return None
	spans, snote = _spans(first - DAY_MS, now + W_MS)
	if snote:
		print "  note: %s" % snote
	try:
		live = _live()
	except (Exception, Throwable):
		live = {}
	plan, drift, steps = [], [], []
	saved = dict(_S.get("band") or {})
	try:
		for p in PUMPS:
			key, label, short = p[0], p[4], p[5]
			print ""
			f = _first_window(key)
			if f is None:
				print "%-7s %s - never ran at pressure in the table" % (short, label)
				continue
			wins = _load(f - (SETTLE_W + 1) * W_MS, None, key)[key]
			J, x = _judged(wins, spans, _prun(wins), f, now + W_MS)
			man = refs.get(key)
			ra, rb, rnote = _ref_span(key, man)
			ref = _stats([j for j in J if ra <= j[0] < rb], ra, rb) if ra is not None else None
			ref_ok = ref is not None and ref["n"] >= REF_MIN_N
			ref_used = ref_ok and rb <= now - LONG_GAP_DAYS * DAY_MS
			b0, b1 = _base_span(now, man)
			base = _stats([j for j in J if b0 <= j[0] < b1], b0, b1)
			cur = _stats([j for j in J if j[0] >= now - NOW_DAYS * DAY_MS], now - NOW_DAYS * DAY_MS, now)
			recent = dict((w, r) for w, r in wins.items() if w >= now - KEEP_DAYS * DAY_MS - W_MS)
			_S["band"] = {}
			r0 = analyse(key, recent, base, ref if ref_used else None, spans, live.get(key), now)
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
							steps.append((s[0], short, "%s %+.1f" % (nm, s[2] - s[1])))
				print "        moved       %s" % mv
			elif not ref_ok:
				print "        moved       - no reference to judge it against yet"
			else:
				print "        moved       - too little steady running in the last %d days (n %d)" % (NOW_DAYS, cur["n"])
			sharp = [s for s in (sP, sT) if s is not None and s[3]]
			a = None
			if key in sk:
				print "        card        %s  (skipped)" % _rb_verdict(r0)
				continue
			if sharp:
				a = _pday(max([s[0] for s in sharp])) + DAY_MS
			elif key in fk:
				a = today - REF_DAYS * DAY_MS
			elif movedP or movedT:
				drift.append(short)
				print "        card        %s  - DRIFT: moved slowly, not rebased (it may be wear)" % _rb_verdict(r0)
				continue
			else:
				print "        card        %s" % _rb_verdict(r0)
				continue
			b = min(a + REF_DAYS * DAY_MS, today)
			nj = [j for j in J if a <= j[0] < b]
			if b <= a or len(nj) < REF_MIN_N:
				print "        card        %s  - too little running since the step to rebase (%d windows of %d) - run again in a few days" % (
					_rb_verdict(r0), len(nj), REF_MIN_N)
				continue
			new = _stats(nj, a, b)
			new_used = b <= now - LONG_GAP_DAYS * DAY_MS
			man2 = (a, b, REBASE_NOTE, None)
			nb0, nb1 = _base_span(now, man2)
			nbase = _stats([j for j in J if nb0 <= j[0] < nb1], nb0, nb1)
			_S["band"] = {}
			r1 = analyse(key, recent, nbase, new if new_used else None, spans, live.get(key), now)
			plan.append((key, short, a, b))
			print "        new ref     %s to %s  n %4d  P %s  T %s  - %s; 8 weeks %s" % (_fmt(a, "d MMM"), _fmt(b, "d MMM"), new["n"],
				_n(new["P"]["med"]), _n(new["T"]["med"], "%+.1f"), "in use at once" if new_used else "long check from %s" % _fmt(
				b + LONG_GAP_DAYS * DAY_MS, "d MMM"), ("from %s" % _fmt(nb0, "d MMM")) if nb0 > now - BASE_DAYS * DAY_MS else "as before")
			print "        card        now %s  ->  rebased %s" % (_rb_verdict(r0), _rb_verdict(r1))
	finally:
		_S["band"] = saved
	print ""
	print "SUMMARY"
	print "  rebase: %s" % (", ".join(["%s from %s" % (s, _fmt(a, "d MMM")) for k, s, a, b in plan]) or "none")
	print "  drift - moved slowly, left alone (may be wear; force=[...] to rebase): %s" % (", ".join(drift) or "none")
	if steps:
		print "  steps by day (a swap between two pumps steps both the same day):"
		for d in sorted(set([x[0] for x in steps])):
			print "    %s  %s" % (_fmt(_pday(d), "EEE d MMM yyyy"), ", ".join(["%s %s" % (x[1], x[2]) for x in steps if x[0] == d]))
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
