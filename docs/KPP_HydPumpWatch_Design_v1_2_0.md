# KPP Hydraulic PUMP WATCH - Design

**Version:** 1.2.0 - **Date:** 2026-10-28 - **Author:** Adriaan
**Status:** built 28 Oct, not installed: `forensics.hydPump` 1.0.5 (rebase after a sensor swap, references taken at the
next refresh, the 8-week baseline from a hand-set reference). On site: 1.0.4 with `HydraulicsDiagnosticsCard` 1.7.0 and
its popup `HydPumpWatchDetail` 1.0.0 (19 Oct). Owner of `forensics.hydPump` and the tables `hydraulics.pump_window`,
`hydraulics.pump_band`, `hydraulics.pump_ref`.
**Siblings:** `forensics.hydLeak` (tank LEAK WATCH - the oil level), `forensics.hyddiag` 1.4.0 (pump status, the pump
popups' diagnostics), `forensics.anomalyWatch` 1.15.0 (the Hydraulics row), view `HydraulicsDiagnosticsCard` 1.7.0 (the
HydPanel cards) and its popup `HydPumpWatchDetail` 1.0.0, `SafetyPlantOverview` 1.23.0.
**Session record:** `DashboardandPLC_Raw_Log_2026-10-17_A` (17 - 19 Oct 2026); `DashboardandPLC_Raw_Log_2026-10-28_A`
1.1.0 (28 Oct - the transmitter swap, 1.0.5).

History
- 1.2.0 2026-10-28 - 1.0.5: pressure transmitters were swapped between pumps (Adriaan, 28 Oct) - the DB P6 and GRA P1
  steps (section 12) are swaps, not wear. `rebase()` (section 15) checks every pump against its reference and gives
  each one that stepped a new reference from the day after its step; a reference set or cleared by hand is taken at the
  gateway's next refresh (its cached reference and baseline dropped, a held band let go); the 8-week baseline starts at
  a hand-set reference when that is inside it (section 5).
- 1.1.0 2026-10-19 - on site: the pump map as found (1.0.1), short names (1.0.2), the long reference from each pump's
  first running windows, Big John (TNB P1) and "runs, no pressure" (1.0.3), the DETAILS popup (1.0.4); the sensors (ifm
  PV8000) and the IO-Link masters; the references as found and the first findings (section 12); CORRECTION -
  `hydraulics.pump_events` holds no start / stop event, so it is no run-state source (1.0.0 said "every 60 s since
  23 Jul").
- 1.0.0 2026-10-18 - first issue, built and tested off the gateway.

---

## 1. Why

Each of the 18 sensored hydraulic pumps (17 from 1.0.0; the Big John crane's power pack from 1.0.3) has an ifm PV8000 at
the pump - one IO-Link sensor for pressure (bar) and temperature (degC) - on line since April (9 Apr Grading, 16 Apr the
rest). The PLC (`HydraulicPumpProtections`) trips on fixed limits - for COS HydUnit1 Pump 1 high alarm 250 bar / 75 degC,
low alarm 50 bar. A pump that starts leaking stays well inside those limits for weeks. PUMP WATCH learns each pump's own
normal from the historian and says when it moves away from it.

**What a leaking pump looks like on these two sensors** (research, section 14):

| Leak | Pressure at the pump | Temperature at the pump |
|---|---|---|
| Internal (worn pistons / vanes / valve plate, compensator) - the slow one | the running level sags; dips under load get deeper and recover slower (the pump cannot make up the flow it loses inside) | rises against the oil it draws: oil forced across a pressure drop without doing work turns to heat (about 0.06 degC per bar of drop, so oil leaking from 115 bar to case comes back about 7 degC warmer); field rule: pump housing more than 10 degC over the reservoir is a warning, 20-25 degC a rebuild |
| External at the pump (seal, fitting, hose) | sags if the loss is large; dips deeper | little change; the tank level falls - LEAK WATCH sees it |
| Sensor | flat line, out of range, no data | the same |

Both sources say the same thing about limits: case drain flow and temperature vary by pump, so take the baseline when the
pump is known good and judge the change against it - which is what this does.

## 2. Pumps and signals

House-tree pump folders `KPP/<area>/.../Hydraulic Stations/<unit>/Pumps/Pump <n>` as found on site (1.0.1); short names
by area (1.0.2).

| Card | Pumps (short name - label) | PLC | Temperature reference |
|---|---|---|---|
| SDB | DB P1 - P4 (Debarker Pump 1 - 4, HydUnit1); DB P5 - P6 (Debarker Pump 5 / 6 (HydUnit2 Pump 1 / 2) - in the house tree's HydUnit1 folder as Pump 5 - 6) | `SDB_General.HydraulicPumps[1]` - `[6]` | HydUnit1 tank; HydUnit2 has none - its two pumps against each other (peer) |
| GRA | GRA P1 (Grading Pump 1 (drive)); GRA P2 - P3 (cylinder) | `GRA_General.HydraulicPumps[1]` - `[3]` | HydUnit1 tank |
| COS | COS1 P1 - P3 (HydUnit1); COS3 P1 - P2 (HydUnit3) | `COS_Area.HydUnit1_Pumps[1]` - `[3]`, `HydUnit3_Pumps[1]` - `[2]` | HydUnit1 and HydUnit3 tanks |
| TNB | TNB P1 (the Big John crane's power pack, HydUnit4 Pump 1); TNB P2 (T&B Pump 2 (star loader)); TNB P3 - P4 | `TnB_Area.Pumps[0]` - `[3]` | HydUnit4 tank |

- The T&B station folder numbers its pumps 1 - 3 by the PLC array: its Pump 1 is `Pumps[1]` = physical pump 2 (the star
  loader), Pump 2 = physical 3, Pump 3 = physical 4. `Pumps[0]` - Big John - is in no station folder: its own tags
  `KPP/TnB/Devices/Pumps/HydUnit4Pump1` (`KPP_HydPump_BigJohn_Tags` 1.0.0, 19 Oct) - `Status/Pressure`,
  `Status/Temperature`, `Motor/Status/Running` (`Program:Chippers.MCC.HydUnit4Pump1`), `Setpoints/SensorBypass` (no
  history).
- **Big John's pressure:** `TnB_Area.Pumps[0].Status` is never written - its PV8000 is read into `Pumps[0].PV8000` only
  (no `HydraulicPump` AOI runs for it). Until the two tags point at `TnB_Area.Pumps[0].PV8000.Pressure` / `.Temperature`
  (or a PLC rung `Map_PV8_To_Pump_Status(BigJohn_MapPV8,TnB_Area.Pumps[0].PV8000,TnB_Area.Pumps[0].Status)` fills its
  status), TNB P1 reads "runs, no pressure".
- Per pump: `Status/Pressure`, `Status/Temperature` (the popup trends them from the historian), `Motor/Status/Running`
  (the motor's run state - not `Status/Running`, which is a flow bit). Anomaly Watch areas: DEBARKER = SDB, GRADING =
  GRA, COS = COS and T&B (as the tank watch).

**Sensors** (`KPP_COS_V20p`): each pump an ifm PV8000 (PV-400-SEG14-UFRVG/US/ /: 0 - 400 bar; temperature -40 to 90 degC,
+-2 K; G 1/4 male, DIN EN ISO 1179-2; M12; IO-Link device 1214) on an ifm AL1920 IO-Link master - COS1 ports 3 - 7,
COS2 ports 2 - 5, Debarker ports 3 - 8, Grading ports 3 - 5. ifm's AOI `PV8_8PORT_IOL` scales word 0 by 0.1 bar (device
1214) and word 2 by 0.01 degC into each pump's `PV8000` member; `Map_PV8_To_Pump_Status`, inside the `HydraulicPump`
AOI, copies them and the sensor fault bits into its `Status`. The five tank temperatures come from HYDAC level and
temperature sensors (vendor 348, device 925150) on port 1 of each master (and COS1 port 2).

**Running** (a window counts as running only under pressure):
- with a run state - the historian's `Motor/Status/Running` (time share in the window): the pump ran at least 95 % of the
  window AND its pressure stayed over 10 bar all window. A run state left stale or a pump running unloaded is not judged.
  `hydraulics.pump_events` (the hyddiag start / stop capture) was to be the fallback where a run state is not historised
  - it holds no start / stop event (`check()` 18 and 19 Oct; the capture's error handler calls a function that does not
  exist), and every pump's Running is in the history, so no pump uses it;
- with none, its lowest pressure in the window stayed over 40 % of its usual running pressure (the 90th percentile).
`check()` says which source each pump uses (on site: the tag for all 18). For standby against measuring a pump counts as
running in a window when its run state shows any running and its pressure came up in it - a pump that runs on and off
reads "measuring ... it runs on and off", not "not running".

**Sensor bypassed:** a pump whose sensor protection is bypassed in the PLC (the diagnostics `BypassActive` the pump popup
shows, else `Setpoints/SensorBypass`) is not judged - "sensor bypassed". The diagnostics folder is found by the PLC
reference (`forensics.hyddiag.PUMPS`), not by the faceplate's path numbering (1.0.1).

**Runs, no pressure** (1.0.3): a pump whose motor ran `NOPRESS_N` (4) whole windows of production in the last 2 h while
its pressure stayed under `NOPRESS_P` (1 bar) all that time is not judged - the transmitter not connected or not
reading (TNB P1 since 19 Oct). A pump idling unloaded at a few bar is not caught by it.

## 3. Windows (`hydraulics.pump_window`)

15-minute windows, like LEAK WATCH: three historian reads per chunk for all 18 pumps - time-weighted average (pressure,
temperature, running, the five tank temperatures, plant downtime and smoko), minimum and maximum (pressure,
temperature). Stored: `p_avg p_min p_max t_avg t_min t_max run run_src ref_t ref_src dt sm src`.
`ref_t` is the tank temperature for the window; a unit with a tank sensor is only ever judged against its tank (a window
without the tank temperature has no T - another zero would mix into its normal). Only SDB HydUnit2, which has no tank
sensor, takes the median of its other pumps that ran all the window (by their run share, or with none known, their
pressure never under 10 bar in it). `ref_src` tank / peer / none. Due windows 3 min after they close; one older gap of
the last 3 days filled per refresh; `backfill(days, skip_days, chunk_h)` for history (written to the table only, not
held in the console's memory; it prints the rows and the pumps with a pressure per day). Each path group is read in the
house-tree form (`[TL-KPPWS01-01]...`) or the historian form (`histprov:...:/tag:...`) - whichever answers; a hole in
the history is just a hole (only a motor run state that is in the history in neither form is left out for 6 h); rows
stamped at the end of their interval are moved back one window.

- **The historian returns 0.0, not nothing, for a tag before its first sample.** The pressure tags have history from 16
  Jan with zeros until the sensors came in, so the table holds windows from 21 Jan (the 1.0.1 backfill) - a pump's
  first rows are not its sensor's start (section 5). A backfill from before a tag existed writes zero rows: TNB P1's
  windows start 19 Oct 10:25, with no backfill.
- **Quirk (not fixed):** after a module restart the gap fill re-reads the oldest window of `KEEP_DAYS`
  (`_load(now - KEEP_DAYS * DAY)` is not floored to a window) - harmless (it wrote zero rows for TNB P1 for 16 Oct
  10:15 and 10:30).

## 4. Judged windows

A window is judged when the pump ran all of it and the two windows before it (warm oil), the plant was not in downtime or
on smoko for half of it, it is not in a Shut Plan shift (`forensics.peWatchJudge.shut_spans`) nor within 30 min after a
shut, downtime or smoko, and it has a pressure. Its three numbers:

- **P** running pressure = `p_avg`
- **D** dip depth = `p_avg - p_min` (how far the pressure falls under load inside the window)
- **T** temperature over the oil it works = `t_avg - ref_t` (none when there is no reference)

## 5. Normal - two references

- **Baseline (short):** the judged windows of the last 56 days, ending 2 days ago; per number the median and the spread
  (1.4826 x MAD, at least P 1.0 bar, D 1.5 bar, T 0.5 degC); 96 windows (24 h of steady running) at least, else
  *learning*. Worked out every 6 h (a learning one every 15 min, so a console backfill shows within a window). Catches a
  change over days. **From 1.0.5 it starts at the start of a reference set by hand when that start is inside the 56
  days** - after a sensor swap or a pump change the windows before it are not this pump's normal; the pump learns again
  from its first 96 windows after the change (with the 2-day guard: about 3 days of running).
- **Reference (long)** (1.0.3): from the first window the pump ran at pressure, its first 1,344 judged windows
  (`REF_RUN_N` - about two weeks of running; at least 96), or the period set with `set_reference()` / `rebase()` after a
  pump change or a sensor swap. Used once it ended 42 days before now (`LONG_GAP_DAYS`). Catches slow wear the rolling
  baseline would learn in. 1.0.0 - 1.0.2 took the first 28 days the table holds - 21 Jan to 18 Feb, before the sensors -
  so no reference held a judged window and the two long checks never ran (replay 19 Oct).
- **As found** (replay on 1.0.3, 19 Oct): SDB 16 Apr - 5 May (979 - 987 windows), GRA 9 - 25 Apr, COS 16 Apr - 2 May,
  T&B 16 Apr - 17 Jul (TNB P4 to 3 Jul); each used from about six weeks after it ended. TNB P1: none until it has run
  two weeks with a pressure.
- **`set_reference(key, from, to, note)`** after a pump change or a deliberate duty change (`hydraulics.pump_ref`;
  dates `yyyy-MM-dd`, `to` exclusive, default from + 28 days; `to` must be after `from` - 1.0.5). **From 1.0.5 the
  gateway reads the references every refresh and takes a new or cleared one at once**: the pump's cached reference and
  baseline go and a band it holds is let go, so it is judged afresh within 15 min - no library save (1.0.4 read them
  every 24 h and kept a held band up to 6 h more). At the first refresh after a reload a held band last confirmed before
  the pump's reference row was written (`pump_ref.updated`) goes the same way. A failed reference read keeps the last
  references (1.0.4: none for that refresh - the April ones).

**Recent:** the median of the judged windows of the last 12 h; 16 at least (4 h of running), else *standby* (not run in
the last 2 h) or *measuring*.

## 6. Checks (each 0-100 on the Anomaly Watch scale)

A check scores on the smaller of its significance (z = change / spread: 2 -> 0, 3.5 -> WATCH 60, 5 -> HOT 80) and its size
(absolute: ref -> 0, watch -> 60, hot -> 80) - a shift must be both real and big enough to matter. Only the bad direction
counts (a pump running cooler or at a higher pressure is not raised).

| Check | Change | Size ref / WATCH / HOT | Row / card text |
|---|---|---|---|
| PRESSURE LOW (short) | baseline P - recent P | 2 / 5 / 10 bar | pressure -8 bar |
| DIPS DEEPER (short) | recent D - baseline D | 3 / 8 / 15 bar | dips 9 bar deeper |
| RUNS HOTTER (short) | recent T - baseline T | 1 / 3 / 6 degC | 6.9 degC hotter |
| PRESSURE LOW (long) | reference P - recent P | 3 / 8 / 15 bar | -18 bar since Apr |
| RUNS HOTTER (long) | recent T - reference T | 1.5 / 4 / 8 degC | +4.5 degC since Apr |
| SENSOR | flat (no movement through the newest 20 judged windows of the last 3 days - 5 h of running - where it normally moves 1 bar / 0.3 degC a window), or out of range (pressure -1..400 bar, temperature -30..130 degC) | WATCH | sensor |

The flat rule assumes the historian stores the sensor's small movements: `check()` prints the history deadband - a
deadband as large as the movement inside a quiet window would read flat (open item 6).

The pump's score is its worst check, capped at HOT (the PLC limits are the alarms).

**Bands hold** (no flicker; kept in `hydraulics.pump_band`, so a project save or a gateway restart keeps them): a raised
band holds while the score stays at its keep level (WATCH 30, HOT 70) and drops 6 h after the last pass there - the text
reads "HOT held, 5.5 degC hotter" / "WATCH held, now normal" meanwhile. Through a not-judged state (standby, measuring,
learning, a shut, no data) a raised band holds up to 72 h from its last judged pass: "HOT held, standby" - a pump taken
off line for a suspected leak stays marked until it runs again; judged normal then, it drops at once. A reference set or
cleared by hand lets a held band go (1.0.5, section 5).

**Not judged:** plant shut, sensor bypassed, runs with no pressure, standby, measuring, learning, no data (no pressure
window for 2 h), error.

## 7. What it shows

- **Anomaly Watch, Hydraulics row** (`anomalyWatch` 1.15.0): tanks (hydLeak) and pumps (hydPump) share the row. The
  worst (band, then index) leads its value, index and headline; the other follows in the detail and the history. Names
  by area from 1.0.2 (DB P1, GRA P1, COS1 P2, TNB P2; labels "Debarker Pump 5 (HydUnit2 Pump 1)", "Grading Pump 1
  (drive)", "T&B Pump 2 (star loader)"). Values: "tank steady; 6 pumps OK", "tanks OK; 5 pumps OK, 3 idle", "COS1 P2 6.9
  degC hotter", "GRA P1 -64 bar since Apr", "U3 losing 40 L/day" (a tank leading). One asset per tank and per pump (pumps
  grey when not judged). History text, e.g. "Hydraulics HOT - COS HydUnit1 Pump 2 runs +10.2 degC over its tank, normal
  +3.2 (z 13.9): 7.0 degC hotter - oil forced back through a worn pump turns to heat - also +7.0 degC since Apr - 6 h of
  running against the last 56 days".
- **Hydraulics cards** (`HydraulicsDiagnosticsCard` 1.7.0): a PUMP WATCH section under LEAK WATCH (LED, title, "5 judged,
  1 idle - each against its own 8 weeks", a gold DETAILS pill, badge OK / WATCH / HOT / IDLE / LEARNING / SHUT / NO DATA /
  STALE) and one line per pump: LED, short name, the running pressure and the temperature over its tank, each a marker on
  a gauge against its own normal (the tick is its median, the green band +-2 spreads, the ends +-6 - the marker follows
  the check that scores highest, short or long), the numbers and the verdict; a pump not judged shows its live values
  and why. The DETAILS pill and a click on the pump lines open the DETAILS popup (1.7.0 - the 1.6.0 hover text held
  every pump's full text and covered the cards; LEAK WATCH keeps its hover). The state pill reads PUMP WATCH / PUMP HOT
  when a pump leads (LEAK ... when the tank does or they tie); the card border follows the worst. The card is 354 px
  tall; the HydPanel 420 px (`SafetyPlantOverview` 1.23.0, just below the Anomaly Watch panel since 1.22.1).
- **The DETAILS popup** (`HydPumpWatchDetail` 1.0.0 at `Application/Safety/Components/HydPumpWatchDetail`; `detail(code)`,
  1.0.4): the PUMP WATCH section read in full - an SVG sheet as tall as its pumps need (760 px wide). A header: PUMP
  WATCH, the card's sub-line and badge, "results of HH:mm" and a legend (normal - its steady running of the last 56 days;
  reference - its first 14 days of running at pressure, used from 42 days after; how to read the gauges). Per pump a block: LED, short name, label and verdict chip; for a judged
  pump three gauges - PRESSURE, DIPS UNDER LOAD, TEMPERATURE OVER ITS TANK (or OVER THE UNIT'S OTHER PUMP) - each with
  the number now, "normal X, reference Y" and the marker; for one not judged its live values; then its full text (up to
  4 lines). Stale results are marked; on an error the sheet reads ERROR, never raises. The popup: id
  `hydPumpDetail_<card>`, 780 px wide, the sheet's height + 44 up to 720, draggable and resizable; a second click
  closes it; its binding reads `detail()` every 30 s.
- **Console:** `check()`, `backfill(days, skip_days, chunk_h)`, `replay(days, every_h)`, `status()`, `trend(key)` (monthly
  medians - wear since the sensors went in), `set_reference(key, from, to, note)`, `detail(code)`, `rebase(dry, force,
  skip)` (1.0.5, section 15).

## 8. Tables (`KPP_HydPump_schema_apply_v1_0_0.py`)

- `hydraulics.pump_window` (pump, win_start PK; p_avg, p_min, p_max, t_avg, t_min, t_max, run, run_src, ref_t, ref_src,
  dt, sm, src, updated) + index on win_start - 1,728 rows a day with 18 pumps, about 630,000 a year.
- `hydraulics.pump_band` (pump PK; band, since, updated).
- `hydraulics.pump_ref` (pump PK; ref_from, ref_to, note, updated) - only when a reference is set by hand. 1.0.5 reads
  `updated` (written by every `set_reference`) and falls back to the three columns where it is missing.

## 9. Runtime

Polled from the Anomaly Watch slow pass (60 s) like LEAK WATCH: `poll()` starts a background refresh when a window is due
(or a shut has just ended) and returns at once; a refresh is three historian reads for all 18 pumps, the analysis and one
band write. `rows(area)`, `card(code)` and `detail(code)` read the last results (published in the gateway globals too, so
a Perspective binding sees them); `detail()` builds a card's sheet once per results and keeps it. Never raises out of
`poll()`, `rows()`, `state()`, `card()`, `detail()`. Results older than 2 h show as stale. The baselines are worked out
from the table every 6 h (one read of 56 days per pump), the references every 24 h - and at once for a pump whose
reference set by hand changed (1.0.5: the reference rows are read every refresh).

## 10. Install (as done)

1. **18 Oct** - `KPP_HydPump_schema_apply_v1_0_0.py` (DRY_RUN, then live); `forensics/hydPump`; `check()` (read and confirm
   before going on); `backfill(30)` in 30-day parts back to 21 Jan; `replay(60)`; Anomaly Watch 1.15.0; the card into a
   fresh view; the overview 1.23.0 (sizes only, paste over). `KPP_HydPump_Install_v1_0_1.txt` (1.0.1 - the paths;
   backfill again after it, it rewrites the rows).
2. **1.0.2** - paste over and save (names only).
3. **1.0.3** - first `KPP_HydPump_BigJohn_Tags_v1_0_0.py` (DRY_RUN, then live - four tags), then paste over and save. No
   backfill (the windows are unchanged). `KPP_HydPump_Verify_v1_0_0.py` (read-only): the table per pump, the PREVIEW's
   historian reads timed, the replay per pump.
4. **1.0.4** - any `set_reference` first (the references are cached 24 h); paste over and save; create the view
   `Application/Safety/Components/HydPumpWatchDetail` and paste `HydPumpWatchDetail_view_v1_0_0.json`; the card - delete
   `HydraulicsDiagnosticsCard`, save, recreate it with the same name and folder and paste 1.7.0 (it adds components).
5. **Big John** - repoint `Status/Pressure` and `Status/Temperature` of `KPP/TnB/Devices/Pumps/HydUnit4Pump1` to
   `ns=1;s=[COS_PLC_1756CPU]TnB_Area.Pumps[0].PV8000.Pressure` / `...PV8000.Temperature` (or the PLC rung in section 2).
6. **1.0.5** (28 Oct, to do) - paste over and save; Script Console `forensics.hydPump.rebase()` (read-only - check the
   REBASE list against the swapped transmitters), then `forensics.hydPump.rebase(False)`; the cards follow at the next
   refresh (15 min).

## 11. Tests off the gateway

**18 Oct (1.0.0).** A fake gateway (the library through 2to3 on CPython 3.11, `system.*` faked, PostgreSQL 16 for the
tables) with a simulated plant: 17 pumps on a two-shift week from 9 Apr, shuts on 2 Sep and 15 Oct, smoko and downtime,
the T&B motors known only from start / stop events, SDB HydUnit2 with no run state at all.

| Scenario | Result |
|---|---|
| COS U1 P2 internal leak, +7 degC / -4 bar / +5 bar dips over 3 days | WATCH at +3.2 degC (about a day of running after the onset), HOT at +6.3 degC a day later; held through the shut and standby; repaired, judged normal on its next run and dropped |
| SDB U1 P1 pressure down 8 bar 20 h ago | WATCH 72 "pressure -8 bar" |
| GRA drive pump +5 degC slow wear over six months | short check normal (it learns), long check WATCH 63 "+4.5 degC since Apr"; trend() shows the climb month by month |
| COS U3 P1 pressure sensor flat 8 h | WATCH "sensor" |
| SDB U2 P2 +4 degC against its peer | WATCH 66; U2 P1 (cooler against it) not raised |
| COS U1 P3 sensor lost 3 h | NO DATA |
| Standby / duty-change pumps | standby, measuring, judged as they run |
| The other pumps over 21 days of replay | no false WATCH |
| T&B with the event capture stopped at 14:05 | not judged after the stop (before the pressure rule: a false HOT) |
| Restart, database down, history path fallback, end-stamped rows, busy guard | bands back from the table; last results stand; fallback found; same windows; one refresh at a time |
| Anomaly Watch merge, card transform, card SVG | as section 7; SVG valid XML, rendered and checked at 1920 px |
| Independent review (6 findings, all fixed and re-tested) | a hole in the tank history no longer switches tank units to the peer reference or leaves the tank group out (before: healthy pumps WATCH "3 degC hotter"); a pump at 80 % run share reads measuring, not "not running"; a non-ASCII reference note reads; a bypassed sensor is not judged; the backfill holds nothing in the Designer; the card's band case() gets an integer |

**19 Oct (1.0.3, 1.0.4).** The simulated plant given the site's facts - zeros from 21 Jan before the sensors, Big John's
transmitter dead.

| Stage | Result |
|---|---|
| t7 - the long reference | the site's bug reproduced on 1.0.2 (n 0 on every pump) and gone on 1.0.3; TNB P1 with a dead pressure reads "runs, no pressure", with a live one it learns |
| t8 - "runs, no pressure" | its edges: the pressure up in one window of the 2 h - not it; idling unloaded at 3 - 7 bar - not it; no baseline - learning; a HOT pump that loses its pressure - "HOT held" |
| t9 - `KPP_HydPump_Verify` | the table, the timed reads with a Gateway Error 500 and a read time-out planted (a failed read tried again without TNB P1), the replay per pump |
| t10 - `detail(code)` | the four sheets rendered and looked at (the header over the sub-line, the wrap widths and the chip width fixed from the PNGs); valid XML; no results yet, stale results, an unknown card, a failing `card()` - never raises |
| t11 - the views | the card 1.7.0 click script and the popup's transform run against 1.0.4; Python 2 grammar; ASCII |
| Regression | the 18 Oct stages on 1.0.3 and 1.0.4 - the analysis output identical |

**28 Oct (1.0.5).** A simulated plant on PostgreSQL 16: 18 pumps, 5 Apr - 28 Oct, 357,030 windows, a two-shift week; the
site's steps - DB P6 down 25 Sep (135 -> 111), GRA P1 down 1 May (116.5 -> 52.5) - plus TNB P2 up 10 Aug (115 -> 169: a
swap the card never raised), COS3 P1 temperature +5.7 degC from 1 Oct, COS3 P2 a slow drift 124 -> 114 bar (Jun - Oct,
wear), Big John only from 19 Oct.

| Stage | Result |
|---|---|
| Regression | 1.0.4 and 1.0.5 give the same result for every pump with no reference set by hand; DB P6 and GRA P1 HOT "since Apr" as on site |
| `rebase()` dry | REBASE DB P6 from 26 Sep (long check from 5 Dec, 8 weeks from 26 Sep), GRA P1 from 2 May (in use at once), TNB P2 from 11 Aug, COS3 P1 from 2 Oct; COS3 P2 DRIFT (still WATCH "-10 bar since Apr"); Big John "no reference yet"; the other 12 steady; nothing written |
| `rebase(False)` + the running gateway's next refresh | the four references written; the four pumps judged afresh and normal, their held HOT bands let go in the table; COS3 P2 still raised; the refresh after: no change |
| Reload after a rebase | a held band confirmed before the reference row was written dropped; one confirmed after it kept ("HOT held, now normal") |
| Also | `replay()` with the baseline rule; the reference read without an `updated` column; `set_reference` refuses `to` not after `from`; `force` / `skip` (a name not known is said); Python 2 grammar; ASCII |

Also: Python 2 grammar and an AST check for Python-3-only syntax on every script, ASCII only, the views' scripts executed
with a value, None and no library.

## 12. On site (18 - 19 Oct; 28 Oct)

- **Replay on 1.0.3, 60 days** (19 Oct): 15 pumps normal 92 %, not judged 7 %, no WATCH or HOT - the limits stand.
- **DB P6 - HOT 40 %**, since Fri 25 Sep: its running pressure 129.5 - 139.6 bar from August to 24 Sep, about 111 from 25
  Sep - level with DB P5 (about 110), running cooler (T -2.6); the card "-18 bar since Apr". If the step was deliberate:
  `forensics.hydPump.set_reference("SDB_U2P2", "2026-09-26", None, "set down 25 Sep")`.
- **GRA P1 (drive) - HOT 98 %:** April median 116 - 117 bar, 52 - 53 from May and flat since - one step, a duty change;
  the card "-64 bar since Apr". `forensics.hydPump.set_reference("GRA_U1P1", "2026-05-01", "2026-05-29", "drive
  pressure lower from May")`.
- **28 Oct:** both still HOT on the cards ("-18 bar since Apr", "-62 bar since Apr"). Adriaan: field devices (pressure
  transmitters) were swapped - hence the pressure differences; use the existing level as current. 1.0.5 `rebase()` does
  it for every pump that stepped (section 15).
- **TNB P1 - runs, no pressure** (section 2) - reads 168 bar on 28 Oct: its tags are repointed; its reference builds from
  its first two weeks of running.
- **The station motors** (`KPP_HydMotor_Bindings_Probe` 1.0.0): no pump's own motor (`Pumps/Pump N/Motor`, the run state
  PUMP WATCH reads) is wrong. The station `Motors/Pump N` instances are - debarker U1 Motors/Pump 6 on Pump 2's block,
  grading Motors/Pump 1 and 3 on each other's feedback and Safe, copies in the T&B and debarker HydUnit2 folders - used
  only by an old faceplate on no page. The pump popups' diagnostics for DB P5 - P6 and the T&B pumps: `forensics.hyddiag`
  1.4.0.

## 13. Open

1. Big John: the tags repointed (or the rung) - then TNB P1 learns; its reference after two weeks of running.
2. DB P6 and GRA P1 (and any swap partner): `rebase()` then `rebase(False)` (1.0.5) - replaces the two `set_reference`
   lines of section 12.
3. Pumps that cycle on and off inside 45 minutes are never judged (measuring) - `replay()` shows the not-judged share per
   pump (7 % on site).
4. Pressure decay after a stop (the classic leak test) needs the raw samples around each stop: next version, once
   `check()` shows whether the sensors hold pressure after a stop.
5. "Ask Azztec AI": a pumps intent beside the tanks one (`forensics.anomalyAsk`).
6. The SENSOR flat rule against the history deadband (`check()` prints it): if healthy pumps raise "sensor", the
   deadband is the suspect - widen FLAT_N or drop the flat rule for that pump.
7. Where a unit has a case drain line, a temperature sensor on it is the strongest single wear signal.
8. `forensics.hyddiag` - the start / stop capture writes nothing (its error handler calls `system.util.getStackTraceAsString`,
   which does not exist); not needed by PUMP WATCH.
9. The gap-fill quirk (section 3) - floor the oldest window when next in the code.
10. A swapped transmitter also swaps its temperature offset (+-2 K) - a rebased pump's T is judged from its new level;
    if swaps recur, label the transmitters (serial per pump) so a swap is recorded, not inferred.

## 14. Sources

- Machinery Lubrication, "10 Ways to Check Hydraulic Systems with Thermal Imaging" - case drain hotter than the inlet as
  bypassed oil does no work; the rise grows with wear; set the baseline when the pump is new.
- Panagon Systems, "Predictive Maintenance Hydraulics: A Practical Playbook for Pumps" - housing minus reservoir: normal
  up to 10 degC, warning 10-20, alarm above 20-25; case drain flow against the baseline +20 % / +40 %; pressure ripple at
  constant load; establish your own baseline.
- Panagon Systems, "What Causes Hydraulic Pump Overheating" - heat any time oil is forced across a pressure difference
  without doing useful work; declining pressure stability and slow response point to internal leakage.
- Eksploatacja i Niezawodnosc 2024;26(2):184039 - pressure decay rate linear in the internal leakage rate.
- Throttling heat: dT = dp / (rho cp), about 0.06 degC per bar for mineral oil (870 kg/m3, 1.9 kJ/kg K).
- ifm PV8000 data sheet (PV8000-00_EN-GB, TME copy) - range, connections, IO-Link device ID 1214, process data.

## 15. Rebase after a sensor swap (1.0.5)

`forensics.hydPump.rebase(dry=True, force=None, skip=None)` - Script Console, on the stored windows (the table, not the
historian), with the library's own judged-window rules. Per pump (all 18):

- its running pressure by month (judged windows), its long reference (period, n, P, T; in use / used from / too few
  windows; "set by hand" and its note), its 8 weeks (from a hand-set reference when that is inside them) and its last 14
  days (`NOW_DAYS`);
- **moved:** the last 14 days' P 8 bar or more (`MOVE_P`, the long check's WATCH size) or T 4 degC or more (`MOVE_T`)
  from the reference - **either way**: a swapped transmitter can read high or low, and one reading high hides wear later
  (the card raises only low and hot). Needs a reference of 96 windows and 96 windows in the last 14 days;
- **the day it moved:** from the daily medians (days with 16 judged windows - 4 h of running), the first day of the new
  level - a day nearer the new level than the old, the new level holding from it on (nine days in ten, six of its first
  seven); **step** when the week from that day against the week before it is 60 % of the move or more (`STEP_SHARP`),
  else **drift**;
- **REBASE** (a step in P or T): a new reference from the day after the (later) step, 28 days (`REF_DAYS`), to today at
  most - its level since the step as its normal; at least 96 judged windows in it, else "too little running since the
  step - run again in a few days". Used at once when it ended 42 days ago (an old step - GRA P1, May), else from 42 days
  after its end (DB P6: early December) - its 8-week check covers it meanwhile, from the day after the step;
- **DRIFT** (moved, no step): listed and left alone - it may be wear; `force=["COS3 P2"]` rebases it anyway (no step: its
  last 28 days); `skip=[...]` never rebases;
- the card's verdict now and rebased (`analyse()` with no held band).

A summary lists the rebase plan, the drifts and **the steps by day** - a swap between two pumps steps both on the same
day. `rebase()` prints only; `rebase(False)` writes the plan with `set_reference()` (note "sensor swap or pump change -
its level since the step (rebase)"); the gateway takes the new references at its next refresh (section 5).
