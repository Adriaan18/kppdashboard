# DashboardandPLC Raw Log - 2026-10-28 A

**Version:** 1.0.0 - **Author:** Adriaan - **Layer:** RAW - append-only, never rewritten
**Session:** one chat, Wed 28 Oct 2026 from 15:12 (NZDT); lettered A - no 2026-10-28 log was in the project.
Two asks: (1) a 30-day history of the HMI alarms on the new booth HMIs (`Application/Booth`), so the crews can see what
the alarm was when a reset was done, and readable by the AI box; (2) RESET ALL IGs as one press ("hold the reset for
3.5 s then again for 0.2 s") on the Diag view cards and on the new Safety Diagnostics popup, a button on the Diag view
CardsRow to the popup, and the card's open button to the popup instead of the old Tui pages.
**Sources:** the export `MainSCADA_Timberlands_2026-10-28_1422_1.zip`; the controller export `KPP_COS_V20T.L5K`
(exported Tue 27 Oct 20:34:43, 1756-L84ES, v35, safety locked); two screenshots (the Safety Diagnostics popup on COS at
15:05, the Diag view header and cards).
**Run on the gateway:** nothing. Tested off the gateway (section 8).
**Design of record:** this log.

---

## 1. Scope (NZDT, Wed 28 Oct)

- **15:12** - the two asks above, the L5K and the export attached.

## 2. Findings

- **The HMI reset in the safety PLC** (every `<AREA>_IG<n>` routine, e.g. `_101_COS_IG1`):
  - rung "GROUP RESET BUTTON": `GroupResetONS` = the FALLING edge of any of the group's reset buttons (ONS on XIO),
    blocked while `FaultResetPulse` is on;
  - rung "GROUP FAULT RESET": any reset button held -> `tFaultResetTON` (PRE 3000 on every group) -> ONS -> TOF
    `tFaultResetPulse` -> `FaultResetPulse`, which unlatches `GroupFaultActive` and (through `AllGroupFaultReset`)
    resets the area's DCS / solenoid / pressure device faults;
  - `GroupEn` = ((GroupResetONS AND AllFeedbacksOk) OR GroupEn) AND AllInputsOk AND channels OK AND NOT
    GroupFaultActive - a reset cannot pass an open gate, an activated isolator or a pressed E-stop; gates with
    `ResetRequired` clear only at their own local reset button;
  - the HMI bit is `<X>_ToSafetyMap.<X>_HMI_RB` (standard, safety tag map -> `<X>_SafetyMap`); the standard routine
    `_099_HMI_RB_Timeout` clears it after 5 s; safety task 50 ms;
  - **`tFaultResetPulse.PRE` is 500 ms on every group except Grading - GRA_IG1-3 2000 ms.** A tap inside the pulse is
    ignored, so the asked "3.5 s then 0.2 s" with a fixed short gap loses the Grading group reset - modelled: 61 of
    100 presses lost with a 1.0 s gap;
  - **what each HMI reset reaches** (the rungs): SDB IG1-4; GRA IG1-3; COS IG1-2 + TNB IG1-5 + CHP IG7; TNB IG1-5;
    CHP IG1-7; HOG IG1-5. DDB has no HMI reset (DDB_IG1/2 only, no HMI_RB) - monitoring only;
  - **PLC defect (not touched, safety locked): `_102_COS_IG2` uses `ONSAux[0].7` for two branches** of its
    GroupResetONS rung (`COS_SafetyMap.COS_HMI_RB` and `CHP_SafetyMap.CHP_RB_08`). The two ONS instructions overwrite
    each other's storage bit, so COS IG2 (Winch ropes) gets a group reset on EVERY scan while either button is HELD
    (modelled: 21 reset scans in a 1 s hold; COS IG1 one, on release) - a level reset where the design is a release
    edge, and a held or stuck Chip Back Entrance button resets COS IG2 continuously. The only shared ONS bit in the
    safety programs. Fix when the safety program is next unlocked: give one of the two ONS a spare `ONSAux` bit.
- **The HMI alarms** on the new booths are Ignition alarms in `ia.display.alarmstatustable` (AlarmPanel and the
  Alarms popup), filtered by display path per booth: SDB `SDB,HOG`, GRA `GRA, SeqDeck`, COS
  `COS,TnB,Sortline,PulpDeck,T&B`, T&B `T&B,Sortline,PulpDeck,TnB`; the Sortline booth has no alarm panel. The booth
  tables cannot acknowledge (no toolbar, selection off). An alarm journal exists on the gateway (`queryJournal` is used
  by `forensics.kickerHeat` and `forensics.sortDiag`) - not used here: a purpose-built table keeps 30 days under
  `shared.purge` and is plain for the AI box.
- The old press-and-hold HMI reset buttons write the same bits and stay (unchanged): MapCards SDB / GRA / COS / TNB /
  CHP / HOG (mouse down True; mouse up AND mouse leave False - a hover-out writes False even without a press) and the
  Zone view (down / up).

## 3. Built (not installed)

- **`booth.safetyreset` 1.0.0** (new, `booth` package): `press(area, who, station)` runs on a gateway thread - hold
  3.5 s, release, wait until 3.0 s + the area's pulse + 0.8 s after the hold began (gap GRA 2.3 s, the rest 1.0 s),
  tap 0.2 s, release, read the groups back at 1.2 s (and 1 s later if any is not energized). Guards: one sequence per
  area (lock in `system.util.globals`, taken over only when 2 min old; tag reads 2 s and writes 3 s time out, so a
  sequence cannot outlive its lock); refused when the bit is already on (held from another screen) and for DDB; a True
  is written once, never retried, and every way out writes False - also when the True write came back Bad; the hold
  is watched every 250 ms and abandoned (FAILED, "another screen released the reset") when another screen writes the
  bit False. `state(area)` feeds the buttons (FAULT RESET n s, GROUP RESET IN n s, CHECKING, RESET DONE green, RESET
  SENT orange with what is still off, RESET FAILED red; 12 s, then the last result as a note; card fields `cls`,
  `cardBg`, `cardFg` for the dark Diag cards). `recent(ig)` names the HMI user to the history. Each press is one
  history row stamped at the press. `check()` - read only.
- **`forensics.alarmHistory` 1.0.0** (new): table `alarm.hmi_history` (+ `alarm.engine_status` heartbeat, view
  `alarm.v_history` with NZ local times, a COMMENT on every column for the AI box). Kinds: `alarm` (one row per
  Ignition alarm occurrence: active time and value, cleared, acknowledged and by whom; `clear_est` when the clear was
  seen late), `safety` (IG ENERGIZED = a reset was done, DE-ENERGIZED, FAULT, FAULT CLEARED, ISOLATED, ISOLATION OFF -
  with the why from `booth.safety` and the HMI user when an HMI reset did it), `reset`, `msgack`. Timer
  `AlarmHistory_FixedDelay` 1000 ms: one `queryStatus` diffed by event id, one read of the IG flags, the database only
  on change (200 rows a statement), a heartbeat a minute. An alarm gone from the status list is closed after 3 polls
  without it, at the first poll that missed it; a row closed by estimate takes the alarm's state again if it comes
  back (reopened, or its real clear time). After a restart the open occurrences not in the status list are closed
  2 min after the start (clear time = engine start, detail says so). A row the database refuses is left out and
  logged, the rest written; with the database down the engine keeps its state and writes on return. NUL characters
  removed; each distinct error logged once a minute. Alarms active more than 30 days ago are followed in memory, not
  written. The engine needs only the schema, tables and indexes - the view and the comments never block it. `rows()`
  for the popup, `install()`, `check()`.
- **`shared.purge` 1.2.0**: job "HMI alarm history" - `alarm.hmi_history`, keep 30 days.
- **Views:** Booth Alarms popup 1.1.0 (ACTIVE / HISTORY - 30 DAYS tabs; range 1 h - 30 days, ALL / ALARMS / SAFETY +
  RESETS, search; reads only while the tab is open, every 15 s), AlarmPanel 1.3.0 ("All alarms + 30-day history"),
  MessageAckButton 1.1.0 (each press into the history), SafetyDiag popup 1.2.0 (RESET ALL IGs block under the
  groups), AreaSafetyCard 1.5.0 (one-press reset as a tap target - container + label like the open button, class
  bound to the state: glass gold idle, solid amber running, green done, orange partial, red failed, grey DDB; the open
  button opens the popup on its area), SafetyPlantOverview 1.25.0 (SAFETY DIAGNOSTICS tile at the end of the CardsRow
  - opens on the area that needs attention most). Key order as Ignition writes it (sorted) - the writer reproduces the
  AreaSafetyCard and SafetyPlantOverview exports byte for byte, so only the changes differ.

## 4. Decisions

1. One press, no PLC change: the sequence runs on the gateway against the existing HMI reset bits; the PLC's 5 s
   timeout stays the stuck-bit guard.
2. Hold 3.5 s as asked; the gap is per area from the PLC's own pulse presets (Grading 2 s).
3. A press always does the 3 s fault reset first - the same as holding the button; a fault still present re-latches
   and the read-back says so.
4. Reset available from the same places as before (no role gate - the old buttons had none); every press is logged
   with the user and the screen.
5. Alarm history in its own table (not the alarm journal), 30 days under `shared.purge`, IG changes and HMI presses in
   the same timeline.
6. The Diag card reset answers a tap or a click only - not a keyboard Enter / Space on a focused button.

## 5. Rules banked - staged, not compiled

For `KPP_Platform_Rules`:
1. GuardLogix group reset here is two actions on one bit: hold >= tFaultResetTON for the fault reset, then a release
   edge outside the TOF fault-reset pulse for the group reset. Read every group's pulse preset before timing a
   sequence (Grading 2000 ms, the rest 500 ms).
2. Two ONS instructions sharing a storage bit turn an edge into a level: each overwrites the other's bit every scan.
   Scan a program for duplicate ONS operands before trusting an edge.
3. `system.util.globals` holds state for the JVM's life (survives a project save) - locks and engine state for
   gateway threads live there, keyed by version; create entries with setdefault.
4. A gateway sequence that writes a PLC bit True: write the True once (a retry can add an edge), mark it written
   BEFORE the write (a Bad result can still have reached the PLC), write False on every way out, bound every tag
   call with a timeout, and never take over a lock a live thread can still hold.
5. The glass button classes (`gbtn`, `gbtn-gold`, ...) set background, colour and border `!important` - a state
   colour needs the class bound off, not an inline colour on top.
6. An alarm missing from one `queryStatus` poll has not ended: confirm over a few polls, and let a row closed by
   estimate be reopened by the alarm's own state.

For `KPP_Domain_Data_Reference`:
7. `alarm.hmi_history` / `alarm.v_history` / `alarm.engine_status` (columns in the database comments); HMI reset
   reach per area (section 2).

## 6. Open

1. Install (section 9) and a first live press at a controlled moment on one area; confirm the history fills.
2. The `_102_COS_IG2` shared `ONSAux[0].7` - for the next safety unlock (Kenny / the safety integrator).
3. The old MapCards / Zone press-and-hold reset buttons - leave, or point them at `booth.safetyreset`.
4. A read-only database login for the AI box on `alarm.*`.
5. Knowledge Index 1.60.0 drafted, not written - the project knowledge is at 1.915 of 2 MB; old index copies
   (v1_53_0 - v1_58_0) to delete first.

## 7. Corrections and mistakes

- None after delivery. In design: the asked fixed timing was checked against the L5K before building and changed to
  a per-area gap (Grading pulse 2 s).
- Before delivery an independent review found 11 issues, all fixed and re-tested: a lock could be taken over while
  its thread was still writing (30 s stale, no tag timeouts); one missed poll or a restart closed occurrences that
  were still active; a True write that came back Bad was not followed by False; an old screen releasing the bit
  mid-hold went unnoticed; views pasted over existing ones merge by position (install into empty views); the glass
  class hid the card's result colours; a focused card button reset on Enter / Space; `who` None was logged as
  "None"; the reset row carried the end time, not the press; one bad row stopped the engine; alarms older than 30
  days were written and purged again every night.

## 8. Proof before delivery

- Python 2.7 grammar check of every library and every new view script; no f-strings or other 3-only syntax; ASCII
  only in everything written here (two characters already in SafetyPlantOverview left as they were); no em or en
  dash.
- A scan model of the reset rungs parsed from the L5K (ONS storage bits as written - the shared bit included -, TON
  3000, TOF per group, device-fault latch, 50 ms safety task, the 5 s HMI timeout) driven by the real library through
  a stand-in for `system.*` with random write latency: one press per area with faults, isolators and gates mixed -
  every group that could reset did, isolated / gated / faulted ones did not and were named; 900 random presses
  (latency 5 - 400 ms) - 0 lost; with a fixed 1.0 s gap Grading lost 61 of 100; guards: bit held elsewhere, write
  failure, DDB, a 60 s lock busy, a 130 s lock taken over; review cases: another screen releasing mid-hold -
  abandoned at 1.8 s with one True write; a True write reaching the PLC but reporting Bad - bit False, no retry, no
  PLC timeout; `who` None -> "no login"; the history row stamped at the press; card colours per state (amber, red at
  once while the last False writes run, green).
- The history engine against PostgreSQL 16 (local): 1,500 alarms in status (500 cleared, 750 acknowledged) - first
  tick 41 statements (25 schema, 8 inserts, 7 updates, 1 heartbeat), 300 clearing at once 2 statements (one per alarm
  before batching); install 25 statements; alarm active / ack / clear
  / gone between polls (closed only on the 3rd missed poll, at the 1st) / a 2-poll blip not closed / reopened when it
  came back / a real clear over an estimate / first seen cleared; a row refused by a CHECK constraint left out while
  its neighbours were written, no retry, engine not in error; a NUL in a label removed; database down 3 ticks -
  alarm and IG change written on return; restart - nothing closed in the first 2 min, then closed at the engine
  start, an alarm still active over the restart kept open, no duplicates; IG edges with the why and the HMI user;
  `rows()` for each booth filter, mode and search; `check()`; `shared.purge` 1.2.0 dry and live (31-day row gone,
  29-day kept).
- Every new view expression balanced and pointing at declared props; every event script scope G; the scripts run in
  the stand-in (tabs, chips, history transform, MESSAGE ACK logging, popup and card presses, the card reset as a tap
  target with its class bound, the Diag tile opening on the faulted area).

## 9. Deliverables (final versions)

- `booth_safetyreset_v1_0_0.py` -> `booth/safetyreset` [new]
- `forensics_alarmHistory_v1_0_0.py` -> `forensics/alarmHistory` [new]
- `shared_purge_v1_2_0.py` -> `shared/purge` [1.1.0]
- `BoothAlarmsPopup_view_v1_1_0.json` -> `Application/Booth/Popups/Alarms` [1.0.0]
- `BoothAlarmPanel_view_v1_3_0.json` -> `Application/Booth/Components/AlarmPanel` [1.2.0]
- `BoothMessageAckButton_view_v1_1_0.json` -> `Application/Booth/Components/MessageAckButton` [1.0.1]
- `BoothSafetyDiag_view_v1_2_0.json` -> `Application/Booth/Popups/SafetyDiag` [1.1.0]
- `AreaSafetyCard_view_v1_5_0.json` -> `Application/Safety/Components/AreaSafetyCard` [1.4.1]
- `SafetyPlantOverview_view_v1_25_0.json` -> `Application/Safety/SafetyPlantOverview` [1.24.1]
- Gateway timer `AlarmHistory_FixedDelay` (fixed delay 1000 ms, dedicated thread): `forensics.alarmHistory.tick()`
- This log.
