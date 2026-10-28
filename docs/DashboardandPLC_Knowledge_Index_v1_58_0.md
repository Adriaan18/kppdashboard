# DashboardandPLC Knowledge Index

**Version:** 1.58.0
**Status:** Active · **Date:** 2026-10-23 · **Author:** Adriaan

**Changelog:**
- v1.58.0 - REGISTRATION for the 2026-10-23_A session (Operator KPIs - ten asks plus Trina's knife question; one chat,
  Fri 23 Oct 12:09 - about 14:00; built on 1.57.0). Raw Log `2026-10-23_A` added. **(1) Findings (code and PLC, nothing
  run on the gateway):** Dave's `sdb.profile` stores PLC bit 12 (knife-arm ZERO PRESSURE, also set by the PLC on its
  own) as "knife arms" and bit 14 (the knife joystick) as "zero pressure", every bit on the light-curtain word - 2.9 m
  ahead of the knives (roll 2.0 m); reverses re-sample the re-fed piece; stalls add phantom length; 6 cumulative
  dropouts split a stem; the gaps KPI is an average in mm of every gap (waits and split pieces in) and rewards
  nose-to-tail feeding; auto stem gap control (5000 mm) is off; the Stem Gap Histogram NQ has no booth filter and hid
  gaps under 0.5 m; Design v3.13 has 12 errors against live v3.12.0 (thresholds and weights match); saw logs reach the
  pulp deck only by the manual sweep and no manual sweep is recorded; Training Review's Save reload cleared the KPI
  panel. **(2) Built, not installed:** `sdb.ringcapture` 1.0.0 (shadow, aligned to the knives, live tag) + setup + PLC
  `L08B_RingFlags` 1.0.0 + Knife Check page 1.0.0 + SDB Map StemPressure 2.0.0 + Debarker Detail 1.1.0; corrected
  Debarker KPIs, close gaps, gap histogram 2.0.0, knot / defect call NQs, `operator.kpi` 1.3.0, tabs SDB Corrected and
  Grading Calls, OperatorKPI 1.9.0; Design v3_14_0 + `KPP_KPI_Calibration_Probe` 2.0.0 (HTML approval pack, proposal
  v3.13.0 - scoring unchanged until Trina and Phil approve); `KPP_PulpDeck_SawLog_Probe` 1.0.0; Trina's "bark on stems"
  explainer (docx); Training Review fix (`kpi_snapshot`, library 1.5.0, view 1.8.0); HR Final Report (schema `hr` with
  lock triggers, `hr.finalreport` 1.0.0, three views, Business side menu 1.7.0, Business home 2.6.0, route
  `/business/hr`). **(3) CORRECTIONS banked:** M1 - M2 (Raw Log 2026-10-23_A section 13). **(4) Staged, not compiled:**
  `KPP_Domain_Data_Reference`, `KPP_Platform_Rules`, `KPP_Working_Method` - Raw Log 2026-10-23_A section 11. **(5)
  OPEN:** installs (sheet `KPP_OperatorKPI_Install_2026-10-23_v1_0_0.md`), the backfill depth, the approval pack and
  scorecard 3.13.0, Phil on the 50 / 50 blend, a pulp deck recorder, item 5's second reading - Raw Log 2026-10-23_A
  section 12.
- v1.57.0 - REGISTRATION for the 2026-10-22_A session (a Visitor Sign In change request from management - the 2-minute
  return and a mandatory induction question; the On site card scroll arrows; PLANT SHUT on a normal day; a glow on the
  induction boxes; Log Stop Positioning moved to Machine Settings; one chat, Thu 22 Oct 16:58-18:55; built on 1.56.0).
  Raw Log `2026-10-22_A` added. **(1) Findings:** the PLANT SHUT badge and the Hubheader pill are labels hidden by a
  `props.style.display` binding, which the gateway ignores on labels - the title beside the badge showed the shut data
  right, so the 14 Oct F1 cause is found (not the date path); 30 such labels project-wide; Hubheader 1.5.0 returned on
  shut days only and read page props in an expression; 69 of 117 pages carry the Hub header; `dbo.visit` had no place
  for an answer; Contact Information never reads `visitType`; the COS Map carried the Log Stop Positioning embed into
  eight views. **(2) Built:** Hubheader **1.6.1** (the Reception login back to the visitor Menu after 2 min without a
  touch, any day - one polled script transform reads the page, the step and the idle time; the shut-day window removed;
  the countdown pill on `position.display`), User Verification **1.1.3** ("Have you been inducted at KPP?" in
  management's words, Continue gated on an answer, the answer stored, the boxes glowing gold on the stylesheet's
  `wmAiGlowPulse` until answered), Visitor Card **1.3.0** (no scroll arrows), Menu **2.10.0** (PLANT SHUT on
  `position.display`), COS Map **1.1.0** (Log Stop Positioning removed), MachineSettings **1.0.5** (the panel on COS
  infeed and saws, path-swapped), `dbo.visit.inducted` BIT NULL and NQ `Exchange/Visitor Sign In/Visit/Set Inducted`.
  **(3) Live:** the column added and the NQ smoke 0 rows (18:00); the induction step on the client (18:00); the glow
  accepted 18:35. **(4) CORRECTIONS banked:** M1 (1.6.0 / 1.1.0 hid labels with `props.style.display`), M2 (1.1.2's
  glow cut square by the container clip - the mock left containers unclipped), M3 (the mock's `alignItems` default), M4
  (the REQUIRED pill); the 14 Oct F1 badge cause. **(5) Staged, not compiled:** `KPP_Platform_Rules`,
  `KPP_Domain_Data_Reference`, `KPP_MachineSettings_Design`, `KPP_Working_Method` - Raw Log 2026-10-22_A section 9.
  **(6) OPEN:** the kiosk return on the gateway (it proves `lastActivity` moves on a touch); the badge on a normal day
  and on the next shut; installs of Visitor Card 1.3.0, Hubheader 1.6.1, Menu 2.10.0, COS Map 1.1.0 and
  MachineSettings 1.0.5; the 27 other labels; the answer shown nowhere yet - Raw Log 2026-10-22_A section 10.
- v1.56.0 - REGISTRATION for the 2026-10-12_B session (the 2026-10-08_A chat continued after its 12 Oct close - 12 Oct
  12:16-20:35 and the NEW auto trial 13 Oct 11:49-17:16, closed out Wed 21 Oct 14:29; built on 1.55.0). Raw Log
  `2026-10-12_B` added. **(1) Audited and rebuilt:** the COS NEW auto package 1.0.0 (another chat, on `KPP_COS_V20n`)
  had six faults - tags-only L5X, braking up to 2000 mm/s2 (contact 730 not 250), an endless push on a stalled stem,
  clamps 0.45 s early, the infeed at half speed under run-slow, spring-back cut 14-37 mm short - never import; **1.0.1**
  in its place (`_103` 1.0.1 new, `_100` 1.3.1, `_149` 1.1.0, `_110` 1.2.1, `_055` 1.2.1, `_260` 1.3.1 flag 31, `_261`
  1.1.1 codes 17 / 18 / 19 / 36; tags 1.0.1, codes ADD, AutoModeChip / NewAutoSettings 1.0.1, LogStopPositioning 1.3.1;
  sheet `KPP_COS_NewAuto_Install_v1_0_1.txt`), behind `NA_Req` (two taps, logged in, read-back, audit row), the chain
  interlocks untouched; proven by static check, a 13-scenario scan simulation (NEW off = STANDARD every scan) and an
  independent review. **(2) Installed and live:** NEW taken Tue 13 Oct 13:08:14 (`BA_Enable` 1, defaults); at 3.8 h
  (LiveCheck 1.0.1): contact p50 460 -> 238 mm/s, PosReached to saw 0.76 -> 0.60 s, 0.46 s quicker a cut outside the
  saw like for like (about 1.1 s a stem, est. 116 vs 112 stems an hour), hand clamps 48 -> 17 %, jogs 50 -> 36 %,
  blade-clear OK; 9 re-seats (7 on stems 15926 / 15971), 4 holds 41-43 mm past on mostly cut 4. **(3) Built:**
  Processing Analytics 0.1.2 (`pa_cos_cut.na_mode` / `na_sa` / `na_held` / `na_switch`, report `modes`, the STD vs NEW
  tab - `PA_COS_Modes_view` 0.1.0, `PA_Page_view` 0.1.2; DB applied 13 Oct 12:30), P2 1.0.1 (6 h query slices),
  read-only `KPP_COS_NewAuto_PreFlight` 1.0.0 and `KPP_COS_NewAuto_LiveCheck` 1.0.1; two team emails (NEW auto and the
  sweep switch; the manual handling Permit bar on Debarker, Grading, T&B and Chippers). **(4) Findings:** COS Watch's
  300 / 600 mm speed points are an artefact in both modes and `overrun_mm` p90 (1.5-1.8 m) is not run-on alone;
  `NA_ReSeats` is per approach. **(5) CORRECTIONS banked:** M1 - M7 (Raw Log 2026-10-12_B section 5). **(6) Staged,
  not compiled:** a NEW auto owner (to settle), `KPP_COSWatch_Design`, `KPP_Domain_Data_Reference`,
  `KPP_Working_Method`, `KPP_Platform_Rules` - Raw Log 2026-10-12_B section 9. **(7) OPEN:** Raw Log 2026-10-12_B
  section 10 (the sorter length proof NEW vs STD, the re-seat stems, the cut 4 holds, tuning, making NEW permanent, P2
  section F, the PA Modes view import).
- v1.55.0 - REGISTRATION for the 2026-10-21_A session (one chat, Wed 21 Oct 08:39 - 12:04; built on 1.54.0). Raw Log
  `2026-10-21_A` added. **(1) Delivered, install not told:** low plant air made visible - the Debarker Ring on the SDB
  Map flashes red / dark at 1 Hz with a "LOW AIR x.x bar" pill while `PT/PlantAir/Pressure` is under its own LowLimit
  (SDB Map 1.4.0 - the Debarker Overview only, not the Safety cards; `KPP_Stylesheet_RingLowAir` 1.0.0 - @keyframes
  `kpp-ring-lowair`, steady red without it); for the grading booth the new view
  `Application/Debarker/Components/LowAirTile` 1.0.0 - red and flashing while low, amber "x min ago - bark on likely"
  for 10 min after (tag history, MinMax, a script transform) - on Grading Overview 1.5.0 under the PT reading. **(2)
  Findings:** "the pressure on top" is plant air (`KPP/Grader/Devices/Sensors/PT/PlantAir`, LowLimit 5 / HighLimit 7.2
  bar, about 6 bar with dips to about 3.4 over 12 h); the live GRA Map root is `GRAMap_v1_1_0` (the never-import file of
  2026-10-10_A); export thumbnails can be stale; inline SVG animation was unproven live (only an unused symbol had it).
  **(3) CORRECTIONS banked:** M1 - M3 (Raw Log 2026-10-21_A section 6). **(4) Staged, not compiled:**
  `KPP_Platform_Rules`, `KPP_Domain_Data_Reference`, `KPP_Working_Method`, `Workmate_Perspective_Rules`
  (cross-reference) - Raw Log 2026-10-21_A section 8. **(5) OPEN:** Raw Log 2026-10-21_A section 9 (the installs and a
  live check, the 10 min hold against a real dip, a per-stem PLC flag, the GRA Map root, the COS Overview, this
  morning's low air).
- v1.54.0 - REGISTRATION for the 2026-10-06_A session (one chat, opened Tue 6 Oct with the chainsaw downtime audit,
  worked 12, 14 and 16 Oct, closed out Wed 21 Oct 08:52; built on 1.53.0). Raw Log `2026-10-06_A` added. **(1) Three
  Capex documents for KT management:** the Debarker infeed chainsaw V1.0 - V1.6 ($170K, $60K budgeted; payback 13 months
  on halving the chainsaw downtime and a quarter of the bent-stem stops after the saw), the Hogger MCC replacement V1.0
  ($60K on Mark Coker Electrical estimate 11515; installation, MCBs and contingency are allowances to confirm with Ken)
  and AI stem grading Phase Two V1.0 ($125K on the TuiTech quote of 19 June 2026, expired - refresh; the full system
  $200 - 240K a future Capex after the accuracy gate). **(2) Behind the chainsaw case:** `KPP_ChainsawDT_Audit` 1.0.0
  (1,896 stops / 178 h since Jan 2011, 92 % the saw failing) and `KPP_BentStem_Probe` 1.0.0 (1,965 bent-stem stops /
  152 h after the saw since 2019; 43 % more of them on shifts with the saw down 15 min or more). **(3) Finding:** the
  5-second cut gives back 78 h a year of infeed time ($840K a year at $180 a minute), but across 1,250 shifts the cut
  time shows no lost production - the time goes with the extra piece a cut makes (about 18 s); kept out of the payback
  as a ceiling with a share table and framed as headroom for the COS speed-up; V1.5 - V1.6 add a plain-words note on
  the COS model and its screenshot. **(4) CORRECTIONS banked:** M1 - M5 (Raw Log 2026-10-06_A section 5). **(5) Staged,
  not compiled:** `KPP_Working_Method`, `KPP_Domain_Data_Reference` and a KT document build owner to settle (Raw Log
  2026-10-06_A section 9). **(6) OPEN:** Raw Log 2026-10-06_A section 10 (Kona pricing to 30 Oct, the measured share,
  the cut-counter drop, the MCC and AI Grader allowances and budget status).
- v1.53.0 - REGISTRATION for the 2026-10-14_E session (one chat, Wed 14 Oct 12:36 to Thu 15 Oct 15:30, closed out Wed 21
  Oct 08:35; built on 1.52.1) and for Raw Log 2026-10-20_A (the Value $ chat, 19 Oct 16:12 - 20 Oct 10:19, left out of
  1.52.1). Raw Logs `2026-10-14_E` and `2026-10-20_A` added. **(1) Built and live (14 Oct):** the Value Recovery section
  for Renata - side menu Value, page `/ValueRecovery`, tabs Origin / Crews / Grading booth / COS booth / Stems / Explore
  / How it works: `kppstems.vr_stem`, `vr_state`, `gra_call` and `vr_build` / `vr_report` / `vr_stems` /
  `vr_stem_detail` (`KPP_VR_DB_apply` 1.0.0), `analytics.valuerecovery` 1.0.0 with timer `VR_Build` (backfilled from 4
  Sep), three NQs, nine views, `Hubsidemenu` 1.10.0, `shared.whatsnew` 1.5.0; the PLC grade call recorder
  `_311_GradeCallWatch` 1.0.0 (Grading_Area, a new last rung 8) and its reader `forensics.gradeCalls` 1.0.0 (timer
  `GradeCalls_FixedDelay`); verify 17 PASS (16:07). **(2) Findings:** every butt cut traced to its origin (the last 7
  days at 14 Oct: 80 % behind a grader split, 1 % another butt call, 17 % the optimiser alone - 32 % of the chip - and
  0.2 % a COS override with no call); USNR `overridecount` is 0 and solution type 0 is not an override flag - COS Watch
  is the only override source (from 7 Oct); the USNR stem links to `kppstems.stems` on 16 % only, the grader's call set
  on 98 %; split calls carried no conveyor speed until the recorder; most split calls are made with the outfeed stopped
  (the first afternoon); a marked split costs about 2.6 x the chip of a button split. **(3) Delivered, install not
  told:** Page 1.0.1 (the loading bar derived from the report's own window - no latch) and 1.0.2, hover tips on every
  view (Origin, Crews, COS 1.0.1, Grading 1.0.2, Stems 1.0.3, Explore 1.0.1), `analytics.valuerecovery` 1.0.1 (the
  graders chart key in plain words) - the Page is 1.0.3 and the library 1.1.0 since 2026-10-20_A. **(4) 2026-10-20_A in
  short:** the butt defects meeting in $ ($9.47 a butt cut, about $1.69M a year at the optimiser's log prices), the 19
  Oct restart wipe (`analytics.processing` gone - the Processing builder now in `analytics.valuerecovery`), the
  Financials tab (`kppstems.vr_money_*`, NQ Money, library 1.1.0, Page 1.0.3, Financials 1.0.5). **(5) CORRECTIONS
  banked:** M1 - M5 (Raw Log 2026-10-14_E section 12). **(6) Staged, not compiled:** `KPP_Platform_Rules`,
  `KPP_Domain_Data_Reference`, `KPP_Working_Method`, `Workmate_Perspective_Rules` (cross-reference) - Raw Log
  2026-10-14_E section 13 and Raw Log 2026-10-20_A "Knowledge Index - add"; 2026-10-20_A's "bump root.meta.name" meets
  the compiled rule that root's name stays `root` - settle it at the compile. **(7) OPEN:** Raw Log 2026-10-14_E section
  14 (the installs to check, the `_311` import route, retention for `vr_stem` and `gra_call`, Production 2.14.0, the
  verify's version check, `KPP_ValueRecovery_Design` to write) and Raw Log 2026-10-20_A "Open" (the chip price, the
  baseline, the meeting actions, the cause of the wipe).
- v1.52.1 - REGISTRATION for the 2026-10-20_B session (the 2026-10-19_B chat into Tue 20 Oct, 19 Oct 21:07 - 20 Oct
  about 11:15; built on 1.52.0). Raw Log `2026-10-20_B` added; `KPP_TrkAdvisor_Design` 1.1.3 -> **1.1.4** (NEW 11.12 the
  first day, NEW 11.13 the scan against the plan by log size; 11.2 and 11.7 - 11.8 for 1.0.3). **(1) On site:**
  `trk.advisor` 1.0.2 one run since 19 Oct 21:00 through project saves. The first day (report 1.1.0, 24 h): 9,076
  scans, 99.7 % as Tui where Tui had its own data; 10 cases where Tui gave one log's data to two logs (7 into another
  bin, 3 of them a needless regrade), 6 the advisor wrong on an open cut 15 - 48 behind; only 9 of 286 never-scanned
  cuts in Bin 0. The data cut: SED reads +3.7 % of the log, LED under the plan by its taper, the COS ring's Y = X.
  **(2) Delivered:** `KPP_TrkAdvisor_Report` 1.1.0 and `KPP_TrkAdvisor_DataCut` 1.0.0 (read only, run on site);
  `trk.advisor` **1.0.3** (old open cuts cost more for each log settled since, never scanned after 6; SED a share of the
  plan, LED by the plan's taper) with `KPP_TrkAdvisor_Install_v1_0_3`, not yet installed. **(3) Staged, not compiled:**
  `KPP_Domain_Data_Reference`, `KPP_Working_Method`, `DashboardandPLC_Knowledge_Standard` - Raw Log 2026-10-20_B
  section 7.2. **(4) Corrections:** M9 - M10 (section 7.1). **(5) OPEN:** install 1.0.3 and the day check after it -
  section 8. Not registered here: Raw Log `2026-10-20_A` (the Value $ chat).
- v1.52.0 - MERGE + REGISTRATION. **(0) Merge:** 1.50.3 (the third post-close addition to 2026-10-19_B) and 1.51.0 (the
  2026-10-17_A registration) were both built on 1.50.2 - both are carried here, row by row (from 1.50.3 the advisor
  rows, `KPP_TrkAdvisor_Design` 1.1.3, the regrade note and its staged rule; from 1.51.0 PUMP WATCH, `KPP_CM_Design`
  1.1.0 and its staged rows); neither file is to be used on its own again (section 4).
  **REGISTRATION for the 2026-10-15_C session** (a third chat on the shut day, Thu 15 Oct about 12:00 - 19:30, closed
  out Tue 20 Oct 10:29: Anomaly Watch stands down for a Shut Plan shift; the hydraulic tank LEAK WATCH; LEAK WATCH on
  the hydraulics cards; a short Anomaly Watch headline). Raw Log `2026-10-15_C` added - it answers 1.51.0's open item
  (the 15 Oct work in no index). **(1) New compiled doc:** `KPP_HydLeak_Design` **1.0.0** (LEAK WATCH as installed,
  1.0.3). **(2) Findings:** the low-level warnings sit at the running level (95 / 96 / 90 / 93 / 93 % against 96 - 100
  %) - LEAK WATCH judges the days to the ALARM; the tank level grows 0.13 - 0.33 % per degC; the fill stations' booked
  litres do not match the level rise (4 Oct T&B: 133 L, +1.7 %); a real leak on the T&B HydUnit4 (about 90 - 100 L a day
  from the Wed 14 Oct downtime; WATCH on site after the shut - 46 L/day, alarm in about 5 d); the replay of 1 - 15 Oct
  raised the T&B HOT and the Debarker WATCH before their 12 Oct fills; `system.file.saveFile` is not in the 8.3
  Designer's console. **(3) Built and live:** `forensics.peWatchJudge` 1.5.0 (the Shut Plan), Anomaly Watch 1.14.0 (the
  shut, the first verdict, the Hydraulics row - now 1.15.0), `KPP_HydLeak_schema_apply` 1.0.0 (applied),
  `forensics.hydLeak` 1.0.3, `HydraulicsDiagnosticsCard` 1.5.1 (LEAK WATCH in place of the PUMPS count - now 1.7.0).
  **(4) Delivered, not confirmed:** Ask 1.4.1. **(5) CORRECTIONS banked:** M1-M6 (Raw Log 2026-10-15_C section 8).
  **(6) Staged, not compiled:** `KPP_Platform_Rules`, `KPP_AnomalyWatch_Design`, `KPP_Domain_Data_Reference`,
  `KPP_Working_Method`, `Workmate_Perspective_Rules` (cross-reference) - section 9. **(7) OPEN:** section 10 - the T&B
  leak, COS HydUnit1 WATCH after the shut, the fill litres, Debarker HydUnit2 (no tank sensor), the AnomalyWatchMethod
  popup, Ask 1.4.1.
- v1.51.0 - REGISTRATION for the 2026-10-17_A session (one chat, Sat 17 Oct about 12:00 to Mon 19 Oct 18:06: the COS
  encoder rate-ceiling flags, PUMP WATCH - the hydraulic pump watch on 18 pumps, the station motors and pump popups,
  Big John and the IO-Link masters, the motor vibration baselines; built on 1.50.2). Raw Log `2026-10-17_A` added.
  **(1) Compiled docs:** `KPP_HydPumpWatch_Design` 1.0.0 -> **1.1.0** (first registered - 1.0.0 was in the project
  with no index row, index 1.49.0 item (5)) and `KPP_CM_Design` 1.0.0 -> **1.1.0** (Raw Log 2026-10-09_A items 6-7
  compiled; the baseline tool 1.1.0, the GRAOF re-take). **(2) Findings:** the COS encoder rate flags are the
  `_250` pass time (v3.3.0 multiplies by 11.0 - 9.09 ms - against a scan that moves with the code); every pump's
  sensor is an ifm PV8000 (pressure and temperature), the tanks HYDAC, the Debarker tank 2 port empty; Big John's
  sensor reads in `TnB_Area.Pumps[0].PV8000` - its `Status` members are never written; a pump's run state is its
  motor's Running; `hydraulics.pump_events` holds no event - `hyddiag.capturePumpEvents` calls the missing
  `system.util.getStackTraceAsString`; the GRAOF bearing reading flat week on week, about +15 % the last three days;
  the Tracker task period read 20 ms on 18 Oct 06:23 - the half-rate task of Raw Log 2026-10-19_B section 4 (for the
  Line Tracker chat). **(3) Built and live:** `forensics.hydPump` 1.0.3 then 1.0.4 (the long reference from each
  pump's first running windows, "runs, no pressure", `detail()`), its schema, Anomaly Watch 1.15.0, the Hydraulics
  card 1.7.0 with the DETAILS popup, plantDiag 1.4.0, overview 1.22.1, the Big John tags (to repoint), the GRAOF
  baseline (19 Oct 17:47:16, n 985). **(4) Delivered, not confirmed:** `_250` v3.4.0, `forensics.hyddiag` 1.4.0,
  overview 1.23.0. **(5) CORRECTIONS banked:** M1-M7 (Raw Log 2026-10-17_A section 9). **(6) Staged, not compiled:**
  `KPP_Platform_Rules`, `KPP_Domain_Data_Reference`, `KPP_Working_Method`, `KPP_AnomalyWatch_Design`,
  `KPP_LineTracker_Design` and `Workmate_Perspective_Rules` (cross-references) - section 10. **(7) OPEN:** section 11 -
  the `_250` install, the Big John repoint, DB P6 / GRA P1 references, hyddiag 1.4.0 and `pump_events`,
  `StateWord = load` on `CM_GRAOF`, the Labour weekend bearings, and the 15 Oct work in no index (LEAK WATCH
  `forensics.hydLeak` 1.0.3, Anomaly Watch 1.14.0, `peWatchJudge` 1.5.0, Hydraulics card 1.5.1).
- v1.50.3 - third post-close addition to 2026-10-19_B (19 Oct 12:05 - 18:40): Raw Log `2026-10-19_B` **1.2.0 -> 1.3.0**
  (section 15 appended, sections 1-14 unchanged) and `KPP_TrkAdvisor_Design` **1.1.2 -> 1.1.3** (NEW 11.11, the first 7
  hours). **(1) On site:** 2,648 scans in 7 h - 99.8 % as Tui where Tui had its own data, 99.4 % as the tracker; a log
  into the wrong bin caught (Tui 19306-1 bin 18, the advisor and the tracker 19306-2 bin 25); one probably the
  advisor wrong (an open cut seven stems back); the lead to the kick 54 s median. A project save at about 17:51
  started the advisor again - its model back to phase 0's. **(2) Delivered, not yet installed:** `trk.advisor`
  **1.0.2** (the state in the gateway's globals - project saves carry on; one tick at a time; the model from the table
  at a real start) with `KPP_TrkAdvisor_Install_v1_0_2`; proven on the simulation (four saves - the same as none).
  **(3) The user's COS regrade idea** (a selected prune cut instead of a regrade, a chip piece to the next planned cut,
  the rest as planned; the advisor checks the grades) - after this is running, for `KPP_COS_RegradeView_Design`.
  **(4) Staged, not compiled:** `KPP_Platform_Rules` - section 15.1. **(5) OPEN:** install 1.0.2; after two or three
  days the report and 1.0.3 (design 8 items 15 - 17) - section 15.2.
- v1.50.2 - second post-close addition to 2026-10-19_B (19 Oct 10:52 - 12:10): Raw Log `2026-10-19_B` **1.1.0 ->
  1.2.0** (section 14 appended, sections 1-13 unchanged) and `KPP_TrkAdvisor_Design` **1.1.1 -> 1.1.2** (NEW 11.10,
  the first hour on site). **(1) On site:** `trk.advisor` 1.0.1 running since about 10:50; the first hour (11:58) -
  351 scans, 341 named, all as Tui (335 of 335 where Tui had its own data), the tracker's piece paired for 338, 331 of
  332 as the tracker; no plan for the COS's manual cuts (pieces Tui labels with one log, bin 10) and one butt log read
  far from its plan. **(2) CORRECTION banked:** M8 - the lead to the kick is 52 s median on site (p10 31 s, min 3 s),
  not the simulation's 5 - 7 s; design 11.9, 8 item 12 and 12 corrected. **(3) Staged, not compiled:**
  `KPP_Working_Method` - section 14.2. **(4) OPEN:** the report over a shift or a day; the manual cuts in the ring and
  the big butt logs (design 8 items 13 - 14) - section 14.3.
- v1.50.1 - post-close addition to 2026-10-19_B (19 Oct 10:09 - 10:50): Raw Log `2026-10-19_B` **1.0.0 -> 1.1.0**
  (section 13 appended, sections 1-12 unchanged) and `KPP_TrkAdvisor_Design` **1.1.0 -> 1.1.1**. **(1) Installed:**
  the advisor phase 1 - `kppstems.trk_advice` / `trk_advice_state` (PASS 54 / 3), `trk.advisor` 1.0.0 and the timer
  `TrkAdvisor_FixedDelay` (about 10:15); `test_read()` all read, reads 225 ms on average; the first 26 logs decided,
  all as Tui. **(2) Finding:** sorter_engine 0.2.2 drains its whole live ring every tick with one `readValues` per slot
  - a cycle of about 10 s: the scan rows come 0 - 10 s after the scan, two at a time, and the ids jump; 1.0.0's pairing
  with the tracker by time left 15 of the first 18 scans without a piece. **(3) Delivered, not yet installed:**
  `trk.advisor` **1.0.1** (the piece paired when a scan is settled, in order, checked against the advisor's and Tui's
  identities) with `KPP_TrkAdvisor_Install_v1_0_1`; proven on the simulation given sorter_engine's drain - 2,128 scans,
  no decision and no piece wrong (1.0.0 there: 109 of 171 not paired, 17 wrong). With the rows late the lead to the
  kick has a p10 at or below 0 s - phase 2 needs the scan sooner. **(4) CORRECTION banked:** M7 (Raw Log 2026-10-19_B
  section 13.1). **(5) Staged, not compiled:** `KPP_Working_Method`, `KPP_Platform_Rules` - section 13.2. **(6) OPEN:**
  the 1.0.1 install and its status; the report after an hour; sorter_engine's cycle before phase 2 - section 13.3.
- v1.50.0 - REGISTRATION for the 2026-10-19_B session (the 2026-10-16_A chat went on into Mon 19 Oct, 05:24 - about
  09:40; lettered B - `2026-10-19_A`, the weekly report chat, was in the project by 08:50; built on 1.49.0). Raw Log
  `2026-10-19_B` added. **(1) Compiled doc bumped:** `KPP_TrkAdvisor_Design` 1.0.2 -> **1.1.0** (phase 0's result -
  GO; phase 1 as built; the way to Tui's kicks). **(2) Tracker 1.2.0 on site:** `KPP_Trk_230_SrtIdentity_v1_2_0.L5X`
  was refused on import (Error 12740-0 - tag names that differ only in case, `Y_n` / `Y_N`, `Y_q` / `Y_Q`); 1.2.1
  renamed them and went in with the other five files before 06:09; RING 06:09, WATCH 06:11 and 07:48 (`Srt_CosMem` 1
  from about 07:45). **(3) Findings:** the Tracker task ran at 50 scans a second from about 17:50 on 17 Oct (100
  before; `Trk_PeriodMs` 10) - `Trk_Tick` at half speed, the displayed speed doubled and the kicker return window 5 s:
  both wrong-bin kicks of 19 Oct; the 8 - 9 ms `Trk_MaxScanUs` peaks are higher-priority tasks (8,431 us with
  `Trk_Enable` 0); by 07:48 the speed read right and 0 of 226 kicks went into another bin (what was changed - to
  confirm). Phase 0 (72 h): GO - length +0.35 % / 27 mm, SED +9.6 / 8.6, LED -18.1 / 16.1, volume -0.5 % / 3.4 %, 98 %
  of the length-fitting neighbours told apart. COS regrades (14 days): 69.5 a day, 25.9 m3, a ceiling of about NZD 2.0
  M a year; Re-Optimize dropped (the user). The ?? on the Sortline Map are the tracker's ghosts - mostly logs with no
  T&B message. **(4) Delivered, not yet installed:** the identity advisor phase 1 (shadow, gateway only) -
  `trk.advisor` 1.0.0 (timer `TrkAdvisor_FixedDelay` 1 s; reads `sorter_logs`, the COS ring and the tracker's event
  ring; writes `kppstems.trk_advice` / `trk_advice_state`, nothing to the PLC), its schema script, report probe and
  install sheet; WATCH probe 1.6.1 (the landing PE dropout judged on the tracker's own gap). Proven off the gateway
  on a simulated line: nine runs, 2,131 scans - none decided wrong, no tracker piece paired wrong (a restart, the
  database and OPC away, a 5 min stop, the tracker off, the scanner +1.8 %, heavy faults). **(5) CORRECTIONS
  banked:** M1-M6 (Raw Log 2026-10-19_B section 9). **(6) Staged, not compiled:** `KPP_Platform_Rules`,
  `KPP_Working_Method` - section 10; the 1.2.0 site record for `KPP_LineTracker_Design` and the probe numbers for
  `KPP_COS_RegradeView_Design`. **(7) OPEN:** what changed on the PLC on 17 Oct about 17:50, and what was changed by
  07:48; the advisor install and its report; `ScanEncoderScale`; the scanner order; the COS regrade view (later) -
  section 11.
- v1.49.0 - REGISTRATION for the 2026-10-19_A session (the KPP Daily report and the Monday Weekly report showed two
  Stem vs Forecast figures for 1-18 Oct - forecast to date 59,258 against 66,800 on the same 67,819 m3; one chat, Mon
  19 Oct 07:42-08:31). Raw Log `2026-10-19_A` added; no 19 Oct log and no index ADD were in the project at close.
  **(1) Findings:** the daily is right - its line is the 1 Aug rule (`shared.dailyproduction` 4.7.14: predicted /
  days in the month per day, 102,056 / 31 x 18 = 59,258); `shared.weeklyreport` 0.8.1 was built beside daily 4.7.12
  and never got the 1 Aug fixes - predicted / scheduled shifts x 2 for every day, shut days included (102,056 / 55 x 2
  x 18 = 66,800): 62 / 55 = 12.7 % fast in October, 115,045 by the month end against 102,056; the two agree only in a
  month with no shut shifts. The same weekly code read `Production/DailyVolume_30d` (relative to today - day 1 dropped
  when a week ends on the 31st, past weeks in EmailReports empty) and the Monday's month for the month-to-date figures
  (1 Nov actuals against October's forecast). **(2) Delivered, not yet installed:** `shared.weeklyreport` **0.8.2** -
  the Month-to-Date bar and the chart on one basis built the daily's way (`_mtd_basis`: the Sunday's month, the daily's
  kpi_daily pull, calendar pro-rata, the daily's intro); the bar's pace rule, the weekly targets, scorecard and
  WeeklyStats unchanged; ASCII clean. Proven off the gateway: a CPython harness ran the old weekly, the new one and the
  live daily's block verbatim - the old code reproduced the screenshot, the new intro equals the daily's character for
  character (29 / 29). **(3) CORRECTIONS banked:** M1-M2 (Raw Log 2026-10-19_A section 5). **(4) Staged, not
  compiled:** `KPP_Reporting_Technical_Reference`, `KPP_Domain_Data_Reference`, `KPP_Working_Method` - section 6.
  **(5) OPEN:** the install and its check (the week of 12 Oct reads 59,258 / 114 %); the weekly MTD bar's forecast
  pace - scheduled shifts or calendar days (asked); the weekly's Daily Volume chart still on `DailyVolume_30d` for past
  weeks; `claude/KPP_HydPumpWatch_Design_v1_0_0` (17 Oct) is in the project but registered by no index or raw log -
  for its own session's close-out (section 9).
- v1.48.2 - second post-close addition to 2026-10-16_A (18 Oct 18:27 - 20:00): Raw Log `2026-10-16_A` **1.1.0 ->
  1.2.0** (section 14 appended, sections 1-13 unchanged). **(1) Designs:** `KPP_TrkAdvisor_Design` 1.0.0 -> **1.0.2**
  (the mark-off against what was just cut, T&B swaps, PE slip, a log taken off the sortline after a cross-up; NEW
  section 9 - the sortline scanner replacement); NEW `KPP_COS_RegradeView_Design` **1.0.0** (concept - the COS operator
  regrades on the spot, e.g. a missed prune, and the stem is re-optimised instead of a 12 m cut to the regrade bin).
  **(2) Delivered, not yet run:** `KPP_COS_Regrade_Probe_v1_0_0` (read only - COS regrades a day, their length, place
  in the stem, size, grades, who, the value at stake). **(3) Scanner to order:** Banner A-GAGE EZ-ARRAY 1200 mm, 4-20
  mA - `EA5E1200Q` + `EA5R1200PIXMODQ`, cordsets `MAQDC-815` / `-830`, `EZA-USB485-01` (advisor design 9). **(4)
  Findings (V20o):** COS overrides are console buttons (Regrade 8281, bin 10; button 6 the 12 m cut); Re-Optimize
  builds a type-14 packet but its send rung fires on a word nothing writes - it never reaches the optimiser; the grades
  go to the optimiser once, in the graders' type-11 defect packet (Pruned = type 1); possible `RemaningLength` bug after
  an A-saw manual cut. **(5) Staged, not compiled:** `KPP_Domain_Data_Reference` - section 14.1 items 16-19. **(6)
  OPEN:** order the scanner; run the two probes; USNR on a second defect packet for a solved stem and the re-opt time.
- v1.48.1 - post-close addition to 2026-10-16_A (18 Oct 17:48 - 18:25): Raw Log `2026-10-16_A` **1.0.0 -> 1.1.0**
  (section 13 appended, sections 1-12 unchanged). **(1) New design:** `KPP_TrkAdvisor_Design` **1.0.0** (concept - the
  gateway identity advisor: the split agreed with the user - the PLC tracks and kicks, the gateway decides which log is
  which when the PLC cannot tell; what the controller and the gateway hold per log; Tui's scan check; the score on
  length, SED, LED and volume; the window aligned to the COS cut order; the timing; the `Adv_*` mailbox; phases 0-3).
  **(2) Delivered, not yet run:** `KPP_TrkAdv_Geometry_Probe_v1_0_0` (read only, `sorter_logs` - phase 0's go / no-go).
  **(3) Findings (V20o):** Tui's `_065` checks length and volume only (SED_Y / LED_Y off); `_066` copies the first of up
  to 3 sortline slots either side that passes, centred (as written) on the newest log on the line; the scanner is a
  one-axis light curtain, its result in after the heads + 150 mm + about 190 ms; `sorter_logs` keeps the X diameters
  only. **(4) CORRECTIONS:** C1-C4 (Raw Log 2026-10-16_A section 13). **(5) Staged, not compiled:**
  `KPP_Domain_Data_Reference`, `KPP_Working_Method` - section 13.1 items 12-15. **(6) OPEN:** run the probe; then the
  shadow advisor (phase 1).
- v1.48.0 - REGISTRATION for 2026-10-16_A: the 2026-10-15_A chat went on from Fri 16 Oct 06:52 to Sun 18 Oct (no log
  of 16 or 17 Oct was in the project; `KPP_DigitalTwin_COS_Design` 1.2.0 already named this one). Raw Log
  `2026-10-16_A` added. **(1) Compiled docs bumped:** `KPP_LineTracker_Design` 1.0.1 -> **1.2.1** (1.1.0, 1.1.1 and
  1.1.2 on site, the WATCH run, 1.2.0 designed, the DATA run, 1.2.0 built and proven off the PLC - sections 14-18; the
  1.0.2 staging of 1.47.2 went into 1.1.0) and `KPP_DigitalTwin_COS_Design` 1.1.0 -> **1.2.0** (saved forecasts).
  **(2) Installed:** the regrade marks library `forensics.sortMarks` and its 20 tags (16 Oct 08:18); tracker 1.1.0 (16
  Oct evening), 1.1.1 (by 17 Oct 05:57) and 1.1.2 (17 Oct about 07:30) - each an online routine import and JSR repoint;
  Sortline Map 1.3.1 (the Tracker mode). **(3) Findings:** the T&B data comes 2.6 - 3.4 s before its landing; the
  landing PE loses a log for a stretch and sees it again; a kick returns on the other contactor 800 ms after full out;
  conveyor 2 is 0.2857 mm a count; TailDetect2 gives TailDetect1's signal; 1.1.2's positions and kicks are right and
  its identity losses (1.3 % ghosts) are in the data - the T&B sends the last message again instead of the next log's
  (9 of 205 on 18 Oct), every message carries its COS slot; the Logix driver serves no whole array as one OPC value.
  **(4) Delivered, not yet installed:** tracker 1.2.0 (six routine L5X files, 151 new tags, `Srt_CosMem` 0) with
  `KPP_Trk_Install_v1_2_0` and probe 1.6.0; the twin's saved forecasts (page 1.2.0, `twin.web` 1.1.0, doPost, table
  `public.twin_forecast`); the regrade marks 1.1.0 (map 1.2.1, SortlineBin 1.1.0, NQ `Sortline/BinMarks`, the glow);
  Sortline Map 1.3.2 (opens on Tracker). **(5) CORRECTIONS banked:** N1-N11 (Raw Log 2026-10-16_A section 8).
  **(6) Staged, not compiled:** `KPP_Platform_Rules`, `KPP_Working_Method`, `KPP_Domain_Data_Reference` - section 9.
  **(7) OPEN:** the 1.2.0 install and its RING / WATCH runs, the cases 1.2.0 cannot tell (to a gateway identity
  advisor - agreed 18 Oct as the next design: the plant does not run without the gateway, and it sees what the PLC
  cannot), the section 2 start ghosts,
  TailDetect2's wiring, the middle PE, the confirmations - section 12.
- v1.47.2 - post-close addition to 2026-10-15_A (15 Oct 13:40 to Fri 16 Oct 06:52): Raw Log `2026-10-15_A` **1.1.0 ->
  1.2.0** (section 13 appended, sections 1-12 unchanged). **(1) Installed:** `SortlineOverview_view_v1_2_0` (the
  Setpoints button now the Log Stop Positioning settings chip; a Sort Register button); the Sort Register live once its
  named query's Database was set to `KPP_production` (it was Workmate - the dropdown rule again). Probe 1.1.0 HISTORY:
  the scanner has read long logs about 1 % short since June and about 1.3-1.5 % since late September; logs to bins 3 +
  10 15.9 -> 20.8 per 1000, most of the rise COS regrades; `kpi.sortline_kpi` has nothing after mid-August. **(2)
  Conveyor 1 measured at the startup** (`KPP_Conv1_Calibrate_v1_0_0`, read-only, 15 Oct 19:59): 0.3034 mm a count (PE
  length fit 0.30348 +/- 0.00103; scanner over 72 h 0.3034). `ScanEncoderScale` 0.2997 -> 0.3034 recommended (not yet
  set; a 9 m log then kicks about 55 mm later); `Conv1Scale` 0.2850 stays - Tui's kick positions are set against it, its
  PE positions are true mm (32,651 counts between the section 1 start and pre-scanner PEs = 9,906 mm against Tui's
  9,940). **(3) The tracker switched on** (`Trk_Enable` 1, 19:40): PE2 matched 27 of 98 - the logs were made at PE2 with
  their T&B data. Put down to the scale at first; CORRECTED at the write-up (M14) - at 0.2850 the PE2 error is about
  -320 mm, inside a 2,000 mm window - so `KPP_Trk_Watch_Probe` before any PLC edit. **(4) The comms clean-up - a direct
  read 883 ms -> 57 ms** (22 Sep 47): the 22 Sep probe tags and `Diag_50ms` deleted; device Timeout 500 -> 2,000 ms, Max
  Concurrent Requests 16 -> 24, CIP Connection Size 500 (4000 tried, no gain); Default 1,000 -> 2,000 ms; a new Direct
  group `Diagnostics_5s` (5,000 ms) with 3,492 diagnostic tags (`KPP_Comms_DiagGroup_v1_0_0`); FastLeasedTags 250 -> 500
  and Discretes 500 -> 1,000 (leased rate, OPC UA publishing and sampling), LeasedTags leased 1,000 -> 2,000. The device
  Details page: about 246 requests a second asked against 165-185 answered, then about 162. Read-only `KPP_Comms_Survey`
  1.0.0 / 1.1.0. **(5) CORRECTIONS banked:** M7-M14 (Raw Log 2026-10-15_A section 13.4). **(6) Staged, not compiled:**
  `KPP_Platform_Rules`, `KPP_Domain_Data_Reference`, `KPP_Reporting_Technical_Reference`, `KPP_Working_Method`,
  `KPP_KickerHeat_Design`, `KPP_LineTracker_Design` (1.0.2) - section 13.5. **(7) OPEN:** `ScanEncoderScale`; the
  tracker watch probe and K2-K6; the regrade marker on the Sortline Map; the slower polls (kicker prox lights, COS
  Positioning Capture, the KickerHeat Overload members on LeasedTags); `kpi.sortline_kpi`; the optional comms items -
  section 13.7.
- v1.47.1 - post-close addition to 2026-10-15_B, and the merge of 1.46.1: Raw Log `2026-10-15_B` **1.0.0 -> 1.1.0**
  (section 12 appended, sections 1-11 unchanged) and `KPP_MachineSettings_Design` **1.0.0 -> 1.1.0**. **(0) Index
  history:** 1.46.1 (the 2026-10-15_A post-close addition) and 1.47.0 (this session's registration) were both built on
  1.46.0, minutes apart; this version carries both - the 1.46.1 entry below and its rows (`KPP_LineTracker_Design`, the
  2026-10-15_A raw log and deliverables, section 4). **(1) Installed on the gateway:** probe 1.0.0 OK 103 / CREATE 108;
  installer 108 tags and `sortline.manual_kick_event` (CHECK 1 of 108 Good - new tags on `LeasedTags` read
  `Uncertain_InitialValue` first; the next probe OK 211); the page in use. **(2) Findings and fixes:** the grading encoder
  scales are held x 1000 in the PLC (Echo showed 625 as 0.6250) and the saw pre-lower toggles exist (settings 1.0.1); the
  cut speed table and the saw prox windows built (1.0.2, 33 tags) and taken off at Adriaan's request (1.0.3,
  `KPP_MachineSettings_RemoveTags` 1.0.0 - 0 of 49 left); every editor opened on 2,130 (the Designer saves a persistent
  property's live value as its default, and `key` defaulted to `ls.stop.ref`) - views 1.0.1 seed per key; hidden rows
  showed (labels ignore `props.style.display` bindings - `position.display`); everyone saw VIEW ONLY -
  `{session.props.auth.user.roles}` reaches `runScript` as QualifiedValues - settings 1.0.4 and manual kick 1.0.1 unwrap
  them. **(3) Added:** manual kick for Big Balls as well as Sparky (manual kick 1.0.2, ManualKick 1.0.1); a setting
  changed in the last 48 h glows (settings 1.0.5; the project stylesheet's `wm-field-glow` and `wm-brand-a-glow`, no
  stylesheet change; SettingRow 1.0.2, SettingCell 1.0.1, ScaleCalc 1.0.2, AreaItem 1.0.1, MachineSettings 1.0.3); the
  settings watch (settings 1.0.6, `KPP_SettingsWatch_Install` 1.0.0, MachineSettings 1.0.4) - gateway timer
  `Settings_Watch` (10 s, dedicated) logs a change made outside Ignition (Echo, Studio 5000, the PLC program) in
  `setpoint_history` as `outside Ignition` after a 20 s wait for an Ignition row, baseline in `public.setpoint_watch`;
  the table made and the timer running 15:24 (198 tags, all readable). **(4) CORRECTIONS banked:** M13-M16 (Raw Log
  2026-10-15_B section 12.4) - M14-M16 reached the gateway (the 2,130 editor, the hidden rows, VIEW ONLY for everyone).
  **(5) Staged, not compiled:** `KPP_Platform_Rules` / `Workmate_Perspective_Rules`, `KPP_Working_Method`,
  `KPP_Domain_Data_Reference`, `KPP_Reporting_Technical_Reference` - Raw Log 2026-10-15_B section 12.7. **(6) OPEN:**
  C2-C11, the install of manual kick 1.0.2 and the glow views, the watch's first outside change, `VolumeScaleAdjustEnable`
  XIC or XIO, the RMC set-scale buttons, the half-turn member (Raw Log 2026-10-15_B section 12.8).
- v1.47.0 - REGISTRATION for the 2026-10-15_B session (the last Echo screens - Machine Settings 1-4, Sort Line Settings
  and Manual Kick Control on FactoryTalk View SE - rebuilt in Ignition Perspective; one chat, Thu 15 Oct from about
  10:10; lettered B - 2026-10-15_A was in the project). Raw Log `2026-10-15_B` added. **(1) New compiled doc**
  `KPP_MachineSettings_Design` **1.0.0**. **(2) Findings:** every Echo settings tag mapped onto `COS_PLC_1756CPU` - 206
  settings (102 with an Ignition tag already, 104 new) plus 5 manual kick command tags; the PLC spells `RefererncePos`;
  `DisableSickPEArrays` is inverted against Echo's wording; the COS conveyor encoder scales reach the RMC only with
  Echo's "Set encoder scale in RMC" (not in the sheet) - view only; Echo's short / long stem grading kick positions are
  one PLC member; eight Echo fields have no tag in the sheet (`ECHO_GAPS`); manual kick runs on Echo's own bits
  (`LSL_Sorter.KickerJog.*`, `LSL_Sorter.KickerManualKick.*`). **(3) Built, tested off the gateway, not installed:**
  `engineering.settings` 1.0.0 (the catalog, the feeds, the checked write with PLC read-back and `setpoint_change()`),
  `engineering.manualkick` 1.0.0 (Sparky only; hold-to-jog with a gateway dead man, two-press kick,
  a gateway lock and the command bits confirmed off before any number changes, watchdog timer `ManualKick_Watchdog`
  with a heartbeat jog and kick check, `sortline.manual_kick_event`), the Machine Settings page (`/Engineering/Settings`, seven areas in plant order, cards
  balanced over 1-4 columns from `page.props.dimensions`), six components, the SettingEditor and ManualKick popups,
  EngineeringMenu 1.4.0 (Setpoints -> Settings); probe and installer 1.0.0. **(4) CORRECTIONS banked:** M1-M12 (Raw Log
  2026-10-15_B section 5), all caught before delivery - M6 only by rendering the views, M7 (non-persistent custom props
  with no binding do not exist at runtime) and M8 (a kicker number that could change under a running jog) by an
  independent review - 12 findings, all acted on except tag write permissions (section 6), M9 (`onStartup` without
  `import system`) and M10 (`import threading`, shadowed here by the `operator` package) by reading
  `KPP_Platform_Rules`; a second review of the fixes - 7 findings, the top one a watchdog timer nothing proved was
  running (now a heartbeat that jog and kick check) - and a third check of those - 4 findings (a slow release eating the
  tap bounce, a hung audit insert hiding the bits from the watchdog, a prune race, the wall clock) - and a fourth, clean
  of anything above LOW - all acted on (section 6); M11 (a kept jog blinding the watchdog) and M12 (the Script Console's `getGlobals()` is the Designer's)
  while implementing them. **(5) Staged, not
  compiled:** `KPP_Platform_Rules` / `Workmate_Perspective_Rules` (an input in a flex row keeps its own width; a layout
  from `page.props.dimensions`; balanced columns; non-persistent props; `getGlobals()` belongs to its JVM; ages and
  waits on a monotonic clock),
  `KPP_Working_Method` (look at the views before delivery; an HMI action that moves machinery), `KPP_Domain_Data_Reference`
  (the Echo settings on the one controller) - Raw Log 2026-10-15_B section 10. **(6) OPEN:** the install and checks C1-C9, a PLC jog timer, tag write permissions,
  the nudge directions, the PE check window and anti-sap members, KickerToJog for bays 1-2, the `ECHO_GAPS` fields,
  retiring the old popups and FTView.
- v1.46.1 - post-close addition to 2026-10-15_A: Raw Log `2026-10-15_A` **1.0.0 -> 1.1.0** (section 12 appended,
  sections 1-11 unchanged). **(1) The tracker is in:** imported, verified and downloaded in the shut with no faults (K1,
  Run about 11:17); the fault test K7 passed with the line down (`Trk_LastFault` 4020). CORRECTION: the scan time is
  elapsed time - 2,186 us with the tracker OFF (the higher-priority 10 ms tasks) - so the 1.0.0 sheet's "over 2000 us
  switch off" was wrong; `KPP_Trk_Install_v1_0_1.txt` judges the rise. **(2) The regrade pile (Bryce, 12:06):** Tui's
  regrade routing read from V20o (`_065` / `_066` scanner check, data copy from a matching COS memory, over 8.7 m to bin
  3, else bin 10; COS manual cuts and regrades to bin 10); Tui's decisions to 3 + 10 rose from 10-15 to 19-24 per 1000
  logs, most from COS regrades; bin 2's 9.6 m logs scan 135 mm short (median) against a 150 mm window - 1 in 6 to bin 3,
  and Bryce confirmed those logs are in spec (false regrades); the scanner reads about 1.2-1.4 % short; bins 4 / 5 are
  not Tui's regrades (physical, bay 2); a sortline chain section was replaced - theory: a changed mm per count moves the
  scanner and Tui's kicks together; no scale change before the tracker measures conveyor 1 after startup. **(3) Built:**
  `KPP_SortRegrade_Probe` 1.0.0 (run) and 1.1.0 (weekly history since May from `kpi.sortline_kpi`), the **Sort
  Register** 1.0.0 (named query `Sortline/SortRegister`, view `Application/Sortline/SortRegister`, page
  `/sort-register`) - where Tui sent every log and why, for the team. **(4) Staged** (Raw Log 2026-10-15_A section
  12.4): `KPP_Domain_Data_Reference` (the regrade routing; sorter_logs is written before the kick; `kpi.sortline_kpi`),
  `KPP_Platform_Rules` (named queries substitute only declared parameters; test SQL on a local PostgreSQL),
  `KPP_Working_Method` (an export is a data source; ask quality before fixing a measurement). **(5) OPEN:** the chain
  date and section, the history output, the tracker's conveyor 1 measurement after startup, bins 4 / 5 into 3, COS
  regrades, the Sort Register install.
- v1.46.0 - REGISTRATION for the 2026-10-15_A session (the shut day, 15 Oct: the script read rate, then the KPP Line
  Tracker - a new sortline tracking in Structured Text beside the Tui code). Raw Log `2026-10-15_A` added. **(1) New
  compiled doc** `KPP_LineTracker_Design` **1.0.1** (1.0.0 went to Adriaan for sign-off and is superseded - not in the
  project knowledge). **(2) The read rate:** `KPP_COS_ReadRate_Probe_v1_0_0` - verdict C, the Ignition driver, not the
  PLC: about 244 ms a request (47 ms on 22 Sep), the tags changing about every 0.93 s, the PLC values fresh; the
  leftover `Diag/LogStopProbe` tags (19, on the 50 ms Direct group `Diag_50ms`) still enabled - delete them, then the
  device status and settings, one change at a time. **(3) The tracker:** program Trk in a new periodic task Tracker (10
  ms, priority 14) in COS_CPU - 17 ST routines, 146 program tags, 7 data types (`Trk_Piece`, `Trk_Seg`, `Trk_Station`,
  `Trk_Event`, `Trk_Area`, `Trk_Kick`, `Trk_FaultRecord`); shadow only (reads the sortline encoders, raw PEs, kicker
  contactors and T&B data; writes only its own tags), its own fault routine, `Trk_Enable` 0 after the download. Proven
  off the PLC: a static check against the V20o export of 15 Oct 06:30 and a scan-level simulation of the delivered ST
  with Logix semantics against a physical sortline - 18 scenarios pass (80 logs: every kick by the right piece into the
  right bin, match error at most 10 mm; scale error, missing data, dead and bouncing PEs, counter wrap, a full pool, a
  fault and the K7 fault test, stops, a power loss, the bay 1-2 "b" kickers, a 25-minute soak). An independent review of
  the L5X before delivery found no blocker; from it the bay 1-2 "b" kicker contactors are read too (Tui fires "b" with
  "a"; a tripped "a" leaves "b" alone), the K7 fault test `Trk_TestFault` was added, and the restart on `S:FS` (found in
  parallel) went in. **(4) Deliverables:** `KPP_Trk_Program_v1_0_0.L5X` (Import Program, offline, then download in the
  shut), `KPP_Trk_Install_v1_0_0.txt`, read-only `KPP_Trk_Watch_Probe_v1_0_0.py`. **(5) Staged** (Raw Log 2026-10-15_A
  section 10): `KPP_Platform_Rules` (the Logix ST semantics an off-PLC proof must copy; the driver-queue signature; a
  tag and a data type never share a name; the V20o controller fault handler clears type 3 and 4 faults, not a watchdog;
  restart on `S:FS`), `KPP_Domain_Data_Reference` (bays 1-2 have two kickers, "b" fires with "a"), `KPP_Working_Method`
  (simulate the delivered ST against a physical plant, scan by scan, and test the test; a new tracker goes in beside the
  old one, reading only). **(6) OPEN:** the download and the switch-on (K1-K7), the comms clean-up, tracker slice 2 (the
  gateway side), the restart time; from 2026-10-14_D the twin 1.1.0 on Live and the booth map glide.
- v1.45.1 - post-close addition to 2026-10-14_D: Raw Log `2026-10-14_D` **1.0.0 -> 1.1.0** (section 11 appended,
  sections 1-10 unchanged) and `KPP_DigitalTwin_COS_Design` **1.0.0 -> 1.1.0**. The twin went onto Live in the evening
  (the zip, page 1.0.0, three.js, page `/twin`). `twin.live.check()` listed 34 bad keys - PLC members no view uses, so
  the Ignition folders had no tag for them (`StemQueue/Conveyors_n_` members, `VaxData_n_/Bin`, `LogStopConv`
  `LogData_4_-7_`); `KPP_Twin_MissingTags_v1_0_0.py` created them read-only from working siblings - PASS, then 0 bad.
  The live picture moved stop-start: page 1.0.0 interpolated whole-plant snapshots (one about every 0.3 s, the tag
  groups refreshing out of step) while each PLC value changes about every 0.7 s - delay 0.4 s, so stems glided and
  stood; the 1.0.0 test mock updated every value in step and hid it. Page `KPP_Twin_COS` 1.1.0 smooths each value
  between its own changes, timed by the tag timestamps `twin.live` 1.1.0 now returns (`ts`; cache 100 ms; poll 200 ms;
  the picture about 1.2-1.5 s behind) - on an asynchronous mock 27 % -> 0 % of moving frames standing still. Delivered
  21:45, not yet confirmed on Live. Faster script reads would not help (the read takes 4-90 ms; the PLC's 0.7 s refresh
  is the limit). The booth maps (COS, GRA, TNB, Sortline) step for the same reason - the SDB Map glide offered, COS Map
  first. Staged: `KPP_Platform_Rules` (missing members in per-view folders; per-value smoothing on tag timestamps),
  `KPP_Working_Method` (an asynchronous timing fixture; the kymograph), `KPP_Reporting_Technical_Reference` (the twin on
  Live) - Raw Log 2026-10-14_D section 11.
- v1.45.0 - REGISTRATION for the 2026-10-14_D session (the KPP Digital Twin, COS first - a 3D view of the whole line for
  a 3840 x 2160 screen with LIVE data, a 60-minute REPLAY and a simulator with dials; one chat, Wed 14 Oct about
  14:40-16:50; lettered D - A, B and C of 14 Oct were in the project). Raw Log `2026-10-14_D` added. **(1) New compiled
  owner** `KPP_DigitalTwin_COS_Design` **1.0.0**. **(2) Findings:** a WebDev page that shows live tags needs a
  Perspective view holding them - `system.tag.readBlocking` holds no lease, so the twin view carries a 352-tag
  expr-struct lease keeper; the COS PLC's 0.7 s update puts the smoothed picture about 0.8 s behind; the plant in one
  frame (X = 0 at the COS A saw; GRA from `LocationOffsets[2]`, T&B 16.0 and SDB -133.8 estimated) with 11 conveyor
  lengths and their sources; the model calibrated to the 8-9 Oct audit - 114.5 stems an hour, 31.4 s a stem = 27.4
  untouched + 1.2 touches + 1.6 drops + 1.2 waiting (audit 113.1 / 31.8 = 27.5 + 1.0 + 1.6 + 1.6) - with residuals that
  cancel under the totals (first cut +0.8 s, later stop cut about -2 s, stopless about +0.9 s, 1.16 later cuts a stem
  against 1.02, T&B stops 15 against about 26 an hour); in the model infeed follow takes 1.5 s a stem off untouched auto
  but at today's supply the COS then waits for stems (no gain), with stems always ready it is worth +8.5 % and the
  outfeed / T&B becomes the next limit; the braking curve on stopless cuts costs about 0.6 s a stem. **(3) Built, tested
  off the gateway, not installed:** page `KPP_Twin_COS` 1.0.0 (three.js r128 from the gateway folder), `twin.live` 1.0.0
  (352 tags, one read cached 200 ms), `twin.web` 1.0.0 (ui / lib / live / health), WebDev `twin` doGet 1.0.0, view
  `Application/Twin/TwinCOS` 1.0.0, import zip `KPP_Twin_import` 1.0.0; no new tag, PLC change or table. **(4) Staged,
  not compiled:** `KPP_Platform_Rules`, `KPP_Working_Method`, `KPP_Domain_Data_Reference`,
  `KPP_Reporting_Technical_Reference` - Raw Log 2026-10-14_D section 9. **(5) OPEN:** the install and the commissioning
  checks C1-C11 (the log stop conveyor `CurrentPosition` lead or trail, the T&B datum, saw heights, the stop lowered
  signal, the estimated speeds); phase 2 - replay from `cos_moves` / `pa_cos_cut`, per-cut calibration, the outfeed stop
  model, the SDB / GRA / Chippers areas.
- v1.44.0 - REGISTRATION for the 2026-10-14_C session (the Reception Hub Length / Volume / Stems against the KPP Daily
  Report - the team leaders' question; one chat, Wed 14 Oct, 08:11-10:05 and post-close from 10:39, on the same 07:56
  export as 2026-10-14_A; lettered C - the Hub Pulse log reached the project first). Raw Log `2026-10-14_C` **1.1.0**
  added. **(0) Index history:** at close this session was first registered as `2026-10-14_B` (10:32 - a 1.43.0 that
  missed the Hub Pulse ADD, its raw log written over that session's claude/ copy), then in a 1.43.1 built on 1.42.0
  plus the ADD; both removed from the project - this version is built on the Hub Pulse chat's full 1.43.0 (Raw Log
  2026-10-14_C M3 and section 11). **(1) Findings:** the Hub gauges read the DB query tags
  `KPP/General/Data/Production/{Current,Previous}Shift/*` on `report.stems_by_shift` - Length the RECOVERED length (cut
  logs added up per stem, `kppstems.stems`), Stems primary pieces only (Length and Volume summed every piece) - while
  the Daily Report reads the PLC scanned counters (`cos_kpi_data` -> `prod_summary`); the report's own shift card read
  the Hub tags. The Hub's way of counting was Echo's, kept at the 25 Jun cutover for continuity. 13 Oct night: Hub
  28,961 m against report 30,131.5 m - trim about 143 m (USNR 0.5 %) and about 1,027 m (3.4 %) scanned with no stem row
  (volume the same, 3.6 %); pieces 1,172 captured / 1,196 grading / 1,235 USNR; `TransformationsStemLengthsLastShift`
  is the USNR stem length (30,287 m). **(2) Built and live:** the Hub Length / Volume tags on the PLC meter - current
  OPC on the booth items (group Default), previous `cos_kpi_daily` (09:10, CHECK 4 of 4); probe
  `KPP_HubLength_vs_Report_Probe` 1.0.0; `report.stems_by_shift` 1.1.0 (08:52, Stems every piece) - withdrawn, see (3).
  **(3) Delivered, not confirmed:** `report.stems_by_shift` 1.2.0 - a broken stem's 2nd piece adds its length and
  volume but is not counted as a stem (Adriaan 10:42; the 1.0.0 counting, `NULLIF` on `piece_size`), applier 1.2.0;
  projection rate NQs `Stems/Projections/Stem Length Rate` / `Stem Volume Rate` 2.0.0 (`cos_kpi_data`, last 20 min).
  **(4) CORRECTIONS banked:** the first reply had Length primary-only and the gap mostly trim (M1, M2); the 08:40
  "count the 2nd pieces also" answered M1 and was acted on as a Stems change (M4); `KPP_Reporting_Technical_Reference`
  section 7's "in-flight stem, regrade decrements" is wrong (staged). **(5) Staged, not compiled:**
  `KPP_Reporting_Technical_Reference`, `KPP_Domain_Data_Reference`, `KPP_Working_Method`, `KPP_Platform_Rules`,
  `DashboardandPLC_Knowledge_Standard` - Raw Log 2026-10-14_C sections 9 and 11. **(6) OPEN:** apply view 1.2.0, then
  the team-leader email; the projection NQs; the 19:00 boundary; the 3.5 % capture shortfall (missed stems or re-scans;
  and whether Echo ran the same before 25 Jun); the Safety overview shift card and the Hub Avg gauges still on the stem
  rows (the Avg gauges count every piece); the Hub's dead params (C1).
- v1.43.0 - REGISTRATION for the 2026-10-14_B session (Visitor Sign In PLANT SHUT badge; the shut-day kiosk return; Hub
  Key Metrics icons; the Hub revamp - Workmate Pulse; banner stats; one chat, Wed 14 Oct 09:09-10:22). Raw Log
  `2026-10-14_B` added. **(1) Findings:** the badge read NQ `Production/Shuts/ForDate` (DateTime param fed a string,
  json format) - not reproduced in the console, root cause unconfirmed, path changed to `schedule.kpp.getShut`; 15 Oct
  is a day-shift shut; the shut schedule is mostly single-shift (13 shut days in 26 weeks, 1 full); `material/approval`
  and `material/inventory_2` are not in the icon set; `WO_C_header.Entry_date` and `WO_C_Details.Closed_Date` exist;
  the banner's Open WOs counted only WOs raised, Stems / Lengths are per-shift ProdStats counters. **(2) Built and
  live:** `workmate.hubpulse` 1.0.0 -> 1.0.3 (Workmate Pulse - backlog, PM health, work calendar with shut days, age,
  bad actors, PO spend, live feed, tile KPIs; `mine()`), Hub 1.16.0 -> **1.16.1**, `Components/HubPulse/FeedRow` 1.0.0,
  Hubheader **1.5.0** (shut from `schedule.kpp`; Reception shut-day 2-minute return to the visitor Menu on
  `session.props.lastActivity`, countdown pill), Visitor Menu **2.9.0**; probe `KPP_Hub_Probe` 1.0.0 PASS 10:05.
  **(3) CORRECTION banked:** Hub 1.16.0 collided with the 2026-08-16_A `Hub_View_v1_16_0` (M1); Pulse 1.0.0 hatched only
  full shuts (M2). **(4) Staged, not compiled:** `KPP_Platform_Rules`, `KPP_Domain_Data_Reference`,
  `KPP_Reporting_Technical_Reference`, `Workmate_Knowledge_Journal` (cross-reference), `KPP_VisitorSignIn_Audit` - Raw
  Log 2026-10-14_B section 9. **(5) OPEN:** the 15 Oct shut-day kiosk (06:00 open, 2-minute return, pill, badge "Day
  shift shut"); the badge on a normal day; the length tag unit; archive HubCharts T1-T6.
  `DashboardandPLC_Knowledge_Index_ADD_2026-10-14_B` merged and retired.
- v1.42.0 - REGISTRATION for the 2026-10-14_A session (the MLD monthly summary gave two different Augusts - Jen; one
  chat, Wed 14 Oct). Raw Log `2026-10-14_A` added. **(1) Findings:** `shared.mlyproduction` 0.3.0 passed exclusive
  07:00 ends (the 1st of the next month 07:00; today 07:00) to the MLY by-day NQs, which since v3.0.0 (2026-08-06)
  include the END DATE in full - so the August email (built about 07:37 on 1 Sep by the LogData clock) carried 1 Sep's
  first 112 logs (44.3 m3, 685 m) and 1 Sep as a 30th production day, while the September email's August column
  (calendar-month buckets) did not. August is 56,612.1 m3 / 725,448 m / 136,828 logs / 29 days; the September email
  matched calendar September exactly. The daily emails carried the next morning's scans before 07:04 (3-42 logs on 5 of
  8 mornings); downtime sections unaffected; the EmailReports MLY Monthly tab added the whole next 1st on a re-render.
  **(2) Built and live:** `shared.mlyproduction` 0.3.1 (inclusive dates for daily, monthly, history, trend and MTD;
  `_first_of_month`; the monthly downtime end), probe `KPP_MLY_MonthBoundary_Probe` 1.0.0 - LIBRARY FAIL on 0.3.0, PASS
  on 0.3.1 (08:35). **(3) CORRECTION banked:** the first read put the August build at the 07:10 schedule and the
  September column inflated by 1 Oct - both wrong (M1). **(4) Staged, not compiled:** `KPP_Platform_Rules`,
  `KPP_Reporting_Technical_Reference`, `KPP_Working_Method`, `KPP_Domain_Data_Reference` - Raw Log 2026-10-14_A section
  9. **(5) OPEN:** the reply to Jen; the 07:37 build - a manual send, or the LogSorter clock about 27 min ahead; the
  first sends on 0.3.1 (15 Oct daily, 1 Nov monthly).
- v1.41.1 - post-close addition to 2026-10-13_A: Raw Log `2026-10-13_A` **1.0.0 -> 1.1.0** (section 11 appended,
  sections 1-10 unchanged) - the 17:01 morning check (nothing new after smoko) and the project knowledge cleanup:
  `KPP_PEWatch_Morning_Check_v1_1_1.py` added; superseded index versions, Domain Data Reference 1.8, the morning check
  1.0.0, the P5 probe 1.0.0 and claude/ duplicates of root files deleted (section 4). Raw logs NOT consolidated (a
  retyped archive cannot be checked against the append-only originals); three same-name raw log pairs left to sort in
  claude.ai. One `KPP_Working_Method` rule staged (Raw Log 2026-10-13_A section 11).
- v1.41.0 - REGISTRATION for the 2026-10-13_A session (Anomaly Watch event review; no judging on smoko unless the COS
  booth is logged in; WallControlPEs out of the judging while the Sonics is out; one chat, Tue 13 Oct). Raw Log
  `2026-10-13_A` added. **(1) Findings:** of 22 events in 8 h, five were false - four WallControlPEs "blind ... sweep on
  failover" HOT (the wall PEs no longer trigger the sweep: the Sonics is out and the Sweep PE arrays trigger it,
  2026-10-12_A) and the 15:16 COS_ConvPreArrayStemDetect "sees nothing" HOT (the 15:00 smoko window, its chatter upstream
  PEArray3 counting with no stem through the COS); the rest real (DB_Infeed flicker, PEArray3 stuck - both cleaned 12:35;
  CHP disc 1 sensor blip; Kicker 10 heat). `public.booth_operator_history` writes an operator-NULL row on logout that
  covers the smoko; no COS login in any of the 12 smokos of 10-13 Oct, 0-1 stems each. **(2) Built and live:** registry
  `forensics.peWatchReg` 1.6.0 (WallControlPEs returning), judge `forensics.peWatchJudge` 1.4.2 (SMOKO 10:30-11:00 /
  15:00-15:30 day and night not judged unless a COS login with an operator covers half the window; no SILENT in the first
  window after; WALL only while WallControlPEs is manual; `smoko_now()` / `break_now()` / `break_windows()`), morning
  check 1.1.1, smoko probe 1.0.1 - proven by the 16:00 morning check. **(3) Delivered, not confirmed:** Anomaly Watch
  1.13.0 (encoders not judged on smoko, smoko history lines). **(4) CORRECTIONS banked:** judge 1.4.0 / probe 1.0.0
  counted the operator-NULL rows as logins (M1); the first window after a smoko carried the smoko's silent run (M2) - never
  install judge 1.4.0 / 1.4.1 (section 4). **(5) Staged, not compiled:** `KPP_PEWatch_Design`, `KPP_AnomalyWatch_Design`,
  `KPP_Domain_Data_Reference`, `KPP_Working_Method` - Raw Log 2026-10-13_A section 9. **(6) OPEN:** confirm Anomaly Watch
  1.13.0 and the first smoko lines (22:30); any other break; WallControlPEs back to manual when the Sonics returns; the
  morning check on the judge's link results.
- v1.40.0 - REGISTRATION for the 2026-10-12_A session (the Debarker outfeed auto sweep back on the Sweep PE array; one
  chat, Mon 12 Oct, closed Tue 13 Oct). Raw Log `2026-10-12_A` added. **(1) Findings:** in V20n (12 Oct 10:38)
  `Outfeed._220_OutfeedSweep` R4 starts the auto sweep on the Wall Control PEs (`PE_SweepArrayPE1` / `PE4`, 500 mm
  before the wall, for the Sonics tool - Jacob, Tui) with a failover on the Sweep PEs' blocked distance at
  `SDB_OFSpeedReduction_FailoverDist` 4500 mm; the rung before the change is in neither V20n nor the project knowledge;
  `_221` puts the kick at `SweepPos` 3500 less a speed correction (800 -> 3050 mm over 50 -> 70 m/min) - 450 mm past the
  Sweep PEs at the 100 m/min run-fast speed; R20's `SlowForSweep` unlatch is AFI'd; the Debarker "Sonics Tool" rung
  ramps the feed (`SDB_OFSpeedReduction_*`); a full-controller L5K's values decode against the datatypes (a value read
  by eye misled once - M1). **(2) Delivered, import not confirmed:** `_220_OutfeedSweep_v1_1_0` - R4 only, behind the
  new program BOOL `UseSweepArray` (0 = the wall array as now, 1 = the Sweep PE array at `SpeedCompSweepPos`) - built
  from the L5K as a minimal-context routine L5X with an install sheet and fallback rung text; proven off-PLC (checker
  over all 64 live Outfeed rungs and 7 planted faults; switch 0 equal to the live rung in all 294,912 single-scan states;
  switch 1 kicks once per stem on the Sweep array). **(3) Carried:** the Processing Analytics builder loss (1.39.1 OPEN)
  verified in the 12 Oct 17:23 export and logged in Raw Log 2026-10-12_A section 2 - still OPEN. **(4) Staged, not
  compiled:** `KPP_Platform_Rules`, `KPP_Working_Method`, `KPP_SDB_StemTracking_Reference` - Raw Log 2026-10-12_A
  section 9. **(5) OPEN:** the install and whether the minimal-context import goes in clean; the kick point on the floor
  (`SweepPos`); a pre-Sonics backup to confirm the reconstruction; the Sonics slow-down rung - keep or retire; the PA
  rebuild and backfill.
- v1.39.1 - post-close addition to 2026-10-08_A: the Claude Doc "COS Stem Cycle Audit - 8-9 Oct 2026" loaded into the
  project knowledge as `KPP_COS_StemCycle_Audit_2026-10-09_v1_0_0.md` (raw - an analysis of record; the bridge chart as a
  table; a Word copy `.docx` alongside) and registered under raw sources. **OPEN, found 12 Oct (to be logged with the next
  raw log):** the Processing Analytics builder is gone from the project - in the 12 Oct 17:23 export
  `script-python/analytics/processing` is itself a script resource (`resource.json`, `files: []`, actor `external`,
  Mon 12 Oct 10:41:18) and the `cos` script nested in it has vanished, the trap that emptied `schedule` three times
  (`KPP_Platform_Rules` 1.14). Timer `PA_COS_Build` fails from then, so Processing Analytics stops at 10:41 (the 12 Oct day
  shift showed Willie H only - no stem after 10:41 was built) until `processing` is rebuilt as a plain
  package with `cos` inside and the gap is backfilled. No other package in that export is also a script resource.
- v1.39.0 - REGISTRATION for the 2026-10-08_A session (the COS stopless approach behind `BA_Enable`, hand clamps,
  COS Moves and Processing Analytics - the stem cycle audit of 8-9 Oct, the cut timing probe, COS Watch operator buttons
  and the T&B link, the Grading seq deck reverse switch for Sparky; one chat, 8-11 Oct, closed 12 Oct - registered after
  2026-10-09_A and 2026-10-10_A, which closed first). Raw Log `2026-10-08_A` added. **(1) Findings:** on stopless cuts
  the infeed and log-stop conveyors ran 2.6x / 2.4x the COS command in the last 600 mm, the approach surged after the
  DT50 slowdown and lurched at 150 mm, the A clamps pre-closed on a moving stem, R27 / R20 re-geared a butt with a Stop
  request and `_055` R26 applied run-slow twice; a stem clamped by hand while moving runs on 188-241 mm; the 1 s
  positioning capture missed most cuts; two reads of a busy PLC ring in one OPC batch come from different scans. The
  audit over 1,865 stems (8-9 Oct): 31.8 s a stem now, 27.5 untouched auto, 23.3 at the booth's best - leaving the COS
  in auto +3 %, the outfeed stops and the waits for stems about +5 % each, half the gap to the best in auto itself; most
  of the gap between operators is the wood. `LogLoaderRevallow` ON gives a 10 min reverse window (`tSeqDeckRev`), OFF no
  limit; its External Access was Read Only. **(2) Built and live:** `_102_COS_ButtApproach` 1.0.0 with `_100` 1.2.0,
  `_110` 1.1.0 and `_055` 1.1.0 (tried 8 Oct; `BA_Enable` at close not recorded); `_261_COSMoves` 1.0.1,
  `kppstems.cos_moves`, `forensics.cosMoves` 1.0.2 (recording from 8 Oct 19:55); Processing Analytics 0.1.x
  (`kppstems.pa_cos_*`, timer `PA_COS_Build`, NQs `Analytics/Processing/COS/*`, page `/Analytics/Processing`); P1
  GainsAudit and the Claude Doc "COS Stem Cycle Audit - 8-9 Oct 2026"; the COS Watch operator page
  (`forensics.cosWatchOp` 1.0.0, `/coswatch-op`) in use 10 Oct; the T&B COS WATCH button; the SeqDeckRev tags (PASS).
  **(3) Delivered, not confirmed:** `_260` 1.2.0 (flag 30 hand clamp), Log Stop Positioning view 1.2.0 / help 1.3.0 /
  NQ 1.2.0, PA 0.1.1 with side menu 1.9.0 (Analytics for every login), operator page 1.1.0, T&B 1.2.1, Grading 1.4.0;
  P2 CutTiming to run on Mon 12 Oct. **(4) CORRECTIONS banked:** T&B and Grading Overview 1.0.0 were built on the 8 Oct
  export - never import (section 4); P6 1.0.0 counted rows with no target as BA; `cosMoves` 1.0.0 lost events (slot
  from `MV_Head`); the independent review's seven findings went in before delivery. **(5) Staged, not compiled:**
  `KPP_Platform_Rules`, `KPP_Working_Method`, `KPP_Domain_Data_Reference`, `KPP_COSWatch_Design`,
  `KPP_COS_StopApproach_Spec`, `Workmate_Perspective_Rules` (cross-reference) - Raw Log 2026-10-08_A section 9. COS
  Moves and Processing Analytics have no compiled owner - a new `KPP_ProcessingAnalytics_Design` is proposed (item 21).
  **(6) OPEN:** Monday's booth session and P2; `BA_Enable` and the BA decision; the installs; hand clamps by operator
  (P7); the PA reference after a week; the outfeed stops and the waits for stems; retention for `cos_moves` /
  `pa_cos_cut`.
- v1.38.0 - REGISTRATION for the 2026-10-10_A session (sweep auto tiles on the TNB, SDB and GRA maps; the Debarker stem
  diameter card; one chat, Sat 10 Oct). Raw Log `2026-10-10_A` added; `DashboardandPLC_Knowledge_Index_ADD_2026-10-10`
  merged and retired. **(1) Findings:** each sweep's PLC auto bit - `COS_OF_Area.TnBSweep` / `PulpDeckSweep` /
  `DrumChipperSweep` `.SweepInAuto`, `SDB_Outfeed.Sweep.Auto` (short and long stem arms), `Grading.Sweep.SweepInAuto`
  (Sweep 1 and 2); Ignition tags already existed for the Pulp deck, Drum chipper and Debarker bits, none for T&B or
  Grading, and no view showed any of them; the desk auto buttons and lamps (COS outfeed `COS_OF_Area.IO`, Debarker
  `SDB_Outfeed.IO`); `TnB_AutoButtonPressCount` 22,230; the Drum chipper sweep is not used (Adriaan); one structure item
  fails a whole OPC read batch (`Bad_Failure`); `lineHeight: 1` labels draw scroll arrows; the TNB Map's Bin 0 panel and
  T&B sweep setpoints button show on the Safety cards. **(2) Built and live:** tags
  `KPP/COS/OF/Data/TnBSweep/SweepInAuto` (07:41) and `KPP/Grader/Data/Sweep/SweepInAuto` (08:25), both read only, PASS
  on read-back; `SweepAutoTile` 1.0.0 and TNB Map 1.2.7 on screen (07:44, all AUTO). **(3) Delivered, import not yet
  confirmed:** `SweepAutoTile` 1.0.1, TNB Map 1.2.9 (T&B and Pulp deck tiles, hidden on the Safety cards), SDB Map
  1.3.0, GRA Map 1.1.1, Debarker Overview 1.3.1 (the stem diameter card to the reference picture); two read-only probes.
  **(4) CORRECTION banked:** the SDB and GRA maps were first issued as `SDBMap_view_v1_1_0` / `GRAMap_view_v1_1_0` with
  the root renamed - the SDB name clashed with the retired 2026-09-25_A SDB Map 1.1.0 and map roots stay `root`; never
  import either (section 4). **(5) Staged, not compiled:** `KPP_Platform_Rules`, `KPP_Domain_Data_Reference`,
  `KPP_TnB_Bin0_Design`, `KPP_Working_Method`, `Workmate_Perspective_Rules` (cross-reference) - Raw Log 2026-10-10_A
  section 9. **(6) OPEN:** the imports; a desk test of each auto button; hide the Bin 0 panel on the Safety cards; tiles
  on the COS Overview; T&B auto button presses per shift.
- v1.37.0 - REGISTRATION for the 2026-10-09_A session (PE Watch link scoring, the sun on Section1Start, the chipper
  knife cards, the motor work log, the PE and encoder baseline check; one chat, 6 and 9 Oct). Raw Log `2026-10-09_A`
  added. **(1) Findings:** judge 1.2.0's link checks replayed over 1-6 Oct (S4) took runs of small logs past TED3, a
  13-over-12 on SweepPEs, COS_Conv against its chattering upstream, PEArray3's chatter and a healthy size element for
  misses - fixed in 1.2.1 / 1.2.2 before anything reached the rows; Section1Start goes blind in the low evening sun
  (18:15-18:45 on 2, 4 and 5 Oct, sun due west 6-11 deg up, Scanner still counting - confirmed by Adriaan); the
  Downtime History opened on the Designer's saved range (no onStartup); the knife cards stopped at 28 / 29 sets (the
  history window) and stayed red after a change (120 min grace); two button rules wrote `cm.knife_change`; the PE cards
  read LEARNING whatever the judge held. S5 (9 Oct): the 4 Oct set holds on 20 of 23 links and 26 of 26 eyes and the
  rules rebuild it (23 of 23 links); the two COS drifts are the pre-array eye's back-and-forth chatter (1.24-3.83 per
  PEArray3 block by day while COS_Conv / PEArray3 holds 1.25-1.42); TED3's silent limit is tight. Encoders: same-stem
  lengths Grading outfeed / Debarker feedworks within 2.9 %; one corroborated stand-still (Sort section 1, Thu 8 Oct
  09:15); new COS rate-ceiling raises since `_100` v1.1.0. **(2) Built and live:** judge `forensics.peWatchJudge` 1.3.0
  (SILENT with a witness, RATIO with blame, ELEMENT, WALL, the sun), registry 1.5.0 (SUN, SITE), Anomaly Watch 1.12.2
  (link scoring on the photo-eye rows, the sun mark, new bearings), Ask Azztec AI 1.3.0 (#missed, #sun), view lib 1.3.0,
  `TimeRangeSelectorMini` 1.3.0 (WTD), `cm.knife_auto` 1.4.0 (`press()` - one rule behind every button, condition-based
  changes logged), `CM/KnifeDelta` 1.7.0 (90-day history), `CMKnifeCard` 1.9.1, `CMChippers` 1.6.2, `cm.maint` 1.0.0
  with `cm.maint_event` (the 1 Oct greasing seeded), `CM/VibState` 1.2.0, `CMVibrationCard` 2.6.0, `CMWorkLog` 1.0.0;
  tools S4 1.1.0, CM S9, S5 1.0.1; a changes summary for the team (Claude Doc). **(3) Delivered, not yet run:**
  `KPP_PEWatch_baseline_set` 1.1.0 (HOURS 168, KEEP, WIDER; dry run next). **(4) Staged, not compiled:**
  `KPP_PEWatch_Design`, `KPP_AnomalyWatch_Design`, `KPP_CM_Design`, `KPP_Working_Method`, `KPP_Platform_Rules`,
  `KPP_Domain_Data_Reference`, `Workmate_Perspective_Rules` (cross-reference) - Raw Log 2026-10-09_A section 9. **(5)
  OPEN:** the re-take dry run, then live; COS_Conv re-pointed to PEArray3 or KEPT; the Section1Start sun cover; the
  proof test; the Sort section 1 encoder; the COS rate ceilings; the Labour weekend bearings (Sat 24 Oct) and the new
  references 14 days after.
- v1.36.0 - REGISTRATION + COMPILE for the 2026-10-07_A session (COS Watch and the COS log stop positioning, 6-8 Oct).
  Raw Log `2026-10-07_A` added. **(1) Findings:** the two COS PE array offsets had never been measured - taped 7 Oct
  from the A saw: log-stop array 1670 mm (PLC 1550), upstream array 1450 mm upstream (PLC -1500); the frame ran about
  120-140 mm behind the stem and 64 % of AUTO stop cuts were sawn without PosReached (`_152` R0 does not wait for it),
  yet the sorter measured those logs the same; after the fix 7 %, and dead reckoning between the arrays is good to about
  10 mm. Stems meet the stops at 450-470 mm/s p50 (the 30-unit final-approach floor); short butts in AUTO arrive too
  fast (3 of 12 within 35 mm); the PE first-edge lead is 4.3 / 0.3 mm (flicker is not a cause); the PE array symbols lit
  on eye 1 only; the Engineering menu popup was clipped and closed by the wrong id. **(2) Built and live:**
  `_260_COSWatch` 1.0.0 -> 1.1.0 (PLC cut recorder), `forensics.cosWatch` 1.1.0 and its timer, `kppstems.cos_watch` /
  `cos_watch_mark`, panel `COSWatch` 1.1.0 (`/coswatch`), Engineering menu 1.3.0; `_100_COS_ConveyorControl_v1_1_0` with
  `_101_COS_PEFirstEdge_v1_0_0`; the offsets 1670 / -1450; the master purge `shared.purge` 1.0.0 (dry run only); probes
  P1-P5. Not confirmed: purge 1.1.0 and its event, overview 1.22.0, the PE symbol views. **(3) New compiled owners:**
  `KPP_COSWatch_Design` **1.2.0** and `KPP_COS_StopApproach_Spec` **0.3.0** (draft, parked). **(4) COMPILE +
  CORRECTION:** `KPP_Domain_Data_Reference` **1.8 -> 1.9** - section 10 rewritten on the measured offsets (v1.8's -60 mm
  first approach, -330 to -900 mm restart slip and 1.8 / 0.7 / 0.28 m/s withdrawn), sections 8 and 9 added to, em / en
  dashes swept. **(5) Staged, not compiled:** `KPP_Platform_Rules` (items 1-14), `KPP_Working_Method` (15-18),
  `Workmate_Perspective_Rules` (cross-reference 13-14) - Raw Log 2026-10-07_A section 9. **(6) Index fixes:** a second
  raw log named `2026-10-03_A` (T&B sweep cancel line and Bin 0 forensics, 1-3 Oct) and its design `KPP_TnB_Bin0_Design`
  1.0.0 were in the project but never registered - registered now (1b, section 3); the two `2026-10-03_A` files differ
  by their Session line. The `KPP_Reporting_Technical_Reference` row read 1.4.0 - 1.5.0 is the live doc (section 4
  already retired 1.4.0). **(7) OPEN:** set `COS_StoplessTargetOffset` to 0; save the PLC project; confirm the installs
  in (2); the approach cap and C2 (parked); the panel Err for stop cuts; the re-approach slip (-434 mm p50).
- v1.35.0 - REGISTRATION + COMPILE for two sessions of one chat: 2026-09-28_A (the Sorter Diagnostic reset, `_107`, kick
  fails on the KickerAnomaly card) and 2026-09-30_B (the first Anomaly Watch builds 1.0.0-1.1.1, the PLC clock and
  daylight saving, the debug-counter check). Raw Logs `2026-09-28_A` and `2026-09-30_B` added. **(1) Why now:** the
  28 Sep close-out never reached the project knowledge, and its index name 1.33.0 went to the 2026-09-30_A registration;
  its compiled files are re-based here and its 28 Sep index file is never to be uploaded (section 4). **(2) Findings:**
  `_107_KickerForensics` (the routine the docs called `_106`) stopped counting kick cycles on 17 Sep - its DINT scan tick
  wrapped negative; RESET COUNTERS was read and cleared by both `_107` (MainRoutine R12) and `_102` (R14), so `_102`
  almost never reset; COS_CPU's clock stayed on standard time after 27 Sep, so PLC-stamped times read an hour early.
  **(3) Built and live:** `_107` / `_102` v1.2.0 (one-owner reset pulse, tick held in range), `forensics.sortReset`
  1.0.0 and SorterDiagnosticPopup 2.3.0, `forensics.kickerHeat` 1.5.0 with KickerAnomaly 1.6.0 / cell 1.2.0, the
  Anomaly Watch tags, timer and engine 1.0.0-1.1.1 (superseded by 1.2.0-1.11.0 of 2026-10-03_A), the daylight-saving
  flag set on COS_CPU. **(4) COMPILE:** `KPP_KickerHeat_Design` **1.4.0 -> 1.6.0**, `KPP_Platform_Rules` **1.17 ->
  1.19**, `KPP_Working_Method` **1.2 -> 1.3**, `KPP_Control_Text_Standard` **1.0.0 -> 1.2.0** (28_A and 30_B items;
  1.5.0 / 1.18 / 1.1.0 of 28 Sep never uploaded). Still staged: the 2026-09-30_A and 2026-10-03_A section 9 items for
  `KPP_Platform_Rules` and `KPP_Working_Method`, and 2026-09-30_B's one Working Method item. **(5) OPEN:** `_107` /
  `_102` v1.2.1 (remove the debug counters), clear the daylight-saving flag on 4 Apr 2027, the fails stamped an hour
  early 27-30 Sep (correction offered), whether overview 1.21.0 still opens `AnomalyChippersPopup` / `AnomalyWatchMethod`.
- v1.34.1 - post-close addition to 2026-10-03_A: the daily PE check `KPP_PEWatch_Morning_Check_v1_0_0.py` (read-only;
  ENGINE, CLEAN, SILENT, RATIO, ELEMENTS, WALL, FLOW, VERDICT) and the handover `KPP_PEWatch_NextChat_Starter_v1_0_0`
  (state, morning routine, kit for the next chat, next steps) registered under raw sources.
- v1.34.0 - REGISTRATION for the 2026-10-03_A session (PE Watch and Anomaly Watch, 30 Sep - 3 Oct). Raw Log
  `2026-10-03_A` added. **(1) Findings:** the old PE diagnostics fault an empty running conveyor and count encoder
  counts, not blocks; the encoder routines' run flags mean drive on, setpoint or line mode - never "commanded to move" -
  so every pause reads as a stall and every deliberate reverse as a fault; HOG `AllStandstillsOk` is a bare OTE (always
  true) and `GroupIsolated` does not wait for standstill; PE3 `SDB_I00902` is AFI'd (the IFM laser `SDB_I00406` runs the
  outfeed holddown); the outfeed sweep fails over to the sweep PEs, so dead wall PEs never stop the line;
  `cm.load_rollup_machine_check` refused GRAOF and `backfill_vib` hid it; no PE link's ratio moves with stem size; the
  3 Oct 04:30-05:10 DB_Infeed event was PE2L blocked between stems. **(2) Built:** PLC recorders in four areas (SDB
  1.1.0), engine `forensics.peWatch` 1.1.0, registry 1.4.0, view 1.2.0, baseline preview and set, cleaning check
  `forensics.peWatchJudge` 1.1.0 with Cleaned marks, `forensics.anomalyWatch` 1.2.0 -> 1.11.0 (five areas, history,
  shift strips, Motors and Hydraulics rows, encoder stalls judged against the eyes on the conveyor), Ask Azztec AI
  1.2.0, plantDiag 1.3.0, encoder PLC routines (COS 3.3.0, Grading 3.6.0, Sorting 1.1.0), standstill card 1.3.0, the
  GRAOF constraint fix; schemas `pewatch` and `anomalywatch`. **(3) New compiled owners:** `KPP_PEWatch_Design`
  **1.1.0** (the 1 Oct draft 1.0.0, first registered) and `KPP_AnomalyWatch_Design` **1.0.0**. **(4) CORRECTIONS
  banked:** M9-M17 (Raw Log 2026-10-03_A section 5) - AreaSafetyCard 1.2.0 withdrawn (HOG "no monitor" came from a stale
  tag CSV); GRAOF fix 1.0.0 read only the outer error; preview 1.0.x set limits from the worst window. **(5) Staged, not
  compiled:** `KPP_Platform_Rules`, `Workmate_Perspective_Rules`, `KPP_Domain_Data_Reference`, `KPP_Working_Method` -
  Raw Log 2026-10-03_A section 9. **(6) OPEN:** confirm the COS / Grading encoder routines, the remaining run flags and
  direction checks in the PLC, PE Watch link scoring and the proof test, the bark-on check output, the Hydraulics index,
  the HOG `GroupIsolated` review.
- v1.33.0 - REGISTRATION for the 2026-09-30_A session (chipper knife clock and verdict, motor vibration on four
  motors, 22-30 Sep). Raw Log `2026-09-30_A` added. **(1) Findings:** the window-count HOURS IN CUT overstated cutting
  3x on the discs and 7x on the drum; the clock lines that best track belt chip volume are 15 / 12.5 / 2.5 % torque
  (DISC1 / DISC2 / DRUM - the drum idles near 1-1.5 %); the knife-change step is sharpest on time-weighted current with
  duty flat (153 / 164 / 91 A) and the within-set delta carries duty cycle; the drum's torque step is the wrong sign
  (inferred boundaries); per-chipper chip volume does not exist (`usnr.logdetail.destinationname` NULL, `chip_daily`
  drum grade unused); split by machine state, idle vRMS is a tight band and aRMS ignores cutting; Disc 2 aRMS runs 1.8x
  the healthy Disc 1 (common mode: idle r 0.83, aRMS r -0.09); the grader outfeed has no idle, only an 18-30 % torque
  load band; 33,406 mg is the VVB301 over-range code (outfeed 29 % of samples, drum 0.15 %); the 28 Sep tools incident
  hit the disc, was invisible to the motor sensors and left no lasting damage. **(2) Built:** `cm_rollup` 1.3.0 ->
  1.7.0 (time-weighted clock, verdict on current, vibration windows by state, GRAOF band), schema ADDs 1.1.0 / 1.2.0 and
  `cm.vib_rollup` / `cm.vib_baseline`, NQs `CM/KnifeDelta` 1.6.0 and `CM/VibState` 1.1.0 (Disc 2 aRMS against Disc 1),
  knife card 1.8.0, vibration card 2.5.1 with an electricians' method popup 1.3.0, overview 1.16.2 (four motor cards),
  tags for Disc Motor 1 and the Grader Outfeed, four baselines, a knife-record correction, six probes, an Anomaly Watch
  spec. **(3) New compiled owner** `KPP_CM_Design` **1.0.0**. **(4) CORRECTIONS banked:** version collision with the 03
  Sep saw session (card 1.6.0 / NQ 1.4.0 reissued as 1.7.0 / 1.5.0); the 'zero belt volume' set periods were a pairing
  artifact; the vibration card never refreshed (no polling) - fixed in 2.5.1 with a string rate, which conflicts with
  the `KPP_Platform_Rules` 'no polling key' body rule (staged correction); VVB010 ceiling 48 -> 50 g pending. **(5)
  Staged, not compiled:** `KPP_Platform_Rules`, `KPP_Domain_Data_Reference`, `KPP_Working_Method`,
  `Workmate_Perspective_Rules` - Raw Log 2026-09-30_A section 9. **(6) OPEN:** `knife_auto` 1.3.0, the automatic knife
  WO, outfeed mount check and VVB010 swaps, Disc 2 bearing and re-baseline, `CM/Chippers` cut points, saw current lines.
- v1.32.0 - REGISTRATION + COMPILE for the 2026-09-27_A session (Sortline kicker signal drops,
  kick-fail history, prox lights). Raw Log `2026-09-27_A` added. **(1) Findings:** real
  overload trips take 1-5 min to clear (the relay cooling) - none of duty / mixed / first-kick
  / repeat cleared in under 15 s; the 18 that did (8 common, 8 low-duty, 2 idle) are the
  overload-OK input dropping at line stops and starts; the Sorter Diag K-FAILURES list is the
  PLC kick-fail ring (`LSL_KickerFailLog*`, 50 deep), not overloads, and its tiles read 0
  because they come from `_106`; kick failures lead into overloads on Kicker 17 and Kicker 11
  (mechanical); Kicker 7 logged 29 FAIL Fwd Kick in a week; the kicker prox members polled on
  `LeasedTags`. **(2) Built:** engine `forensics.kickerHeat` v1.4.0 (signal drop - cleared in
  under 15 s; mechanical - a kick failure in the 10 min before; the fail ring copied into
  `sortline.kicker_fail_event`), `forensics.kickerTrend` v1.2.0 and KickerTrend v1.4.0 (1 h and
  4 h ranges, signal drops grey, kick failures orange), card v1.4.0, popup v1.8.0, overlay
  v1.3.0, method popup v1.2.0; prox members moved to `FastLeasedTags` with a 1 s on-screen
  hold. **(3) CORRECTION banked:** the signal-drop 'stop' rule (a line standstill near a
  low-load trip) was wrong - it hid 71 real trips, up to 67 min long - and was removed (engine
  v1.4.0; `KPP_KickerHeat_SignalFix_v1_0_0.py` restored them); the lesson is staged for
  `KPP_Working_Method`. **(4) COMPILE:** `KPP_Platform_Rules` **1.16 -> 1.17** (5 rules),
  `KPP_KickerHeat_Design` **1.3.0 -> 1.4.0**. **(5) Still staged:** `KPP_Working_Method` and
  `KPP_Control_Text_Standard` (Raw Logs 2026-09-26_A and 2026-09-27_A, section 9). **(6) OPEN:**
  `_106`, Kicker 7 (29 fwd-kick fails), Kicker 10 (rev-kick fails, WO-260927-007), idle prox
  pattern -> stuck-out warning, slice 5.
- v1.31.0 - REGISTRATION + COMPILE for the 2026-09-26_A session (Sortline kicker overload
  trips) and its post-close addition 2026-09-26_B (kicker trend). Raw Logs `2026-09-26_A`
  and `2026-09-26_B` added. **(1) Findings:** most kicker trips are NOT frequency (25 of 163
  at the kicker's busiest); Kicker 10 is the frequency case and trips below its own 2.0
  line; Kicker 2a first-kick, Kicker 16 repeat, four same-second events (MCC); `_106` kicker
  forensics stopped 17 Sep 12:09; `KickerEnables` is BOOL[64] shown as DINT words and one
  bit of the word is OPC-writable; the enable is the kicker AOI's RunPermission.
  **(2) Built:** engine `forensics.kickerHeat` v1.1.0 (heat, per-trip verdicts common /
  repeat / idle / first-kick / duty / low-duty / mixed, 175-trip backfill,
  `TripsTodayJson`), KickerAnomaly card v1.2.0 in the Overview footer, map overlays with
  TRIP / ISO / OFF and vertical prox lights, kicker popup v1.5.0, enable / disable through
  `forensics.kickerEnable` v1.1.0 (one-bit write, read-back, audit - proven on Kicker12),
  Workmate quick WO and open-WO deep link (`forensics.kickerWO` v1.1.0, WO-260926-007),
  Workmate right "Sortline kicker enable" (Menu_ID 133) with Security Setup v2.9.2, and
  (_B) the kicker trend popup in the VSD Trend Data style (`forensics.kickerTrend` v1.0.0 -
  kicks from `sorter_logs`, faults from the trip table, full history, no historian).
  **(3) New compiled owner** `KPP_KickerHeat_Design` **1.3.0**. **(4) COMPILE:**
  `KPP_Platform_Rules` **1.15 -> 1.16** (16 rules + a dated addendum) and
  `Workmate_Knowledge_Journal` **3.8 -> 3.9** (3.22 menu rights, 3.23 work orders from
  outside WOMaint); `KPP_Platform_Rules_ADD_2026-09-26`,
  `Workmate_Knowledge_Journal_ADD_2026-09-26` and `DashboardandPLC_Knowledge_Index_ADD_2026-09-26`
  merged and retired. **(5) CORRECTION banked:** the ADD's "display bindings do not hide
  labels on this gateway" became an addendum to the 2026-09-18_A display rule - the v1.0.0
  labels also carried a literal `display: 'none'`, and a `try(..., 'flex')` fallback failed
  open; cause not isolated. **(6) Still staged:** `KPP_Working_Method` and
  `KPP_Control_Text_Standard` items in Raw Log 2026-09-26_A section 9 (the HMI panel style
  standard, set by the user). **(7) OPEN:** `_106`, Kicker 10 line / OL setting, idle prox
  pattern -> stuck-out warning, trend smoke test, slice 5.
- v1.30.0 - REGISTRATION + COMPILE for the 2026-09-25_A session (SDB debarker stem
  tracking). Raw Log `2026-09-25_A` added. **(1) Twin stems**: `_201` rung 1
  re-tested the curtain flag that rung 0 had just cleared in the same scan, so every
  stem matched at the outfeed PE was created twice (UnexpectedStems 91,226); fixed in
  v1.2.0 (decision computed once), plus two `LastMemoryUsed` operand slips (`_202`
  R1, Outfeed `_220` R20). Live: 77 of 78 stems matched in 45 min, 1.00 memories per
  stem. **(2) Map motion**: `SDBMap_View_v1_2_0` - CSS glide on the stem labels, off
  while the view mounts (v1_1_0 slid stems in from their saved positions - do not
  import). **(3) Outfeed scale**: the `_101` DINT `EncoderScale` rounded 13.154 to 13
  (positions 1.2% short) - REAL tag, verified. **(4) Length of record**: four sources
  over 135 stems showed the outfeed PE length (fences, grading, map) long and
  erratic; v1.3.0 makes the curtain length the length of record behind
  `SDB_StemTrack.PE_PosUpdate.DB_LC.BOOLs[1]`, set to 1 on 26 Sep. COMPILE:
  `KPP_Platform_Rules` **1.14 -> 1.15** (new sections "Perspective motion" and
  "Ladder logic (Logix runtime)", three L5X-editing entries, one view-generator
  entry), `KPP_Working_Method` **1.1 -> 1.2** (one paired comparison is not evidence;
  prove ladder off-PLC; versioned routine names; behaviour changes behind a switch),
  NEW `KPP_SDB_StemTracking_Reference` **1.0.0** (no doc owned SDB tracking -
  Knowledge Standard section 4). Open items in the raw log section 10.
- v1.29.0 - COMPILE pass for 2026-09-24_A. `KPP_Platform_Rules` **1.13 -> 1.14**:
  `KPP_Platform_Rules_ADD_2026-09-24` merged and retired, as a NEW section
  "Project resources on disk (Project Library, exports)" - a Project Library
  package must be a plain FOLDER (a package that is also a script resource loses
  the scripts nested inside it whenever the gateway re-reads the project from
  disk, which emptied `schedule` three times), the delete-SAVE-recreate order for
  converting one, `lastModification.actor` and what `external` means, the export
  as a forensic record, and `resource.json` timestamps being UTC. Additive - no
  existing entry changed.
- v1.28.0 - REGISTRATION for the 2026-09-24_A session. Raw Log `2026-09-24_A`
  added. SHUT PLAN / SCHEDULED SHUTS - the `schedule` package wipe ROOT-CAUSED
  and fixed structurally after three occurrences. **(1) Third wipe confirmed**
  in the 2026-09-22 export: `script-python/schedule/resource.json` `files: []`,
  actor `external`, `2026-09-20T22:41:49Z` = Mon 21 Sep 10:41 NZST, `kpp` and
  `mly` gone; both ShutEdit views therefore rendered their `LOAD FAILED`
  placeholder in every cell (earlier wipes 2026-09-01 and 2026-09-12 20:32).
  **(2) CAUSE**: `schedule` is the ONLY package in the project that is itself a
  script resource - it carries its own `resource.json` (`hintScope: 2`), a
  leftover of the 2026-07-31 split that created `kpp`/`mly` INSIDE the old
  `schedule` script. When the gateway re-reads the project from disk it
  re-persists that resource and the nested scripts do not survive; every
  plain-folder package (`cm`, `operator`, `production`, `shared`, ...) came
  through the same events untouched. 392 resources carry actor `external` and
  391 of them are the 10 May import - the 392nd is this package. **(3) FIXED**
  by rebuilding `schedule` as a plain PACKAGE (delete the script node, save,
  New Package, then the two scripts) with `schedule.kpp` + `schedule.mly`
  **v1.2.0**; verify `KPP_schedule_verify_v1_1_0` 7/7 PASS (82 days cross-checked
  against `schedule.shut` / `mly.shut`, 8 KPP and 6 MLY shut days, write round
  trip on both tables). v1.2.0 also closes open item 3 of 2026-09-18_A -
  `startup_time` now reads `scheduled_startup_time` - and makes `putShut`
  update-then-insert, never insert an empty day, and refuse the `LOAD FAILED`
  placeholder. No view changes. **(4) Staged**:
  `KPP_Platform_Rules_ADD_2026-09-24` (4 rules: packages must be plain folders,
  `actor: external` means read off disk, an export is a forensic record,
  `resource.json` timestamps are UTC). **(5) OPEN**: the on-disk listing of
  `script-python\schedule` on TL-KPPWS01 has not been pasted back, so the
  structural fix is confirmed only by the code working; the trigger (restart or
  scan at the two timestamps) is still unidentified; a stray
  `WO_NQ_PMFilter_v1_0_0/` folder sits in the project root on the gateway disk.
- v1.27.0 - COMPILE pass for 2026-09-22_B. `KPP_Platform_Rules` **1.12 -> 1.13**
  (14 rules into OPC / PLC reads and Perspective, plus a NEW section "View
  generators") and `KPP_Domain_Data_Reference` **1.7 -> 1.8** (NEW section 10
  COS log stop positioning, NEW section 11 SDB debarker profile and the two SDB
  KPIs, section 8 tables, section 9 gotchas). Both `_ADD_2026-09-22_B` files
  merged and retired. Additive - no existing entry changed. Also corrects the
  Domain Data Reference row, which read 1.6 while v1.7 was loaded.
- v1.26.0 - REGISTRATION for the 2026-09-22_B session (afternoon, same day as
  `_A`). Raw Log `2026-09-22_B` added. COS LOG STOP POSITIONING and DEBARKER
  DETAIL. **(1) Tui camera quote (NZ$114k) dropped on evidence**: two read-only
  probes - stem placement at the stops is repeatable to better than +/-40 mm
  over 103k `sorter_logs` rows, and `COS_PLC_1756CPU` cannot be polled faster
  than ~700 ms so the slip probe's timing numbers were junk while its
  difference-of-deltas slip held (-60 mm first approach, -330..-900 mm restart
  after a cut, corrected by R8). The remaining damage is manual jogging: any
  joystick input drops auto and jog runs at MedSpeed with no position cap.
  **(2) Built**: positioning capture `dataengine.kpp.capture.cos_positioning`
  -> `kppstems.cos_positioning_events` (manual / jog / overrun / auto-drop per
  approach, operator from `Operator.Current.ID`), Log Stop Positioning panel
  on the COS Overview with a "?" popup, `operator.kpi` v1.2.0 + four NQs +
  the OperatorKPI "Log Stops" tab. **(3) For Trina**: SDB KPI definitions
  pinned from the DB (bark on = knives OR rollers raised; stems > 3.5 m only;
  > 5 % rule) and a Debarker Detail view - score strip vs crew, per-shift
  line, lift bands, worst-30 stems with click-to-draw stem profile - as an
  OperatorKPI tab and a Training Review button. **(4) Staged**:
  `KPP_Platform_Rules_ADD_2026-09-22_B` (14 rules: OPC throughput, sequential
  batch items, `Uncertain_InitialValue`, CutComplete pulse, `ManualCutsDone`
  semantics, the COS login tag, polling rate as string, `try()`, root-container
  `self.view`, table row click, expr-struct null vs empty, NQ path as authored,
  fixed-grid panels, generator `%%` escaping + exec-test) and
  `KPP_Domain_Data_Reference_ADD_2026-09-22_B` (positioning frame and
  constants, `StopLowered`, `cos_positioning_events`, `sorter_logs` as ground
  truth, the sdb profile schema and the two KPI formulas).
- v1.25.0 - `KPP_Platform_Rules` **1.12**: both staged ADDs merged into their
  topical sections and retired - the 11 Visitor-session rules (from Raw Log
  2026-09-18_A section 6, `DashboardandPLC_Knowledge_Index_ADD_2026-09-18`) and
  the 14 camera-session rules (`KPP_Platform_Rules_ADD_2026-09-22`). New section
  "Windows host (TL-KPPWS01) & PowerShell". 25 entries added, no existing entry
  changed.
- v1.24.0 - REGISTRATION for the 2026-09-22_A session (spans 09-01 -> 09-22).
  Raw Log `2026-09-22_A` added. CAMERA LIVE VIEW built from nothing. **(1) New
  compiled owner** `KPP_Camera_LiveView_Reference` **1.0.0** - relay
  architecture (cameras -> go2rtc on TL-KPPWS01 -> browser MSE, video never
  through the gateway), relay runbook with the watchdog task, stream keys and
  naming (printed site list = NX510 names), the H.264-only codec rule with the
  Hikvision Sub Stream and i-PRO Stream(3) fixes, a 46-camera estate snapshot,
  camera-side traps (session cap -> NVR route, missing default gateway,
  `OPTIONS *`), the camera views and relay pill, a troubleshooting table.
  Supersedes the never-loaded `KPP_Camera_LiveView_Setup` working notes.
  Credentials stay in the relay yaml only. **(2) Platform rules staged** (14) in
  `KPP_Platform_Rules_ADD_2026-09-22`: iframe 300x150 collapse -> container-query
  units; unsized Icon grows; Flex Repeater `elementPosition`/`elementStyle`;
  script transform `code` is body only; `now(30000)` expr-struct polling; one
  repeater for mixed rows; `httpClient(timeout=)`; script vs network faults; the
  `operator` package shadow; Script Console runs on the Designer PC; group policy
  blocks Python on TL-KPPWS01; schtasks 72 h limit; PowerShell `>` is UTF-16LE;
  `copy /Y` fails. **(3) CORRECTION**: the `KPP_Platform_Rules` row read 1.9 -
  the file in project knowledge is v1.11 (2026-08-06); the row had not followed
  the v1.10/v1.11 bumps.
- v1.23.0 - REGISTRATION for the 2026-09-18_A session (spans 09-17 -> 09-18).
  Raw Log `2026-09-18_A` added. VISITOR SIGN IN audited end to end, cleaned up
  and extended; SHUT PLAN rescued on the way. **(1) Full audit** of the
  2026-09-17 export - 41 views, 79 NQs, 5 modules, 2 reports, 24 style classes,
  34 config keys, every reference traced: 16 dead views, 35 dead NQs, 7 NQs
  referenced but MISSING, 19 live defects. Register `KPP_VisitorSignIn_Audit`
  **1.2.0** (stays as the audit of that export; the raw log carries what changed
  after it). **(2) CORRECTION banked**: a change script with `enabled: null` is
  ENABLED (only `false` disables; 88 null / 72 true / 2 false project-wide) -
  audit v1.1.0 had wrongly listed the kiosk `Config` admin screen,
  `Component/Image` and three Configuration NQs for deletion. **(3) NQ layer
  fixed**, smoke 11/11: `People/Signout` v1.1.0 closes ONLY the open visit (42
  guest-days had been over-stamped by a second sign-out), `People/All Guests`
  v1.1.0 filters `active = 1` (8 removed contacts still on the kiosk),
  `People/Guest Exists` v1.1.0 never matches a blank email (2 blank-email guests
  held 27 visits - visitors were being signed in as someone else), `Visit/Add`
  v1.0.0 CREATED (Add visit had never worked), `Visit/Remove` v1.1.0 made an
  Update Query (a DELETE in a Query-type NQ returns no result set),
  `Staff/Item` v1.1.0 casts the bit columns (Status showed Off for active
  staff). **(4) Sign-in badge REMOVED** on request - Create + Config views,
  `Distribution Values` v1.1.0, 7 config keys deleted, report `Sign In Badge`
  and NQ `Badge Info` retired; badge was already dead by config and
  `reportProjName` pointed at a project that does not exist. Host notification
  email unchanged and live. **(5) Staff save repaired**: `list(item.photo)`
  threw on a NULL photo before the one-shot button reset, so the form stuck on
  "Writing" and nothing saved. **(6) KIOSK 10x LIGHTER**: staff photos ride
  inside every card as base64 and re-transfer on every key press - 1.07 MB per
  `All Staff` call; photos resized to 200 px (0.09 MB, originals backed up),
  new `photo` library, kiosk Staff + Guest screens now load once and filter in
  an `expr-struct` transform as you type, PostgreSQL `Suggested Users` section
  removed. **(7) RECEPTION SHUT-DAY BOARD**: `Menu` v2.8.0 (banner, visit-type
  tiles, live on-site panel with two-tap sign-out), `Menu Tile` + `Visitor Card`
  components, page `/receptionhub/visitors`, Hubheader v1.3.0 with
  Reception-only Visitor Sign In / Visitor Sign Out / Shut Day buttons and
  auto-open 06:00-22:00 on a shut day, driven off `schedule.shut` via NQ
  `Production/Shuts/ForDate`. **(8) SHUT PLAN RESCUED**: Project Library
  `schedule` was an EMPTY package (`files: []`, actor "external",
  2026-09-12 20:32 NZST - second wipe after 2026-09-01), so every calendar cell
  showed LOAD FAILED; `schedule.kpp` + `schedule.mly` rebuilt at v1.1.0,
  verified 8/8 with a write round trip on both tables. Cause still unknown -
  check `wrapper.log` Saturday evenings on TL-KPPWS01. **(9) Perspective rules
  banked** (11, staged for `KPP_Platform_Rules`): hidden components still take
  flex space - use `props.style.display`, and a static `display` beats its own
  binding; `if()` on an unset custom prop errors "If function got a null first
  argument" - wrap in `coalesce()`; `self.view.custom.X` must be declared on the
  VIEW not the root container; image `fit.mode` is absolute/contain/cover/
  percent/none only; Text Field needs `deferUpdates: false` to publish per
  keystroke; JSON-format query bindings return dates as EPOCH MILLIS; a scalar
  NQ fallback fires on an empty result, not just on error; the Script Console
  echoes bare expression values including a leading docstring.
- v1.22.0 - BACKFILL REGISTRATION for an earlier session dated **2026-06-30**,
  logged today (2026-09-04) at Adriaan's instruction - the chat predates the
  July raw-log series and had never been captured. Raw Log `2026-09-04_A`
  added (covers the 06-30 work). STEM GRADE DASHBOARD + KPP DAILY REPORT
  session. Banked, load-bearing findings: **(1) `stemnumber` is a cyclic
  ~10,005 counter** (10,005 distinct all-time vs 1.66M `stemid`) - never
  `count(distinct stemnumber)` or `group by stemnumber` over >1 cycle; 30-day
  Stems read 10,002 vs true ~59,776 (~6x undercount); use `stemid`; fixed in
  `Production Summary Stemlevel` + `Recent Stems Stemlevel` (also fixes inflated
  per-stem Logs from recycled numbers merging stems). Shared `Production
  Summary` (Simulator Report) still on stemnumber, left by design. **(2) NQ
  `.sql` must be BARE** - a leading `--` header breaks the `:param` binder
  (`syntax error at or near ":"`); rationale goes in a companion `.md`.
  **(3) Perspective exports silently DROP custom-prop + param DECLARATIONS**
  while keeping the `propConfig` bindings - a binding with no declared prop
  does not evaluate; caused a blank Stem Inspector and an onStartup
  `AttributeError`; the export had 4 custom keys / 1 param vs 20 / 3 referenced.
  Rule: verify `custom`/`params` blocks after every export before re-import;
  GradeDashboard v1.0.20 is the complete reference. **(4) Chip volume** trusted
  figure is `kppchip.chip_scanner_daily.volume` (chipper's own scanner, all
  chip incl binwood) via `prod_summary.chip_volume`, NOT COS
  `cos_kpi_data.total_scanned_chip_volume` (~6x low, 118 vs 742); hourly source
  is `kppchip.chip_scanner_data.start_ts` (sums to the daily); `ProductionByHour`
  v1.1 buckets it hourly, 7-to-7 shift derived from the timestamp. **(5) Stem
  Inspector data**: `Stem Logs` v2 reads `usnr.logdetail` (real chip lengths;
  `prod_report` has length 0 for bin-999 chips) - logdetail keys on `stemid`,
  has NO `stemnumber`/`forestcompart` (echo `:StemNumber`, HA from prod_report);
  defects positional in `usnr.stemdefect` (16 types, startpos/endpos mm) drawn
  as staggered labelled bands; **knots do NOT exist per-stem** - only as
  aggregated grading KPIs (`GradingKPIData.Knot8/10/12cm`, no stemid/position).
  **(6) Waste** genuinely uncaptured (`waste_coeff`/`waste_vol` null day+night);
  null-safe transform shows '-' (the old raw Format transform threw "Cannot
  format given Object as a Number" on null; "works in Designer" was just a
  non-null preview). **(7) ShiftStatus pace arrow** must compare PROJECTED
  end-of-shift vs previous-shift final (not partial-so-far vs whole-previous,
  which is always "behind"); no target tag exists; 15-min early-shift steady
  guard. **(8) LIVE default-ON** - a Designer project SAVE re-mounts the view
  and resets non-persistent custom props to default; defaulting `liveMode` true
  survives the save and suits a production board; selection guard hardened for
  a not-yet-loaded `liveStem`. **(9) mini stem-engine kpiRow tile** reuses the
  gateway's existing `se-*` + `se-stopped` classes (no stylesheet change), fed
  by `forensics.stemEngine.status`. Deliverables: GradeDashboard v1.0.20,
  Stem Logs NQ v2.2, Stem Defects NQ v1, ProductionByHour NQ v1.1, ShiftSummary
  view v1.1, ShiftStatusChipLight view v1.1. NOTE: this session's builds
  (06-30) PREDATE the July condition-monitoring / MLY / TimberPay work already
  registered above - it is filed here only for completeness of the record.
- v1.21.0 - REGISTRATION for the 2026-08-31_B session (same day, second
  session). Raw Log `2026-08-31_B` added. ACTION WEEKLY DIGEST: new library
  `shared.action_email_weekly` v1.0.0 + Scheduled event `Workmate Action weekly
  digest` (`0 8 * * 1`) - every Monday 08:00 one branded email per action OWNER
  listing their open actions (Overdue / Due this week / Other open), Adriaan in
  every `to=`, owner-less actions as a separate no-owner summary to Adriaan.
  Thin sibling of `shared.po_email_morning` v1.4.1 with the data layer swapped;
  validated end-to-end in an offline `system.*` stub harness + wkhtmltoimage
  render before the first gateway paste, so live `preview()` / `testSend()` /
  Outlook all passed first time. Banked: **the three "morning Work Order
  email" candidates and their shapes** (`MP Morning Digest` 07:10 one-to-list;
  `Workmate PO morning approval digest` 08:00 one-per-approver - the pattern
  for any "everyone responsible, copy me" request; `ShutWO*Email` 19:00
  one-to-list shut-gated) and **the two live SMTP conventions in one gateway
  (`smtp='Email'` vs `smtpProfile='KPPDashBoard'`) - new work follows the KPP
  rule, `smtp='Email'`, sender `workmate@kt.co.nz`**; **the Action data model
  as read for email** (`Action_Header.User_Id_Owner`; email is on
  `User_Contact_Details.Email_Id_1/2` NOT `Users`; `Priority.Priority_Title` +
  `Sort_Sequence`; L3 Area via the Search v1.0.4 `loc_area` CTE; open =
  R/H/P/K/A/V, G Promoted excluded; ANumBadge tints pre-computed to solid
  hex). Live findings: **50 open actions, 6 owners, 20 with NO owner, and not
  one `Due_Date` set** - priority titles (`Action Today` / `this week` / `this
  month` / `As sched. permits`) are the real urgency signal, so undated rows
  sort by `Sort_Sequence` and a by-priority sectioning is the v1.1.0
  candidate. Platform rules: **never `%`-format a SQL string - LIKE patterns
  collide with it; token-replace the IN-list and bind the rest**;
  **`system.date.daysBetween` counts whole 24 h periods, so normalise the due
  date to midnight before bucket tests and day counts**; **three stacked
  section tables only align with `table-layout:fixed` + percentage `width`
  attrs on every `<th>`** (auto layout let one long badge re-grid a table);
  **dedupe on the row key whenever a contact-details style join is not proven
  unique**. Routing: no email / inactive owner / admin-is-owner all resolve to
  Adriaan, never dropped; one external owner address (`maintenance@tll.co.nz`)
  flagged as a standing item.
- v1.20.0 - REGISTRATION for the 2026-08-31_A session (spans 08-29 -> 08-31).
  Raw Log `2026-08-31_A` added. TRAINING REVIEW: Trina's
  `Monthly_training_review_template.xlsx` replaced by a full Perspective stack -
  `operator.training_review` / `training_focus` / `training_prereq`, seven NQs
  under `Report/Training/`, library `operator.trainingreview`, entry view on the
  Operator KPIs shell (new Training Review tab), and an A4 print path. Built
  bottom-up with a smoke test at every layer (16 NQ / 34 library / 12 printData
  checks), so the only faults that reached the screen were layout. Platform
  rules confirmed or newly banked: **a view param fed by a parent ContentView
  MUST declare `paramDirection: "input"` in view-level `propConfig` - without
  it the parent's write is discarded in silence and the param stays null**
  (header sat on today's month while the selector said July; every working
  sibling tab carries the two lines, and a `null` default was never the
  problem); **`basis` on a flex child is measured along the PARENT's direction -
  height in a column, WIDTH in a row** (heights passed to row children rendered
  as 120px slivers), and **`grow: 1` alone does NOT split a row evenly because
  `flex-basis: auto` lets a nowrap title set the width - `basis: "0px"`
  alongside `grow: 1` is what forces an even split**; **a Named Query silently
  inherits the project default datasource, which on this gateway is SQL Server -
  the error names a missing PostgreSQL table but is issued by the mssql
  driver**; **font-vs-box undersizing grows scroll arrows in Perspective flex,
  and on a printable a scrollbar does not print so the content behind it is
  lost rather than clipped**; **a component whose `props.path` is fully bound
  always reads "View Not Specified" on the Designer canvas - design mode does
  not evaluate bindings** (ContentView has no static path; PeriodSelector
  renders because its path is a literal, and its dead show/hide bindings are
  the corroborating tell); **a DDL preflight verify runs against the PRE-change
  state by definition, so every column it names must be gated on
  `information_schema`** (v1_1_0's verify threw on its own DRY_RUN pass);
  **`AttributeError: '...script.Pro' object has no attribute X` means the VIEW
  was imported ahead of the LIBRARY** - the truncated class is the project
  script module wrapper. Domain findings: **the spreadsheet stores weights as
  fractions under `0%` cell formatting, so Trina types 25 and reads 25% - the
  first live test typed 10/15/20 and stored 1000%/1500%/2000%**, resolved by
  keeping fractions in the database and converting at the view boundary through
  `toPercent`/`toFraction`; **a monthly review scores one month AND plans the
  next, so `training_focus` keys on its own `plan_month` and is not a child of
  the review** - next month's plan becomes that month's scored table for free;
  **`finalised_at` is a separate question from `updated_at`** (the latter moves
  on every write) and **the status pill reports the STORED status, never the
  dropdown**; **save COMPACTS focus rows before trimming**, because a
  positional trim deletes the wrong row when row 2 is cleared and row 3 kept;
  **`compositeScore` renormalises over the weight that carried a score**, so a
  half-finished review does not read as a failing one (verified against the
  workbook's own formula, 0.6). Architecture notes: 73 flat custom props rather
  than array-index bidirectional bindings (write-back into an array element is
  the fragile part, and verbosity is free in a generated view); one `loadKey`
  trigger with one `onChange`, and Save bumps a nonce so the grid returns
  compacted exactly as stored; `printData()` returns a fully PRE-FORMATTED
  payload so the printable carries exactly one transform; print refuses rather
  than printing stale.
- v1.19.0 - REGISTRATION for the 2026-08-24_B session (spans 08-14 -> 08-24).
  Raw Log `2026-08-24_B` added. Two threads. (1) TNB STARLOADER PANEL taken
  live on the TnB Map, via four wrong-binding faults that each looked like a
  display bug: **`FltIn` is bit 3 of BOTH `udt_RMC_StatusBits` and
  `udt_RMC_ErrorBits` - StatusBits is the input STATE (normally on),
  ErrorBits is the fault; any RMC fault display reads ErrorBits ONLY**;
  `SetPositionReq` hardcodes `MOV(0,cmd[1])` in `_091` rung 11 so it ALWAYS
  zeroes the axis - a "SET POS" button was a disguised SET ZERO, replaced by
  `PositionReq` (cmd 20); **AOI parameters declared `ExternalAccess="None"`
  are unreadable over OPC no matter what** (`Pumps[3].AOI.RunConfirmFwd`) and
  the readable equivalent is `MotorControl.Status.Running` one rung
  downstream - NOT `Status.Running`, which is a different hydraulic bit;
  **`system.tag.configure` writes a nonexistent tagGroup happily and the tags
  then silently stop scanning with `Error_Configuration("Tag Group Invalid")`
  - verifying the configured NAME proves nothing**, resolved onto the
  existing `FastLeasedTags` (Leased 600000/250 ms; **a console readBlocking
  is not a subscription so leased tags read stale from the console - that is
  correct behaviour**). FolErr is REAL - the axis parks 4.6-4.8 deg past
  target every index; **a position offset CANNOT fix it (shifts actual and
  target together)** - the lever is RMCTools In Position Tolerance F24:56
  (6.0, applied) and **Pos Error Tolerance F24:57 (0.25 -> 10.0, PENDING) -
  the RMC names the BIT "Following Error" but the PARAMETER "Pos Error
  Tolerance"**. Rotary axis (Unwind 360) error must wrap:
  `(a-t) - 360*floor(((a-t)+180)/360)`. (2) KNIFE SYSTEM matured from "it
  works" to "we know how much to trust it": real rhythm is **12 h knives
  (03:00/15:00), smoko 03:00-03:30, bi-weekly 07:00-19:00 Thursday shut**;
  `cm.knife_auto` added (self-healing, NOT a cron; grace 120 min, dup +/-5 h,
  >=4 loaded windows, **and a START-LAG guard so a post-shut restart is not
  read as a boundary change - no shut schedule needed**); the panel button
  was being used as a RESET by two users on two days (15 bogus rows) so it
  now says `TAP AGAIN TO LOG`, auto-disarms in 6 s and refuses a duplicate
  within 6 h. **THE MEASUREMENT VERDICT: DISC1/DISC2 (one rotor, independent
  sensors) correlate r=0.931 with median difference 3.3 points against
  set-to-set SD 15.8 - 6 % of variance is measurement, 94 % is real wood.
  Threshold tuning is therefore futile and was abandoned; piece size drives
  load (r=0.59, slope 0.46/0.45 - a 10 % bigger piece costs 4.5 % more
  torque) while feed rate does not (0.08-0.25), but correcting for it
  recovers only ~10 % so normalisation is PARKED.** The display changed
  instead - the chip now ranks each set against that machine's own 30-day
  p75/p90 and a trend line counts how many of the last four ran above normal.
  New platform traps: **the Script Console prints the value of a bare
  expression statement** (stray `0`s from `runUpdateQuery`, dicts from
  `setdefault` - assign to `_`), and **`runPrepUpdate` per row is a separate
  transaction so defaulted `now()` differs between them**, which silently
  broke a pair join on timestamp equality.
- v1.18.0 - REGISTRATION for the 2026-08-19_A session (spans 08-18 -> 08-19).
  Raw Log `2026-08-19_A` added. (1) VISITOR SIGN-IN LOADS: KPP_Visitor audited
  (MSSQL 2019 Express, db `visitor`); PWC loaded as company 1197 + guests
  1384-1388; twelve KT staff loaded as ids 21-32 and hidden from the kiosk -
  the `People/All Staff` NQ never read `hidden` (write-only flag), patched to
  v1.1.0 with `AND s.hidden = 0`. `RemoveStaff` hard-delete script for David
  Cameron built, deliberately unrun. Liaanna Hay duplicated (staff 19/20).
  (2) KPPDAILYREPORT PRINT OUTAGE root-caused as FOUR stacked layers: inert
  kt classes in meta.classes (never part of the old behaviour); the 08-03
  export proving request-print itself worked on stylesheet v2.41; v2.56's
  extension guard hiding Perspective's `printWindow` iframe (a BODY-LEVEL
  SIBLING of #app-container) from OUTSIDE - fixed v2.57; and the same guard
  running INSIDE the print document (request-print CLONES the project
  stylesheets - the 08-17 "renders without the stylesheet" rule is FALSE) -
  fixed v2.58 by arming the guard with `body:has(> #app-container)`.
  **HARD RULE: every global @media print rule must be context-armed or it
  also fires inside every request-print document.** Print scale ceiling:
  Chrome fits by the taller axis; one-sheet side-by-side tops out ~80-85%
  (landscape + minimum margins recovers most). Final set: KPPDailyReport
  v1.13.0 (Print Report + paper-only PrintHeader), ShiftProduction v1.2.0,
  stylesheet v2.61. KPPDailyPrintable is a DEAD END - delete. Workmate-vault
  corrections shipped as `Workmate_Perspective_Rules_ADD_2026-08-19_v1_0_0`.
- v1.17.0 - REGISTRATION for the 2026-08-16_A session. Raw Log `2026-08-16_A`
  added. **TIMBERPAY IS LIVE** - the CleverTime-to-iPayroll Excel/VBA tool is
  ported to Ignition: `payroll` schema (5 tables) on `KPP_production`, 2026
  history seeded (26 lookups, 16 batches, 1,565 rows), library
  `timberpay.timberpay`, 6 Named Queries, view `TimberPay_v1_5_0`. The VBA
  audit's two real defects were structural and both die with the port:
  the overlap check was ADVISORY ONLY (flagged rows still uploaded) and
  de-dup compared against ONE user-picked file. Classification ladder
  UNCHANGED -> CHANGED -> OVERLAP -> NOLOOKUP -> NEW; only NEW auto-includes.
  Proven live on `01_08_2026.csv` (NEW 36 / OVERLAP 9 / UNCHANGED 23 /
  NOLOOKUP 1), and re-importing the same file after export returned NEW 0 -
  the loop closes. **NEW PLATFORM TRAPS: (a) Ignition SILENTLY IGNORES
  Named Query parameters the query does not declare, while an undeclared
  `:Token` in the SQL reaches Postgres verbatim as `syntax error at or near
  ":"` - the character position tracks the token, which is the tell;
  (b) `bidirectional` belongs INSIDE `binding.config`, not beside `type` -
  misplaced it is silently ignored and every query bound to the prop returns
  nothing while the NQs test perfectly; (c) Ignition expressions have NO
  `startsWith()` and `page.props.path` is script-only - docked menu
  highlighting uses the `ProductionSideMenu` onStartup fragment map plus a
  session message; (d) WebDev resources must be IMPORTED as a zip - large
  Designer pastes truncate over RDP and produce a bare 501, and methods
  default to DISABLED on a new resource; (e) Perspective iframes never retry
  a failed load.** Business Systems added as the third Core System with its
  own `/business/*` namespace, side menu and expo landing page (glassmorphism
  recipe + WebDev Canvas2D access-control scanner). Shared-library edits ship
  as COMPLETE FILES - a pasted instruction note broke `shared.whatsnew`.
- v1.16.1 - Library packaging correction. `cm_rollup` now lives in Project
  Library package `cm`, so the timer and console calls are
  `cm.cm_rollup.run()` / `cm.cm_rollup.backfill(14)`.
  `CM_load_rollup_v1_1_0.py` supersedes v1_0_0 (logger renamed to
  `cm.cm_rollup`). Package `cm` shadows no Jython 2.7 stdlib module.
  Raw Log `2026-08-14_B` bumped to v1.1.0 with the corrected install order,
  which also now cites `CM_knife_schema_console_v1_0_0.py` as the Script
  Console route for the DDL.
- v1.16.0 - REGISTRATION for the 2026-08-14_B session. Raw Log `2026-08-14_B`
  added. Knife-bluntness visibility system: bluntness is a DELTA (trailing
  8 h loaded-avg torque vs 24 h post-knife-change baseline), chips
  SHARP < +10 % / WATCH +10-25 % / BLUNT > +25 % (provisional). Operator logs
  changes via two-press button -> `cm.knife_change`; Gateway Timer (Fixed
  Delay 300 s) `cm.cm_rollup.run()` fills `cm.load_rollup` 15-min loaded windows
  using per-tagid t_stamp ranges only (no live aggregates over sqlth_1_data);
  UI reads NQ `CM/KnifeDelta` (polling key omitted per hard rule). Confirmed
  `SafetyPlantOverview` never used `CM/Chippers` - it embeds CMVibrationCard;
  new `CMKnifeCard` component embedded x3 on the overview (v1.14.0) and knife
  chips + button on `CM_Chippers` v1.6.0.
- v1.15.1 - PumpRun resolution (2026-08-14_A follow-up). OPC probe: the
  `TnB_Area.Pumps[i].AOI` members are not externally readable (plain Bad /
  NodeIdUnknown for all i). Correct source is the house tree:
  `KPP/TnB/Devices/Hydraulic Stations/HydUnit4/Motors/Pump 1..6/Status/Running`.
  `StarLoaderPanel_View_v1_0_2` binds the hydraulics dot to an isGood-guarded
  any-pump-running OR (supersedes v1_0_1/v1_0_0); the Bad tag
  `KPP/TnB/Data/StarLoader/PumpRun` is DELETED (never worked, no history).
- v1.15.0 - REGISTRATION for the 2026-08-14_A session. Raw Log `2026-08-14_A`
  added. Probe-driven close-out of 08-12_B: the chipper drives were ALREADY
  historised for months under `KPP/Chippers/Devices/Motors/<Motor>/Status/*`
  (tagids 950-981, deadband 0.5, 1 h heartbeat) - `CM/DriveLoad` was a
  duplicate and was deleted same-day (18 sqlth_te rows retired cleanly).
  RULE: check sqlth_te + `Devices/Motors` before creating any drive/load tag.
  `CM_Chippers_View_v1_5_0` rebinds the LoadStrip to the Motors tree (v1_4_0
  must not be imported). Historian: `sqlth_1_data` is ONE partition to 2075 -
  console aggregates time out; use per-tagid ORDER BY t_stamp DESC LIMIT n
  seeks. Jython `except Exception` missed Java Throwable again - all probes
  now dual-catch. StarLoader: `Star Feeder Forward` = HMI_Controls[0].6 (a
  DIFFERENT device from the wheel jog .17) - no duplicate; axis verified live
  in degrees, degScale 1.0; sole gap is `PumpRun` (Bad) - micro-probe issued.
- v1.14.0 - REGISTRATION for the 2026-08-12_B session. Raw Log `2026-08-12_B`
  added. Three small projects researched from the COS PLC exports and built to
  S1 with **ZERO PLC CHANGES**: (1) TnB StarLoader panel for TNB Map -
  `RMC.AxisStatus.TnB.StarLoader.*` is controller-scoped and live, manual
  control reuses the existing HMI bits (jog bits are LEVEL-HELD, hold-pos
  SELF-CLEARS); (2)+(3) chipper knife-bluntness load monitoring - the
  `MCC_ATV` AOI already publishes scaled `Status.Current` (A) and
  `Status.Torque` (%) for DiskChipperMotor1/2 + DrumChipper at
  Program:Chippers scope, so "arrays in the PLC" were never needed.
  `CM/DriveLoad` UDT + 3 instances, `CM_Chippers` v1.4.0 LoadStrip,
  `StarLoaderPanel` v1.0.0 + SVG (wheel rotation via its own svg component's
  `position.rotate.angle` - the map-proven pattern). Tag imports GATED on the
  historian probe (never rename historised tags - 08-12_A E8). Probes not yet
  run.
- v1.13.0 - REGISTRATION for the 2026-08-12_A session. Raw Log `2026-08-12_A`
  added (SS3). **CONDITION MONITORING IS LIVE AT KPP** - two ifm IO-Link
  vibration sensors (VVB010 on Chipper Disc Motor 2 `CHP_IOLINK_DSC2_PORT1`,
  VVB301 on Drum Chipper Motor `CHP_IOLINK_DRM_PORT3`) through a new
  `CM/VibMotor` UDT, **29 historised tags on `KPP_production`**, a standalone
  `CM/Chippers` view and a parameterised `CMVibrationCard` embedded into
  `SafetyPlantOverview` **v1.13.0** as "SMART MOTOR CONDITION MONITORING".
  **ZERO PLC CHANGES** - the ifm AOIs already output scaled REALs, so the whole
  build is read-only OPC; the spec's packed-word assumption was disproved from
  the L5X before any build. Units corrected: a-values are **milli-g not g**.
  **CM DELIBERATELY SITS OUTSIDE WORKMATE** - Workmate stays the portable core
  for other customers, CM is plant-specific; own top-level `CM` tag folder and
  `CM` view folder (renamed from `WM_CM` while only idle data existed). **NEW
  PERSPECTIVE TRAP: view params are SILENTLY DISCARDED unless declared
  `"params.<Name>": {"paramDirection": "input", "persistent": true}` in the
  view-level propConfig** - the view renders its own defaults with no error, and
  the first card looked correct because it matched the defaults; two wrong
  theories chased before comparing against the working `HydraulicsDiagnosticsCard`.
  Three sparkline facts: component is `ia.display.sparkline`, data prop is
  `props.points`, trace colour is top-level `props.color` (NOT
  `desired.stroke.color`); tag-history `tags` needs an ARRAY - bind
  `custom.tagpath[0].path` per `RingPressureSetpointRegulator`. **A DYNAMIC
  Y-AXIS IS WRONG FOR A TREND** - an expression-bound `range.high` rescales the
  whole trace every poll; replaced with a static `ScaleMax` input param.
  **SENSOR COMPARISON CORRECTED FROM DATASHEETS** - VVB301 (NZ$779) is CHEAPER
  than VVB010 (NZ$875.20) and BOTH carry BLOB; the 010 wins on band (10 kHz vs
  5.6 kHz), g-range (50 vs 16 g) and stud mounting, so **010 for chippers/large
  drives, 301 as general plant standard**. Field evidence already tightening it:
  drum aPeak **13.4 g against the 301's 16 g ceiling**. ISO 2.3/4.5/7.1 edges are
  Group-1-rigid placeholders and probably wrong for an impact machine - now input
  params, to be set from observed distribution. Also: **deleting a tag folder
  does NOT retire its `sqlth_te` rows** (29 cleared by guarded console script).
  STAGED, not yet compiled: Platform Rules (paramDirection, sparkline id/props/
  colour, tag-history array binding, static trend axis, sqlth_te retire-on-delete),
  Domain Data Reference (`CM` tag family + AOI member map + units),
  Reporting Technical Reference (CM surfaces + CMPanel placement),
  ConditionMonitoring Spec bump to v1.2.0.
- v1.12.0 - REGISTRATION for the 2026-08-10_A session. Raw Log `2026-08-10_A`
  added (SS3). **THE OFFICE WEEKLY FEED IS LIVE** - two new tables
  `dbo.WeeklyStats` + `dbo.WeeklyReportColour` in the **`Transformations`**
  database, dev on KTSQLDEV and live on **KTSQL02**, written by
  `shared.weeklyreport` **v0.8.1** on each Monday run from the values it
  already computes for the email (upsert on `WeekEnd`, wrapped so a DB failure
  can never stop the send). **THE TARGET WAS NOT WHAT THE REQUIREMENTS DOC
  SAID** - the doc specified the `KPP` database on KTSQLDEV/KTSQLSYS; four
  candidate targets were pursued and abandoned before the answer was settled
  not by a document but by **where Vivi had already granted `svc_Ignition`**
  (ddladmin/reader/writer on Transformations, live + dev). New rule: where the
  grants are is where the table goes. **KTSQLSYS IS AN ALIAS FOR KTSQL02** -
  `@@SERVERNAME` disagrees with the Connect URL host; same class as the
  `TLSQL01_Resources` -> KTSQL02 rebrand artefact. **CLONING AN IGNITION
  DATASOURCE DOES NOT COPY THE EMBEDDED PASSWORD** - the clone faults with
  `Login failed for user '<user>'`, which reads as a missing account and sent a
  full diagnostic detour after non-existent logins, auth modes and
  `securityadmin`; the disproof was a working connection using the same login
  on the same instance. Two probe rules: `fn_my_permissions` **throws** for
  low-privilege logins so its error is noise, `IS_MEMBER` is the load-bearing
  check; and `IS_MEMBER` reports the **current DB context only**, so
  cross-database it returns `None` meaning "wrong question", not "no rights".
  Colour master keys on **ROLE not metric** (the report traffic-lights by
  performance, so the same tile is green or orange by result) with hex read
  from `code.py` constants - screenshot-eyeballed hex was wrong on all six.
  STAGED, not yet compiled: Platform Rules (datasource-clone secret, alias
  hosts, `fn_my_permissions` vs `IS_MEMBER`, connection-name-vs-`DB_NAME()`),
  Reporting Technical Reference (the two new tables + the
  `KTSQLSYS_Transformations` connection + the weeklyreport persist path).
- v1.11.0 - REGISTRATION for the 2026-08-06_B session + a COMPILE pass on
  `KPP_Platform_Rules` (**v1.10 -> v1.11**). Raw Log `2026-08-06_B` added (SS3).
  **YARD IS NOW ITS OWN REPORTING AREA** - page `/Reports/Yard/Yard`, rail item
  above MLY, two tabs (Daily Production + SED Distribution); the leaf views did
  not move, the new container embeds them in place. **FOUR NEW EXPLORATION
  REPORTS**: `Yard Processors/SED Distribution` v1.0.4 (Belinda - replaces the
  Sticks report from `[Sticks_Sync].dbo.vLogs`, adds grade multi-select,
  operator and length filters), `KPP SED Distribution` v1.0.2 (same for the KPP
  line from `usnr.prod_report`, chip toggle), `Butt Cuts Exploration` v1.2.1 and
  `Booth Calls Exploration` v1.1.2 (both Renata - one pivotable NQ each, four
  group-by modes off a `CASE :groupby` key). Production container **v2.12.0**,
  Hubsidemenu **v1.3.0**, stylesheet **v2.44 + v2.45** (attractor class family
  with a written-in retirement policy). **THE KNIGHT-RIDER BAR RELAPSED** - a
  rule documented since 2026-07-19_A was rediscovered the expensive way, and
  Platform Rules v1.11 now records that it is a TWO-part trap whose halves mask
  each other (dead reusable component + a lower script that ignores the
  query-binding double-fire), plus: read the rules doc, do not grep the
  stylesheet. Three further Perspective rules compiled - root container
  `meta.name` must stay `root` (renaming kills every `/root/...` binding); a
  cloned chart carries the donor's hard-coded axis range; stat props need a
  pre-keyed literal AND `coalesce()`. **THREE SHIFT CONVENTIONS CONFIRMED** -
  USNR 2/3, booth 1/2, maintenance 06:00, with **booth 1 = USNR 2 = day**;
  proven by `operator.shift_times` plus a same-day stem-count cross-check after
  a derived prune-call shift silently joined day calls onto night rows.
  STAGED, not yet compiled: Domain Data Reference (`vLogs`, `CH Disc Start`
  semantics, HA junk ranges, `operator.*` booth family), Reporting Technical
  Reference (new Yard area + four views + six NQs + the single-NQ pivot
  pattern), Workmate Perspective Rules (attractor family), Working Method
  (layered smoke-test shape; round before bucketing on `numeric`).
- v1.10.0 - REGISTRATION for the 2026-08-06_A session + the first
  COMPILE/CORRECTION pass since v1.9.x. Raw Log `2026-08-06_A` added (SS3).
  **THE TR FOLD IS REMOVED** - `usnr.prod_report` **v2.0.0**, gradename =
  `trim(l.gradename)` for all rows; the `LIKE 'TR%' -> 'TR'` collapse and its
  one-off `TR  1` exemption are gone. Trina's `TR  M` / `TR  S` were the
  SECOND recurrence, and the fold was also silently breaking ORDER
  COMPLETION (the Product NQ joins on grade + nominal_length; orders carry
  full variant names) - six order/length pairs now match incl. TR M 4250 and
  TR S 4250; month totals unchanged (61,540 logs / 20,309.3 m3); two legacy
  bare-`TR` orders (4800, 6050) now correctly show NO MATCH and need an
  office decision. **MLY DAILY 31st FIXED** - `Production By Day` +
  `Production By Day and Grade` **v3.0.0**: KPP's 07:00 `util.endOfMonth`
  convention was amputating MLY's last operating day of EVERY month (only
  visible as the missing 31st); NQs now use whole-calendar-day sargable
  ranges. **MONTHSELECTOR COLLISION RESOLVED** (carried from 08-01_B) -
  original component retained, EmailReports monthly leaves **v1.0.2** bind
  `selectedMonth`. COMPILED THIS PASS because the fixes CONTRADICTED existing
  text: `KPP_Domain_Data_Reference` **v1.6 -> v1.7**,
  `KPP_Platform_Rules` **v1.9 -> v1.10** (VIEW-CASE rule rewritten + new
  rules: an exemption branch treats the symptom, the rule itself is usually
  wrong; a shared date helper can carry a site-specific convention),
  `KPP_Reporting_Technical_Reference` **v1.4.0 -> v1.5.0**. Still staged:
  fleet-check before creating a Components/Objects component and silent
  param-binding failure (-> `Workmate_Perspective_Rules`); wrong-system
  probes still exclude that system, identify a surface by its column set
  (-> `KPP_Working_Method`).
- v1.9.10 - CORRECTION to the 2026-08-01_B registration: the "new"
  MonthSelector collided with an EXISTING `Components/Objects/MonthSelector`
  (param `selectedMonth`, embedded by the Boardpack). New component
  withdrawn; RESTORE zip issued
  (`view_Components_MonthSelector_RESTORE_original_v1_0_0.zip`); monthly
  leaves now **v1.0.2** binding `selectedMonth` + `defaultToLast: true`.
  Raw Log 2026-08-01_B bumped to **v1.0.1** (E2 rewritten). Fleet-check
  rule staged for Workmate_Perspective_Rules.
- v1.9.9 - REGISTRATION for the 2026-08-01_B session (same day, after _A was
  cut). Raw Log `2026-08-01_B` added (SS3). **EmailReports grown 2 -> 5
  tabs** (KPP Daily | KPP Weekly | KPP Monthly | MLY Daily | MLY Monthly) on
  one leaf contract (render_data_uri / send_from_view / _coerce_date /
  render_for_web); `shared.monthlyreport` **0.2.4 -> 0.2.6**,
  `shared.mlyproduction` **0.2.3 -> 0.3.0** (ref_date threading), NEW
  reusable **`Components/Objects/MonthSelector` v1.0.0** (chevrons snap to
  the 1st, clamps at current month, defaults to previous month). **KOS
  fixes:** BoardpackCard v1.1.0 adds the missing `pct1` case (uptime showed
  "1" = int-fallthrough of 0.887); 74.3 = 74.3 proven the 60-SHIFT IDENTITY
  (hours x 60 / 60) by 13-month recompute, not a bug; SummaryGroup +
  SummaryActual/Forecast NQs identified as an UNEMBEDDED legacy surface -
  left untouched. **THE VOLUME TRIANGLE CLOSED (119,575 / 123,172 /
  124,842):** recon chain v1.2-v1.4 proved usnr.prod_report is stem x log
  (sum logvolume, never raw stemvolume); the canned monthly reads
  **kppstems.kpi_daily** (USNR block commented out) with a
  current-month-only 07:00 refresh; the daily MTD chart dropped DAY 1 in
  31-day months; capture runs **~-1.4% volume / ~5% stems under USNR every
  day** (drops small stems) and June only "agreed" because USNR lost Jun-11
  entirely - accidental correctness. ALIGNMENT DECISION: kpi_daily is the
  headline family everywhere (`shared.dailyproduction` **4.7.12 -> 4.7.15**:
  dedicated MTD pull, PRO-RATA forecast line ending at Predicted Plant
  Volume, month figure in the intro, E10 truncation loop paid;
  monthlyreport 0.2.6 chart on kpi_daily); USNR = labelled reconciliation
  reference. **FY panels ACQUITTED** - the "wrong" totals are exact sums
  (FY25 1,186,163 / FY26 1,313,072); backfill console B1 showed all canned
  months ok, B2 never run; sum-check before bug-hunt. **FREEZE AUTOMATED:**
  NEW event `Boardpack Close Monthly` (5 7 1 * *; month always, quarter
  Sep/Dec/Mar/Jun, FY on Jun; refresh-first; conflict-do-nothing) - the
  07:10 monthly email now always reads FROZEN; **July 2026 frozen at
  123,207 / 123,064, uptime 0.8873**. Data-quality: USNR Jun-11 missing;
  kpi_daily stems degrade retroactively (Jun-8/15/16). Staged rules at the
  log's tail for Platform / Domain / Tech Ref / Perspective passes.
- v1.9.8 - REGISTRATION for the 2026-08-01_A session (Qube/MLD throughput
  question -> exec report -> multi-year dashboard -> go-forward sync closed).
  Raw Log `2026-08-01_A` added (SS3). **THE ANSWER, for reuse:** MLD production
  per shift is down and it is NOT the piece mix and NOT more stoppages - it is
  feed pace while running (583 -> 536 logs per running hour 2023->2026, while
  running hours per shift went UP 9.44 -> 9.58); worth ~440 logs / ~174 m3 per
  operating day. A separate supply-mix factor (piece volume 0.43 -> 0.39 m3 at
  flat length) compounds it for the per-tonne contract. Deliverable
  `KPP_MLY_Debarker_Throughput_Review_v1_0_0` (PDF + Word). **STANDING #1
  CLOSED:** NEW `mly.pace_daily` + NEW **`db.sync.mly.production` v1.0.0**
  (upserts production AND pace) + 2 sync NQs + scheduled `Sync MLY Production`
  20:10 daily; backfilled 997 days to 2023-05-22; `mly.production_daily` is now
  a deliberate HYBRID (997 `logdata` + 1,227 `xlsx`, manual record kept where
  the scanner was down). Dashboard reads NO LogData at view time. NEW library
  **`shared.mlytrends` v1.7.0** + 4 multi-year NQs; NEW Reports/MLY tabs
  **Multi Year Production / Multi Year Pace / Loaders** (page reordered to open
  on Multi Year Production, container v1.4.0). NEW **`mly.planned_label` +
  `is_planned`** through `downtime_ev`/`_detail`/`_clean` - maintenance days
  flagged SEPARATELY from `is_break` on purpose (folding them together would
  render a shut day as 100% uptime and gut the cause chart); uptime chain
  deliberately untouched, that is v2.3.0's job. `shared.mlyproduction`
  **v0.1.8 -> v0.2.3**: monthly Key Metrics comparison (This Month | Last Month
  | Prior 6-Mo Avg), daily + monthly downtime sections ported from
  `shared.dailyproduction`, reason-level bar labels, maintenance excluded like
  smoko, section reorder. KT financial year (Jul-Jun) applied to all yearly
  charts. NOT a reference-doc compile - staged rules at the raw log's tail
  (**`except Exception, e` does not catch Java exceptions in Jython** - highest
  priority, it invalidates the isolation of existing probe scripts; never
  memoise a failed build + Designer-vs-gateway JVM memos; NQ Database dropdown
  defaults to last-used; trim-and-re-append `while` fixed-point check; hand-built
  legends lose click-to-toggle; `stepLine` styling ignored by the wrapper;
  is_break vs is_planned; pace metric definitions; FY convention; safety red is
  for safety information only) are for the next `KPP_Platform_Rules` /
  `KPP_Domain_Data_Reference` / `KPP_Reporting_Technical_Reference` /
  `Workmate_Perspective_Rules` pass. **LIVE LATENT BUG FLAGGED AT KPP:**
  `shared.dailyproduction._render_pareto_chart_png` has the same infinite
  truncation loop fixed here in v0.2.2 - one long cause name will hang the KPP
  daily report.
- v1.9.7 - REGISTRATION for the 2026-07-31_A session (MLY stood up as its own
  reporting area, two working days 07-30/07-31). Raw Log `2026-07-31_A` added
  (SS3). NEW **`mly` schema** in KPP_production - a full mirror of the TuiTech
  Downtime app at 10.15.16.21 (found by reading the connection string out of
  `DownTime.exe` + its `.config`; the DB we already query, MLY_LogSorter, never
  held downtime): tables `downtime`/`area`/`subarea`/`cause`/`reason`/
  `shift_period`/`actual_shifts`/`excluded_label`/`shut`/`production_daily`, and
  views `downtime_ev`/`_desc`/`_detail`/`_clean`, daily/weekly/monthly rollups,
  `reliability_shift`/`_daily`, `downtime_health`, `production_daily_all`. NEW
  datasource `MLY_DownTime`. NEW sync **`db.sync.mly.downtime` v1.0.0** + 7 NQs,
  scheduled `Sync MLY Downtime` 20:00 daily; 35,762 rows mirrored. NEW **Reports/
  MLY page** (5 tabs: MLY Daily, MLY By Grade, Downtime, Downtime Detail,
  Scheduled Shuts) - MLY tabs REMOVED from Reports/Production (v2.5.0), MLY nav
  button added (Hubsidemenu v1.2.0, forest green). **`schedule` package SPLIT**
  into `schedule.kpp` + `schedule.mly` (only two callers project-wide, both in
  Calendar/ShutEdit). NEW `mly.shut` + Scheduled Shuts calendar (MLY = Wednesday,
  the day before KPP's Thursday). Smoko excluded from reportable downtime via the
  configurable `mly.excluded_label` (reportable 31,940 / 9,597.9 h; breaks 3,683).
  Trina's manual workbook imported to `mly.production_daily` (2,218 days back to
  2019-06-03 - the only surviving pre-2023 production record; LogData was purged
  when full, NOT the downtime DB). **TWO SHARED FIXES touching KPP too:**
  `table_utils` v1.1.0 (hh->HH, every ParametricTable timestamp project-wide read
  13:42 as 01:42) and `ParametricTable` v1.2.0 (persisted-fossil-dataset and
  Bad_Stale-on-load both fixed with an empty-dataset default). MAJOR retracted
  error logged: the workbook DOWNTIME import never ran (INSERT referenced a
  non-existent `src` column, parse-failed, wrote zero) and the "missing rows" it
  chased were a `"%.1f"`-vs-half-up rounding artifact + stale pre-correction
  classifications - workbook downtime import ABANDONED, DB is authoritative. NOT
  a reference-doc compile - staged rules at the raw log's tail (Designer-export
  zip format + no-leaf-to-folder import, NQ-dropdown-must-save, bare-except-hides-
  wrong-answers, verify-columns-against-live-schema, walk-the-JDBC-cause-chain,
  never-key-a-float-through-display-rounding, nullif+filter roster denominators,
  mirror-fixes-revert-fix-at-source, ParametricTable persistence, HH-not-hh, the
  MLY domain section, the MLY schema/source/page map, TuiTech connection-recovery)
  are for the next `KPP_Platform_Rules` / `KPP_Domain_Data_Reference` /
  `KPP_Reporting_Technical_Reference` / `KPP_Migration_Reference` pass.
- v1.9.6 - REGISTRATION for the 2026-07-29_A session (PlantKPI completion ->
  data-quality arc). Raw Log `2026-07-29_A` added (SS3). Library
  **`shared.plantperformance` v1.6.0** (getCrewTrend, getDowntimePareto,
  getFidelityByOperator, availability sanity guard - v1.5.0 could emit a
  NEGATIVE PPI). PlantKPI -> **v1.7.0** (six tabs: + Crews, + Availability;
  fidelity-by-operator on Execution; loading scanners and no-data notes).
  TeamKPI -> **v1.5.0** (multi-year spans on Monthly, Average-only labels on
  lookbacks, scanners on all four tabs). **FOUR DATABASE VIEWS PATCHED:**
  `team_summary_monthly_per_shift` v2.0 and `summary_monthly_per_shift` v2.0
  (physical stem-size guard, later tightened to 0.4-5.0),
  `downtime.reliability_shift` v2.0 (negative uptime clamped/NULLed), and
  `grading_kpi_daily` (NOT EXISTS against the NEW table
  `kppstems.grading_kpi_exclusions`, 5 sample-loss shifts). Grading capture
  itself was fixed at source on 16 Jun 2026. NOT a reference-doc compile -
  staged rules at the raw log's tail (composite-key join testing, the
  loading-flag pattern and its four failure modes, multi-source charts,
  guard-the-view-not-the-capture, Postgres view-SQL normalisation, the
  OR-filter parenthesis trap, mandatory matview refresh, import-order
  verification) are for the next `KPP_Platform_Rules` (->2.0) / Tech Ref
  (->1.5) pass.
- v1.9.5 - REGISTRATION for the 2026-07-28_A session (PlantKPI build-out ->
  TeamKPI rework). Raw Log `2026-07-28_A` added (SS3). NEW script library
  **`shared.plantperformance` v1.3.0** (PPI = Availability x Rate x Quality,
  empirical 16-cell piece-size/length standard, period drill-down). NEW report
  page **PlantKPI v1.1.0** with four tabs (Performance, KPIs vs Production,
  Execution, Rate Standard) at bundle **v1.1.6**, plus the Plant sidemenu
  button (Hubsidemenu v1.1.0). Scorecard lib -> **v3.12.0** (metric-
  parameterised getTrend + getMetricOptions, for Phil's per-KPI and per-
  category graphs). OperatorKPI shell -> **v1.5.0** with NEW **Progress Table
  v1.1.0**; Progress -> **v1.5.0**. TeamKPI -> **v1.1.1** (shared
  PeriodSelector replaces Dave's DateRangeSelectorNew on Monthly and
  Distribution; Value Recovery / Waste / tab strip switched to the light
  views). NOT a reference-doc compile - staged rules at the raw log's tail
  (resource.json manifest + versioned roots, flex-canvas resizeDelay, canvas
  glow/breathe, retrofit-in-same-pass, persistent-prop rename hazard,
  empirical self-benchmark, watch-metrics-outside-the-index) are for the next
  `KPP_Platform_Rules` (->2.0) / Tech Ref (->1.5) pass.
- v1.9.4 - REGISTRATION for the 2026-07-27_A session (Kerry COS root cause ->
  Plant Performance kickoff). Raw Log `2026-07-27_A` added (SS3). Scorecard lib
  -> **v3.11.1** (3.10.4 cache bump for the COS NQ v2; 3.11.0 getTrend/
  getKpiMatrix; 3.11.1 active-only filter + opCats). Three COS NQs -> v2
  (occurrences hours-anchored LEFT JOIN fix - the event-anchored single-KPI
  trap silently dropped Kerry/Clint/Darren/Matt; minutes chart NQ; minutes-
  per-hour NQ incl. booth 2->3 bug). NEW NQ Report/KPI/Operator/Booth Hours.
  OperatorKPI shell -> **v1.4.0** (three new tabs: Booth Hours v1.0.0,
  Progress **v1.2.3** [band+median trend, all-operators mode, glow/breathe
  halo, team wording], KPI Matrix v1.0.0 [Embr matrix heatmap]). NOT yet a
  reference-doc compile - staged lessons listed at the raw log's tail
  (event-anchor rule; whole-struct guarded transforms; canvas glow/breathe
  vs CSS; Embr bundled plugins + scriptable options; active-flag pattern)
  are for the next `KPP_Platform_Rules` (->2.0) / Tech Ref (->1.5) pass.
- v1.9.3 - COMPILE pass for the 2026-07-19_B session (upgrades the v1.9.2
  registration). `KPP_Platform_Rules` 1.8 -> **1.9** (new dated section
  "Scorecard cache, calibration & Perspective wiring - hard-won 2026-07-19":
  NQ named-param must be declared or `:name` passes through unbound; Script-
  Console CREATE OR REPLACE is gateway-wide; result cache = single scheduled
  writer + SAVE before manual warm + SCRIPT_VERSION stamp/bump; cache whole
  fleet, filter at read, live period always fresh; content-swap mount returning
  `{}` starves that tab; calibration method target=best/worst=just-past-max +
  period-SUM normalisation; plain-hyphen-only in ALL deliverables incl. docs).
  `KPP_Reporting_Technical_Reference` 1.3.0 -> **1.4.0** (§11 Operator-KPI
  scorecard subsystem: 10 calibrated KPIs, `operator.scorecard_cache` + warm
  timer, Oct-2025 floor, manager/Explain toggles, timeliness min/month +
  proportional-booth view, three new NQs). Scorecard lib v3.10.3; both
  timeliness fns exclude Chippers; `ScorecardCacheWarm` timer -> Dedicated;
  Booths By Day NQ 3rd param added - both 07-19_B mechanical to-dos closed.
- v1.9.2 - registration bump for the 2026-07-19_B session (Operator-KPI review:
  Phil/Trina meeting changes + full fleet calibration + result cache + Oct-2025
  floor + Forensics/Timeliness fixes). Raw Log `2026-07-19_B` added (§3) with its
  deliverables. NOT yet a reference-doc compile - the durable lessons (version-
  fight save-before-warm / single-refresh-owner cache timer; NQ named-param must
  be declared or passes through unbound; Script-Console CREATE OR REPLACE is
  gateway-wide; result-cache pattern with SCRIPT_VERSION invalidation; calibration
  method target=best/worst=just-past-max; timeliness period-SUM min/month
  normalisation; mount `return {}` starves embedded tabs; **plain-hyphen-only
  rule, no em/en dash - banked to memory**) are STAGED for the next Platform
  Rules (→1.9) / Tech Ref (→1.4) compile. Scorecard lib → **v3.10.3**; new
  `operator.scorecard_cache` table + `ScorecardCacheWarm` timer; `operator.kpi`
  → v1.1.0; three new NQs (Waste %, T&B occ/hr, Booths By Day). Also carries the
  07-19_A compile (Platform Rules 1.8 / Tech Ref 1.3.0 / Control Text Standard
  1.1.0) which itself was not yet folded into this index.
- v1.9.1 - added `KPP_Control_Text_Standard` **1.0.0** (project-wide selector/
  control typography: 13px bold #242E30 centred values via the
  `kpp-selector-value` Advanced-Stylesheet class - inner input elements ignore
  wrapper `props.style`, verified on DaySelector). DaySelector → v1.2.1
  (class-wired), WeekSelector → v1.1.0 (prev-week default + range-box centre).
- v1.9.0 - compile pass for the 2026-07-18 EmailReports / Hub-tiles session
  (Raw Log 2026-07-18_A). `KPP_Platform_Rules` 1.7 → **1.8** (new dated section:
  unicode escapes per-layer; java `system.date.parse` blank throw; iframe `src`
  + Designer data-URI freeze guard; **display:false does NOT prevent embedded-
  view mounting → single path-swapped Content**; query-bound null-guards;
  `meta.classes`→`props.style.classes` activates dormant classes; null custom
  defaults break commit; `runScript(…,0)` tile-feed pattern; WebDev resource
  type + 402; session `hub-nav-active` rule).
  `KPP_Reporting_Technical_Reference` 1.2.0 → **1.3.0** (§10: EmailReports
  views + data-URI render/send, `shared.reporttiles` v1.2.0 + NQ provenance,
  Hub tile scorecards, Production v2.4.0 restructure, nav wiring). New script
  lib `shared.reporttiles`; `shared.dailyproduction` → v4.8.1;
  `shared.weeklyreport` → v0.2.1. Raw Log `2026-07-18_A` added (§3).
- v1.8.0 - MERGE of the two independent 2026-07-15 sessions. Session `_A` (USNR
  Product / Chip & PcSz) had bumped the docs to platform 1.6 / domain 1.5 /
  tech-ref 1.1.0 / index 1.7.0. Session `_B` (Echo Report refresh + date fix, Raw
  Log 2026-07-15_B) produced overlapping bumps at the SAME numbers; its lessons
  were merged ON TOP of the `_A` versions and bumped a further step:
  `KPP_Platform_Rules` 1.6 → **1.7** (scope-G script actions; Gateway TIMER vs
  SCHEDULED tabs; single-refresh-owner rule CORRECTED - audit the schedule, a
  rogue retired-Echo sync was a 2nd refresher; 07:00 date-picker rule;
  page-scoped-sendMessage soft refresh + view-custom `refreshBinding` folded into
  the Perspective section). `KPP_Domain_Data_Reference` 1.5 → **1.6** (§3 refresh
  ownership corrected; §7 date-cast rule). `KPP_Reporting_Technical_Reference`
  1.1.0 → **1.2.0** (§4a matview cadence + 3-owner correction, §6a report refresh,
  §6b 07:00 date fix, F6-F8). Raw Log `2026-07-15_B` added (§3). The `_B`
  Perspective lessons live in `KPP_Platform_Rules` (not a separate ADD).
- v1.7.0 - compile pass for the USNR Product / reporting session (Raw Log
  2026-07-15_A). `KPP_Platform_Rules` 1.5 → 1.6 (new "Perspective views" section:
  onChange JSON shape, no `system.util.later`, onStartup `import system`,
  chart-js annotation init, `refreshBinding` handle, inline-label loading-bar,
  NQ double-fire, footer null-guard, DebugConsole session scope; + PostgreSQL
  `nullif` divide guard and VIEW-CASE grade-collapse). `KPP_Domain_Data_Reference`
  1.4 → 1.5 (prod_report VIEW grade collapse + `TR  1` exemption, COMPART,
  BK-OPT dead → completion recompute, three div-by-zero guards).
  `KPP_Reporting_Technical_Reference` 1.0.0 → 1.1.0 (§3.4 USNR objects, §6 USNR
  rows).
- v1.6.0 - waste-fix compile pass (Raw Log 2026-07-09_A §E4): `KPP_Platform_Rules`
  1.4 → 1.5; `KPP_Domain_Data_Reference` 1.3 → 1.4.
- v1.5.0 - waste-pipeline investigation banked (Raw Log 2026-07-09_A).
- v1.4.0 - renamed `Workmate_Knowledge_Index` → `DashboardandPLC_Knowledge_Index`.
- v1.3.0 - raw-log series corrected to `DashboardandPLC_Raw_Log`.
- v1.2.0 - raw-log series adopted (§3): one log per session, append-only.
- v1.1.0 - KPP capture/reporting merged in; `KPP_Project_Knowledge_Index` retired.
- v1.0.0 - initial front door.

**Rule.** Load this first. Open other docs only when their read-when trigger
fires. Every delivery that adds or bumps a doc updates this index in the same
pass (`DashboardandPLC_Knowledge_Standard` §3). **Same-day multi-session note:**
when two sessions land on the same day, they take different letter suffixes
(`_A`, `_B`) AND must not both bump a compiled doc to the same number - the
second merges on top and bumps again (see v1.8.0).

---

## 1a. Compiled docs - Workmate side (version-bumped in place)

| Doc | Version | Read when… |
|---|---|---|
| `DashboardandPLC_Knowledge_Index` | 1.57.0 | Always - this file. |
| `DashboardandPLC_Knowledge_Standard` | 1.3.0 | Writing, merging or retiring any knowledge doc. *(staged: Raw Log 2026-10-14_C section 9 item 11 - list the project docs before taking a raw log letter or an index number, and merge any index ADD written since the index was read.)* *(staged: Raw Log 2026-10-20_B section 7.2 item 12 - build the next index on the newest one in the project and list the project docs again just before writing it: 1.51.0 was built on 1.50.2 while 1.50.3 was written, and 1.52.0 came in while 2026-10-20_B was being written.)* |
| `Workmate_Perspective_Rules` | 2.0 | Any Perspective build/debug. *(staged: `Workmate_Perspective_Rules_ADD_2026-07-09` - merge at next touch. The 2026-07-15 Perspective lessons went into `KPP_Platform_Rules` v1.6/v1.7 instead; the 2026-09-25_A motion lessons (CSS transition, mount settle flag) into v1.15.)* *(also staged: the 2026-09-30_A view-commit lesson - "expected string, got null" on a clean file after a long Script Console run.; the 2026-10-03_A lessons - a glow clipped by the parent's overflow, a click bubbling out of a card, the view-level onStartup, delete-and-recreate when components change, never write from a binding.)* *(also staged: the 2026-10-07_A lessons - a PE array drawn as one symbol shows only its first eye; close a popup by the id it was opened with and size a menu popup from its items - Raw Log 2026-10-07_A section 9 items 13-14.)* *(also staged: the 2026-10-09_A cross-reference - a view with no onStartup opens on the values last saved in the Designer - Raw Log 2026-10-09_A section 9 item 13.)* *(also staged: the 2026-10-10_A cross-reference - `lineHeight: 1` labels draw scroll arrows, an overlay on a shared map follows its `Labels` param, the small status tile pattern - Raw Log 2026-10-10_A section 9 items 4-6.)* *(also staged: the 2026-10-08_A cross-reference - a role-gated control (enabled from the session roles, a bidirectional tag binding, a who-can-change line) - Raw Log 2026-10-08_A section 9 item 9.)* *(also staged: the 2026-10-15_B cross-reference - an input in a flex row keeps its own width; a layout that follows the screen from `page.props.dimensions`; balanced card columns; a non-persistent custom prop with no binding does not exist at runtime until written; `system.util.getGlobals()` belongs to the JVM it runs in - the Script Console's is the Designer's; ages and waits on a monotonic clock - Raw Log 2026-10-15_B section 10 items 1-4, 8 and 9.)* *(also staged: the 2026-10-15_B post-close cross-reference - the Designer saves a persistent property's live value as its default (reset and seed in `onStartup`; no param default that names a real record); session roles reach `runScript` as QualifiedValues; a glow on a repeated row goes on an inner element with room - a repeater with `overflow: hidden` clips an outer halo - Raw Log 2026-10-15_B section 12.7 items 11, 12 and 15.)* *(also staged: the 2026-10-17_A cross-reference - a sheet too long for a tooltip goes behind a button, a popup sized to its content - Raw Log 2026-10-17_A section 10 item 13.)* *(also staged: the 2026-10-15_C cross-reference - a component taking another's place keeps its style on the open sessions; a card fed by a script transform returning a dict; an SVG data URI built once per result - Raw Log 2026-10-15_C section 9 items 2, 4-5.)* *(also staged: the 2026-10-14_E cross-reference - a loading bar derived from the answer's own window (no latch over two change scripts), `try()` does not catch Bad_NotFound, `numberFormat "0"`, hover tips on a title row - Raw Log 2026-10-14_E section 13 items 1-4; and the 2026-10-20_A Perspective items - a swapped view.json leaves the old rows' state on the rows that take their places, meta.visible false keeps the flex slot, an embedded tab's first query answer can be for no dates (a Nonce parameter) - Raw Log 2026-10-20_A "Knowledge Index - add"; its "bump root.meta.name" meets the compiled rule that root stays `root`.)* |
| `Workmate_Gold_Standards` | 1.3 | Starting a new view/component - what to copy and why. |
| `Workmate_Compact_Table_Standard` | 1.0.0 | Adding or styling any table. |
| `Workmate_View_Index` | 1.0 | Locating a Workmate view / confirming its version. |
| `Workmate_AI_Architecture` | 1.1 | Anything `workmate-ai` - layers, tools, security, phasing. |
| `KPP_Plant_Memory_Export` | 1.1.0 | Workmate plant/SCADA context - project state, curated rules, people, DBs, safety forensics. |

## 1b. Compiled docs - KPP capture/reporting side

| Doc | Version | Read when… |
|---|---|---|
| `KPP_Working_Method` | 1.3 | **First read for any KPP task** - build cycle, verify-don't-guess, shadow-first, approval gate; probe the premise, test a rule on the full history, stopgaps that report a verdict, machine-changing HMI actions. *(staged items: Raw Logs 2026-09-30_A, 2026-10-03_A, 2026-09-30_B, 2026-10-07_A, 2026-10-09_A, 2026-10-10_A, 2026-10-08_A, 2026-10-12_A, 2026-10-13_A, 2026-10-14_A, 2026-10-14_C and 2026-10-14_D, section 9 - and 2026-10-13_A section 11 item 8, 2026-10-14_C section 11 item 13, 2026-10-14_D section 11 items 12-13.)* *(staged: Raw Log 2026-10-15_B section 10 items 5-6 - look at the generated views before delivery: render them with the bindings evaluated and screenshot them at the real screen width; an HMI action that moves machinery: one gateway lock, the command bits read off before a number changes, the dead man armed first, a watchdog timer with a heartbeat the actions check, audit rows off the lock, a PLC timer as the real dead man, then an independent review and a check of each round of fixes.)* *(staged: Raw Log 2026-10-15_B section 12.7 item 18 - say what an audit table does not see before building on it.)* *(staged: Raw Log 2026-10-15_A section 13.5 items 23-25 - read the load before choosing what to change (requests per rate on the driver's Details page, not tag counts), then one change and one survey each; two independent measurements before a scale change, and a verdict that prefers the fit with the wider range; check a cause by its arithmetic before a PLC edit.)* *(staged: Raw Log 2026-10-16_A section 9 items 4-7 - a proof run reads its sources once, no edit while it runs; a simulation proves what it models - review the code before the final proof run, then prove again; check that a second sensor is not a copy of the first before a probe judges by it; every version line is part of the install; and section 13.1 item 15 - a figure for the chat comes from the source.)* *(staged: Raw Log 2026-10-19_A section 6 items 3-5 - a fix to one library goes to its clones in the same pass (search the project for the same block); prove a harness on the reported numbers first - the old code must reproduce the screenshot before the new code is judged; a CPython harness is not Jython - compare floats with a tolerance.)* *(staged: Raw Log 2026-10-19_B section 10 items 4-5 - a probe's verdict must not rest on samples coarser than what it judges; pair records across systems by the time of the event they share and a measure, not by an identity under test nor first come first served (a record left over shifts every pair after it).)* *(staged: Raw Log 2026-10-19_B section 13.2 item 6 - before timing anything on a data source, read how it is produced - a timer's period is not the source's latency.)* *(staged: Raw Log 2026-10-19_B section 14.2 item 8 - a simulation's timing that a conclusion rests on is measured on site before the conclusion is passed on; until then it is the simulation's.)* *(staged: Raw Log 2026-10-17_A section 10 items 8-10 - a rebuilt tool reproduces the records in use before it writes (REPRO); close a chat out the day its design doc goes into the project; before a backfill, check what the change touches.)* *(staged: Raw Log 2026-10-15_C section 9 items 9-10 - tune a detector on the plant's own history first (export, reproduce the replay off the gateway, tune, replay); render a card change from real results and look at it before delivery.)* *(staged: Raw Log 2026-10-20_B section 7.2 item 11 - a "how far back" rule over a sequence number made inside a program breaks when it starts again or the numbering jumps - count the events that passed instead.)* *(staged: Raw Log 2026-10-14_E section 13 item 10 - a capture reader caught mid catch-up reads like a stall: check where its first stored record sits against the ring, and the batch size, before calling it stuck.)* *(staged: Raw Log 2026-10-22_A section 9 item 10 - an HTML mock of a view copies the gateway's defaults - containers clip, alignItems stretch, labels scroll.)* |
| `KPP_Platform_Rules` | 1.19 | Writing/debugging any capture script, NQ, event/timer script, Script Console code, **or Perspective view (bindings/events/components)** - Jython, gateway scripting (scope-G, TIMER vs SCHEDULED), OPC reads, PostgreSQL (matview single-owner audit, nullif), Perspective quirks, reporting date handling. Also any helper process or probe on TL-KPPWS01 (group policy, scheduled tasks, PowerShell quirks). **Also any Project Library restructure or a resource that has vanished** - packages must be plain folders, `actor: external`, export forensics. **Also any Logix ladder logic or L5X edit** (decide once into a bit, DINT scales, action-body extraction, Use Existing on import) **and moving components in a view** (CSS transition, mount settle flag). **Also any HMI view that writes to the PLC or shows a list in every session** (two-press arm, one-bit writes to DINT words, engine-published lists, install into an EMPTY view, `runScript` cadence). **Also a PLC pulse the HMI misses** (tag group poll against pulse length, an on-screen hold). *(staged: Raw Log 2026-09-30_A section 9 - including a correction candidate: the "no `polling` key" body rule against the 2026-09-22_B string-rate rule.)* *(staged: Raw Log 2026-10-03_A section 9 - the DB error cause chain, stale tag CSVs, the transaction dry run, L5X ST line newlines, a shared module counter.)* *(staged: Raw Log 2026-10-07_A section 9 items 1-14 - two PLC constants that cancel change as a pair, a load-bearing JSR, a forensic recorder armed against the item's own target, classify an event from the scan before, the PE first-edge lead, a ladder routine L5X from a program export, secrets out of a routine's context, an ambiguous CTE column, one master retention purge, a PLC ring's natural key, the Script Console's module copy, print the DB `ERROR:` line, two Perspective items.)* *(staged: Raw Log 2026-10-09_A section 9 items 13-14 - a view with no onStartup opens on the values last saved in the Designer; a set written as many rows goes in one transaction, read back, undo printed.)* *(staged: Raw Log 2026-10-10_A section 9 items 1-6 - one structure item fails an OPC read batch (`Bad_Failure`), the console browse cost, find a PLC struct from an existing tag's `OpcItemPath`, `lineHeight: 1` scroll arrows, an overlay on a shared map follows its `Labels` param, the small status tile pattern.)* *(staged: Raw Log 2026-10-08_A section 9 items 1-9 - a busy PLC ring read in one OPC batch (slot from the sequence number), a provider's readers check its switch and its active bit, two settings that act at different moments under one switch, a program export's stale tag values, External Access for an HMI write, a new tag's first seconds, a library's version string in its rows, analysis in PostgreSQL functions behind a one-call JSON NQ, a role-gated control.)* *(staged: Raw Log 2026-10-12_A section 9 items 1-2 - decode a full-controller L5K's live tag values against the datatypes, never by eye; a routine L5X built from a full-controller L5K (`N:` text as is, the `RC:` strings, `$` escapes) - whether a minimal-context routine L5X imports clean online is pending.)* *(staged: Raw Log 2026-10-14_A section 9 items 1-2 - changing what an NQ's parameters mean is an API change, re-check every caller (NQ v3.0.0 and the MLY email library); an inclusive-date NQ fed the next period's first moment includes that whole day, as much as exists at run time.)* **Also (1.18 / 1.19): a PLC request bit more than one routine clears, a free-running scan counter, the controller clock and daylight saving, live tag values in a program export, building a routine L5X from one, `runScript` load on hidden tabs, a spinning element in a coordinate container, sizing a fixed panel.** *(staged: Raw Log 2026-10-14_B section 9 items 1-4 - SVG data-URI charts from a gateway library via one `runScript` nonce prop; `material/approval` and `material/inventory_2` missing from the icon set; the kiosk return on `session.props.lastActivity` / `page.props.primaryView` (pending proof 15 Oct); a string into an NQ DateTime param - prefer `CAST(? AS date)` (candidate).)* *(staged: Raw Log 2026-10-14_C section 9 items 9-10 - switching a DB query tag to OPC with `system.tag.configure(..., 'm')` (the query settings stay, so the undo is the value source back to `db`; copy the item path from a working tag; check value and quality after a few seconds); a console applier that replaces a view (live definition compared, owner role and schema CREATE checked, dependents listed, same columns, undo printed).)* *(staged: Raw Log 2026-10-14_D section 9 items 1-3 - a WebDev page that shows live tags needs a Perspective view holding them (an expr-struct lease keeper - `readBlocking` holds no lease); a single-file web app served the `planner_api` way, vendored kit files under `/lib`, an absolute redirect for the bare path; the iframe Designer guard with a `designerPreview` param.)* *(staged: Raw Log 2026-10-14_D section 11 items 10-11 - Ignition folders built for the views hold only the members the views use: check a new consumer's paths on the gateway, create a missing member read-only from a working sibling's item path; live motion from a PLC slower than the screen - smooth each value between its own changes on its tag timestamp, never whole snapshots (a faster read returns the same value).)* *(staged: Raw Log 2026-10-15_B section 10 items 1-4 - an input in a flex row keeps its own width (`minWidth` 0); a layout that follows the screen (`page.props.dimensions.primaryView.width`, enabled at startup, into the runScript feed; columns from computed card heights; an indexed property binding; a bound `position.basis` inside a scroll container); wrapped rows of cards leave holes - balance them over columns; a custom prop marked non-persistent with no binding does not exist at runtime until written (scripts raise AttributeError) - keep it persistent and reset it in `onStartup`, seeded once; `system.util.getGlobals()` belongs to the JVM it runs in - the Script Console's is the Designer's, gateway state is checked through a `runScript` binding; a dictionary there made with `setdefault` and versioned - item 8; ages and waits in gateway code on `java.lang.System.nanoTime`, not `time.time()` - item 9.)* *(staged: Raw Log 2026-10-15_B section 12.7 items 10-17 - labels ignore `props.style.display` bindings on the gateway, reconfirmed (`position.display`); the Designer saves a persistent property's live value as its default; session roles into `runScript` are QualifiedValues - unwrap `.value`; FTView numeric displays imply decimals - read the PLC member's raw value before setting limits; a new tag's first minutes on `LeasedTags` (CHECK 1 of 108 Good, all OK at the next probe); a glow on a repeated row from the stylesheet's own classes on an inner element (candidate); watching tags for changes made outside an audit path (a wait for the audit row, never its own rows, ages by the database, a baseline table, a mute, a heartbeat row, a dedicated thread); 8.3 timer scripts sit inside `def handleTimerEvent():`.)* *(staged: Raw Log 2026-10-15_A section 13.5 items 16-19 - the Logix driver's Details page is the comms measure (requests, actual interval and overload per rate; asked = requests / rate against what the PLC answers - COS_PLC_1756CPU 165-185 a second; arrays and whole structures cheap, scattered members dear); the levers in the order they worked (the group rates; not CIP Connection Size; Max Concurrent Requests not separated); a Leased group with a set OPC UA Sampling Interval samples at it, leased or not; a named query's Database dropdown keeps the last one used - again with the Sort Register.)* *(staged: Raw Log 2026-10-16_A section 9 items 1-3 - the Logix driver serves no whole Logix array as one OPC value (`Bad_AttributeIdInvalid`), read the elements; an ST routine L5X imports online with the program as context and its new tags, callees first; a higher-priority task can interrupt between two reads - read a packet counter before and after its fields.)* *(staged: Raw Log 2026-10-19_B section 10 items 1-3 - Logix names ignore case: two tags, members, routines or types that differ only in case are one name and the import is refused (Error 12740-0) - check it in every generator; a periodic task can run slower than its period - count time from the clock, or check the scan count against the clock when times look off; `LastScanTime` is elapsed time with the higher-priority tasks inside it - see a routine's own cost with it switched off.)* *(staged: Raw Log 2026-10-19_B section 13.2 item 7 - `readValues` in a loop over a PLC ring costs a round trip each, about 250 ms on `COS_PLC_1756CPU` - read the pointers and only the new slots, or the set in one call.)* *(staged: Raw Log 2026-10-19_B section 15.1 item 9 - a gateway timer's state held in its Project Library module goes with every project save: keep it in `system.util.getGlobals()` (plain data, versioned) and run one tick at a time across the old and the new copy with a Java lock kept there.)* *(staged: Raw Log 2026-10-17_A section 10 items 1-4 - `queryTagHistory` returns 0.0 before a tag's first sample; a rate from counts per pass needs the real pass time (GSV WallClockTime inside UID / UIE); `system.util.getStackTraceAsString` does not exist; decoding an AL1920 IO-Link master and an AOI tag from a full-controller L5K.)* *(staged: Raw Log 2026-10-15_C section 9 items 1-5 - `system.file.saveFile` is not in the 8.3 Designer's console (java.io to Downloads); a component taking another's place in a container keeps its style on the open sessions (set its box properties, refresh the page); results for bindings through `system.util.getGlobals()`, STALE past a limit; an SVG data URI built once per result; the fillWo script-transform pattern for a card.)* *(staged: Raw Log 2026-10-14_E section 13 items 1-5 - a loading bar raised and lowered by two change scripts can stay on; when the query echoes its parameters, bar = answered window != asked window, capped; `try()` does not catch Bad_NotFound - set every key in the transform; `numberFormat "0"` for stem numbers, HA and cm; hover tips (`meta.tooltip`) on a card's title row with a `material/info` icon; a Project Library script is not seen until the project is saved.)* *(staged: Raw Log 2026-10-20_A "Knowledge Index - add", Ignition Perspective - a swapped view.json leaves the old rows' state on the rows that take their places (close the view in the Designer first, open a fresh browser tab after); meta.visible false keeps the flex slot and its gaps; an embedded tab's query can run before the page passes its params - ignore answers with no window, ask again with a Nonce. NB its "bump root.meta.name" meets the compiled rule that root's name stays `root` - settle at the compile.)* *(staged: Raw Log 2026-10-22_A section 9 items 1-7 - labels ignore a `props.style.display` binding (the third case; buttons and containers honour it - `position.display` for labels); flex containers clip a child's box-shadow (`overflow: visible` and padding up the chain); an inline `style.animation` naming stylesheet keyframes works on a component; `alignItems` unset behaves as stretch; a binding on an unwritten `session.custom` key paints Bad_NotFound; a kiosk idle return read in one polled script transform; a fixed-height label needs a line height equal to its box.)* |
| `KPP_Domain_Data_Reference` | 1.9 | Touching `kpp_production`, gauges, or any stem/log/KPI data - three-feed picture, matview chain + refresh ownership, waste semantics, USNR reporting layer, 07:00 date rule, decodes. Also COS log stop positioning and the COS login (section 10, corrected in 1.9 - the measured PE offsets, the stop cut sequence, contact speed at the stops, stopless cuts and butts, the PE arrays and the first-edge lead, `_100` v1.1.0 and `_101`), the SDB debarker profile and the two SDB KPI formulas (section 11). *(still staged: Raw Log 2026-09-30_A section 9 - `chip_daily` drum grade unused, `logdetail.destinationname` NULL, VVB301 over-range code.; Raw Log 2026-10-03_A section 9 - the cm machine CHECK, stem mean diameter, HOG / SDB / encoder-routine PLC facts, the new `pewatch` and `anomalywatch` tables.; Raw Log 2026-10-09_A section 9 item 15 - the Debarker outfeed reads stems at about half length while the feed still pushes them, the same-stem pair Grading outfeed / Debarker feedworks, PE2L on a stopped feed.; Raw Log 2026-10-10_A section 9 item 7 - the sweep auto bits (COS outfeed `SweepInAuto`, `SDB_Outfeed.Sweep.Auto`, `Grading.Sweep.SweepInAuto`), the desk auto buttons and lamps, the Pulp deck sweep is the desk's disc sweep, the Drum chipper sweep is not used, the T&B auto button press counter.; Raw Log 2026-10-08_A section 9 items 15-18 - the COS stopless approach mechanics (zone commands and ratios, gearing, pre-close, run-slow, one speed unit about 16 mm/s, a hand clamp on a moving stem runs on 188-241 mm), `cos_moves` / `pa_cos_*` / `cos_watch` flag 30 / the operator marks, the 8-9 Oct stem cycle baseline, the sequence deck reverse window and its tags.; Raw Log 2026-10-13_A section 9 items 4-5 - `public.booth_operator_history` (a logout writes an operator-NULL row running to the next login; zero-length NULL rows at shift change; a login is a row with an operator), smoko 10:30-11:00 and 15:00-15:30 day and night, the COS booth also runs the downtime application.; Raw Log 2026-10-14_A section 9 item 7 - MLY first scans 06:57-07:03 on a normal morning.)* *(staged: Raw Log 2026-10-14_B section 9 items 5-6 - the shut schedule is mostly single-shift (13 shut days in 26 weeks, 1 full) and any shift shut is a shut day; ProdStats ReportData counters (`TotalStems`, `TotalScannedStemLength`) are per shift.)* *(staged: Raw Log 2026-10-14_C section 9 items 4-6 and section 11 item 12 - the Hub gauge bindings table (Stems = `report.stems_by_shift` 1.2.0, primary pieces; Total Length / Volume = the PLC `TotalScannedStem*` for the current shift, `cos_kpi_daily` for the previous); a broken stem's 2nd piece adds its length and volume but is not counted as a stem; the report shift functions (`at_time` default `now()`, the date functions on `current_date`); the 13 Oct night capture shortfall (stem rows 3.4 % length after trim / 3.6 % volume under the PLC scanned; pieces 1,172 captured / 1,196 grading / 1,235 USNR).)* *(staged: Raw Log 2026-10-14_D section 9 items 7-8 - the plant in one frame (X = 0 at the COS A saw) with the conveyor lengths and their sources; the COS cycle as modelled (`_205` B / C offsets, stop cuts 2.13-13.13 m) and the live record units and spellings (VaxData / LastCut cm, outfeed `Position` - 5000, `RemaningLength`, `Lenght`).)* *(staged: Raw Log 2026-10-15_B section 10 item 7 - the Echo settings on the one controller: the PLC members behind each Echo settings field (the catalog in `engineering.settings`), the `RefererncePos` spelling, `DisableSickPEArrays` inverted, the COS encoder scales and the RMC, Echo's manual kick bits (ScanHMIBay is a bin; odd bins forward; kicker = (bin + 1) / 2).)* *(staged: Raw Log 2026-10-15_B section 12.7 item 19 - the grading encoder scales held x 1000 in the PLC; the saw pre-lower toggles; Echo's cut speed table and the saw prox windows in the PLC (left off the page); `setpoint_history` rows `outside Ignition` from the settings watch; `public.setpoint_watch`.)* *(staged: Raw Log 2026-10-15_A section 13.5 items 20-21 - conveyor 1 is 0.3034 mm an encoder count: `Conv1Scale` 0.2850 stays (Tui's kick positions are set against it; its PE positions `DistTo0` are true mm), `ScanEncoderScale` true at 0.3034 and it still moves a long log's kick by half the length change; conveyor 2 not measured; the COS PLC connection (192.168.12.1, the L84ES embedded port; 192.168.12.2 is COS_R1's ENBT) and its tag groups as left on 16 Oct.)* *(staged: Raw Log 2026-10-16_A section 9 items 8-11 - the T&B data path (Tui's packet count, the COS slot on every message, the last message sent again), Tui's TrackingErrors is `NumOfLogsCorrected`, the sortline signals and conveyor scales; the plant does not run without the Ignition gateway - PLC and gateway work split by time; and section 13.1 items 12-14 - Tui's scan check and data copy, the one-axis scanner and when its result lands, the COS ring; `sorter_logs` keeps the X diameters only; and section 14.1 items 16-19 - the COS overrides (console buttons, Regrade 8281, bin 10), re-optimisation's type-14 packet and its dead trigger word, the grades sent once in the type-11 defect packet, the sortline scanner's offset is its near edge.)* *(staged: Raw Log 2026-10-19_A section 6 item 2 - the Stem vs Forecast line is calendar pro-rata in both reports (with the 2026-08-01_B E9 rule, still staged); the per-shift formula - forecast / scheduled shifts x 2 for every calendar day - overshoots the month by 62 / scheduled shifts; forecast / scheduled shifts stays right for a shift or running-day target.)* *(staged: Raw Log 2026-10-17_A section 10 items 5-7 - the IO-Link masters and sensors (ifm PV8000 on all 18 pumps, HYDAC tanks, Debarker tank 2 empty); the hydraulic pump map, house folders against the PLC arrays, Big John in `Pumps[0].PV8000`, run state from the motor; the pump sensors' start and two pressure steps.)* *(staged: Raw Log 2026-10-15_C section 9 item 8 - the hydraulic tanks: the level sensors and their historian folders, the 15 Oct setpoints, litres per 100 %, the temperature effect, booked fill litres against the level rise.)* *(staged: Raw Log 2026-10-20_B section 7.2 item 10 - the sortline scanner against the COS plan (19 - 20 Oct, 8,735 logs): SED +3.7 % / 2.9 % of the plan SED; LED under the plan by the plan's taper (-7 mm under 50 to -104 mm at 200 +, the spread 9 - 57 mm); volume +0.3 % / 3.2 %; length +0.65 % / 18 mm; the COS ring's Y diameters equal X.)* *(staged: Raw Log 2026-10-14_E section 13 items 6-9 - COS overrides only from COS Watch (USNR `overridecount` 0 on every stem, solution type 0 not a flag); the USNR stem links to `kppstems.stems` on 16 %, the grader's call set on 98 %; the grade call recorder `_311_GradeCallWatch` and `kppstems.gra_call`, the PLC clock 11.8 s ahead of the gateway; Value Recovery's who and origin rules.)* *(staged: Raw Log 2026-10-20_A "Knowledge Index - add", Database - `usnr.logdetail.marketvalue` is $ a log (matches `prod_summary` $/m3 to 0.5 %), not `productionvalue`; the price file values chip at about $1/m3; `kppstems.sorter_logs.vax_value_m3` / 10 = $ a m3.)* *(staged: Raw Log 2026-10-22_A section 9 item 8 - `KPP_Visitor` `dbo.visit.inducted` BIT NULL, 1 inducted / 0 not / NULL before 22 Oct.)* |
| `KPP_Reporting_Technical_Reference` | 1.5.0 | The definitive DB/schema/NQ/UI provenance map - every table/view/matview/NQ/tag/surface (incl. USNR Product / Chip & PcSz / completion recompute; daily-report refresh cadence + ownership; refresh button + date mechanics). *(staged: Raw Log 2026-10-14_A section 9 items 3-4 - `shared.mlyproduction` 0.3.1, the email caller of the MLY by-day NQs, passes inclusive dates (daily, monthly, history, trend, MTD); the monthly email's Last Month / 6-mo avg columns come from calendar-month buckets, never from the previous email.)* *(staged: Raw Log 2026-10-14_B section 9 item 8 - the Hub Workmate Pulse (`workmate.hubpulse`, panels, sources, bindings) and the banner sources.)* *(staged: Raw Log 2026-10-14_C section 9 items 1-3 - the Hub tag family `KPP/General/Data/Production/*` rewired (CurrentShift Length / Volume OPC on the PLC `ReportData.TotalScannedStem*`, PreviousShift Length / Volume from `cos_kpi_daily`, Stems on `report.stems_by_shift` 1.2.0, primary pieces) and `TransformationsStemLengthsLastShift` (the USNR stem length); surfaces S2 / S3 on the PLC meter, the Safety overview shift card and the Hub Avg gauges still on the stem rows, the projection rate NQs 2.0.0; CORRECTION to section 7 - "Hub slightly < booth (in-flight stem, regrade decrements)" is wrong: the stem rows ran 3.9 % under on 13 Oct night, trim about 0.5 % and about 3.4 % scanned with no stem row.)* *(staged: Raw Log 2026-10-14_D section 9 item 9 - the digital twin surface: WebDev `twin`, `twin.live` / `twin.web`, view `Application/Twin/TwinCOS`, page `/twin`, `C:\WorkmateData\Twin`.)* *(staged: Raw Log 2026-10-14_D section 11 item 14 - the twin on Live since 14 Oct: page `/twin` and the 34 tags created for it under `StemQueue/Conveyors_n_`, `CurrentStem/VaxData/VaxData_n_/Bin` and `LogStopConv/LogData/LogData_4_-7_`.)* *(staged: Raw Log 2026-10-15_B section 12.7 item 20 - the Machine Settings surfaces: page `/Engineering/Settings`, timers `ManualKick_Watchdog` / `Settings_Watch`, tables `sortline.manual_kick_event` / `public.setpoint_watch`, the watch's rows in the Setpoint Changes report.)* *(staged: Raw Log 2026-10-15_A section 13.5 item 22 - the Sort Register live on `KPP_production` and the Sortline Overview's Sort Register button (1.2.0); the tag group `Diagnostics_5s` and its folders; the rates the screens see (FastLeasedTags 500, Discretes 1,000, LeasedTags 2,000 while leased, Default 2,000).)* *(staged: Raw Log 2026-10-19_A section 6 item 1 - both emails build Stem vs Forecast the same way (`shared.weeklyreport` 0.8.2): `kppstems.kpi_daily` per `productiondate`, month start to the reported day (the Sunday for the weekly), the forecast pro-rata over calendar days, the reported day's month for the weekly's Month-to-Date bar and chart, the Monday's month for its weekly targets; `Production/DailyVolume_30d` is relative to `CURRENT_DATE` - never for a period picked by date.)* |
| `KPP_Migration_Reference` | 1.5 | Any migration/capture/cutover work. *(staged: `KPP_Migration_Reference_ADD_2026-07-09` - merge at next touch.)* |
| `KPP_Stem_Ack_Responder` | 1.0 | Working on the stem-ack / handshake. |
| `KPP_055NEW_DESIGN` | 1.0 | The cutover PLC ack routine - what changed from `_055`. |
| `KPP_Echo_Retirement_SRD` | 1.0 | Scoping retirement work - Q1-Q7. |
| `KPP_PLC_Capture_Requirements` | 1.1 | AS-IS Tui capture surface, PLC UDT formats. |
| `KPP_Control_Text_Standard` | 1.2.0 | Styling ANY toolbar/filter control or selector - typography tokens + the `kpp-selector-value` stylesheet class (paste-once CSS block). Also any new HMI panel or card - the panel style (section 5) and plain words on values (section 6). |
| `KPP_Reporting_Suite_Memory` | 1.0.0 | KPP report-stack work - daily/weekly/simulator internals, NQ standard, KT brand tokens. |
| `KPP_VisitorSignIn_Audit` | 1.2.0 | Any Visitor Sign In work - live/dead register for every view, NQ, script, report, style class and config key, the 19+ defect list with severity and slice, and the delete list. Audit of the 2026-09-17 export; changes after it are in Raw Log 2026-09-18_A. *(changes after the audit also in Raw Log 2026-10-14_B - Menu 2.9.0 shut source `schedule.kpp`, Hubheader 1.5.0 shut-day kiosk return.)* *(changes after the audit also in Raw Log 2026-10-22_A - the kiosk return every day for the Reception login (Hubheader 1.6.1), the mandatory induction question and `dbo.visit.inducted` (User Verification 1.1.3, NQ `Visit/Set Inducted`), Visitor Card 1.3.0, Menu 2.10.0 - PLANT SHUT on `position.display`, the 14 Oct F1 cause.)* |
| `KPP_Camera_LiveView_Reference` | 1.0.0 | Anything camera live view - adding, renaming or removing a camera, a tile not playing, the relay pill not green, changing camera stream settings, go2rtc. Relay runbook, naming, codec rule, estate snapshot, camera traps, troubleshooting. Holds no credentials (relay yaml only). |
| `KPP_SDB_StemTracking_Reference` | 1.0.0 | Anything SDB debarker stem tracking - stems on the SDB Map, twins, the 10 m / 8 m fences, the stem length sent to grading, the curtain length switch - and before editing any Tracking1 routine. Layout constants, life of a stem, routine map, settings, counters, member map, what each length means, probes. *(staged: Raw Log 2026-10-12_A section 9 items 5-7 - also read for the Debarker outfeed auto sweep trigger: the four sweep array eyes (Sweep PEs PE2 / PE3, Wall Control PEs PE1 / PE4 for the Sonics tool), `_220_OutfeedSweep_v1_1_0` and `UseSweepArray`, the kick point (`SweepPos` less the `_221` correction), the `SDB_OFSpeedReduction_*` set and the Sonics feed ramp, the AFI'd `SlowForSweep` unlatch.)* |
| `KPP_KickerHeat_Design` | 1.6.0 | Anything Sortline kicker - overload trips and their verdicts, the heat / anomaly index, the KickerAnomaly card, map overlays and prox lights, the kicker popup, the kicker trend, enabling or disabling a kicker (Workmate right "Sortline kicker enable"), quick WOs from the popup. Engine `forensics.kickerHeat`, tags `KPP/SortLine/Data/KickerHeat`, tables `sortline.kicker_trip_event` / `kicker_enable_event`, calibration, open items. Also signal drops, the mechanical verdict and the kick-fail history (`sortline.kicker_fail_event`), prox lights. Also kick fails on the card, the Sorter Diagnostic RESET COUNTERS (one-owner reset pulse), `_107_KickerForensics` (the routine once called `_106`; its scan tick) and PLC-stamped times under daylight saving - section 9b. *(staged: Raw Log 2026-10-15_A section 13.5 item 26 - the sortline Diagnostic, `KickerFailLog` and `KickerLastFail` folders on `Diagnostics_5s` (5 s Direct); the kicker prox members on FastLeasedTags, now 500 ms (the 1 s on-screen hold assumed a faster poll - watch the prox lights); the Overload members on LeasedTags - a gateway read holds no lease, so with no screen open the engine can read values up to 10 min old (latent).)* |
| `KPP_CM_Design` | 1.1.0 | Anything chipper knives or motor vibration - the knife cards and their clock (hours in cut) and verdict (motor current), the per-machine torque / current lines and how they were set, `cm.cm_rollup`, `cm.knife_change` / `load_rollup` / `vib_rollup` / `vib_baseline`, `CM/KnifeDelta` and `CM/VibState`, the vibration cards, baselines and the Disc 1 twin reference, the Grader Outfeed load band, the VVB010 / VVB301 sensors and the over-range code, `knife_auto` and knife-record corrections, the automatic knife WO outline.. Also the motor work log (`cm.maint`, the bearings and greasing buttons), `CM/VibState` 1.2.0, the baseline tool `CM_vib_baseline_set` 1.1.0 (REPRO, then the re-take), the GRAOF re-take and its StateWord. Session record: Raw Log 2026-10-09_A, 2026-10-17_A section 8. |
| `KPP_PEWatch_Design` | 1.1.0 | Anything photo eye - the PE Watch registry (eyes, links, elements, USE flags and the rulings behind them), the PLC recorders and their install, engine `forensics.peWatch` and schema `pewatch`, the baseline (preview, set, rules), the cleaning check and Cleaned marks (`forensics.peWatchJudge`), the PE Watch popup, link scoring still to build, the old PE diagnostics it replaces. *(staged: Raw Log 2026-10-09_A section 9 items 1-4 - link scoring as built (judge 1.3.0: SILENT with a witness, RATIO with blame, ELEMENT, WALL), the sun (registry SUN / SITE), the S4 replay, the S5 check and the set tool 1.1.0 (KEEP, WIDER), the COS pre-array chatter against a steady COS_Conv / PEArray3.)* *(staged: Raw Log 2026-10-13_A section 9 items 1-2 - smoko windows not judged unless the COS booth is logged in, no SILENT in the first window after (judge 1.4.2, `smoko_now()` / `break_now()` / `break_windows()`); WallControlPEs returning while the Sonics is out, WALL only while it is manual (registry 1.6.0).)* |
| `KPP_AnomalyWatch_Design` | 1.0.0 | Anything Anomaly Watch - the area index and its rows (photo eyes, encoders, motors, drives, hydraulics, kicker heat, chippers), scoring bands, the encoder mutes and the stall cross-check, events and `anomalywatch.event`, the shift strip and `anomalywatch.shift`, Ask Azztec AI (`forensics.anomalyAsk`), the area card, Live events card, history and Ask popups. *(staged: Raw Log 2026-10-09_A section 9 item 5 - link scoring on the photo-eye rows (WATCH 60 / HOT 80 / earlier 30), the sun mark, new bearings on the Motors rows, Ask #missed and #sun.)* *(staged: Raw Log 2026-10-13_A section 9 item 3 - smoko on the rows: encoders not judged ("smoko to HH:mm"), the smoko history lines under COS, kicker heat and chipper sensors not paused (Anomaly Watch 1.13.0).)* *(staged: Raw Log 2026-10-17_A section 10 item 11 - the Hydraulics row: tanks (`forensics.hydLeak`, 1.14.0) and pumps (`forensics.hydPump`, 1.15.0).)* *(staged: Raw Log 2026-10-15_C section 9 items 6-7 - the shut (1.14.0: SHUT on every card, the first verdict seeded from the history) and the Hydraulics row from `forensics.hydLeak` with its short headline `h`.)* |
| `KPP_COSWatch_Design` | 1.2.0 | Anything COS Watch - the PLC cut recorder `_260_COSWatch` and its record (columns, flag bits, target arming), `forensics.cosWatch` and its timer, `kppstems.cos_watch` / `cos_watch_mark`, the panel (`/coswatch`, ENGINEERING MENU) and what its columns mean (Err after the PE offset fix), the crew marks, `export()`, the master retention purge `shared.purge` and `public.purge_log`. *(staged: Raw Log 2026-10-08_A section 9 item 19 - `_260` 1.2.0 flag 30 hand clamp, the operator buttons `forensics.cosWatchOp` and `/coswatch-op` with the T&B link, the marks in P2, the Log Stop Positioning counts from `cos_watch`.)* |
| `KPP_COS_StopApproach_Spec` | 0.3.0 | DRAFT, parked 7 Oct. Changing how a COS stem approaches the log stops - contact speed at the stops, short butts overshooting in AUTO, the final-approach floor (C2), the approach cap (C3), what to do before restarting the work. *(staged: Raw Log 2026-10-08_A section 9 item 20 - the stopless approach as built behind `BA_Enable` (`_102` 1.0.0, `_100` 1.2.0, `_110` 1.1.0, `_055` 1.1.0), the review, the simulation, P5 1.1.0 / P6 1.0.1, the 8 Oct trial; BA is a braking curve for AUTO stopless cuts only, C3 stays parked.)* |
| `KPP_TnB_Bin0_Design` | 1.0.0 | Anything T&B sweep or Bin 0 - the sweep setpoints and the cancel line (`_115` v1.1.0, `TnB_CancelLinePos`), the Engineer-only setpoint lock, Bin 0 forensics (PLC `_081`, `forensics.bin0Capture`, `kppstems.bin0_forensics` / `bin0_reason`, the reason codes and who owns them), the TNB Map Bin 0 panel, toggle and popup, the deferred `_080` rung 3 fix. Registered late (v1.36.0); session record: the T&B `2026-10-03_A` raw log. *(staged: Raw Log 2026-10-10_A section 9 item 8 - the T&B SWEEP tile on the TNB Map, from `KPP/COS/OF/Data/TnBSweep/SweepInAuto`; Bin 0 reasons 12 and 30 are what it is there to stop.)* |
| `KPP_DigitalTwin_COS_Design` | 1.2.0 | Anything KPP Digital Twin - the 3D line view (LIVE / REPLAY / SIM) and its install (on Live since 14 Oct), WebDev `twin`, `twin.live` (the 352-tag map, one cached read, the position change times `ts`) and `twin.web`, view `Application/Twin/TwinCOS` and its lease keeper, the 34 tags created for it, the drawing rules for each PLC record, the live motion (each value smoothed between its own PLC changes on its tag timestamp, the adaptive delay), the plant in one frame (conveyor lengths, PE and bin positions and their sources), the simulator (the COS cycle, 57 dials) and its calibration against the 8-9 Oct audit with the residuals, Compare and What if, saved forecasts (`public.twin_forecast` on KPP_production, `twin.web` 1.1.0 routes, WebDev doPost, page 1.2.0), the commissioning checks C1-C11, phase 2. Not Dave's optimiser simulator (`shared.simulatorreport`). Session record: Raw Log 2026-10-14_D (section 11 the Live install and the motion fix); saved forecasts Raw Log 2026-10-16_A section 3. |
| `KPP_LineTracker_Design` | 1.2.1 | Anything KPP Line Tracker - program Trk and task Tracker in COS_CPU, the new tracking in Structured Text beside the Tui code: the whole-line data model (pieces, segments, stations, events, areas, kicks), positions from segment counts in true mm (`Srt_Scale1` 0.3034, `Srt_Scale2` 0.2857), PE debounce in conveyor travel, matching, ghosts, misses, the section 2 transfer, kicks and the Tui comparison, the event ring and the export block, the fault routine, the sortline pilot (its stations, settings and rules), the scan budget, the installs (1.0.0 the download in the shut; 1.1.0 - 1.2.0 online routine imports and JSR repoints), the commissioning checks K1-K8 (K2 as `KPP_Trk_Install_v1_0_1`: elapsed time - judge the rise), the off-PLC proofs and the next slices. Also the site record: the LIVE run and 1.1.0 (the landing re-anchored at the PE clear), the kicker return stroke (1.1.1), the landing PE losing a log (1.1.2), the WATCH and DATA runs, and 1.2.0 - every T&B message counted and classed (DATA), a history of 16, the identity checked by length at section 1 start (`_230_SrtIdentity`: two logs as one, a missed log's ghost, data given up, the COS memory slots behind `Srt_CosMem`), IDENTITY / TUI_ID events, the kick on the measured length, station 5 off across switch-ons, the cases it cannot tell (sections 14-18). Not the Tui sortline code (`LSL_Sorter`). In the controller since 15 Oct; 1.1.2 running since 17 Oct; 1.2.0 on site since 19 Oct (the 230 as 1.2.1 - Logix names ignore case), `Srt_CosMem` 1; next design the gateway identity advisor (18.7; `KPP_TrkAdvisor_Design`). Probe `KPP_Trk_Watch_Probe` 1.6.1 (RING / LIVE / WATCH / DATA). Session record: Raw Log 2026-10-15_A (section 12 the download), 2026-10-16_A (sections 4, 6, 7), 2026-10-19_B (sections 2, 4, 6, 8). *(staged for its next version: Raw Log 2026-10-19_B sections 2, 4, 6 and 8 - the 1.2.0 site record: the RING and WATCH runs, `Srt_CosMem` 1, the Tracker task at 50 scans a second from 17 Oct about 17:50 (`Trk_Tick` at half speed - the speed display and the kicker return window), the ?? ghosts, probe 1.6.1.)* *(cross-reference: Raw Log 2026-10-17_A section 10 item 12 - the Tracker task period read 20 ms on 18 Oct 06:23.)* |
| `KPP_TrkAdvisor_Design` | 1.1.4 | Anything about the gateway identity advisor for the Line Tracker - which log is which decided on the gateway for the cases tracker 1.2.0 cannot tell: the split (the PLC tracks and kicks, the gateway decides identity), what the controller and the gateway hold per log (the COS ring `LSL_COS_MemoryData`, Tui's scan records `LSL_Sorter.LogData`, `sorter_logs`), how Tui checks a scan (`_065` / `_066`), the score on length, SED, LED and volume, the mark-off against what was just cut, the window aligned to the COS cut order with T&B swaps and logs taken off the sortline, the timing to the kicks, the `Adv_*` mailbox and `_240_SrtAdvice`, phases 0-3; section 9 the sortline scanner replacement (Banner EZ-ARRAY 1200 mm, 4-20 mA); section 10 phase 0's result (GO - the model of scan minus plan); section 11 phase 1 as built, `trk.advisor` 1.0.0 (what it reads and why not the export block, the decision and the hold for the next scan, the tracker's piece by time at the scanner PE, `kppstems.trk_advice`, the timer and the load, the report, the proof off the gateway, the install); section 12 the way to Tui's kicks (the decision, not the outputs; step 1 the logs with no T&B message of their own). Phase 1 on site since 19 Oct 10:15 (`trk.advisor` 1.0.1 from about 10:50 - the pairing, 11.3), sorter_engine's 10 s cycle (11.5), the first hour, 7 hours and day on site (11.10 - 11.12 - 99.7 % as Tui on its own data; Tui giving one log's data to two logs; the advisor wrong on old open cuts; the lead to the kick 54 s median), project saves kept in 1.0.2 (11.5), the scan against the plan by log size (11.13 - SED a share of the log, LED by the plan's taper, the ring's Y = X), 1.0.3 (11.2 - old cuts by the logs settled since; 11.7 its proof). Session record: Raw Log 2026-10-16_A sections 13-14, 2026-10-19_B sections 3, 5, 7, 13, 14 and 15, 2026-10-20_B. |
| `KPP_COS_RegradeView_Design` | 1.0.0 | Anything about regrading at the COS - the COS operator's overrides today (console buttons, Regrade 8281, bin 10, the 12 m cut), re-optimisation (the type-14 packet and why it never reaches the optimiser), how the grades reach the optimiser (the graders' type-11 defect packet, Pruned = type 1), the planned view (Prune to X m, re-solve, confirm, every regrade recorded), what USNR must confirm, phases 0-3. Concept, nothing built; phase 0 probe `KPP_COS_Regrade_Probe` 1.0.0 (run 19 Oct). Session record: Raw Log 2026-10-16_A section 14. *(staged for its next version: Raw Log 2026-10-19_B section 15 - the user's regrade idea: a selected prune cut instead of a regrade, a chip piece to the next planned cut, the rest of the stem as planned, the advisor checking the grades - after the advisor is running; and section 3 - the probe: 69.5 COS regrades a day, 25.9 m3, the butt log 53 %, a ceiling of about NZD 2.0 M a year; Re-Optimize dropped (the user, 19 Oct 06:00); a script that knows from the cut plan which prune products a stem qualifies for shows the operator the possibilities and he picks the length - "We can talk about this later".)* |
| `KPP_MachineSettings_Design` | 1.1.0 | Anything Machine Settings - the Echo settings screens rebuilt (Machine Settings 1-4, Sort Line Settings, Manual Kick Control): page `/Engineering/Settings`, its areas and cards, the catalog in `engineering.settings` (every setting's tag, PLC candidates, limits, Echo name), the setting editor and the checked write (roles - read through their QualifiedValues -, typo guard, two presses, PLC read-back, `setpoint_history`), the balanced card columns, the glow on a setting changed in the last 48 h (`GLOW_H`, the stylesheet's `wm-field-glow` / `wm-brand-a-glow`), the settings watch (timer `Settings_Watch`, `public.setpoint_watch`, a change made outside Ignition logged as `outside Ignition`), manual kick (Sparky and Big Balls - one gateway lock, the command bits confirmed off, the jog dead man and the watchdog timer `ManualKick_Watchdog` with its heartbeat, the kick handshake, `sortline.manual_kick_event`), the probe and the installers, the Echo fields not built, commissioning checks C1-C11. Session record: Raw Log 2026-10-15_B (section 12 the install and after). *(staged: Raw Log 2026-10-22_A section 9 item 9 - MachineSettings 1.0.5 carries the Log Stop Positioning panel on COS infeed and saws, path-swapped, hidden while searching.)* |
| `KPP_HydPumpWatch_Design` | 1.1.0 | Anything PUMP WATCH or the hydraulic pumps - the 18 pumps and their PV8000 sensors, engine `forensics.hydPump` (the windows, the long reference from each pump's first running windows, the checks, "runs, no pressure", `set_reference`, `replay`, `detail()`), its tables, the Hydraulics card and the DETAILS popup, the pump map against the PLC arrays, Big John, `hydraulics.pump_events` (holds no event), the install and the tests, open items. Session record: Raw Log 2026-10-17_A sections 3-7. |
| `KPP_HydLeak_Design` | 1.0.0 | Anything LEAK WATCH or the hydraulic tanks' oil level - the five tank level sensors and their historian folders, engine `forensics.hydLeak` (the 15-minute windows in `hydraulics.tank_window`, the judged windows, the temperature coefficient, the loss rate over 48 h / 24 h with a new base at every fill, the lower edge scored against the low-level ALARM, the band hold in `hydraulics.tank_state`, `check` / `backfill` / `replay`), the Hydraulics row and its short headline, the oil runway on the hydraulics cards (`card()`), the Shut Plan handling (`peWatchJudge` 1.5.0, Anomaly Watch 1.14.0), the proof on 1 - 15 Oct, the settings, the install. Session record: Raw Log 2026-10-15_C. |

## 2. Compiled docs - referenced, not loaded in this project

| Doc | Read when… |
|---|---|
| `Workmate_Knowledge_Journal` | Workmate DB facts - schemas, connections, data quirks. **v3.9** (2026-09-26): menu rights and the missing-row = RWD trap (3.22), work orders raised from outside WOMaint (3.23). |
| `Workmate_NQ_Standard` | Authoring or naming Named Queries. |
| `Button_Standards` | Button classes and styling. |
| `Workmate_Working_Method` | Workmate-side process - delivery, versioning, approvals. |
| `Workmate_Memory_Export` | Re-seeding Claude memory - the 30 delivery rules. |

## 3. Raw sources - ground truth (never rewritten)

| Source | What it is |
|---|---|
| Gateway exports (`MainSCADA_Timberlands_*.zip`) | Full project truth; the View Index is mined from these. |
| `HYDPUMP_REDESIGN_JOURNAL.md` / `VOLUME_MATRIX_JOURNAL.md` | Hydraulic / Volume-Matrix build histories. |
| `Operator_KPI_Scorecard_v3.1.xlsx` | Scorecard weights/design source of truth. |
| KT Brand Guidelines V1.0 (Nov 2025) | Brand palette source. |
| `KPP_Cutover_Runbook_2026-06-25` | Executed cutover runbook - historical record of the flip. |
| `KPP_Session_Handover_2026-06-28` | Post-cutover data validation + `sorter_engine` v0.2.1 fix. |
| `KPP_Stems_Count_Discrepancy_Findings_v1_1` | "688 vs 675" - CLOSED; three meters explained. |
| `KPP_stems_vs_usnr_v1_1.py` / `KPP_sorter_fix_confirm_v1_0.py` | Read-only reconciliation diagnostics. |
| `KPP_waste_*_diag/find/verify_*.py` + `Fix_cos_kpi_daily_waste_v1_0_0.sql` | Waste-pipeline evidence chain + executed fix (2026-07-09). |
| `KPP_refresh_production_views_def_probe_v1_0_0.py` | Read-only console probe - dumped the `refresh_production_views()` proc body (proved it does NOT refresh `kpi_daily_mat`). 2026-07-15_B. |
| `DashboardandPLC_Raw_Log_<date>[_letter]` series | Per-session log - one file per session, append-only. Entries: `2026-07-05_C`, `2026-07-09_A` (waste), `2026-07-15_A` (USNR Product Excel export, Chip & PcSz, Completion recompute, PG div-by-zero cascade, `TR  1` grade fix, Knight-Rider bar), **`2026-07-15_B` (Echo Report refresh: dead scope-C button + soft refresh, matview 15-min "Grade Refresh" timer + three-owner audit, DaySelector 07:00 date fix)**, **`2026-07-18_A` (EmailReports build-out: reports-in-view via data-URI iframe, WeekSelector, `shared.reporttiles` Hub scorecards, Production v2.4.0 single-mount restructure, nav-active fixes)**, **`2026-07-19_A` (WeekSelector/Control-Text-Standard/DaySelector, KR bars + Email Me, three-layer stale-date root cause, Forecast save-aborter, OperatorKPI single-mount + Timeliness page, Scorecard/Printable race)**, **`2026-07-19_B` (Operator-KPI meeting changes: -GRA/+Waste/T&B-occurrences/chipper-exclusion; FULL fleet calibration v3.8.0; manager toggle + Explain-KPIs legend; result-cache v3.10.x + warm timer + Oct-2025 floor; Prune-Forensics `return {}` mount fix; Timeliness proportional booth stacks; dash rule)**., **`2026-07-31_A` (MLY stood up as its own reporting area: `mly` schema mirror of the TuiTech Downtime app, `db.sync.mly.downtime`, Reports/MLY page + 5 tabs, Scheduled Shuts, smoko exclusion, Trina's workbook import)**, **`2026-08-01_A` (Qube/MLD throughput answer + exec report; Multi Year Production/Pace/Loaders tabs; `mly.pace_daily` + `db.sync.mly.production` closing standing #1; `is_planned`; mlyproduction v0.2.3 downtime + month comparison)**., **`2026-08-01_B` (EmailReports 5 tabs + MonthSelector; BoardpackCard pct1; 60-shift identity; volume triangle closed - kpi_daily family, USNR reference; FY panels acquitted; Boardpack Close Monthly event; July frozen 123,207)**., **`2026-08-06_A` (TR fold removed - prod_report v2.0.0 + order Completion repaired; MLY Daily 31st fix; MonthSelector collision resolved; three compiled docs corrected)**., **`2026-08-06_B` (Yard split into its own reporting area; four new exploration reports - Yard SED / KPP SED / Butt Cuts / Booth Calls; attractor CSS family v2.44-v2.45; Knight-Rider RELAPSE written up as a two-part trap; root-name, cloned-chart-axis and stat-null rules; three shift conventions confirmed)**., **`2026-08-10_A` (Office weekly feed live - `WeeklyStats` + `WeeklyReportColour` in Transformations on KTSQL02, weeklyreport v0.8.1 persists on the Monday run; four wrong targets before grants settled it; KTSQLSYS = KTSQL02 alias; datasource clone drops the password; `IS_MEMBER` over `fn_my_permissions`; colour master keys on role)**., **`2026-08-12_A` (Condition Monitoring stood up - VVB010 + VVB301 via `CM/VibMotor` UDT, 29 historised tags, CMPanel in SafetyPlantOverview v1.13.0; zero PLC changes; paramDirection silent-discard trap; sparkline id/props/colour + tag-history array binding; static trend axis; sensor comparison corrected from datasheets - 301 cheaper, drum at 13.4 g of a 16 g ceiling)**., **`2026-08-12_B` (Chipper knife-bluntness load monitoring + TnB StarLoader panel: MCC_ATV publishes scaled torque/current - zero PLC changes; `CM/DriveLoad` UDT + 3 instances; `CM_Chippers` v1.4.0 LoadStrip; `StarLoaderPanel` v1.0.0 + SVG; `TNB/StarLoader` tag folder; three S0 probes, imports gated on historian verdict)**., **`2026-08-14_A` (Probe close-out: chipper drives already historised under the Motors tree - `CM/DriveLoad` deleted same-day; `CM_Chippers` v1.5.0 rebind; sqlth_1_data single-partition aggregate timeout -> LIMIT-seek pattern; Throwable dual-catch; Star Feeder vs Star Loader disambiguated; axis verified in degrees; `PumpRun` fix pending)**., **`2026-08-14_B` (Knife-bluntness system: `cm` schema + knife_change/load_rollup; `cm_rollup` gateway timer; NQ `CM/KnifeDelta`; `CMKnifeCard` component; `SafetyPlantOverview` v1.14.0 KnifeRow; `CM_Chippers` v1.6.0 chips + KNIVES CHANGED button; thresholds provisional pending first knife cycle; Raw Log at v1.1.0 - package `cm` install order)**., **`2026-08-16_A` (TimberPay ported from Excel/VBA to Ignition - `payroll` schema, 2026 history seeded, classification ladder, live on a real CleverTime file and the re-import loop closes; NQ undeclared-parameter trap; `bidirectional` inside `config`; no `startsWith()` in expressions; WebDev import-zip vector; Business Systems pillar + expo landing page with the glassmorphism recipe and the Canvas2D access-control scanner)**, **`2026-08-24_B` (StarLoader panel live on the TnB Map - StatusBits vs ErrorBits FltIn, SetPositionReq always zeroes, ExternalAccess=None AOI params, tag-group-invalid silent stall, FolErr tolerance not offset, rotary error wrap; knife system - 12 h cycle, `cm.knife_auto` with the start-lag shut guard, button-as-reset incident + 6 h guard, 6 % measurement / 94 % wood verdict, piece-size slope 0.46, percentile display)**, **`2026-08-31_A` (Training Review: three tables + 7 NQs + `operator.trainingreview` + entry view + A4 print path; paramDirection input mandatory; flex basis is parent-directional and grow needs basis 0; NQ datasource default is SQL Server; percent-vs-fraction from the `0%` cell format; two focus tables keyed on plan_month; finalised_at vs updated_at; save compaction; composite renormalisation)**, **`2026-08-31_B` (Action weekly digest: `shared.action_email_weekly` v1.0.0 + Monday 08:00 scheduled event, one email per owner + no-owner summary; three morning-email candidates inventoried; two SMTP conventions; Action data model for email; 50 open / 20 unowned / zero due dates; never %-format SQL; daysBetween at midnight; fixed-layout section tables; offline harness first)**, **`2026-09-04_A` (BACKFILL of 2026-06-30: Stem Grade Dashboard maturation + Stem Inspector defect overlay/chip-cut + stemid cyclic-key count fix + KPP Daily Report chip/Waste/ShiftStatus fixes; export-drops-declarations trap; chip = chipper-scanner not COS-scanned; knots not positional)**, **`2026-09-18_A` (Visitor Sign In audited, cleaned up and extended: NQ layer fixed + smoke 11/11, sign-in badge removed, staff save repaired, kiosk photo payload cut 10x and both kiosk search screens filter as you type, Reception shut-day board + header buttons + 06:00-22:00 auto-open, Manager Visitor Log / Visit Edit / CSV exports fixed; `schedule` package emptied a SECOND time by actor "external" - Shut Plan rebuilt and verified 8/8; `enabled: null` means ENABLED)**, **`2026-09-22_A` (Camera live view built: go2rtc relay on TL-KPPWS01 with watchdog task, generated CameraHub/Tile/Pick views + relay health pill, i-PRO fleet on Stream(3) H.264, inventory refreshed from the printed site list + sweep v1.1.0 - booths, Live Deck on .35, sprays decommissioned; 72 h task-limit outage; httpClient kwarg false-DOWN; Python blocked on TL-KPPWS01)**, **`2026-09-22_B` (COS log stop positioning: Tui camera quote dropped on evidence - placement +/-40 mm over 103k sorter_logs, PLC OPC ~700 ms floor, slip -60 mm / -330..-900 mm restart corrected by R8, -1.2 % length-scale question parked; manual-jog mechanics R12/R17/R7; positioning capture + `cos_positioning_events` + Log Stop Positioning panel + "?" popup; operator from `Operator.Current.ID` not the dead `ReportData.OperatorID`; `operator.kpi` v1.2.0 Log Stops tab; Debarker Detail for Trina with the SDB KPI definitions pinned from the DB - bark = knives OR rollers, > 3.5 m only; CutComplete one-scan pulse; four install bugs all mine - NQ path, root-container self.view, `%.%df`, event.value)**, **`2026-09-24_A` (third `schedule` package wipe root-caused and fixed structurally: `files: []` / actor `external` / Mon 21 Sep 10:41 NZST, the only package in the project that is itself a script resource, both ShutEdit calendars on LOAD FAILED; rebuilt as a plain package with `schedule.kpp`/`schedule.mly` v1.2.0, verify 7/7, `scheduled_startup_time` fixed, update-then-insert, placeholder refused)**, **`2026-09-25_A` (SDB stem tracking - twin stems from a same-scan bit test fixed in v1.2.0, map glide `SDBMap_View_v1_2_0`, outfeed scale 13 -> 13.154 mm/count, curtain length of record v1.3.0 behind `PE_PosUpdate.DB_LC.BOOLs[1]` = 1)** , **`2026-09-26_A` (Sortline kicker overload trips - verdict engine and 175-trip backfill, KickerAnomaly card, map overlays with prox lights, kicker popup with an audited one-bit enable / disable, Workmate quick WO and deep link, Workmate right + Security Setup v2.9.2)**, **`2026-09-26_B` (kicker trend popup in the VSD Trend Data style; compile of the three 2026-09-26 ADDs)** , **`2026-09-27_A` (kicker signal drops and the withdrawn line-stop rule, the kick-fail history and the mechanical verdict, prox lights on the fast tag group with an on-screen hold, trend ranges)** , **`2026-09-28_A` (kick fails on the KickerAnomaly card; Sorter Diagnostic RESET COUNTERS - `_107` and `_102` both cleared one request bit, fixed by a one-owner pulse in `_107` / `_102` v1.2.0; `_107`'s scan tick wrapped negative and no kick cycles were counted from 17 Sep; a routine L5X built from the program export and proven off the PLC)**, **`2026-09-30_A` (chipper knife clock on torque and verdict on current, lines from a belt-volume sweep; motor vibration by machine state on Disc 1 / Disc 2 / Drum / Grader Outfeed, baselines and the Disc 1 twin reference; VVB301 over-range code; the 28 Sep tools incident)**, **`2026-09-30_B` (the first Anomaly Watch builds 1.0.0-1.1.1 - four areas, then Sortline and Chippers to the CHP / GRAOF spec, radar and row scroll bars, plain words; COS_CPU's clock and daylight saving; the debug-counter check)**, **`2026-10-03_A` (PE Watch from design to live - recorders, engine, baseline, cleaning check and Cleaned marks; Anomaly Watch on five areas with history, Ask Azztec AI, shift strips and the encoder stall cross-check; standstill card; the GRAOF constraint fix)**, **`2026-10-03_A` - a second file of this name (T&B sweep cancel line and Bin 0 forensics, 1-3 Oct; `KPP_TnB_Bin0_Design`), registered late in v1.36.0**, **`2026-10-07_A` (COS Watch - a PLC cut recorder, panel and crew marks for the booth session; the two COS PE offsets taped and corrected; `_100` v1.1.0 with `_101`; probes P1-P5 - stop cuts, the lag, two encoders, before / after, butt approaches; the master retention purge; PE array symbols lit on any eye; the Engineering menu)**, **`2026-10-09_A` (PE Watch link scoring on the Anomaly Watch rows after two replays of the record; the low evening sun on Section1Start, labelled for a sun cover; Ask Azztec AI #missed / #sun; the PE cards off LEARNING; the Downtime History on WTD; the knife cards - 90-day history, the reference building after a change, one press rule for condition-based changes; the motor work log and the bearings button; the PE and encoder baseline check and the re-take tool)**, **`2026-10-10_A` (sweep auto tiles - each sweep's PLC auto bit found by two read-only probes; the T&B and Grading tags; `SweepAutoTile` on the TNB, SDB and GRA maps, hidden on the Safety cards; the Drum chipper sweep left off as unused; the Debarker stem diameter card restyled)**, **`2026-10-08_A` (the COS stopless approach behind `BA_Enable` and its trial; hand clamps counted; COS Moves - every COS move recorded in the PLC - and Processing Analytics, the stem cycle audit of 8-9 Oct; the cut timing probe for Monday; COS Watch operator buttons and the T&B link; the Grading seq deck reverse switch for Sparky - one chat 8-11 Oct, registered after 2026-10-09_A and 2026-10-10_A)**, **`2026-10-12_B` (COS NEW auto 1.0.1 - the 1.0.0 audit, the install and the 13 Oct trial, Processing Analytics 0.1.2, P2 1.0.1, the pre-flight and live checks), `2026-10-12_A` (the Debarker outfeed auto sweep back on the Sweep PE array - Jacob's (Tui) Sonics wall-array trigger kept behind `UseSweepArray`, default 0; `_220_OutfeedSweep_v1_1_0` built from the V20n L5K and proven off-PLC; the Processing Analytics builder loss verified in the 12 Oct export)**, **`2026-10-13_A` (Anomaly Watch event review - five false events of 22: the WallControlPEs WALL check with the Sonics out, a COS blind flag in the 15:00 smoko; smoko 10:30-11:00 / 15:00-15:30 day and night not judged unless the COS booth is logged in - a login is a booth row with an operator; WallControlPEs returning; judge 1.4.2, registry 1.6.0, Anomaly Watch 1.13.0, morning check 1.1.1, smoko probe)**, **`2026-10-14_A` (the MLD monthly gave two Augusts - `shared.mlyproduction` 0.3.0 passed exclusive 07:00 ends to the inclusive-date MLY by-day NQs (v3.0.0), so the August email carried 1 Sep's first 112 logs and a 30th day while the next email's column did not; 0.3.1 passes inclusive dates everywhere; probe `KPP_MLY_MonthBoundary_Probe` 1.0.0; the September email was right)**, **`2026-10-14_B` (Visitor Sign In PLANT SHUT badge moved to `schedule.kpp`; Reception shut-day kiosk returning to the visitor Menu after 2 minutes idle; Hub Key Metrics icons; the Hub revamp - Workmate Pulse `workmate.hubpulse` with the shut-aware work calendar and live activity; banner stats corrected)**, **`2026-10-14_C` (the Reception Hub Length / Volume / Stems against the KPP Daily Report, a question the team leaders had raised - the Hub read the stem rows (`report.stems_by_shift`: recovered length, the Echo way kept at the cutover) while the report reads the PLC scanned counters; 13 Oct night 28,961 m against 30,131 m - trim about 0.5 % (USNR), about 3.4 % scanned with no stem row; the Hub Length / Volume tags on the PLC meter (current OPC, previous `cos_kpi_daily`); Stems - a broken stem's 2nd piece adds its length and volume but is not counted (view 1.2.0, after a withdrawn 1.1.0 that counted it); projection rate NQs 2.0.0; the team-leader email; lettered C - the Hub Pulse log reached the project first)**, **`2026-10-14_D` (the KPP Digital Twin, COS first - a 3D view of the whole line for a 3840 x 2160 screen with LIVE data (352 tags, a lease-keeper view), a 60-minute REPLAY and a simulator with 57 dials calibrated to the 8-9 Oct audit, Compare and What if; WebDev `twin`, `twin.live` / `twin.web`, view `Application/Twin/TwinCOS`; built and tested off the gateway; post-close (1.1.0, section 11) installed on Live, 34 tags created for it, and the live motion fixed - each value smoothed between its own PLC changes on its tag timestamp, page 1.1.0 / `twin.live` 1.1.0)**, **`2026-10-15_A` (the shut day: the script read rate - verdict C, the Ignition driver queue, the leftover 50 ms Direct group; then the KPP Line Tracker - program Trk, a new sortline tracking in Structured Text beside the Tui code, shadow only, proven off the PLC by a static check and a scan-level simulation, for the download in the shut; post-close (1.1.0, section 12): downloaded and the fault test passed, the scan time check corrected, Bryce's regrade pile traced through Tui's regrade routing - false bin-3 regrades of in-spec 9.6 m logs scanned short - and the Sort Register page; post-close 2 (1.2.0, section 13, to Fri 16 Oct 06:52): the Sortline Overview chip and Sort Register button, the Sort Register live, conveyor 1 measured at 0.3034 mm a count (`ScanEncoderScale` to follow, `Conv1Scale` stays), the tracker switched on, and the Ignition comms cleaned up - a direct read 883 ms -> 57 ms)**, **`2026-10-15_B` (the last Echo screens rebuilt in Perspective - Machine Settings 1-4, Sort Line Settings and Manual Kick Control: every Echo settings tag mapped onto the one controller, the Machine Settings page by area with a checked, logged write and PLC read-back, the Ignition setpoint popups taken in, a Sparky-only manual kick with a gateway dead man; tested off the gateway and rendered before delivery; post-close (1.1.0, section 12): installed on the gateway - the grading scales in PLC units, roles read through their QualifiedValues (everyone had VIEW ONLY), the editor seeded per setting, the cut speed table and prox windows built and taken off; manual kick for Big Balls too; settings changed in the last 48 h glow; the settings watch logs changes made outside Ignition)**, **`2026-10-15_C` (a third chat on the shut day, 15 Oct about 12:00 - 19:30, closed out 20 Oct: Anomaly Watch stands down for a Shut Plan shift - judge 1.5.0, Anomaly Watch 1.14.0; LEAK WATCH - the hydraulic tank leak watch `forensics.hydLeak`, built, installed and tuned on 1 - 15 Oct, a T&B HydUnit4 leak found; LEAK WATCH on the hydraulics cards in place of the pumps count, card 1.5.0 - 1.5.1; a short Anomaly Watch headline, 1.0.3)** **`2026-10-16_A` (the 2026-10-15_A chat went on, Fri 16 Oct 06:52 to Sun 18 Oct: the regrade marks on the Sortline Map and its bins; the twin's saved forecasts; the Line Tracker on site - 1.1.0 (the landing re-anchored at the PE clear), 1.1.1 (the kicker return stroke), 1.1.2 (the landing PE losing a log) imported online; the Sortline Map's Tracker mode; the 30 min WATCH run; 1.2.0 designed on a sequence model; the DATA run - the T&B sends the last message again, every message carries its COS slot; 1.2.0 built - the identity checked by length - and proven off the PLC; the gateway identity advisor agreed as the next design; 1.1.0 section 13 - the advisor's concept design and phase 0 probe, Tui's scan check read from V20o; 1.2.0 section 14 - the scanner to order, the cross-ups, the COS regrade view)**, **`2026-10-19_A` (the KPP Daily and the Monday Weekly showed two Stem vs Forecast figures for 1-18 Oct - the daily's 59,258 is the 1 Aug calendar pro-rata rule, the weekly's 66,800 the per-shift formula the daily dropped then (forecast / scheduled shifts x 2 for every day, 12.7 % fast in October); `shared.weeklyreport` 0.8.2 builds its month-to-date bar and chart the daily's way - kpi_daily, the Sunday's month - proven off the gateway against both libraries)**, **`2026-10-19_B` (the 2026-10-16_A chat went on into Mon 19 Oct: tracker 1.2.0 on site - the 230 refused for names that differ only in case, 1.2.1; the RING and two WATCH runs, `Srt_CosMem` on; the Tracker task at half its rate since 17 Oct evening - the speed display and the kicker return window, both wrong-bin kicks; phase 0 GO and the COS regrade numbers, Re-Optimize dropped; when the tracker can take over from Tui - the decision, not the outputs; the gateway identity advisor's phase 1 built in shadow and proven on a simulated line; WATCH probe 1.6.1; post-close (1.1.0, section 13): installed - sorter_engine writes the scan rows 0 - 10 s late, `trk.advisor` 1.0.1 pairs the tracker's piece in order; post-close 2 (1.2.0, section 14): the first hour of 1.0.1 - all as Tui, the lead to the kick 52 s median; post-close 3 (1.3.0, section 15): the first 7 hours - a wrong-bin log caught; 1.0.2 keeps its state across project saves; the user's regrade idea)**, **`2026-10-17_A` (17 - 19 Oct: the COS encoder rate flags - `_250` v3.4.0 on the wall clock; PUMP WATCH on 18 pumps - built, on site 1.0.1 - 1.0.4, the long reference, the DETAILS popup; the station motors and pump popups; Big John and the IO-Link masters - PV8000 on every pump, HYDAC tanks; the CM baselines reviewed, the tool rebuilt as 1.1.0 and GRAOF re-taken)**, **`2026-10-20_B` (the 2026-10-19_B chat into Tue 20 Oct: 1.0.2 one run through saves; the day check `KPP_TrkAdvisor_Report` 1.1.0 - 99.7 % as Tui on its own data, Tui giving one log's data to two logs (7 into another bin), the advisor wrong on old open cuts (6), 9 of 286 never-scanned cuts in Bin 0; the data cut - SED a share of the log, LED by the plan's taper, the ring's Y = X; `trk.advisor` 1.0.3)**, **`2026-10-14_E` (the Value Recovery section for Renata, 14 - 15 Oct: the link probe P1, the section built on `kppstems.vr_stem` and `analytics.valuerecovery` - origin of every butt cut, crews, the grading and COS booths, stems; the PLC grade call recorder `_311_GradeCallWatch` and `forensics.gradeCalls`; installed and verified 17 PASS; the reader's catch-up read as a stall; the Page's loading bar derived from the report's own window; hover tips on every view; the graders chart key in plain words)**, **`2026-10-20_A` (Value $, 19 - 20 Oct: the butt defects meeting in $ - $9.47 a butt cut; the 19 Oct restart wipe - `analytics.processing` folded into `analytics.valuerecovery`; the Financials tab - `vr_money_*`, NQ Money, library 1.1.0, Page 1.0.3, Financials 1.0.5)**, **`2026-10-06_A` (three Capex documents for KT management, 6 - 16 Oct: the Debarker infeed chainsaw V1.0 - V1.6 on the chainsaw downtime audit and a bent-stem probe; the faster cut - 78 h a year of infeed time, not lost production today; the Hogger MCC replacement V1.0; AI stem grading Phase Two V1.0)**, **`2026-10-21_A` (low plant air made visible, 21 Oct: the Debarker Ring flashes red on the SDB Map with a LOW AIR pill - SDB Map 1.4.0 and the stylesheet keyframes `kpp-ring-lowair`; the grading booth tile - red while low, amber "x min ago" for 10 min after - LowAirTile 1.0.0 on Grading Overview 1.5.0)**, **`2026-10-22_A` (Visitor Sign In, 22 Oct: the management change request - back to the sign-in board after 2 min without a touch for the Reception login, Hubheader 1.6.1, and the mandatory "Have you been inducted at KPP?" stored in `dbo.visit.inducted`, User Verification 1.1.3 with the gold glow; the On site card scroll arrows, Visitor Card 1.3.0; PLANT SHUT on a normal day - the label display binding, Menu 2.10.0; Log Stop Positioning off the COS Map onto Machine Settings, COS Map 1.1.0 and MachineSettings 1.0.5)**, **`2026-10-23_A` (Operator KPIs, 23 Oct: the Debarker knife record decoded and aligned to the knives - `sdb.ringcapture` shadow capture, Knife Check page, SDB Map live marks, PLC L08B; close gaps and corrected Debarker KPIs; knot / defect calls; Design v3_14_0 audit and the calibration probe's approval pack; pulp deck saw-log probe; Trina's bark explainer; Training Review KPI values kept; HR Final Report with lock triggers)** |
| USNR reporting fix SQL (2026-07-15_A) | `prod_report_view_TR1_fix_v1_0.sql`, `production_daily_summary_fn_v1_1.sql`, `stems_by_date_view_v1_1.sql`, `forecast_daily_view_v1_1.sql`, `ProductionByGrade_completion_v1_4.sql`, `StemPcSzByCompart_v1_0.sql`. |
| Echo Report deliverables (2026-07-15_B) | `KPPDailyReport_view_v1_6_0.json`, `ShiftProduction_view_v1_1_0.json`, `ShiftSummary_view_v1_1_0.json`, `DaySelector_view_v1_1_0.json`, `grade_refresh_job_v0_3_1.py`. Detail in Raw Log 2026-07-15_B §E7. |
| EmailReports deliverables (2026-07-18_A) | `dailyproduction_code_v4_8_1.py`, `weeklyreport_code_v0_2_1.py`, `reporttiles_code_v1_2_0.py`, `view_EmailReports_v1_5_2.zip`, `component_WeekSelector_v1_0_1.zip`, `view_HubSidemenu_v1_1_0.zip`, `view_Hubheader_v1_1_0.zip`, `view_Hub_v1_6_0.zip`, `view_Production_v2_4_0.zip`, dormant `webdev_reports_*_v1_0_0.py`. Detail in Raw Log 2026-07-18_A. |
| Operator-KPI deliverables (2026-07-19_B) | Scripts `operator_operatorscorecard_v3_10_3.py`, `operator_kpi_v1_1_0.py`. Views `Scorecard_view_v2_6_0.json`, `ScorecardPrintable_view_v1_3_4.json`, `NewKPIReview_view_v1_2_0.json`, `OperatorKPI_view_v1_2_2.json`, `PruneCallForensics_view_v1_3_0.json`, `Timeliness_view_v1_4_0.json`. NQs (raw SQL) `Waste Percent`, `T&B Cross-ups Occurrences per Hour`, `Booths By Day v1.1.0`. DDL/console `KPP_scorecard_cache_ddl` (→ `operator.scorecard_cache`), `SQL_timeliness_exclude_chippers` (both timeliness fns, APPLIED), `ScorecardCacheWarm_timer_v1_1_0.py`. Probes `KPP_operator_kpi_probe`, `KPP_kpi_calibration_probe`, `KPP_cache_diag`, `KPP_timeliness_nq_test`. Spec `Operator_KPI_Scorecard_Design_v3_10_4.xlsx`. Detail in Raw Log 2026-07-19_B. |
| MLY multi-year + Qube-report deliverables (2026-08-01_A) | Report `KPP_MLY_Debarker_Throughput_Review_v1_0_0.pdf` / `.docx` + build script `KPP_mly_qube_report_build_v1_0_0.py`. Scripts `shared_mlytrends_code_v1_7_0.py`, `db_sync_mly_production_code_v1_0_0.py`, `shared_mlyproduction_code_v0_2_3.py`. Views `view_MLY_MultiYearProduction_v1_1_4.json`, `view_MLY_MultiYearPace_v1_1_9.json`, `view_MLY_MultiYearLoaders_v1_0_2.json` (+ `_v1_0_0.zip`), `MLY_container_view_v1_4_0.json`. Event `scheduled_SyncMLYProduction_v1_0_0.zip`. NQs (raw SQL) `Monthly Production`, `Monthly Pace v1.1.0`, `Cause Group Yearly v1.1.0`, `Loaders Breakdown`, `Downtime Detail v1.1.0`, `Sync DailyProduction`, `Sync DailyPace`. DDL/console `KPP_mly_pace_schema_console_v1_0_0.py` (-> `mly.pace_daily`), `KPP_mly_planned_flag_schema_console_v1_0_0.py` (-> `mly.planned_label` + `is_planned`). Probes `KPP_mly_qube_probe_v1_0_1.py`, `KPP_mly_loaders_probe_v1_0_0.py`, `KPP_mly_multiyear_smoketest_v1_0_0.py`, `KPP_mly_planned_flag_probe_v1_0_0.py`. RETIRED unused: `Monthly Production Workbook`, `Monthly Production LogData`, `Monthly Pace Estimate`. Detail in Raw Log 2026-08-01_A. |
| EmailReports + volume-recon deliverables (2026-08-01_B) | Scripts `shared_dailyproduction_code_v4_7_15.py` (supersedes 4_7_13/14), `shared_monthlyreport_code_v0_2_6.py` (supersedes 0_2_5), `shared_mlyproduction_code_v0_3_0.py`. Views `EmailReports_container_view_v1_6_0.json`, `view_EmailReports_NewTabs_v1_0_0.zip` (KPPMonthly/MLYDaily/MLYMonthly leaves), leaves `view_EmailReports_KPPMonthly_v1_0_2.json` + `view_EmailReports_MLYMonthly_v1_0_2.json` (original MonthSelector, selectedMonth binding), `view_Components_MonthSelector_RESTORE_original_v1_0_0.zip` (new component withdrawn), `BoardpackCard_view_v1_1_0.json`. Event `scheduled_BoardpackCloseMonthly_v1_0_0.zip`. Consoles/probes `KPP_kos_downtime_probe_v1_0_1.py`, `KPP_kos_uptime_fn_probe_v1_0_0.py`, `KPP_Monthly_volume_gap_recon_console_v1_2_0/v1_3_0/v1_4_0.py`, `KPP_canned_monthly_backfill_console_v1_0_0.py` (B2 never needed), `KPP_boardpack_freeze_july_console_v1_0_0.py`. Detail in Raw Log 2026-08-01_B. |
| Yard area + exploration reports (2026-08-06_B) | NQs `NQ_Yard_SED_Distribution_v1_0_0.sql`, `NQ_Yard_SED_Filter_Options_v1_0_0.sql`, `NQ_USNR_SED_Distribution_v1_0_1.sql`, `NQ_USNR_SED_Filter_Options_v1_0_0.sql`, `NQ_USNR_ButtCut_Breakdown_v1_0_2.sql`, `NQ_USNR_ButtCut_Filter_Options_v1_0_2.sql`, `NQ_Grading_BoothCalls_Breakdown_v1_0_1.sql`. Views `view_YardSEDDistribution_v1_0_4.json`, `view_KPPSEDDistribution_v1_0_2.json`, `view_ButtCutsExploration_v1_2_1.json`, `view_BoothCallsExploration_v1_1_2.json`, `view_Yard_v1_0_0.json`, `view_Production_v2_12_0.json`, `view_Hubsidemenu_v1_3_0.json`, `pageconfig_config_v1_1_0.json`. CSS `stylesheet_ADD_v2_44_hub_menu_new.css`, `stylesheet_ADD_v2_45_report_new.css`. Probes/smokes `KPP_yard_sed_probe_v1_0_0.py`, `KPP_yard_sed_smoketest_v1_0_0.py`, `KPP_usnr_sed_probe_v1_0_0.py`, `KPP_buttcut_probe_v1_0_0.py`, `KPP_buttcut_smoke_v1_0_0.py`, `KPP_boothcalls_smoke_v1_0_0.py`, `KPP_boothshift_probe_v1_0_0.py`. Detail in Raw Log 2026-08-06_B. |
| Office weekly feed (2026-08-10_A) | Script `weeklyreport_code_v0_8_1.py` (live: `WEEKLYSTATS_CONN` -> `KTSQLSYS_Transformations`). DDL/console `KPP_WeeklyStats_master_setup_v1_2_0.sql`, `KPP_WeeklyStats_master_build_console_v1_4_0.py` (-> `dbo.WeeklyStats` + `dbo.WeeklyReportColour` in `Transformations`). Probes `KPP_WeeklyStats_db_recon_v1_0_1.py`, `KPP_WeeklyStats_rights_probe_v1_0_2.py`, `KPP_WeeklyStats_bkopt_probe_v1_0_0.py`, `KPP_WeeklyStats_tlsql01kpp_probe_v1_0_0.py`, `KPP_WeeklyStats_svcignition_kpp_rights_v1_0_0.py`, `KPP_WeeklyStats_office_transformations_probe_v1_0_0.py`. Verify `KPP_WeeklyStats_live_persist_verify_v1_0_0.py` (deployment-guarded), `KPP_WeeklyStats_persist_test_v1_0_0.py`, `KPP_WeeklyStats_handoff_readback_v1_0_0.py`, `KPP_WeeklyStats_monday_check_v1_0_0.py`. Superseded: `weeklyreport_code_v0_1_6/7/8.py` (built on the stale 0.1.5 base). Detail in Raw Log 2026-08-10_A. |
| TR / MLY-window fixes (2026-08-06_A) | SQL `KPP_usnr_prod_report_TR_v2_0_0.sql` (+ console applier `KPP_usnr_prod_report_TR_console_v1_0_0.py`), `KPP_NQ_Production_MLY_ProductionByDay_v3.0.0.sql`, `KPP_NQ_Production_MLY_ProductionByDayAndGrade_v3.0.0.sql`. Probes `KPP_mly_grade_names_probe_v1_0_0.py`, `KPP_usnr_TR_grades_probe_v1_0_0.py`, `KPP_usnr_TR_order_match_check_v1_0_0.py`. Views `view_Components_MonthSelector_RESTORE_original_v1_0_0.zip`, `view_EmailReports_KPPMonthly_v1_0_2.json`, `view_EmailReports_MLYMonthly_v1_0_2.json`. Working copy now `MainSCADA_Timberlands_2026-08-06_1255.zip`. Detail in Raw Log 2026-08-06_A. |
| Condition Monitoring - chipper sensors (2026-08-12_A) | Tags `CM_udt_VibMotor_v2_0_0.json`, `CM_instances_v2_0_0.json`. Views `CMVibrationCard_View_v1_5_0.json`, `SafetyPlantOverview_View_v1_13_0.json`, `CM_Chippers_View_v1_3_0.json`. Console `CM_S0_probe_v1_0_0.py`, `CM_S1_verify_v1_2_0.py`, `CM_retire_wmcm_v1_0_0.py` (EXECUTED, 29 rows). Source pack: ifm `VVB010-01_EN-GB.pdf` / `VVB301-00_EN-GB.pdf`, `KPP_COS_V20A_Controller_Tags.CSV`, `MainProgram_Program.L5X`. Superseded: `WM_CM_*_v1_0_0.json`, card v1_0_0-v1_4_0, overview v1_10_0-v1_12_0, `CM_Chippers_View_v1_0_0`-`v1_2_0`, `CM_S1_verify_v1_0_0/v1_1_0`. Detail in Raw Log 2026-08-12_A. |
| Chipper drive-load + StarLoader panel (2026-08-12_B) | Research `KPP_CM2_TnB_Research_v1_0_0.md`. Probes `CHP_S0_driveload_probe_v1_0_0.py`, `TNB_S0_starloader_probe_v1_0_0.py`, `CM2_S0_historian_tag_probe_v1_0_0.py` (read-only, NOT YET RUN). Tags `CM_udt_DriveLoad_v1_0_0.json`, `CM_DriveLoad_instances_v1_0_0.json`, `TNB_StarLoader_tags_v1_0_0.json` (import gated on probe 3). Views `StarLoaderPanel_View_v1_0_0.json`, `CM_Chippers_View_v1_4_0.json` (supersedes v1_3_0). SVG `TNB_StarLoader_v1_0_0.svg`. Source pack: `Chippers_Torque_and_Current_Monitoring.zip` (8 x L5X + `KPP_COS_V20D_Controller_Tags.CSV`), `MainSCADA_Timberlands_2026-08-12_1303.zip`. Detail in Raw Log 2026-08-12_B. |
| Probe close-out + CM rebind (2026-08-14_A) | View `CM_Chippers_View_v1_5_0.json` (bindings proven Good live; supersedes v1_4_0 - DO NOT import v1_4_0). Probes `CM2_S0_historian_tag_probe_v1_1_0.py` (superseded), `CM2_S0_historian_tag_probe_v1_2_0.py`, `TNB_S1_starloader_verify_v1_0_0.py`, `TNB_S1_pumprun_probe_v1_0_0.py` (pending run). Retired on-gateway: `_types_/CM/DriveLoad`, `CM/Chipper/*Load` x3; files `CM_udt_DriveLoad_v1_0_1.json` + `CM_DriveLoad_instances_v1_0_1.json` retired - do not re-import. `StarLoaderPanel_View_v1_0_2.json` (hydraulics dot -> HydUnit4 any-pump-running; supersedes v1_0_1/v1_0_0; delete tag `KPP/TnB/Data/StarLoader/PumpRun`). Detail in Raw Log 2026-08-14_A. |
| Knife-bluntness system (2026-08-14_B) | DB `CM_knife_schema_v1_0_0.sql`; NQ `CM_NQ_KnifeDelta_v1_0_0.sql` (create as `CM/KnifeDelta`, param `machine` String, bare SQL); gateway library `CM_load_rollup_v1_1_0.py` (Project Library package `cm` -> script `cm_rollup`; Timer Fixed Delay 300000 ms dedicated -> `cm.cm_rollup.run()`; one-off `cm.cm_rollup.backfill(14)`; supersedes v1_0_0). Console DDL runner `CM_knife_schema_console_v1_0_0.py`. Views `CMKnifeCard_View_v1_0_0.json` (new component), `SafetyPlantOverview_View_v1_14_0.json` (supersedes v1_13_0), `CM_Chippers_View_v1_6_0.json` (supersedes v1_5_0/v1_4_0 - import v1_6_0 only). Install order + thresholds in Raw Log 2026-08-14_B. |
| TimberPay - payroll transfer (2026-08-16_A) | Audit `TimberPay_VBA_Audit_and_Ignition_Assessment_v1_0_0.md` + extracted source `TimberPay_VBA_Extracted_Source_v2_03_0.bas`. DDL/seed `TimberPay_Schema_v1_0_0.sql`, `TimberPay_Seed_EmployeeLookup_v1_0_0.sql`, `TimberPay_Seed_2026_Uploads_v1_0_0.sql` + console runners `*_ScriptConsole_v1_0_0.py` (DRY_RUN guarded). Library `timberpay_code_v1_0_0.py` (Project Library `timberpay/timberpay`). NQs (raw SQL) `TimberPay_NQ_ImportRows_v1_1_0`, `_ImportBatches_v1_0_0`, `_UploadBatches_v1_0_0`, `_HistoryOpSummary_v1_0_0`, **`_HistoryRows_v2_0_0` (BatchId only - v1_0_0/v1_1_0 superseded, the ClockNo param was never declared)**, `_BannerStats_v1_0_0` (now unused by the view). View `TimberPay_View_v1_5_0.json` (supersedes v1_1_0-v1_4_0). Smoke `TimberPay_NQ_SmokeTest_ScriptConsole_v1_0_2.py` (supersedes v1_0_0/v1_0_1), diagnostic `TimberPay_NQ_ParamDiagnostic_ScriptConsole_v1_0_0.py`. Detail in Raw Log 2026-08-16_A. |
| Business Systems pillar + expo page (2026-08-16_A) | Views `Hub_View_v1_16_0.json` (chips removed, newKeys plumbing dropped), `HubSideMenu_View_v1_5_0.json`, `BusinessSideMenu_View_v1_6_0.json` (supersedes v1_3_0 which broke the rail - do not import), `BusinessHome_View_v1_29_0.json`, `Sunstone_View_v1_0_0.json`. Library `whatsnew_code_v1_3_0.py` (FULL replacement; supersedes v1_2_0). Stylesheet `stylesheet_v2_48_0.css` (complete import file; `hub-chip-new` v1.2.0 in, `hub-card-new` removed). WebDev `WebDev_AccessControl_Import_v1_5_2.zip` (resource `fun/accesscontrol`, GET pre-enabled) + `accesscontrol_doGet_v1_5_2.py`; probe `WebDev_AccessControl_Probe_ScriptConsole_v1_0_0.py`. Source: `Azztec_Enterprise_2026_Marketing_V1_3.docx` (1034 px emblem). Detail in Raw Log 2026-08-16_A. |
| StarLoader panel + knife maturation (2026-08-24_B) | Views `StarLoaderPanel_View_v1_5_5.json` (supersedes v1_0_0-v1_5_4), `TNBMap_View_v1_2_1.json`, `CMKnifeCard_View_v1_5_1.json`, `CMKnifeMethod_View_v1_4_0.json`, `SafetyPlantOverview_View_v1_14_5.json`, `CM_Chippers_View_v1_6_1.json`. Tags `TNB_StarLoader_tags_v1_1_0` / `v1_2_0` / `v1_3_0` / `v1_4_0` (import at `KPP/TnB/Data`, Abort). NQ `CM_NQ_KnifeDelta_v1_3_0.sql` (paste over `CM/KnifeDelta`; supersedes v1_0_0-v1_2_0). Gateway library `CM_knife_auto_v1_2_0.py` (package `cm` -> `knife_auto`; second Timer Fixed Delay 300000 ms dedicated -> `cm.knife_auto.run()`). Fix/repair `TNB_S4_tagfix_v1_0_0.py`, `TNB_S6_fastgroup_fix_v1_1_0.py`, `CM_knife_undo_v1_2_0.py` (EXECUTED, 15 rows), `CM_knife_backdate_v1_0_0.py` (EXECUTED, 6 rows), `CM_knife_seed_v1_1_0.py`. Probes `TNB_S2_axisbits_probe_v1_0_0.py`, `TNB_S3_pump3_probe_v1_0_0.py`, `TNB_S5_tag_smoketest_v1_0_0.py`, `CM_S1_rollup_timer_smoketest_v1_1_0.py`, `CM_S2_setprofile_v1_1_0.py`, `CM_S3_throughput_probe_v1_2_0.py`, `CM_S4_profile_recheck_v1_1_0.py`. Brief `KPP_KnifeChange_Workmate_Brief_v1_0_0.md`. Detail in Raw Log 2026-08-24_B. |
| Training Review - Trina's monthly review (2026-08-31_A) | DDL/console `TrainingReview_DDL_Console_v1_0_0.py` (3 tables + 2 indexes, EXECUTED), `TrainingReview_DDL_Console_v1_1_1.py` (`finalised_at` + backfill, EXECUTED; **supersedes v1_1_0 whose verify threw on its own DRY_RUN pass - do not run v1_1_0**). NQs (raw SQL, folder `Report/Training/`, **datasource `KPP_production` explicitly per NQ**, `Weight`/`Score` as **Float8**): `Review Get v1_1_0`, `Review Upsert v1_1_0` (both supersede v1_0_0; add `updated_at`/`finalised_at`, no param changes), `Focus List`, `Focus Upsert`, `Focus Trim`, `Prereq List`, `Prereq Upsert` (all v1_0_0). Library `operator_trainingreview_v1_4_0.py` -> package `operator` script `trainingreview` (supersedes v1_0_0-v1_3_0; `DEBUG`/`dbg()`, `toPercent`/`toFraction`, `savedInfo`/`savedStatus`, `printData`). Views `TrainingReview_view_v1_6_0.json` (supersedes v1_0_0-v1_5_0), `TrainingReviewPrintable_view_v1_1_0.json` (supersedes v1_0_0; **resource name must be `TrainingReviewPrintable` with NO version suffix - printer and entry view hardcode the path**), `TrainingReviewPrinter_view_v1_0_0.json`, `OperatorKPI_view_v1_6_0.json`. Smokes/tools `TrainingReview_NQ_Smoke_v1_0_0.py` (16 checks), `TrainingReview_Lib_Smoke_v1_0_1.py` (34 checks; supersedes v1_0_0), `TrainingReview_PrintData_Smoke_v1_0_0.py` (12 checks), `TrainingReview_Inspect_Purge_v1_0_0.py` (DRY_RUN guarded). Source `Monthly_training_review_template.xlsx`, working copy `MainSCADA_Timberlands_2026-08-29_0648.zip`. Install order in Raw Log 2026-08-31_A. |
| Action weekly digest (2026-08-31_B) | Library `shared_action_email_weekly_v1_0_0.py` -> package `shared` script `action_email_weekly` (`runWeeklyDigest()` production; `testSend(ownerId=None)` one digest to Adriaan only; `preview()` routing plan, no send; `buildPlan()`/`fetchOpenActions()` data layer; `TEST_MODE` ships True; `smtp='Email'`, from `workmate@kt.co.nz`; logos via `shared.po_email_morning._loadLogoB64`). Scheduled event `Scheduled_Workmate_Action_weekly_digest_v1_0_0.py` (name `Workmate Action weekly digest`, cron `0 8 * * 1`). Verified live: `preview()` 50/6/20, `testSend()` for Brian Jeffery rendered in Outlook. Source export `MainSCADA_Timberlands_2026-08-31_1237.zip`. Install order + standing items in Raw Log 2026-08-31_B. |
| Visitor Sign In audit + Reception board (2026-09-18) | Audit `KPP_VisitorSignIn_Audit_v1_2_0.md` (+ probe `KPP_VisitorSignIn_Probe_v1_0_0.py`). NQs (raw SQL, all `KPP_Visitor`) `KPP_NQ_Exchange_VisitorSignIn_People_Signout_v1_1_0`, `_People_AllGuests_v1_1_0`, `_People_GuestExists_v1_1_0`, `_Configuration_DistributionValues_v1_1_0`, `KPP_NQ_Exchange_VisitorSignInManager_Visit_Add_v1_0_0` (NEW), `_Visit_Remove_v1_1_0` (type change), `_Staff_Item_v1_1_0`. Libraries `photo_code_v1_0_0.py` (package `exchange/visitor_sign_in_manager` -> `photo`), `debug_code_v1_1_0.py`, `schedule_kpp_code_v1_1_0.py` + `schedule_mly_code_v1_1_0.py` (package `schedule`). Views (paste over `view.json`) `VisitorMenu_view_v2_8_0`, `VisitorMenuTile_view_v1_0_0` (new), `VisitorCard_view_v1_2_0` (new), `Hubheader_view_v1_3_0`, `VisitorCreate_view_v1_2_0`, `VisitorConfig_view_v1_1_0`, `VisitorKioskStaff_view_v1_2_0`, `VisitorKioskGuest_view_v1_1_0`, `VisitorStaffDetails_view_v1_2_0`, `VisitorLog_view_v1_1_0`, `VisitEdit_view_v1_1_0`, `VisitorStaffView_view_v1_1_0`, `VisitorContactsView_view_v1_1_0`. Console scripts (DRY_RUN guarded where they write) `KPP_VisitorSignIn_NQSmoke_v1_0_0.py` (11 checks), `KPP_VisitorDB_ConfigFix_v1_1_0.py` (EXECUTED - 3 text fixes, 7 badge keys deleted), `KPP_VisitorSignIn_KioskStaffProbe_v1_0_0.py`, `KPP_VisitorDB_StaffPhotoResize_v1_0_0.py` (EXECUTED - 8 photos, originals in `C:\Users\prinslooa\KPP_StaffPhotoBackup_20260917`), `KPP_schedule_verify_v1_0_0.py` (8 checks). Superseded, do not import: `VisitorMenu_view_v2_0_0`-`v2_7_0`, `VisitorCard_view_v1_0_0`/`v1_1_0`, `Hubheader_view_v1_1_0`/`v1_2_0`, `VisitorCreate_view_v1_1_0`, `VisitorKioskStaff_view_v1_1_0`, `VisitorStaffDetails_view_v1_1_0`, `KPP_VisitorDB_ConfigFix_v1_0_0`, `KPP_VisitorSignIn_Audit_v1_0_0`/`v1_1_0` (wrong delete list). Install order + open decisions in Raw Log 2026-09-18_A. |
| Camera live view (2026-09-22) | Relay config `go2rtc_v1_14_0.yaml` -> `C:\go2rtc\go2rtc.yaml` on TL-KPPWS01 (46 streams; CONTAINS CREDENTIALS - keep out of project knowledge), go2rtc 1.9.14, scheduled task `go2rtc` (watchdog registration in the Reference section 2). Views `CameraHub_v1_3_3.json` (`Cameras/CameraHub`, page `/Cameras`), `CameraTile_v1_3_1.json`, `CameraPick_v1_1_1.json` (`Components/Camera/*`), `Hubsidemenu_v1_6_0.json`, optional `CameraWall_v1_0_4.json`. Generator `gen_CameraHub_v1_3_3.py` (source of all camera views). Probes (read-only, wired laptop) `KPP_subnet_sweep_v1_1_0.py`, `KPP_camera_probe_v1_2_0.py`. Superseded, do not import: `go2rtc_v1_0_0`-`v1_13_0`, `CameraHub_v1_0_0`-`v1_3_2`, `CameraTile_v1_0_0`-`v1_3_0`, `CameraPick_v1_0_0`/`v1_1_0`, `CameraWall_v1_0_0`-`v1_0_3` and the `CameraWallBooth1`/`CameraWallChippers`/`CameraWallSite`/`CameraWall_instances` family, generators `gen_Camera_*`, `gen_CameraTile_*`, `gen_CameraHub_v1_0_0`-`v1_3_2`, probes `KPP_camera_probe_v1_0_0`/`v1_1_0`, `KPP_subnet_sweep_v1_0_0`. Detail in Raw Log 2026-09-22_A. |
| COS log stop positioning + Debarker Detail (2026-09-22_B) | Console `KPP_COS_Positioning_Tags_v1_0_1.py` (creates `[TL-KPPWS01-01]KPP/COS/Positioning`, 28 OPC tags; backfill EXECUTED 33 rows), DDL `KPP_COS_Positioning_DDL_v1_0_0.py`/`.sql` (`kppstems.cos_positioning_events`, EXECUTED). Library `cos_positioning_v1_0_1.py` -> `dataengine.kpp.capture.cos_positioning`, Gateway Timer "COS Positioning Capture" 1000 ms fixed delay -> `tick()` (`DEBUG = True`). NQ `KPP_COS_Positioning_NQ_PositioningShift_v1_0_0.sql` -> `Production/COS/LogStopPositioning`. Views `COS_LogStopPositioning_view_v1_0_4.json` (`Application/COS/LogStopPositioning`), `COS_LogStopPositioningHelp_view_v1_0_0.json` (`Framework/Popups/COSLogStopPositioningHelp`), `COS_Map_view_LogStopPanel_v1_0_0.json` (`Application/COS/COS Map`, one root-level embed), generator `COS_LogStopPositioning_gen_v1_0_4.py`. Operator KPI: `operator_kpi_v1_2_0.py`, NQs `NQ_Report_KPI_COS_Log_Stop_{Manual_Percent,Overruns_per_100_Cuts,Max_Overrun,Cuts}_v1_0_0.sql` (`Report/KPI/COS/Log Stop *`), `LogStopPositioning_view_v1_0_0.json` (`Application/Reports/Operator/LogStopPositioning`), generator `OperatorKPI_LogStops_gen_v1_0_0.py`. Debarker Detail: NQs `NQ_Report_KPI_SDB_{Scores,Shift_Trend,Lift_Histogram,Worst_Stems,Stem_Profile}_v1_0_0.sql` (`Report/KPI/SDB/<name>`, no Detail folder), `DebarkerDetail_view_v1_0_3.json` (`Application/Reports/Operator/DebarkerDetail`), `DebarkerDetailHelp_view_v1_0_0.json` (`Framework/Popups/DebarkerDetailHelp`), `OperatorKPI_view_v1_8_0.json` (root `OperatorKPI_v1_8_0`), `TrainingReview_view_v1_7_0.json` (root `TrainingReview_v1_7_0`), generator `DebarkerDetail_gen_v1_0_3.py`. Probes (read-only, keep): `KPP_COS_LogStop_SlipProbe_v1_1_0.py`, `KPP_LogStop_LengthError_Probe_v1_0_0.py`, `KPP_SDB_Profile_Definitions_Probe_v1_0_0.py`. Superseded, do not import: `KPP_COS_LogStop_SlipProbe_v1_0_0`, `KPP_COS_ManualJog_Probe_v1_0_0`, `KPP_COS_Positioning_Tags_v1_0_0`, `cos_positioning_v1_0_0` (inverted overrun gate), `COS_LogStopPositioning_view_v1_0_0`-`v1_0_3` + generators `v1_0_0`-`v1_0_3`, `OperatorKPI_view_v1_7_0`, `DebarkerDetail_view_v1_0_0`-`v1_0_2` + generators `v1_0_0`-`v1_0_2`. Probe leftovers to delete: tags `[TL-KPPWS01-01]Diag/LogStopProbe`, tag group `Diag_50ms`. Detail in Raw Log 2026-09-22_B. |
| Shut calendar rescue (2026-09-24_A) | Libraries `schedule_kpp_code_v1_2_0.py` and `schedule_mly_code_v1_2_0.py` -> Project Library **package** `schedule` > scripts `kpp` / `mly` (the package must be a plain folder - see the ADD). Verify `KPP_schedule_verify_v1_1_0.py` (Script Console, 7/7, write round trip on 2099-01-01 / 2099-01-07 only). Detail in Raw Log 2026-09-24_A. |
| SDB stem tracking + SDB Map (2026-09-25_A) | PLC routines, imported as new routines with the JSRs repointed: `SDB_100_CheckStemBuffer_v1_2_0.L5X`, `SDB_200_UpdateStemAtDB_LC_v1_3_0.L5X`, `SDB_201_UpdateStemAtDB_OutfeedPEs_v1_3_0.L5X`, `SDB_251_GetStemDataToSend_v1_3_0.L5X` (the v1_2_0 `_200` / `_201` were superseded the same day). In place: `SDB_101_UpdateStemPos_v1_3_0.st`, `_202` R1 and Outfeed `_220` R20 operand fixes. Install sheets `SDB_StemTrack_Fix_Edits_v1_2_1.txt` (supersedes v1_2_0) and `SDB_StemTrack_Fix_Edits_v1_3_1.txt` (supersedes v1_3_0). View `SDBMap_View_v1_2_0.json` (supersedes v1_1_0 - do not import v1_1_0). Probes (read-only) `SDB_StemTrack_Verify_v1_0_0.py`, `SDB_StemPosLength_Check_v1_1_0.py` (supersedes v1_0_0), `SDB_Length_Truth_v1_0_0.py`. Switch `SDB_StemTrack.PE_PosUpdate.DB_LC.BOOLs[1]` = 1 since 26 Sep. Detail in Raw Log 2026-09-25_A and `KPP_SDB_StemTracking_Reference`. |
| Sortline kicker anomaly (2026-09-26_A / _B, 2026-09-27_A, 2026-09-28_A) | Libraries `forensics_kickerHeat_code_v1_5_0.py`, `forensics_kickerEnable_code_v1_1_0.py`, `forensics_kickerWO_code_v1_1_0.py`, `forensics_kickerTrend_code_v1_2_0.py` -> Project Library package `forensics`. Installers (applied) `KPP_KickerHeat_Slice1_Install_v1_0_0.py`, `KPP_KickerHeat_Slice2_Install_v1_0_0.py`, `KPP_KickerHeat_TripsTag_v1_0_0.py`, `KPP_KickerEnable_WorkmateRight_v1_0_2.py`, `KPP_KickerHeat_SignalDrop_Install_v1_0_0.py`, `KPP_KickerHeat_KickFails_Install_v1_0_0.py`, `KPP_KickerHeat_SignalFix_v1_0_0.py`, `KPP_KickerHeat_ProxTagGroup_v1_0_0.py`. Views `KickerAnomaly_view_v1_6_0`, `SortlineKickerHeatCell_view_v1_2_0`, `SortlineKickerHeatRow_view_v1_1_0`, `KickerHeatMethod_view_v1_2_0`, `SortlineKickerOverlay_view_v1_3_0`, `SortlineKickerPopup_view_v1_8_0`, `KickerTrend_view_v1_4_0`, `KickerQuickWO_view_v1_1_0` (at `Framework/Workmate/Popups/KickerQuickWO`), `SortlineOverview_view_v1_1_0`, `SortlineMap_view_v1_1_0`, `SecuritySetup_view_v2_9_2` (+ offline `SecuritySetup_patch_v2_9_2.py`). Generator `KPP_KickerHeat_gen_v1_14_0.py` (card and cell: `KPP_KickerHeat_gen_v1_16_0.py`). Probes (read-only, keep) `KPP_KickerHeat_S1_probe_v1_0_0.py`, `KPP_KickerHeat_S2_probe_v1_0_0.py`, `KPP_KickerHeat_S3_ShortTrips_probe_v1_0_0.py`. Superseded, do not import: every older version of these. Retire: NQ `Sortline/Kicker Trips Today`; tags `KickerHeat/Config/EnableRoles`, `SignalLoadPct`, `StopWindowMin`. Install into EMPTY views. Detail in Raw Logs 2026-09-26_A / _B, 2026-09-27_A, 2026-09-28_A and `KPP_KickerHeat_Design`. |
| Sorter Diagnostic reset + `_107` cycle count (2026-09-28_A) | Library `forensics_sortReset_code_v1_0_0.py` -> `forensics/sortReset`. View `SorterDiagnosticPopup_view_v2_3_0.json` (`Framework/Popups/SorterDiagnosticPopup`), generator `KPP_SorterDiagPopup_gen_v1_0_0.py`. PLC routines imported as new routines with the MainRoutine JSRs repointed (R12, R14): `Sorting_107_KickerForensics_v1_2_0.L5X`, `Sorting_102_KickerDiagnosticBits_v1_2_0.L5X` (+ `.st` source); new program tag `LSL_KickerDiagResetPulse`; the old `_107_KickerForensics` / `_102_KickerDiagnosticBits` stay as rollback until v1.2.1. Builder and proof `KPP_Sorting_ResetFix_gen_v1_0_0.py`. Read-only `KPP_SortDiag_ResetProbe_v1_0_0.py`, `KPP_Sorting_ResetFix_check_v1_0_0.py`. Sources `Sorting_Program.L5X` (28 Sep 12:52:26), `MainSCADA_Timberlands_2026-09-28_1148.zip`. Detail in Raw Log 2026-09-28_A and `KPP_KickerHeat_Design` section 9b. |
| Anomaly Watch first builds (2026-09-30_B) | Tags `KPP_AnomalyWatch_Install_v1_1_0.py` (applied 30 Sep), timer `AnomalyWatch` (5000 ms, dedicated). Still possibly in use: `AnomalyChippersPopup_view_v1_0_0.json`, `AnomalyWatchMethod_view_v1_1_1.json` - confirm against overview 1.21.0. Everything else of 1.0.0-1.1.1 is superseded by 2026-10-03_A (section 4). Spec `KPP_AnomalyWatch_CHP_GRAOF_Spec_v1_0_0.md`. Detail in Raw Log 2026-09-30_B. |
| Chipper knife clock + motor vibration (2026-09-30_A) | DB `CM_knife_schema_ADD_v1_1_0.sql` + console `CM_knife_schema_ADD_console_v1_1_1.py` (applied), `CM_knife_schema_ADD_v1_2_0.sql` + console `_v1_2_0` (applied), `CM_vib_schema_v1_0_0.sql` + console (applied). Library `CM_load_rollup_v1_7_0.py` -> package `cm` script `cm_rollup` (timer unchanged). NQs `CM_NQ_KnifeDelta_v1_6_0.sql` (`CM/KnifeDelta`), `CM_NQ_VibState_v1_1_0.sql` (`CM/VibState`, param `machine` String). Views `CMKnifeCard_View_v1_8_0.json`, `CMKnifeMethod_View_v1_6_0.json`, `CMSawBladeMethod_View_v1_1_0.json`, `CMVibrationCard_View_v2_5_1.json`, `CMVibrationMethod_View_v1_3_0.json`, `SafetyPlantOverview_View_v1_16_2.json`. Tags `CM_tags_v1_1_0.json` (the whole `CM` folder; import at the provider root, collision Ignore). Console `CM_vib_baseline_set_v1_0_0.py` (four baselines taken), `CM_knife_fix_incident_20260928_v1_0_0.py` (applied). Probes (read-only) `CM_S5_setcheck_v1_2_0.py`, `CM_S6_chipsource_probe_v1_0_0.py`, `CM_S7_threshold_sweep_v1_1_0.py`, `CM_S8_vib_probe_v1_0_0.py`, `CM_S9_vib_week1_v1_0_0.py`, `CM_S10_incident_probe_v1_0_0.py`. Spec `KPP_AnomalyWatch_CHP_GRAOF_Spec_v1_0_0.md`. Design of record `KPP_CM_Design`. |
| PE Watch + Anomaly Watch (2026-10-03_A) | PLC `_113_PEWatch_SDB_v1_1_0.L5X`, `_025_PEWatch_GRA_v1_0_0.L5X`, `_252_PEWatch_COS_v1_0_0.L5X`, `_025_PEWatch_SRT_v1_0_0.L5X`; encoder routines `COS_Area__250_EncoderDiagnosticBits_v3_3_0.L5X`, `Grading_Area__023_EncoderDiagnosticBits_v3_6_0.L5X`, `Sorting__023_EncoderDiagnosticBits_v1_1_0.L5X`. Libraries `KPP_PEWatch_engine_v1_1_0.py` (`forensics/peWatch`), `KPP_PEWatch_registry_lib_v1_4_0.py` (`forensics/peWatchReg`), `KPP_PEWatch_view_lib_v1_2_0.py` (`forensics/peWatchView`), `forensics_peWatchJudge_code_v1_1_0.py`, `forensics_anomalyWatch_code_v1_11_0.py`, `forensics_anomalyAsk_code_v1_2_0.py`, `forensics_plantDiag_code_v1_3_0.py`. DB `KPP_PEWatch_schema_apply_v1_0_0.py`, `KPP_PEWatch_cleaned_schema_apply_v1_0_0.py`, `KPP_AnomalyWatch_history_schema_apply_v1_1_0.py`, `KPP_PEWatch_baseline_set_v1_0_0.py` (set written 3 Oct 11:20:44), `KPP_CM_GRAOF_fix_v1_1_0.py` (applied). Views `PEWatchPopup_view_v1_0_0.json`, `AnomalyAreaCard_view_v1_3_0.json`, `AnomalyEventFeed_view_v1_5_0.json`, `AnomalyHistoryPopup_view_v1_1_0.json`, `AnomalyAskPopup_view_v1_2_0.json`, `SafetyPlantOverview_view_v1_21_0.json`, `PlantEncoderDiagnosticPopup_view_v2_11_0.json`, `AreaDiagnosticsCard_view_v1_3_0.json`, `AreaSafetyCard_view_v1_3_0.json`, `Engineeringsubmenu_view_v1_2_0.json`. Read-only tools P1 / P2 / S0 / S1 / S2, `KPP_PEWatch_L1_learnings_v1_0_0.py`, `KPP_PEWatch_S3_baseline_preview_v1_2_0.py`, `KPP_PEWatch_drill_v1_0_0.py`, `KPP_CM_GRAOF_probe_v1_0_0.py`, `KPP_SDB_barkon_check_v1_0_0.py`, daily check `KPP_PEWatch_Morning_Check_v1_0_0.py`. Full register with superseded versions: Raw Log 2026-10-03_A section 7. |
| PE Watch next-chat starter (2026-10-03_A) | `KPP_PEWatch_NextChat_Starter_v1_0_0.md` - **read first when starting a PE Watch chat**: what is live, the every-morning routine with `KPP_PEWatch_Morning_Check`, the files to upload, next steps (link scoring, proof test, retirement), the build rules and facts not to re-learn. |
| T&B sweep cancel line + Bin 0 forensics (the T&B 2026-10-03_A) | Registered late (v1.36.0). PLC `_115_TnBSweepControl_v1_1_0`, `_081_Bin0Forensics_v1_0_0` (COS_Outfeed); `forensics.bin0Capture` 1.0.0 with the timer `Bin0Forensics_FixedDelay`; `kppstems.bin0_forensics` / `bin0_reason`; NQs `Production/COS/Bin0Pieces`, `Production/COS/Bin0ByWho`; popups `Bin0Forensics`, `TnBSweepSP`; the TNB Map Bin 0 panel; lock tool `KPP_TnbSweep_Lock_v1_0_0.py`. Files and versions: that raw log and `KPP_TnB_Bin0_Design` sections 3-10. |
| COS Watch + COS log stop positioning (2026-10-07_A) | PLC (COS_Area, routine L5X built from the program export, imported online): `COS_Area__260_COSWatch_v1_1_0.L5X` + `_260_COSWatch_v1_1_0.st` (last MainRoutine rung; `_v1_0_0` stays in the controller as rollback), `COS_Area__101_COS_PEFirstEdge_v1_0_0.L5X` + `_101_COS_PEFirstEdge_v1_0_0.st`, `COS_Area__100_COS_ConveyorControl_v1_1_0.L5X` + `_100_COS_ConveyorControl_v1_1_0_changes.txt` (MainRoutine R5 repointed; the old `_100_COS_ConveyorControl` stays as rollback). DB `KPP_COSWatch_Schema_apply_v1_0_0.py`, `KPP_COSWatch_Schema_ADD_v1_1_0.py` (applied). Libraries `forensics_cosWatch_code_v1_1_0.py` -> `forensics/cosWatch` (timer `COSWatch_FixedDelay` 5000 ms, dedicated), `shared_purge_code_v1_1_0.py` -> `shared/purge` (scheduled event "Retention Purge" `30 3 * * *`; install not confirmed). Views `COSWatch_view_v1_1_0.json` (`Application/COS/COSWatch`, page `/coswatch`), `EngineeringMenu_view_v1_3_0.json` (`Application/Safety/EngineeringMenu`), `SafetyPlantOverview_view_v1_22_0.json`, `PE_Round_view_v1_1_0.json`, `PE_Array_New_view_v1_1_0.json`, `COS_Map_view_AnyEye_v1_0_0.json` (the last four not confirmed). Probes (read-only) `KPP_COSWatch_P1_StopCut_probe_v1_0_0.py`, `KPP_COSWatch_P2_Lag_probe_v1_0_0.py`, `KPP_COS_P3_TwoEncoder_probe_v1_0_0.py`, `KPP_COSWatch_P4_AfterChange_probe_v1_0_1.py`, `KPP_COS_P5_ButtApproach_probe_v1_0_0.py`. Live settings changed: `LogStopPEOffset` 1670, `COS_ConvPEOffset` -1450. Detail in Raw Log 2026-10-07_A section 7. |
| PE Watch link scoring, the sun, knives and the motor work log (2026-10-09_A) | Libraries `forensics_peWatchJudge_code_v1_3_0.py` (`forensics/peWatchJudge`), `KPP_PEWatch_registry_lib_v1_5_0.py` (`forensics/peWatchReg`), `KPP_PEWatch_view_lib_v1_3_0.py` (`forensics/peWatchView`), `forensics_anomalyWatch_code_v1_12_2.py`, `forensics_anomalyAsk_code_v1_3_0.py`, `CM_knife_auto_v1_4_0.py` (`cm/knife_auto`), `CM_maint_v1_0_0.py` (`cm/maint`). NQs (raw SQL) `KPP_NQ_CM_KnifeDelta_v1_7_0.sql` (`CM/KnifeDelta`), `KPP_NQ_CM_VibState_v1_2_0.sql` (`CM/VibState`). Views `TimeRangeSelectorMini_view_v1_3_0.json`, `CMKnifeCard_view_v1_9_1.json`, `CMChippers_view_v1_6_2.json`, `CMVibrationCard_view_v2_6_0.json`, `CMWorkLog_view_v1_0_0.json` (`Application/Safety/Components/CMWorkLog`). DB `CM_maint_event_DDL_v1_0_0.py` (applied; the 1 Oct greasing seeded). Read-only `KPP_PEWatch_S4_link_replay_v1_1_0.py`, `CM_S9_grease_probe_v1_0_0.py`, `KPP_PEWatch_S5_baseline_check_v1_0_1.py`. Writer `KPP_PEWatch_baseline_set_v1_1_0.py` (DRY_RUN default, HOURS 168, KEEP; dry run next). Team summary: the Claude Doc "KPP Controls and SCADA - Changes and Improvements, 22 Sep to 6 Oct 2026". Detail in Raw Log 2026-10-09_A section 7. |
| Sweep auto tiles + Debarker stem diameter card (2026-10-10_A) | Probes (read-only) `KPP_TnB_SweepAuto_Probe_v1_0_0.py`, `KPP_SweepAuto_Probe_v1_0_0.py`. Tags `KPP_TnB_SweepAuto_Tag_v1_0_0.py` (run 07:41 -> `[TL-KPPWS01-01]KPP/COS/OF/Data/TnBSweep/SweepInAuto`), `KPP_GRA_SweepAuto_Tag_v1_0_0.py` (run 08:25 -> `KPP/Grader/Data/Sweep/SweepInAuto`; its PASS line names GRA Map 1.1.0 - import 1.1.1). Views `SweepAutoTile_view_v1_0_1.json` (new view `Application/TNB/Components/SweepAutoTile`), `TNBMap_view_v1_2_9.json`, `SDBMap_view_v1_3_0.json`, `GRAMap_view_v1_1_1.json`, `DebarkerOverview_view_v1_3_1.json`. The Pulp deck and Debarker tiles read existing tags (`KPP/COS/OF/Data/PulpdeckSweep/SweepInAuto`, `KPP/StemDB/Data/Outfeed/Sweep/Auto`). Detail and install order in Raw Log 2026-10-10_A section 7. |
| COS stopless approach, COS Moves, Processing Analytics, COS Watch operator buttons, Grading seq deck reverse (2026-10-08_A) | PLC (COS_Area, import online, every tag on Use Existing): `COS_Area__102_COS_ButtApproach_v1_0_0.L5X` + `.st`, `COS_Area__100_COS_ConveyorControl_v1_2_0.L5X`, `COS_Area__110_LogStopConvControl_v1_1_0.L5X`, `COS_Area__055_COS_InfeedConveyor_v1_1_0.L5X` (switch `BA_Enable`, default 0; change list `KPP_COS_ButtApproach_Changes_v1_0_0.txt`; the old routines stay as rollback), `COS_Area__260_COSWatch_v1_2_0.L5X` + `.st` (flag 30 hand clamp), `COS_Area__261_COSMoves_v1_0_1.L5X` + `.st`. DB `KPP_COSMoves_Schema_apply_v1_0_0.py` (`kppstems.cos_moves`, `cos_move_codes`), `KPP_PA_COS_DB_apply_v0_1_1.py` (`kppstems.pa_cos_*`). Libraries `forensics_cosMoves_code_v1_0_2.py` (`forensics/cosMoves`, timer `COSMoves_FixedDelay` 2000 ms, dedicated), `analytics_processing_cos_code_v0_1_0.py` (`analytics/processing/cos`, timer `PA_COS_Build` 60000 ms, shared), `forensics_cosWatchOp_code_v1_0_0.py` (`forensics/cosWatchOp`), `shared_whatsnew_code_v1_4_0.py`. NQs (raw SQL) `KPP_NQ_Production_COS_LogStopPositioning_v1_2_0.sql`, `KPP_NQ_Analytics_Processing_COS_Report_v0_1_0.sql` / `_Stems_v0_1_0` / `_StemDetail_v0_1_0` (`Analytics/Processing/COS/*`). Views `COS_LogStopPositioning_view_v1_2_0.json`, `COS_LogStopPositioningHelp_view_v1_3_0.json`, `PA_Page_view_v0_1_1.json` (page `/Analytics/Processing`), `PA_COS_Overview_view_v0_1_0.json`, `PA_COS_Operators_view_v0_1_0.json`, `PA_COS_Stems_view_v0_1_1.json`, `PA_COS_Reference_view_v0_1_0.json`, `PA_KpiTile_view_v0_1_0.json`, `Hubsidemenu_view_v1_9_0.json`, `COSWatchOperator_view_v1_1_0.json` (page `/coswatch-op`), `TNBOverview_view_v1_2_1.json`, `GradingOverview_view_v1_4_0.json` (the last two into an empty view). Tags `KPP_GRA_SeqDeckRev_Tag_v1_0_1.py` (run 11 Oct, PASS -> `KPP/Grader/Data/SeqDeckRev`). Read-only `KPP_COS_P5_ButtApproach_probe_v1_1_0.py`, `KPP_COS_P6_ButtCW_query_v1_0_1.py`, `KPP_COS_P7_HandClamps_byOperator_v1_0_0.py`, `KPP_PA_P1_GainsAudit_v1_0_0.py`, `KPP_PA_P2_CutTiming_v1_0_0.py`. Doc: the Claude Doc "COS Stem Cycle Audit - 8-9 Oct 2026". No compiled owner yet for COS Moves or Processing Analytics. Detail and install notes in Raw Log 2026-10-08_A section 7. |
| `KPP_COS_StemCycle_Audit_2026-10-09` (1.0.0) | **Read when** comparing COS stem times or operators against the first baseline, or re-running P1. The COS stem cycle audit of 8-9 Oct over 1,865 stems: now 31.8 s a stem, untouched auto 27.5, the booth at its best 23.3 (the bridge as a table); per operator left in auto; why some operators are faster (the wood); where touching helps and hurts; next - making auto faster; caveats. Markdown copy of the Claude Doc (claude.ai/artifact/FoZCpzkcLYYrMLBGq7j5a3); Word copy `KPP_COS_StemCycle_Audit_2026-10-09_v1_0_0.docx`. Session record: Raw Log 2026-10-08_A. |
| Debarker outfeed sweep trigger (2026-10-12_A) | PLC (Outfeed, import online): `SDB_220_OutfeedSweep_v1_1_0.L5X` - routine `_220_OutfeedSweep_v1_1_0`, R4's trigger on the new program BOOL `UseSweepArray` (0 = Wall Control PE array with failover, as V20n; 1 = Sweep PE array at `SpeedCompSweepPos`), created by the import; then `_000_MainRoutine` R4 -> `JSR(_220_OutfeedSweep_v1_1_0,0)`, then `Program:Outfeed.UseSweepArray` = 1; rollback 0 or the JSR back to `_220_OutfeedSweep` (left in place). Install sheet `SDB_220_OutfeedSweep_Install_v1_1_0.txt` (fallback: create the BOOL and replace R4 in place - both rung texts). Source `KPP_COS_V20n.L5K` (12 Oct 10:38:40). Detail in Raw Log 2026-10-12_A. |
| Smoko and WallControlPEs in PE Watch / Anomaly Watch (2026-10-13_A) | Libraries `KPP_PEWatch_registry_lib_v1_6_0.py` (`forensics/peWatchReg`), `forensics_peWatchJudge_code_v1_4_2.py` (`forensics/peWatchJudge`), `forensics_anomalyWatch_code_v1_13_0.py` (`forensics/anomalyWatch`; install not confirmed); install in that order. Read-only `KPP_PEWatch_Morning_Check_v1_1_1.py` (the daily check from now on; in the project knowledge since 13 Oct), `KPP_AnomalyWatch_Smoko_probe_v1_0_1.py`. Detail in Raw Log 2026-10-13_A section 7. |
| MLY email report windows (2026-10-14_A) | Library `shared_mlyproduction_code_v0_3_1.py` -> `shared/mlyproduction` (replace all; installed 14 Oct). Read-only `KPP_MLY_MonthBoundary_Probe_v1_0_0.py` (Script Console; MONTHS / NQ / DAILY / LIBRARY / VERDICT - the LIBRARY section is the post-install gate). No NQ, view or event change. Detail in Raw Log 2026-10-14_A section 7. |
| Hub Workmate Pulse + shut-day kiosk (2026-10-14_B) | Library `workmate_hubpulse_v1_0_3.py` -> NEW `workmate/hubpulse` (replace all). Views `Hub_view_v1_16_1.json` (`OperationsHub/Operations Hub/Hub`), `HubPulse_FeedRow_view_v1_0_0.json` (NEW `Components/HubPulse/FeedRow`), `Hubheader_view_v1_5_0.json` (`OperationsHub/HubHeader/Hubheader`), `VisitorMenu_view_v2_9_0.json` (`Exchange/Visitor Sign In/Menu`). Read-only `KPP_Hub_Probe_v1_0_0.py` (shut check + `workmate.hubpulse.probe()`). No NQ, tag or event change. Detail in Raw Log 2026-10-14_B section 7. |
| Hub production figures on the report's meter (2026-10-14_C) | Read-only `KPP_HubLength_vs_Report_Probe_v1_0_0.py` (Script Console; TAGS / DEFS / METERS / SPLIT / HOURS / VERDICT; PD / SHIFT at the top). View `KPP_report_stems_by_shift_v1_2_0.sql` (the definition of record - Stems = primary pieces, `NULLIF` on `piece_size`; rollback to 1.1.0 at the foot; not a Named Query) applied by `KPP_report_stems_by_shift_apply_v1_2_0.py` (Script Console, DRY_RUN default; not yet applied - 1.1.0, Stems every piece, live since 14 Oct 08:52, is withdrawn). Tags `KPP_HubLengthVolume_Tags_v1_0_0.py` (Script Console, DRY_RUN default, undo printed; applied 14 Oct 09:10 -> `KPP/General/Data/Production/{CurrentShift,PreviousShift}/{Length,Volume}`). NQs (raw SQL) `KPP_NQ_Stems_Projections_StemLengthRate_v2_0_0.sql`, `KPP_NQ_Stems_Projections_StemVolumeRate_v2_0_0.sql` (paste over `Stems/Projections/Stem Length Rate` / `Stem Volume Rate`; install not confirmed). No view change. Detail in Raw Log 2026-10-14_C sections 7 and 11. |
| KPP Digital Twin - COS (2026-10-14_D) | Page `KPP_Twin_COS_v1_0_0.html` -> `C:\WorkmateData\Twin\` on TL-KPPWS01; `three_r128.min.js` (three.js r128, MIT) -> `C:\WorkmateData\Twin\lib\`. Import zip `KPP_Twin_import_v1_0_0.zip` (Designer, File > Import): Project Library `twin/live` (`twin_live_code_v1_0_0.py`) and `twin/web` (`twin_web_code_v1_0_0.py`) - package `twin` a plain folder; WebDev python resource `twin` (`WebDev_twin_doGet_v1_0_0.py`, GET only, no auth); view `Application/Twin/TwinCOS` (`TwinCOS_view_v1_0_0.json` - iframe and a 352-tag lease keeper). Then page `/twin` by hand. Smoke `/system/webdev/MainSCADA_Timberlands/twin/health`, Script Console `twin.live.check()`. Installed on Live 14 Oct evening. Then `KPP_Twin_MissingTags_v1_0_0.py` (Script Console, DRY_RUN default - the 34 tags no view had used; run 21:19, PASS); `twin_live_code_v1_1_0.py` (replace `twin/live` - position change times `ts`, cache 100 ms) and `KPP_Twin_COS_v1_1_0.html` (beside 1.0.0, the newest wins - motion per value), delivered 21:45, not yet confirmed. Design of record `KPP_DigitalTwin_COS_Design` 1.1.0 (install section 3, checks section 11); detail in Raw Log 2026-10-14_D sections 7 and 11. |
| Value Recovery section (2026-10-14_E) | Script Console `KPP_VR_DB_apply_v1_0_0.py` (DRY_RUN first; applied 14 Oct 15:41 - `kppstems.vr_stem`, `vr_state`, `gra_call`, `vr_build`, `vr_report`, `vr_stems`, `vr_stem_detail`, `vr_crew_label`, `vr_origin_label`; SQL of record `KPP_VR_DB_v1_0_0.sql`). Library `analytics_valuerecovery_code_v1_0_1.py` -> `analytics/valuerecovery` (1.0.0 installed 14 Oct and backfilled from 4 Sep; now 1.1.0 of 2026-10-20_A), timer `VR_Build` (60000 ms, fixed delay, dedicated). NQs `KPP_NQ_Analytics_ValueRecovery_Report_v1_0_0.sql`, `..._Stems_v1_0_0.sql`, `..._StemDetail_v1_0_0.sql` (`Analytics/ValueRecovery`). Views `VR_Page_view_v1_0_2.json`, `VR_Origin_view_v1_0_1.json`, `VR_Crews_view_v1_0_1.json`, `VR_Grading_view_v1_0_2.json`, `VR_COS_view_v1_0_1.json`, `VR_Stems_view_v1_0_3.json`, `VR_Explore_view_v1_0_1.json`, `VR_Reference_view_v1_0_0.json`, `VR_Tile_view_v1_0_0.json` (`Analytics/ValueRecovery/...`, into EMPTY views; the tips not yet told; the Page now 1.0.3 of 2026-10-20_A). `Hubsidemenu_view_v1_10_0.json`, `shared_whatsnew_code_v1_5_0.py` (installed), `Production_view_v2_14_0.json` (optional). PLC `Grading_Area__311_GradeCallWatch_v1_0_0.L5X` + `_311_GradeCallWatch_v1_0_0.st` + `KPP_GradeCallWatch_Install_v1_0_0.txt` (in 14 Oct, a new last rung 8 of Grading_Area MainRoutine); `forensics_gradeCalls_code_v1_0_0.py` -> `forensics/gradeCalls`, timer `GradeCalls_FixedDelay` (2000 ms, fixed delay, dedicated). Read-only `KPP_VR_P1_ValueRecovery_Probe_v1_0_0.py`, `KPP_VR_P2_Verify_v1_0_0.py`. Sheet `KPP_VR_Install_v1_0_0.txt`. Detail in Raw Log 2026-10-14_E. |
| KPP Line Tracker - sortline pilot (2026-10-15_A) | PLC (COS_CPU, offline, then download in the shut): new periodic task `Tracker` (10 ms, priority 14, watchdog 500 ms), then Import Program `KPP_Trk_Program_v1_0_0.L5X` into it (program Trk and 7 new data types, all Create; nothing on Overwrite); `Program:Trk.Trk_Enable` 0 after the download, 1 with the sortline running. Install sheet `KPP_Trk_Install_v1_0_0.txt` (before / add / download / switch on / roll back / settings). Read-only `KPP_Trk_Watch_Probe_v1_0_0.py` (Script Console; STATE / SORTLINE / STATIONS / PIECES / VERDICT) after 15-30 min of production. Read-only `KPP_COS_ReadRate_Probe_v1_0_0.py` (run 15 Oct, verdict C). Roll back: `Trk_Enable` 0, inhibit the task, delete it at the next download. Installed 15 Oct (K1, K7). Install sheet **`KPP_Trk_Install_v1_0_1.txt`** supersedes 1.0.0 (the scan time is elapsed time - judge the rise). Regrade pile: read-only `KPP_SortRegrade_Probe_v1_1_0.py` (supersedes 1.0.0, adds the weekly HISTORY since May). **Sort Register 1.0.0:** named query `KPP_NQ_Sortline_SortRegister_v1_0_0.sql` -> `Sortline/SortRegister` (Period String, Bin Int4, OnlyIssues Boolean), view `SortRegister_view_v1_0_0.json` -> `Application/Sortline/SortRegister`, page `/sort-register`, sheet `KPP_SortRegister_Install_v1_0_0.txt`. Detail in Raw Log 2026-10-15_A sections 8 and 12. |
| Machine Settings - the Echo settings rebuilt (2026-10-15_B) | Project Library package `engineering` (a plain folder): `engineering_settings_code_v1_0_6.py` -> `engineering/settings` (installed 15 Oct), `engineering_manualkick_code_v1_0_2.py` -> `engineering/manualkick` (Sparky and Big Balls; install not confirmed). Script Console: read-only `KPP_MachineSettings_Probe_v1_0_1.py` (VERDICT OK / CREATE / WAIT, DISCOVER with values); `KPP_MachineSettings_Install_v1_0_0.py` (DRY_RUN default; run 15 Oct - 108 tags, then the 2 pre-lower toggles, table `sortline.manual_kick_event`); `KPP_MachineSettings_RemoveTags_v1_0_0.py` (DRY_RUN default; run - the 33 cut speed / prox window tags and 16 folders gone); `KPP_SettingsWatch_Install_v1_0_0.py` (DRY_RUN default; run - `public.setpoint_watch`, CHECK the heartbeat). Views (a new view into an EMPTY view; a later version that adds no component pastes over): `MachineSettings_view_v1_0_4.json` (`Application/Engineering/Settings/MachineSettings`, page `/Engineering/Settings` with the `/Sortline/Overview` docks), `SettingCard_view_v1_0_1`, `SettingRow_view_v1_0_2`, `SettingGridRow_view_v1_0_0`, `SettingCell_view_v1_0_1`, `ScaleCalc_view_v1_0_2`, `AreaItem_view_v1_0_1` (`.../Settings/Components/`), `SettingEditor_view_v1_0_1`, `ManualKick_view_v1_0_1` (`.../Settings/Popups/`); `EngineeringMenu_view_v1_4_0.json` (`Application/Safety/EngineeringMenu`). The glow views (SettingRow 1.0.2, SettingCell 1.0.1, ScaleCalc 1.0.2, AreaItem 1.0.1, MachineSettings 1.0.3 / 1.0.4) not yet confirmed. Gateway timers, dedicated: `ManualKick_Watchdog` 3000 ms -> `engineering.manualkick.watchdog()`; `Settings_Watch` 10000 ms -> `engineering.settings.watch()` (running 15 Oct 15:24). Design of record `KPP_MachineSettings_Design` 1.1.0 (install section 10, checks section 11); detail in Raw Log 2026-10-15_B sections 8 and 12. |
| LEAK WATCH and the Shut Plan stand-down (2026-10-15_C) | `forensics_peWatchJudge_code_v1_5_0.py` -> `forensics/peWatchJudge` and `forensics_anomalyWatch_code_v1_14_0.py` -> `forensics/anomalyWatch` (installed 15 Oct; Anomaly Watch now 1.15.0 of 2026-10-17_A); `KPP_HydLeak_schema_apply_v1_0_0.py` (Script Console, DRY_RUN default; applied 15 Oct 14:44 - `hydraulics.tank_window`, `hydraulics.tank_state`); `forensics_hydLeak_code_v1_0_3.py` -> `forensics/hydLeak` (new script; installed - `check()`, `backfill(14)`, `replay(14)`); `forensics_anomalyAsk_code_v1_4_1.py` -> `forensics/anomalyAsk` (not confirmed); view `HydraulicsDiagnosticsCard_view_v1_5_1.json` (installed; now 1.7.0); read-only `KPP_HydLeak_export_v1_0_1.py`; sheets `KPP_HydLeak_Shut_Install_v1_0_0.txt`, `KPP_HydLeak_Card_Install_v1_0_0.txt`. Design of record `KPP_HydLeak_Design` 1.0.0 (install section 15); detail in Raw Log 2026-10-15_C sections 2-6 and 11. |
| Sortline Overview, conveyor 1 calibration, comms clean-up (2026-10-15_A section 13) | View `SortlineOverview_view_v1_2_0.json` (`Application/Sortline/Overview`, root `SortlineOverview_v1_2_0`; into an EMPTY view; installed 15 Oct 13:53) - the Setpoints chip and the Sort Register button. Read-only Script Console: `KPP_Conv1_Calibrate_v1_0_0.py` (run 15 Oct 19:59 - conveyor 1 0.3034 mm a count; its VERDICT line is wrong, M10), `KPP_Comms_Survey_v1_1_0.py` (GROUPS / FAST / DEFAULT / LEFTOVER / DIRECT / VERDICT - run before and after any comms change; 16 Oct 06:50 OK, 57 ms). Writer `KPP_Comms_DiagGroup_v1_0_0.py` (MOVE / CHECK / UNDO, DRY_RUN default; run 16 Oct 06:23 - 3,492 tags to `Diagnostics_5s`). Gateway changes (no file): the tag groups and the device settings as left, and the undo, in Raw Log 2026-10-15_A section 13.3. |
| Regrade marks and Sortline Map 1.2.x (2026-10-16_A section 2) | Project Library `forensics_sortMarks_code_v1_0_0.py` -> `forensics/sortMarks` with the 20 String memory tags `KPP/SortLine/Data/RegradeMarks/Conv1_0 .. Conv2_9` and gateway timer `Sortline_RegradeMarks` (1000 ms, dedicated, `forensics.sortMarks.tick()`) - installed 16 Oct 08:18 (`KPP_RegradeMarks_Install_v1_0_0.txt`). `KPP_RegradeMarks_Install_v1_1_0.txt`: views `SortlineMap_view_v1_2_1.json` (`Application/Sortline/Sortline Map`), `SortlineBin_view_v1_1_0.json` (`Components/Objects/Symbols/SortlineBin`), named query `Sortline/BinMarks` (`KPP_NQ_Sortline_BinMarks_v1_0_0.sql`, KPP_production, cached 5 s), `KPP_Stylesheet_BinGlow_v1_0_0.css` (Advanced Stylesheet) - install not confirmed. `SortlineMap_view_v1_2_2.json`, `SortlineKickerOverlay_view_v1_4_0.json`, `Productionsidemenu_view_v1_6_0.json` (the hover fix, the Twin item; 16 Oct 13:46). Each into an EMPTY view. |
| Twin saved forecasts (2026-10-16_A section 3) | `KPP_Twin_Forecast_DDL_v1_0_0.py` (Script Console, DRY_RUN first - table `public.twin_forecast` on KPP_production), Project Library `twin_web_code_v1_1_0.py` -> `twin/web`, WebDev resource `twin` doPost `WebDev_twin_doPost_v1_0_0.py` (no auth, as doGet), page `KPP_Twin_COS_v1_2_0.html` -> `C:\WorkmateData\Twin\`. Design `KPP_DigitalTwin_COS_Design` 1.2.0. Delivered 16 Oct 14:56 - not yet confirmed. |
| KPP Line Tracker 1.1.0 - 1.1.2 (2026-10-16_A section 4) | PLC (COS_CPU, online, line running): Add > Import Routine into program Trk, then the JSR lines in `_000_Main`, Finalize, `Trk_Enable` 0 then 1. 1.1.0: `KPP_Trk_200_SrtInputs_v1_1_0.L5X`, `KPP_Trk_210_SrtLogic_v1_1_0.L5X`, `KPP_Trk_800_Compare_v1_1_0.L5X` (`KPP_Trk_Install_v1_1_0.txt`); 1.1.1: `KPP_Trk_210_SrtLogic_v1_1_1.L5X` (`_v1_1_1.txt`); 1.1.2: `KPP_Trk_210_SrtLogic_v1_1_2.L5X` (`_v1_1_2.txt`) - all installed, 1.1.2 running since 17 Oct about 07:30. Read-only probes `KPP_Trk_Watch_Probe_v1_1_0.py` - `v1_3_2.py` (superseded by 1.6.0). |
| Sortline Map Tracker mode (2026-10-16_A section 5) | `SortlineMap_view_v1_3_2.json` (`Application/Sortline/Sortline Map`, into an EMPTY view; `KPP_SortlineMap_Install_v1_3_2.txt`) - opens on Tracker, reads the tracker's export slots in its own binding (one OPC read a second while it shows Tracker). 1.3.1 installed 17 Oct; 1.3.2 not yet confirmed. `KPP_SmapTrk_Tags_v1_0_0.py` and tag group `TrkMap` (1.3.0) are not used - removed per the 1.3.1 sheet. |
| KPP Line Tracker 1.2.0 (2026-10-16_A section 7) | PLC (COS_CPU, online, line running) - `KPP_Trk_Install_v1_2_0.txt`: Add > Import Routine into program Trk in this order: `KPP_Trk_220_SrtCreate_v1_2_0.L5X`, `KPP_Trk_230_SrtIdentity_v1_2_0.L5X`, `KPP_Trk_200_SrtInputs_v1_2_0.L5X`, `KPP_Trk_210_SrtLogic_v1_2_0.L5X`, `KPP_Trk_800_Compare_v1_2_0.L5X`, `KPP_Trk_010_Init_v1_2_0.L5X` (151 new tags Create, a tag made by an earlier file Use Existing, nothing Overwrite); `Trk_Enable` 0, five lines in `_000_Main` (`Trk_Ver` 10200 and four JSRs), Finalize, `Trk_Enable` 1. Read-only `KPP_Trk_Watch_Probe_v1_6_0.py` (MODE RING after 30 min; WATCH with `Srt_CosMem` 0, then 1). Read-only `KPP_Trk_Watch_Probe_v1_4_0.py` / `v1_5_0.py` (the WATCH and DATA runs of 17 and 18 Oct). Sequence model `KPP_Trk_IdModel_v1_1_0.py` (work tool, in the project knowledge). Roll back: `Srt_IdOn` 0, or the five lines back. Installed 19 Oct before 06:09 with `KPP_Trk_230_SrtIdentity_v1_2_1.L5X` in place of the 1.2.0 file (refused, Error 12740-0) and `KPP_Trk_Install_v1_2_1.txt`; `Srt_CosMem` 1 since about 07:45 (Raw Log 2026-10-19_B). |
| Identity advisor phase 0 (2026-10-16_A section 13) | Script Console, read only: `KPP_TrkAdv_Geometry_Probe_v1_0_0.py` (database `KPP_production`, `kppstems.sorter_logs`, the last 72 h - `HOURS` / `SINCE` / `UNTIL` at the top): the spread of scan minus plan for length, SED, LED and volume; of the neighbour pairs whose lengths fit each other, how many the diameters and volume tell apart (VERDICT). Design `KPP_TrkAdvisor_Design` 1.0.2. Run 19 Oct 06:00 - GO (`KPP_TrkAdvisor_Design` 1.1.0 section 10). |
| COS regrade value (2026-10-16_A section 14) | Script Console, read only: `KPP_COS_Regrade_Probe_v1_0_0.py` (database `KPP_production`, `kppstems.sorter_logs` and `kppstems.stems`, the last 14 production days - `DAYS`, `VALUE_DIFF_NZD_M3`, `PRUNE_ZONE_M` at the top): COS regrades a day, their length, place in the stem, size and grades, who was on the COS and who graded, the value per grade, the money a day. Design `KPP_COS_RegradeView_Design` 1.0.0. Run 19 Oct 06:00 (Raw Log 2026-10-19_B section 3). |
| Sortline scanner replacement (2026-10-16_A section 14) | To order: Banner A-GAGE EZ-ARRAY 1200 mm - emitter `EA5E1200Q`, receiver `EA5R1200PIXMODQ` (PNP, 2 x 4-20 mA, Modbus), 2 x `MAQDC-815` (5 m) or `MAQDC-830` (10 m), `EZA-USB485-01` (set-up). Set-up and checks in `KPP_TrkAdvisor_Design` 9. Not yet ordered. |
| Weekly report Stem vs Forecast fix (2026-10-19_A) | Library `shared_weeklyreport_code_v0_8_2.py` -> `shared/weeklyreport` (replace all, save; 0.8.1 stays as the roll-back until 0.8.2 is confirmed). Check: EmailReports > KPP Weekly > the week of 12 Oct reads "67,819 m3 vs forecast to date 59,258 m3 (month 102,056 m3) - ahead by 8,561 m3, 114%", as the daily of 18 Oct; then Email (Test). No NQ, view, tag or event change. Not yet installed. Detail in Raw Log 2026-10-19_A. |
| KPP Line Tracker 1.2.1 and probe 1.6.1 (2026-10-19_B) | PLC: `KPP_Trk_230_SrtIdentity_v1_2_1.L5X` in place of 1.2.0's 230 (`Y_N` -> `Y_NC`, `Y_Q` -> `Y_P2`; nothing else) with `KPP_Trk_Install_v1_2_1.txt` - installed 19 Oct. Read-only `KPP_Trk_Watch_Probe_v1_6_1.py` (Script Console; the landing PE dropout judged on the tracker's own gap and what followed). Detail in Raw Log 2026-10-19_B sections 2 and 8. |
| Identity advisor phase 1 - shadow (2026-10-19_B, 2026-10-20_B) | `KPP_TrkAdvisor_Install_v1_0_1.txt` (U1 - U2 the update from 1.0.0: paste `trk_advisor_code_v1_0_1.py` over `trk/advisor`, save, `trk.advisor.status()`): Script Console `KPP_TrkAdvisor_Schema_apply_v1_0_0.py` (DRY_RUN first - `kppstems.trk_advice`, 54 columns, and `kppstems.trk_advice_state`); Project Library package `trk` (a plain folder), script `advisor`; `trk.advisor.test_read()`; gateway timer `TrkAdvisor_FixedDelay` (Fixed Delay 1000 ms, dedicated, `trk.advisor.tick()`); `trk.advisor.status()`; after an hour the read-only `KPP_TrkAdvisor_Report_v1_0_0.py`. Writes nothing to the PLC; roll back - disable the timer. Installed 19 Oct about 10:15 with 1.0.0 (the schema PASS, the timer running); 1.0.1 installed about 10:50 (the first hour: design 11.10); 1.0.2 (`trk_advisor_code_v1_0_2.py`, `KPP_TrkAdvisor_Install_v1_0_2.txt` U1 - U2 - the state kept across project saves) installed 19 Oct about 21:00 - one run since. **1.0.3** (`trk_advisor_code_v1_0_3.py`, `KPP_TrkAdvisor_Install_v1_0_3.txt` U1 - U2 - old open cuts, SED a share, LED by taper) delivered 20 Oct about 11:15, not yet installed; roll back - paste 1.0.2. The day check, read only: `KPP_TrkAdvisor_Report_v1_1_0.py` (24 h as shipped), `KPP_TrkAdvisor_DataCut_v1_0_0.py`. Design `KPP_TrkAdvisor_Design` 1.1.4 section 11. |
| COS encoder rate ceiling (2026-10-17_A) | Read-only `KPP_COS_EncoderCeiling_Probe_v1_0_0.py` (run 17 Oct). Library `forensics_plantDiag_code_v1_4_0.py` -> `forensics/plantDiag` (installed). PLC `COS_Area__250_EncoderDiagnosticBits_v3_4_0.L5X` + `_250_EncoderDiagnosticBits_v3_4_0.st`, sheet `KPP_COS_EncoderDiag_Install_v3_4_0.txt` (online import, JSR repoint; v3.3.0 stays as the roll-back; not confirmed). View `SafetyPlantOverview_view_v1_23_0.json` (1.22.1 installed 18 Oct). Detail in Raw Log 2026-10-17_A section 2. |
| PUMP WATCH (2026-10-17_A) | Library `forensics_hydPump_code_v1_0_4.py` -> `forensics/hydPump` (1.0.3 the roll-back), `KPP_HydPump_schema_apply_v1_0_0.py` (applied 18 Oct), `forensics_anomalyWatch_code_v1_15_0.py` -> `forensics/anomalyWatch`, views `HydraulicsDiagnosticsCard_view_v1_7_0.json` and `HydPumpWatchDetail_view_v1_0_0.json` (new), sheet `KPP_HydPump_Install_v1_0_1.txt`, read-only `KPP_HydPump_Verify_v1_0_0.py`. Pumps: read-only `KPP_HydMotor_Bindings_Probe_v1_0_0.py`, `KPP_HydPump_BigJohn_Probe_v1_0_0.py`; `forensics_hyddiag_code_v1_4_0.py` -> `forensics/hyddiag` (not confirmed); `KPP_HydPump_BigJohn_Tags_v1_0_0.py` (run 19 Oct - to repoint to `Pumps[0].PV8000`). Design `KPP_HydPumpWatch_Design` 1.1.0. Detail in Raw Log 2026-10-17_A sections 3-7 and 12. |
| CM vibration baselines (2026-10-17_A) | `CM_vib_baseline_set_v1_1_0.py` (Script Console, DRY_RUN default, REPRO first; the GRAOF row written 19 Oct 17:47:16). Design `KPP_CM_Design` 1.1.0. Detail in Raw Log 2026-10-17_A section 8. |
| Value $ in dollars - the Financials tab (2026-10-20_A) | Script Console `KPP_VR_Money_DB_apply_v1_0_0.py` (DRY_RUN default; applied - `kppstems.vr_money_set`, `vr_money_stem`, `vr_money_build`, `vr_money_report`, butt cuts priced from 4 Sep); NQ `Analytics/ValueRecovery/Money` 1.0.0; `analytics.valuerecovery` 1.1.0 (the money build in every VR_Build tick; `pa_tick` for the PA_COS_Build timer); Page 1.0.3; Financials view 1.0.5 (delivered 20 Oct 05:49, install not told). Read-only `KPP_VR_Money_check_v1_0_0.py`, `KPP_VR_Money_Probe_v1_0_1.py`, `KPP_PA_find_v1_0_0.py`. Doc "KPP Butt Defects - Opportunities" (Claude Docs). Detail in Raw Log 2026-10-20_A. |
| Capex documents - Debarker chainsaw, Hogger MCC, AI Grader Phase Two (2026-10-06_A) | `Capex_-_KPP_Debarker_Infeed_Chainsaw_V1.6.docx` (V1.0 - V1.5 superseded) with `KPP_ChainsawDT_Capex_Chart_v1_0_0.png` (V1.0), `KPP_ChainsawDT_Capex_Fig1_v1_1_0.png`, `KPP_BentStem_Capex_Fig2_v1_0_0.png`, `KPP_ChainsawDT_Capex_Fig3_v1_0_0.png`, `KPP_ChainsawDT_Capex_Fig4_v1_0_0.png`, `KPP_ChainsawDT_Capex_Insert_v1_1_0.docx`; read-only Script Console `KPP_ChainsawDT_Audit_v1_0_0.py` -> `KPP_ChainsawDT_Capex_Audit_v1_0_0.xlsx`; read-only `KPP_BentStem_Probe_v1_0_0.py` -> `KPP_BentStem_Capex_Events_v1_0_0.csv`; `Capex_-_KPP_Hogger_MCC_Replacement_V1.0.docx` with `KPP_HoggerMCC_Capex_Fig1_v1_0_0.png`; `Capex_-_KPP_AI_Grader_Phase_Two_V1.0.docx` with `KPP_AIGrading_Capex_Fig1_v1_0_0.png` and `KPP_AIGrading_Capex_Fig2_v1_0_0.png`. Detail in Raw Log 2026-10-06_A. |
| Debarker low air - ring flash and grading booth tile (2026-10-21_A) | Stylesheet snippet `KPP_Stylesheet_RingLowAir_v1_0_0.css` (append to the Advanced Stylesheet with a ledger line). Views `SDBMap_view_v1_4_0.json` (`Application/Debarker/SDB Map`), `LowAirTile_view_v1_0_0.json` (NEW view `Application/Debarker/Components/LowAirTile`), `GradingOverview_view_v1_5_0.json` (`Application/Grading/Overview`) - all from the 21 Oct 08:38 export. Install order: the snippet, SDB Map, the tile, Grading Overview. Detail in Raw Log 2026-10-21_A section 10. |
| COS NEW auto 1.0.1 and the STD vs NEW comparison (2026-10-12_B) | PLC (COS_Area, online import in this order, every existing tag Use Existing): `_103_COS_NewAuto_v1_0_1.L5X`, `_100_COS_ConveyorControl_v1_3_1.L5X`, `_149_SawAutoClampControl_v1_1_0.L5X`, `_110_LogStopConvControl_v1_2_1.L5X`, `_055_COS_InfeedConveyor_v1_2_1.L5X`, `_260_COSWatch_v1_3_1.L5X`, `_261_COSMoves_v1_1_1.L5X`; sheet `KPP_COS_NewAuto_Install_v1_0_1.txt` (step 5 the JSR swaps behind `Adriaan[9].9`, one online edit; rollback STD twice or the swaps back). Script Console `KPP_COS_NewAuto_Tags_v1_0_1.py` (`KPP/COS/NewAuto`, 28 tags), `KPP_COSMoves_Codes_ADD_v1_0_0.py`. Views `KPP_COS_NewAuto_AutoModeChip_view_v1_0_1.json`, `KPP_COS_NewAuto_NewAutoSettings_view_v1_0_1.json` (new, `Application/COS/NewAuto/*`), `KPP_COS_LogStopPositioning_view_v1_3_1.json`. All installed 13 Oct; NEW live from 13:08:14. PA `KPP_PA_COS_DB_apply_v0_1_2.py` (DRY_RUN default; applied 13 Oct), `PA_COS_Modes_view_v0_1_0.json` (new, `Analytics/Processing/COS/Modes`), `PA_Page_view_v0_1_2.json` (import not confirmed). Read-only `KPP_PA_P2_CutTiming_v1_0_1.py`, `KPP_COS_NewAuto_PreFlight_v1_0_0.py`, `KPP_COS_NewAuto_LiveCheck_v1_0_1.py`. No design owner yet. Detail in Raw Log 2026-10-12_B sections 3 and 7. |
| Visitor Sign In change request, PLANT SHUT, Log Stop Positioning moved (2026-10-22_A) | Views `Hubheader_view_v1_6_1.json` (`OperationsHub/HubHeader/Hubheader`), `VisitorUserVerification_view_v1_1_3.json` (`Exchange/Visitor Sign In/User Verification`), `VisitorCard_view_v1_3_0.json` (`Exchange/Visitor Sign In/Component/Visitor Card`), `VisitorMenu_view_v2_10_0.json` (`Exchange/Visitor Sign In/Menu`), `COS_Map_view_v1_1_0.json` (`Application/COS/COS Map`, into an empty view), `MachineSettings_view_v1_0_5.json` (`Application/Engineering/Settings/MachineSettings`, into an empty view). Script Console `KPP_VisitorDB_InductedColumn_v1_0_0.py` (DRY_RUN default; run 22 Oct - `dbo.visit.inducted`). NQ `KPP_NQ_Exchange_VisitorSignIn_Visit_SetInducted_v1_0_0.sql` -> `Exchange/Visitor Sign In/Visit/Set Inducted` (created 22 Oct). Detail in Raw Log 2026-10-22_A. |
| Operator KPIs - knife record, KPIs, approval pack, Training Review, HR Final Report (2026-10-23_A) | Install sheet `KPP_OperatorKPI_Install_2026-10-23_v1_0_0.md` (order and NQ params). Knife record: `KPP_SDB_RingCapture_Setup_v1_0_0.py`, `sdb_ringcapture_v1_0_0.py` -> `sdb/ringcapture`, `sdb_profile_v1_1_0.py` -> `sdb/profile`, NQs `Report/SDB/KnifeCheck/*` (5), views `KnifeCheck_view_v1_0_0.json` (`Application/Debarker/KnifeCheck`, route `/Debarker/KnifeCheck`), `DebarkerStemPressure_view_v2_0_0.json`, `DebarkerDetail_view_v1_1_0.json`, probe `KPP_SDB_KnifeSignal_Probe_v1_0_0.py`, PLC `SDB_L08B_RingFlags_v1_0_0.L5X`. KPIs: NQs `Report/KPI/SDB/{Close Gaps Percent, Running Gap Average, Knife Joystick Percent, Bark Over 5pc Corrected}`, `Stem Gap Histogram` 2.0.0, `Report/KPI/Grading/{Knot Calls per 100 Stems, Defect Calls per 100 Stems, Defect Calls by Type}`, `operator_kpi_v1_3_0.py`, views `SDBCorrected_view_v1_0_0.json`, `GradingCalls_view_v1_0_0.json`, `OperatorKPI_view_v1_9_0.json`. Approval: `Operator_KPI_Scorecard_Design_v3_14_0.xlsx`, `KPP_KPI_Calibration_Probe_v2_0_0.py`. `KPP_PulpDeck_SawLog_Probe_v1_0_0.py`. `KPP_Bark_On_Stems_Explainer_v1_0_0.docx`. Training Review: `TrainingReview_DDL_Console_v1_2_0.py`, NQs `Report/Training/Review KPI Save` 1.0.0 and `Review Get` 1.2.0, `operator_trainingreview_v1_5_0.py`, `TrainingReview_view_v1_8_0.json`. HR: `KPP_HR_FinalReport_Setup_v1_0_0.py`, `hr_finalreport_v1_0_0.py` -> `hr/finalreport`, views `FinalReport_view_v1_0_0.json`, `FinalReportPrintable_view_v1_0_0.json`, `FinalReportPrinter_view_v1_0_0.json` (`OperationsHub/Business Systems/HR/`), `BusinessSideMenu_view_v1_7_0.json`, `BusinessHome_view_v2_6_0.json`, route `/business/hr`. None installed at the close. Detail in Raw Log 2026-10-23_A section 15. |
| Chat transcripts / session exports | Raw material for compile passes. |

## 4. Retired / remove from project knowledge

| Doc | Fate |
|---|---|
| `PROJECT_KNOWLEDGE_safety_forensics_ADD` | Merged into `KPP_Plant_Memory_Export` v1.1.0. Remove. |
| `KPP_Project_Knowledge_Index` (v1.2, v1.3) | Superseded by this unified index. Remove. |
| `KPP_Migration_Reference_v1_4` | Superseded by v1.5. Remove. |
| `KPP_Platform_Rules_v1_6` | Superseded by **v1.7** (the merge). Remove. |
| `KPP_Domain_Data_Reference_v1_5` | Superseded by **v1.6** (the merge). Remove. |
| `KPP_Reporting_Technical_Reference_v1_1_0` | Superseded by **v1.2.0** (the merge). Remove. |
| `DashboardandPLC_Knowledge_Index_v1_7_0` | Superseded by **v1.8.0**. Remove. |
| `KPP_Platform_Rules_v1_7` | Superseded by **v1.8**. Remove. |
| `KPP_Reporting_Technical_Reference_v1_2_0` | Superseded by **v1.3.0**. Remove. |
| `DashboardandPLC_Knowledge_Index_v1_8_0` | Superseded by **v1.9.0**. Remove. |
| `DashboardandPLC_Knowledge_Index_v1_9_0` | Superseded by **v1.9.1**. Remove. |
| `DashboardandPLC_Knowledge_Index_v1_9_1` | Superseded by **v1.9.3**. Remove. |
| `DashboardandPLC_Knowledge_Index_v1_9_2` | Superseded by **v1.9.3** (compile). Remove. |
| `KPP_Platform_Rules_v1_8` | Superseded by **v1.9**. Remove. |
| `KPP_Reporting_Technical_Reference_v1_3_0` | Superseded by **v1.4.0**. Remove. |
| `DashboardandPLC_Knowledge_Index_v1_9_7` | Superseded by **v1.9.8**. Remove. |
| `DashboardandPLC_Knowledge_Index_v1_9_8` | Superseded by **v1.9.9**. Remove. |
| `DashboardandPLC_Knowledge_Index_v1_9_9` | Superseded by **v1.9.10**. Remove. |
| `DashboardandPLC_Knowledge_Index_v1_9_10` | Superseded by **v1.10.0**. Remove. |
| `KPP_Domain_Data_Reference_v1_6` | Superseded by **v1.7** (TR fold removed). Remove. |
| `KPP_Platform_Rules_v1_9` | Superseded by **v1.10**. Remove. |
| `KPP_Reporting_Technical_Reference_v1_4_0` | Superseded by **v1.5.0**. Remove. |
| `DashboardandPLC_Raw_Log_2026-08-01_B_v1_0_0` | Superseded by **v1.0.1** (E2 correction). Remove. |
| `DashboardandPLC_Knowledge_Index_v1_11_0` | Superseded by **v1.12.0**. Remove. |
| `DashboardandPLC_Knowledge_Index_v1_12_0` | Superseded by **v1.13.0**. Remove. |
| `DashboardandPLC_Knowledge_Index_v1_13_0` | Superseded by **v1.14.0**. Remove. |
| `DashboardandPLC_Knowledge_Index_v1_14_0` | Superseded by **v1.15.0**. Remove. |
| `DashboardandPLC_Knowledge_Index_v1_15_0` / `v1_15_1` | Superseded by **v1.16.0**. Remove. |
| `DashboardandPLC_Knowledge_Index_v1_16_x` / `v1_17_0` / `v1_18_0` | Superseded by **v1.19.0**. Remove. |
| `DashboardandPLC_Knowledge_Index_v1_19_0` / `v1_20_0` | Superseded by **v1.21.0**. Remove. |
| `DashboardandPLC_Knowledge_Index_v1_21_0` / `v1_22_0` | Superseded by **v1.23.0**. Remove. |
| `DashboardandPLC_Knowledge_Index_v1_23_0` | Superseded by **v1.24.0**. Remove. |
| `DashboardandPLC_Knowledge_Index_v1_24_0` | Superseded by **v1.25.0**. Remove. |
| `DashboardandPLC_Knowledge_Index_v1_25_0` | Superseded by **v1.26.0**. Remove. |
| `DashboardandPLC_Knowledge_Index_v1_26_0` | Superseded by **v1.27.0**. Remove. |
| `DashboardandPLC_Knowledge_Index_v1_27_0` | Superseded by **v1.28.0**. Remove. |
| `DashboardandPLC_Knowledge_Index_v1_28_0` | Superseded by **v1.29.0** (compile). Remove. |
| `KPP_Platform_Rules_v1_13` | Superseded by **v1.14** (the merge). Remove. |
| `KPP_Platform_Rules_ADD_2026-09-24` | Merged into `KPP_Platform_Rules` 1.14. Remove. |
| `schedule_kpp_code_v1_1_0` / `schedule_mly_code_v1_1_0` | Superseded by **v1_2_0** - v1.1.0 read a `startup_time` column that does not exist. Remove. |
| `KPP_schedule_verify_v1_0_0` | Superseded by **v1_1_0** (version check + table cross-check + round trip). Remove. |
| `KPP_Platform_Rules_v1_11` | Superseded by **v1.12** (the merge). Remove. |
| `DashboardandPLC_Knowledge_Index_ADD_2026-09-18` | Merged into `KPP_Platform_Rules` v1.12. Remove. |
| `KPP_Platform_Rules_ADD_2026-09-22` | Merged into `KPP_Platform_Rules` v1.12. Remove. |
| `KPP_Platform_Rules_ADD_2026-09-22_B` / `KPP_Domain_Data_Reference_ADD_2026-09-22_B` | Merged into `KPP_Platform_Rules` 1.13 / `KPP_Domain_Data_Reference` 1.8. Remove. |
| `KPP_Platform_Rules_v1_12` | Superseded by **v1.13** (the merge). Remove. |
| `KPP_Domain_Data_Reference_v1_7` | Superseded by **v1.8** (the merge). Remove. |
| `KPP_Camera_LiveView_Setup_v1_0_0`-`v1_2_0` | Working notes, never loaded - superseded by `KPP_Camera_LiveView_Reference` v1.0.0. Do not add. |
| `KPP_VisitorSignIn_Audit_v1_0_0` / `v1_1_0` | Superseded by **v1.2.0** - v1.1.0 listed the live Config admin screen for deletion. Remove. |
| `StarLoaderPanel_View_v1_0_0`-`v1_5_4` | Superseded by **v1_5_5**. Remove - several carry the StatusBits.FltIn fault chip and the SET POS zeroing button. |
| `CMKnifeCard_View_v1_0_0`-`v1_5_0` | Superseded by **v1_5_1**. Remove. |
| `CMKnifeMethod_View_v1_0_0`-`v1_3_0` | Superseded by **v1_4_0** (24 h wording is wrong - the cycle is 12 h). Remove. |
| `SafetyPlantOverview_View_v1_14_0`-`v1_14_4` | Superseded by **v1_14_5**. Remove. |
| `CM_NQ_KnifeDelta_v1_0_0` / `v1_1_0` / `v1_2_0` | Superseded by **v1_3_0**. Remove. |
| `CM_knife_auto_v1_0_0` / `v1_1_0` | Superseded by **v1_2_0** - the 6 h evidence window logs a phantom 15:00 change on shut days. Do not install. |
| `CM_knife_undo_v1_0_0` / `v1_1_0` | Superseded by **v1_2_0** (ID list). Remove. |
| `CM_S2_setprofile_v1_0_0` / `CM_S3_throughput_probe_v1_0_0`-`v1_1_0` / `CM_S4_profile_recheck_v1_0_0` | Superseded - v1_0_0 spread metric was invalid (near-zero denominator) and the S4 pair join used timestamp equality. Remove. |
| `DashboardandPLC_Knowledge_Index_v1_29_0` | Superseded by **v1.30.0**. Remove. |
| `KPP_Platform_Rules_v1_14` | Superseded by **v1.15** (the compile). Remove. |
| `KPP_Working_Method_v1_1` | Superseded by **v1.2**. Remove. |
| `SDBMap_View_v1_1_0` | Superseded by **v1_2_0** - slides stems in from their saved positions when the view opens. Do not import. |
| `SDB_StemTrack_Fix_Edits_v1_2_0` / `v1_3_0` | Superseded by **v1_2_1** / **v1_3_1**. Remove. |
| `SDB_StemPosLength_Check_v1_0_0` | Superseded by **v1_1_0** (per stem, adds the curtain length). Remove. |
| `DashboardandPLC_Knowledge_Index_v1_30_0` | Superseded by **v1.31.0**. Remove. |
| `KPP_Platform_Rules_v1_15` | Superseded by **v1.16** (the compile). Remove. |
| `Workmate_Knowledge_Journal_v3_8` | Superseded by **v3.9**. Remove. |
| `KPP_Platform_Rules_ADD_2026-09-26`, `Workmate_Knowledge_Journal_ADD_2026-09-26`, `DashboardandPLC_Knowledge_Index_ADD_2026-09-26` | Merged into Platform Rules **v1.16**, Journal **v3.9** and this index **v1.31.0**. Remove. |
| `KPP_KickerHeat_Design_v1_0_0` / `v1_1_0` / `v1_2_0` | Superseded by **v1.3.0** (as built, with the kicker trend). Remove. |
| `DashboardandPLC_Knowledge_Index_v1_31_0` | Superseded by **v1.32.0**. Remove. |
| `KPP_Platform_Rules_v1_16` | Superseded by **v1.17**. Remove. |
| `KPP_KickerHeat_Design_v1_3_0` | Superseded by **v1.4.0**. Remove. |
| `DashboardandPLC_Knowledge_Index_v1_32_0` | Superseded by **v1.33.0**. Remove. |
| `CMKnifeCard_View_v1_5_1` / `v1_6_0` / `v1_7_0` | Superseded by **v1_8_0**. Two different files were issued as `v1_6_0` (the 03 Sep saw-session card and a 22 Sep issue that collided with it) - both superseded. Remove. |
| `CMKnifeMethod_View_v1_4_0` / `v1_5_0` / `v1_5_1` | Superseded by **v1_6_0** (v1_5_0 kept the v1_4_0 root name). Remove. |
| `CMSawBladeMethod_View_v1_0_0` | Superseded by **v1_1_0** (it states the old window-count clock). Remove. |
| `CM_NQ_KnifeDelta_v1_3_0` / `v1_4_0` / `v1_5_0` | Superseded by **v1_6_0** (verdict on current). `v1_4_0` was issued twice (03 Sep, 22 Sep) - import neither. Remove. |
| `CM_load_rollup_v1_1_0`-`v1_6_0` | Superseded by **v1_7_0**. A line change needs a re-backfill (`KPP_CM_Design` section 6). Remove. |
| `CMVibrationCard_View_v1_5_0` and `v2_0_0`-`v2_5_0` | Superseded by **v2_5_1** (v2_2_0 hard-coded `CM/Chipper`; before v2_5_1 the card never refreshed). Remove. |
| `CMVibrationMethod_View_v1_0_0`-`v1_2_0` | Superseded by **v1_3_0**. Remove. |
| `SafetyPlantOverview_View_v1_14_5` / `v1_15_x` / `v1_16_0` / `v1_16_1` | Superseded by **v1_16_2** (four motor cards, Grader folder and load state). Remove. |
| `CM_NQ_VibState_v1_0_0` | Superseded by **v1_1_0** (Disc 2 aRMS against Disc 1). Remove. |
| `CM_S5_setcheck_v1_0_0` / `v1_1_0`, `CM_S7_threshold_sweep_v1_0_0` | Superseded by S5 **v1_2_0** / S7 **v1_1_0** for re-runs; their results are in Raw Log 2026-09-30_A. Remove. |
| `CM_knife_schema_ADD_console_v1_1_0` | DRY_RUN twin of **v1_1_1** (the one applied). Remove. |
| `CM_instances_v2_0_0.json` | Superseded by **`CM_tags_v1_1_0.json`** (the whole `CM` folder, four instances) for re-import. The UDT file `CM_udt_VibMotor_v2_0_0.json` stays. Remove. |
| `DashboardandPLC_Knowledge_Index_v1_33_0` / `v1_34_0` | Superseded by **v1.34.1**. Remove. |
| `KPP_PEWatch_Design_v1_0_0` | Superseded by **v1_1_0** (as built; the 1.0.0 draft had layers 2-5 as design only). Remove. |
| `AreaSafetyCard_view_v1_2_0` | WITHDRAWN - its HOG "NO MONITOR" came from a stale tag CSV; use **v1_3_0**. Never import. |
| `KPP_EncoderDiag_PLC_Edits_v1_0_0` | Hand-edit sheet replaced by the three versioned encoder routines (COS 3.3.0, Grading 3.6.0, Sorting 1.1.0). Remove. |
| PE Watch / Anomaly Watch superseded files (2026-10-03_A) | Registry 1.0.0-1.3.0, engine 1.0.0, view lib 1.0.0 / 1.1.0, judge 1.0.0, Anomaly Watch 1.2.0-1.10.0, Ask 1.0.0 / 1.1.0, plantDiag 1.1.0 / 1.2.0, preview 1.0.0-1.1.0, GRAOF fix 1.0.0, history schema 1.0.0 and the superseded view versions - the list is Raw Log 2026-10-03_A section 7. Remove. |
| `DashboardandPLC_Knowledge_Index_v1_34_1` | Superseded by **v1.35.0**. Remove. |
| `KPP_KickerHeat_Design_v1_4_0` | Superseded by **v1.6.0** (the 28 Sep v1.5.0 never reached the project knowledge - do not upload it). Remove. |
| `KPP_Platform_Rules_v1_17` | Superseded by **v1.19** (the 28 Sep v1.18 never reached the project knowledge - do not upload it). Remove. |
| `KPP_Working_Method_v1_2` | Superseded by **v1.3** (the 28 Sep issue). Remove. |
| `KPP_Control_Text_Standard_v1_0_0` | Superseded by **v1.2.0** (the 28 Sep v1.1.0 never reached the project knowledge - do not upload it). Remove. |
| The 28 Sep `DashboardandPLC_Knowledge_Index_v1_33_0` (registration for 2026-09-28_A) | NEVER UPLOAD - the name 1.33.0 belongs to the 2026-09-30_A registration; v1.35.0 carries its content. |
| `forensics_kickerHeat_code_v1_4_0`, `KickerAnomaly_view_v1_4_0` / `v1_5_0`, `SortlineKickerHeatCell_view_v1_0_0` / `v1_1_0`, `KPP_KickerHeat_gen_v1_15_0` | Superseded by engine **v1_5_0**, card **v1_6_0**, cell **v1_2_0**, generator **v1_16_0** (2026-09-28_A). Do not import. |
| Anomaly Watch 1.0.0-1.1.1 (2026-09-30_B) | `forensics_anomalyWatch_code_v1_0_0` / `v1_1_0` / `v1_1_1`, `KPP_AnomalyWatch_Install_v1_0_0`, `AnomalyAreaCard_view_v1_0_0` / `v1_1_0` / `v1_1_1`, `AnomalyWatchMethod_view_v1_0_0` / `v1_1_0`, `SafetyPlantOverview_view_v1_17_0` / `v1_18_0` / `v1_18_1`, `KPP_AnomalyWatch_gen_v1_0_0`-`v1_1_2` - superseded by 2026-10-03_A (engine 1.11.0, card 1.3.0, overview 1.21.0). Do not import. |
| `DashboardandPLC_Knowledge_Index_v1_35_0` | Superseded by **v1.36.0**. Remove. |
| `KPP_Domain_Data_Reference_v1_8` | Superseded by **v1.9** - its section 10 printed the unmeasured offsets 1550 / -1500 and the slip and speed figures built on them. Remove. |
| `KPP_COSWatch_Design_v1_0_0` / `v1_1_0`, `KPP_COS_StopApproach_Spec_v0_1_0` / `v0_2_0` | Chat-only drafts of 2026-10-07_A (0.1.0 held the withdrawn test C1) - superseded by COS Watch Design **1.2.0** / StopApproach Spec **0.3.0**. Never upload. |
| COS Watch superseded files (2026-10-07_A) | `forensics_cosWatch_code_v1_0_0`, `COSWatch_view_v1_0_0`, `shared_purge_code_v1_0_0`, `KPP_COSWatch_P4_AfterChange_probe_v1_0_0` (ambiguous column), `COS_Area__260_COSWatch_v1_0_0.L5X` / `_260_COSWatch_v1_0_0.st` (the routine stays in the controller as rollback), `Engineeringsubmenu_view_v1_2_0` (2026-10-03_A), `SafetyPlantOverview_view_v1_21_0`. Do not import. |
| `DashboardandPLC_Knowledge_Index_v1_36_0` | Superseded by **v1.37.0**. Remove. |
| PE Watch / Anomaly Watch / CM superseded files (2026-10-09_A) | `forensics_peWatchJudge_code_v1_1_0` / `v1_2_0` / `v1_2_1` / `v1_2_2`, `KPP_PEWatch_registry_lib_v1_4_0`, `KPP_PEWatch_view_lib_v1_2_0`, `forensics_anomalyWatch_code_v1_11_0` / `v1_12_0` / `v1_12_1`, `forensics_anomalyAsk_code_v1_2_0`, `KPP_PEWatch_S4_link_replay_v1_0_0`, `KPP_PEWatch_S5_baseline_check_v1_0_0` (the Debarker outfeed pair and one-eye still windows), `CM_knife_auto_v1_2_0` / `v1_3_0`, `CM_NQ_KnifeDelta_v1_6_0`, `CMKnifeCard_View_v1_8_0` / `CMKnifeCard_view_v1_9_0`, `CM_Chippers_View_v1_6_1`, `CM_NQ_VibState_v1_1_0`, `CMVibrationCard_View_v2_5_1`. Do not import. |
| `CMWorkLog_view_v1_0_1` | NEVER IMPORT - built for a fault that was not there (Raw Log 2026-10-09_A M6); `CMWorkLog_view_v1_0_0` is live. |
| `KPP_PEWatch_baseline_set_v1_0_0` | Superseded by **v1_1_0** for every re-take (set in use against new, KEEP, WIDER, one transaction). Remove once 1.1.0 has written a set. |
| `DashboardandPLC_Knowledge_Index_v1_37_0` | Superseded by **v1.38.0**. Remove. |
| `DashboardandPLC_Knowledge_Index_ADD_2026-10-10_v1_0_0` | Merged into **v1.38.0**. Remove. |
| `SweepAutoTile_view_v1_0_0` | Superseded by **v1_0_1** (scroll arrows). Remove. |
| `TNBMap_view_v1_2_7` / `v1_2_8` | Superseded by **v1_2_9** (1.2.7 carried the unused Drum chipper tile; neither hides the tiles on the Safety cards). Remove. |
| `SDBMap_view_v1_1_0` (2026-10-10) | NEVER IMPORT - clashes with the retired `SDBMap_View_v1_1_0` of 2026-09-25_A and renames the map root; use **`SDBMap_view_v1_3_0`**. |
| `GRAMap_view_v1_1_0` | NEVER IMPORT - renames the map root; use **v1_1_1**. |
| `DebarkerOverview_view_v1_3_0` | Superseded by **v1_3_1** (scroll arrows). Remove. |
| `DashboardandPLC_Knowledge_Index_v1_38_0` | Superseded by **v1.39.0**. Remove. |
| `TNBOverview_view_v1_0_0` / `GradingOverview_view_v1_0_0` (11 Oct) | NEVER IMPORT - built on the 8 Oct export; they drop his 1.1.0 changes (the T&B PTW permit bar). Use T&B **v1_2_1** and Grading **v1_4_0**. |
| Superseded files (2026-10-08_A) | `forensics_cosMoves_code_v1_0_0` / `v1_0_1` (events lost / wrong version string), `COS_Area__261_COSMoves_v1_0_0` + `_261_COSMoves_v1_0_0.st`, `KPP_COS_P6_ButtCW_query_v1_0_0` (rows with no target counted as BA), `KPP_COS_P5_ButtApproach_probe_v1_0_0`, `KPP_NQ_Production_COS_LogStopPositioning_v1_1_0`, `COS_LogStopPositioning_view_v1_1_0`, `COS_LogStopPositioningHelp_view_v1_1_0` / `v1_2_0`, `KPP_PA_COS_DB_apply_v0_1_0`, `PA_Page_view_v0_1_0`, `PA_COS_Stems_view_v0_1_0`, `Hubsidemenu_view_v1_7_0` / `v1_8_0`, `COSWatchOperator_view_v1_0_0`, `TNBOverview_view_v1_2_0`, `GradingOverview_view_v1_2_0` / `v1_3_0`, `KPP_GRA_SeqDeckRev_Tag_v1_0_0`. Do not import or run. |
| `DashboardandPLC_Knowledge_Index_v1_39_0` | Superseded by **v1.39.1**. Remove. |
| `DashboardandPLC_Knowledge_Index_v1_39_1` | Superseded by **v1.40.0**. Remove. |
| `DashboardandPLC_Knowledge_Index_v1_40_0` | Superseded by **v1.41.0**. Removed 13 Oct. |
| `DashboardandPLC_Knowledge_Index_v1_41_0`, `DashboardandPLC_Raw_Log_2026-10-13_A_v1_0_0` | Superseded by **v1.41.1** / Raw Log **v1.1.0**. Remove. |
| Cleanup of 13 Oct (Raw Log 2026-10-13_A section 11) | Removed: claude/ index 1.38.0 / 1.39.0 / 1.39.1 and the 2026-10-10 ADD, `KPP_Domain_Data_Reference_v1_8`, `KPP_PEWatch_Morning_Check_v1_0_0`, `KPP_COS_P5_ButtApproach_probe_v1_0_0`, and the claude/ copies of files in the root. Still to sort by hand: the two `2026-10-03_A` logs (different sessions - keep both, rename one), `20260715_B` x2 and `2026-08-24_B` x2. |
| PE Watch / Anomaly Watch superseded files (2026-10-13_A) | `forensics_peWatchJudge_code_v1_3_0`, `forensics_peWatchJudge_code_v1_4_0` / `v1_4_1` (NEVER INSTALL - 1.4.0 counted operator-NULL logout rows as COS logins, so every smoko was judged; 1.4.1 judged the first window after a smoko on the smoko's silent run), `KPP_PEWatch_registry_lib_v1_5_0`, `forensics_anomalyWatch_code_v1_12_2`, `KPP_PEWatch_Morning_Check_v1_0_0` / `v1_1_0`, `KPP_AnomalyWatch_Smoko_probe_v1_0_0`. Do not import or run. |
| `DashboardandPLC_Knowledge_Index_v1_41_1` | Superseded by **v1.42.0**. Remove (root and claude/ copies). |
| `shared_mlyproduction_code_v0_3_0` | Superseded by **v0_3_1** - passed exclusive 07:00 ends to the inclusive-date MLY by-day NQs, so every window carried the next day's early scans (the August email's 30th day). Do not install. |
| `workmate_hubpulse_v1_0_0` / `v1_0_1` / `v1_0_2` | Superseded by **v1_0_3** (1.0.0 / 1.0.1 hatched only full shuts). Do not install. |
| `Hub_view_v1_16_0` (2026-10-14_B) and `Hub_View_v1_16_0` (2026-08-16_A) | Two different files with one number - both superseded by **`Hub_view_v1_16_1`**. Never import either; the next Hub is 1.16.2 or later. |
| `VisitorMenu_view_v2_8_0` | Superseded by **v2_9_0** (shut via `schedule.kpp`). Do not import. |
| `Hubheader_view_v1_3_0` / `v1_4_0` | Superseded by **v1_5_0**. Do not import. |
| `DashboardandPLC_Knowledge_Index_v1_42_0` | Superseded by **v1.43.0**. Remove (root and claude/ copies). |
| `DashboardandPLC_Knowledge_Index_ADD_2026-10-14_B_v1_0_0` | Merged into **v1.43.0**. Remove. |
| `DashboardandPLC_Knowledge_Index_v1_43_0` | Superseded by **v1.44.0**. Remove (root and claude/ copies). |
| `DashboardandPLC_Knowledge_Index_v1_43_1` | Superseded by **v1.44.0** - registered 2026-10-14_C on 1.42.0 plus the 2026-10-14_B ADD, not on the full 1.43.0. Removed from the project. Never upload. |
| `claude/DashboardandPLC_Knowledge_Index_v1_43_0` written 14 Oct 10:32 (not the Hub Pulse chat's 1.43.0) | WITHDRAWN - registered 2026-10-14_C as 2026-10-14_B; removed 10:37. Never use. |
| `claude/DashboardandPLC_Raw_Log_2026-10-14_B_v1_0_0` | Held the 2026-10-14_C log from 10:32, over the Hub Pulse session's claude/ copy of 10:24; removed 10:37. The 2026-10-14_B log is the root copy (uploaded 10:36). |
| `DashboardandPLC_Raw_Log_2026-10-14_C_v1_0_0` | Superseded by **v1.1.0** (section 11 appended - the Echo answer, the 2nd-piece rule, view 1.2.0, the index re-base). Remove (root and claude/ copies). |
| `KPP_report_stems_by_shift_v1_1_0` / `KPP_report_stems_by_shift_apply_v1_1_0` | Superseded by **v1_2_0** - 1.1.0 counted a broken stem's 2nd piece as a stem. Do not run; the 1.2.0 applier replaces the 1.1.0 view. |
| `DashboardandPLC_Knowledge_Index_v1_44_0` | Superseded by **v1.45.0**. Remove (root and claude/ copies). |
| `DashboardandPLC_Knowledge_Index_v1_45_0` | Superseded by **v1.45.1**. Remove (claude/ copy). |
| `DashboardandPLC_Raw_Log_2026-10-14_D_v1_0_0` | Superseded by **v1.1.0** (section 11 appended - installed on Live, the 34 tags, the live motion fix). Remove (claude/ copy). |
| `KPP_DigitalTwin_COS_Design_v1_0_0` | Superseded by **v1.1.0** (live motion per value, `ts`, the 34 tags, the Live install). Remove (claude/ copy). |
| `twin_live_code_v1_0_0` / `KPP_Twin_COS_v1_0_0.html` | Superseded by **v1_1_0** - page 1.0.0 interpolated whole-plant snapshots and ran stop-start on Live. Not project knowledge; keep the 1.0.0 page in `C:\WorkmateData\Twin` and the import zip as the rollback. |
| `DashboardandPLC_Knowledge_Index_v1_45_1` | Superseded by **v1.46.0**. Remove (claude/ copy). |
| `KPP_LineTracker_Design_v1_0_0` | Superseded by **v1.0.1** before sign-off (the build changes and the off-PLC proof). Sent as a file only - not in the project knowledge. |
| `DashboardandPLC_Raw_Log_2026-10-15_A_v1_0_0` | Superseded by **v1.1.0** (section 12 appended - the download, the fault test, the regrade pile, the Sort Register). Remove (root and claude/ copies). |
| `DashboardandPLC_Knowledge_Index_v1_46_0` | Superseded by **v1.46.1** and **v1.47.0** (two branches of it, merged in **v1.47.1**). Remove (root and claude/ copies). |
| `KPP_Trk_Install_v1_0_0` / `KPP_SortRegrade_Probe_v1_0_0` | Superseded by **v1_0_1** / **v1_1_0** - the 1.0.0 sheet's scan-time rule would switch the tracker off for nothing. Not project knowledge. |
| `EngineeringMenu_view_v1_3_0` (2026-10-07_A) | Superseded by **v1_4_0** (Setpoints -> Settings). Do not import once 1.4.0 is in. |
| `DashboardandPLC_Knowledge_Index_v1_46_1` / `v1_47_0` | Superseded by **v1.47.1** (the merge of the two). Remove (claude/ copies). |
| `DashboardandPLC_Raw_Log_2026-10-15_B_v1_0_0` | Superseded by **v1.1.0** (section 12 appended - the install, the fixes, Big Balls, the glow, the settings watch). Remove (claude/ copy). |
| `KPP_MachineSettings_Design_v1_0_0` | Superseded by **v1.1.0**. Remove (claude/ copy). |
| Machine Settings superseded files (2026-10-15_B) | `engineering_settings_code_v1_0_0`-`v1_0_5` (1.0.0-1.0.3 match no role - everyone VIEW ONLY; 1.0.2 holds the cut speed table and prox windows - never install it: the installer would make the 33 tags again), `engineering_manualkick_code_v1_0_0` / `v1_0_1`, `KPP_MachineSettings_Probe_v1_0_0`, views `MachineSettings_view_v1_0_0`-`v1_0_3`, `SettingCard_view_v1_0_0`, `SettingRow_view_v1_0_0` / `v1_0_1`, `SettingCell_view_v1_0_0`, `ScaleCalc_view_v1_0_0` / `v1_0_1`, `AreaItem_view_v1_0_0`, `SettingEditor_view_v1_0_0` (every editor opened on 2,130), `ManualKick_view_v1_0_0`. Not project knowledge; do not install. |
| `DashboardandPLC_Knowledge_Index_v1_47_1` | Superseded by **v1.47.2**. Remove (root copy). |
| `DashboardandPLC_Raw_Log_2026-10-15_A_v1_1_0` | Superseded by **v1.2.0** (section 13 appended - the Overview chip, the Sort Register live, conveyor 1 measured, the tracker on, the comms clean-up). Remove (claude/ copy). |
| `KPP_Comms_Survey_v1_0_0` / `SortlineOverview_view_v1_1_0` | Superseded by **`KPP_Comms_Survey_v1_1_0`** (the DEFAULT section) / **`SortlineOverview_view_v1_2_0`**. Not project knowledge; do not run / import. |
| `DashboardandPLC_Knowledge_Index_v1_47_2` | Superseded by **v1.48.0**. Remove (claude/ copy). |
| `DashboardandPLC_Knowledge_Index_v1_48_0` | Superseded by **v1.48.1**. Remove (claude/ copy). |
| `DashboardandPLC_Knowledge_Index_v1_48_1` | Superseded by **v1.48.2**. Remove (claude/ copy). |
| `DashboardandPLC_Raw_Log_2026-10-16_A_v1_1_0` | Superseded by **v1.2.0** (section 14 appended - the scanner, the cross-ups, the COS regrade view). Remove (claude/ copy). |
| `KPP_TrkAdvisor_Design_v1_0_0` / `v1_0_1` | Superseded by **v1.0.2**. Remove (claude/ copies). |
| `DashboardandPLC_Raw_Log_2026-10-16_A_v1_0_0` | Superseded by **v1.1.0** (section 13 appended - the gateway identity advisor). Remove (claude/ copy). |
| `KPP_LineTracker_Design_v1_0_1` / `v1_1_0` / `v1_1_1` / `v1_1_2` / `v1_2_0` | Superseded by **v1.2.1** (1.2.0 built: section 18). Remove (root and claude/ copies in the project: v1_0_1, v1_1_2, v1_2_0). |
| `KPP_DigitalTwin_COS_Design_v1_1_0` | Superseded by **v1.2.0** (saved forecasts). Remove (claude/ copy). |
| `KPP_Trk_Watch_Probe_v1_0_0` - `v1_5_0` | Superseded by **v1_6_0** (RING / LIVE as before; WATCH and DATA for tracker 1.2.0; K8). Not project knowledge; run 1.6.0 only. |
| `SortlineMap_view_v1_2_0` - `v1_3_1`, `KPP_SortlineMap_Install_v1_3_0` / `v1_3_1`, `KPP_RegradeMarks_Install_v1_0_0`, `KPP_SmapTrk_Tags_v1_0_0` | Superseded by **`SortlineMap_view_v1_3_2`** / **`KPP_SortlineMap_Install_v1_3_2`** / **`KPP_RegradeMarks_Install_v1_1_0`**; the 1.3.0 tags and group are removed. Not project knowledge; do not import. |
| `twin_web_code_v1_0_0` / `KPP_Twin_COS_v1_1_0.html` | Superseded by **v1_1_0** / **v1_2_0** (saved forecasts). Not project knowledge; keep the 1.1.0 page as the roll-back. |
| `DashboardandPLC_Knowledge_Index_v1_48_2` | Superseded by **v1.49.0**. Remove (root and claude/ copies). |
| `weeklyreport_code_v0_8_1` (2026-08-10_A) | Superseded by **`shared_weeklyreport_code_v0_8_2`** - its Stem vs Forecast kept the per-shift forecast formula the daily retired at 4.7.14 and read `Production/DailyVolume_30d`. Live until 0.8.2 is installed, then the roll-back only. |
| `DashboardandPLC_Knowledge_Index_v1_49_0` | Superseded by **v1.50.0**. Remove (root and claude/ copies). |
| `KPP_TrkAdvisor_Design_v1_0_2` | Superseded by **v1.1.0** (phase 0 result, phase 1 as built). Remove (root and claude/ copies). |
| `KPP_Trk_230_SrtIdentity_v1_2_0.L5X` / `KPP_Trk_Install_v1_2_0` | NEVER IMPORT the 1.2.0 230 - refused (Error 12740-0, names that differ only in case); use **`KPP_Trk_230_SrtIdentity_v1_2_1`** with **`KPP_Trk_Install_v1_2_1`**. Not project knowledge. |
| `KPP_Trk_Watch_Probe_v1_6_0` | Superseded by **v1_6_1** - its "TWO LOGS taken as one" rested on 0.5 s reads. Not project knowledge; run 1.6.1. |
| `DashboardandPLC_Knowledge_Index_v1_50_0` | Superseded by **v1.50.1**. Remove (claude/ copy). |
| `DashboardandPLC_Raw_Log_2026-10-19_B_v1_0_0` | Superseded by **v1.1.0** (section 13 appended - the install, 1.0.1). Remove (claude/ copy). |
| `KPP_TrkAdvisor_Design_v1_1_0` | Superseded by **v1.1.1** (the pairing as built in 1.0.1, sorter_engine's cycle). Remove (claude/ copy). |
| `trk_advisor_code_v1_0_0` / `KPP_TrkAdvisor_Install_v1_0_0` | Superseded by **v1_0_1** - 1.0.0 paired the tracker's piece by time and left most scans without one on site. Not project knowledge; 1.0.0 is the roll-back until 1.0.1 runs. |
| `DashboardandPLC_Knowledge_Index_v1_50_1` | Superseded by **v1.50.2**. Remove (root and claude/ copies). |
| `DashboardandPLC_Raw_Log_2026-10-19_B_v1_1_0` | Superseded by **v1.2.0** (section 14 appended - the first hour of 1.0.1). Remove (root and claude/ copies). |
| `KPP_TrkAdvisor_Design_v1_1_1` | Superseded by **v1.1.2** (the first hour on site; the lead corrected - 1.1.1 put one decision in ten after the kick). Remove (root and claude/ copies). |
| `DashboardandPLC_Knowledge_Index_v1_50_2` | Superseded by **v1.50.3** and **v1.51.0** - both built on it side by side, merged in **v1.52.0**. Remove (claude/ copy). |
| `DashboardandPLC_Raw_Log_2026-10-19_B_v1_2_0` | Superseded by **v1.3.0** (section 15 appended - the first 7 hours, 1.0.2). Remove (claude/ copy). |
| `KPP_TrkAdvisor_Design_v1_1_2` | Superseded by **v1.1.3** (the first 7 hours, project saves in 1.0.2). Remove (claude/ copy). |
| `trk_advisor_code_v1_0_1` / `KPP_TrkAdvisor_Install_v1_0_1` | Superseded by **v1_0_2** - a project save started 1.0.1 again and reset its model. Not project knowledge; 1.0.1 is the roll-back until 1.0.2 runs. |
| `DashboardandPLC_Knowledge_Index_v1_50_3` | Superseded by **v1.52.0** (merged with 1.51.0). Remove (root and claude/ copies). |
| `DashboardandPLC_Knowledge_Index_v1_51_0` | Superseded by **v1.52.0** (merged with 1.50.3). Remove (root and claude/ copies). |
| `DashboardandPLC_Knowledge_Index_v1_52_0` | Superseded by **v1.52.1** (2026-10-20_B registered). Remove (claude/ copy). |
| `KPP_TrkAdvisor_Design_v1_1_3` | Superseded by **v1.1.4** (the first day, the scan against the plan by size, 1.0.3). Remove (root and claude/ copies). |
| `trk_advisor_code_v1_0_2` / `KPP_TrkAdvisor_Install_v1_0_2`, `KPP_TrkAdvisor_Report_v1_0_0` | Superseded by `trk_advisor_code_v1_0_3` / `KPP_TrkAdvisor_Install_v1_0_3`, `KPP_TrkAdvisor_Report_v1_1_0`. Not project knowledge; 1.0.2 is the roll-back until 1.0.3 runs. |
| `KPP_HydPumpWatch_Design_v1_0_0` | Superseded by **v1.1.0** (as installed; `pump_events` corrected). Remove (claude/ copy). |
| `KPP_CM_Design_v1_0_0` | Superseded by **v1.1.0**. Remove. |
| `CM_vib_baseline_set_v1_0_0` | Superseded by **v1_1_0** (REPRO; 1.0.0 was never in the project). Do not run. |
| PUMP WATCH superseded files (2026-10-17_A) | `forensics_hydPump_code_v1_0_0` - `v1_0_3` (1.0.0 the wrong folders; 1.0.0 - 1.0.2 a reference from before the sensors; 1.0.3 the roll-back), `HydraulicsDiagnosticsCard_view_v1_6_0`, `SafetyPlantOverview_view_v1_22_1`, `KPP_HydPump_Install_v1_0_0`. Not project knowledge; do not install. |
| LEAK WATCH superseded files (2026-10-15_C) | `forensics_hydLeak_code_v1_0_0` - `v1_0_2` (1.0.0 judged the warnings and fitted across fills; 1.0.1 no card; 1.0.2 the long Anomaly Watch headline), `forensics_anomalyAsk_code_v1_4_0`, `KPP_HydLeak_export_v1_0_0` (`saveFile`), `HydraulicsDiagnosticsCard_view_v1_5_0` (the green caption). Not project knowledge; do not install. |
| `DashboardandPLC_Knowledge_Index_v1_52_1` | Superseded by **v1.53.0** (2026-10-14_E and 2026-10-20_A registered). Remove (claude/ copy) - and the root copy of `DashboardandPLC_Knowledge_Index_v1_52_0`. |
| Value Recovery superseded files (2026-10-14_E) | `VR_Page_view_v1_0_0` - `v1_0_1` (1.0.0 the latched loading bar; the Page is now 1.0.3 of 2026-10-20_A), `VR_Origin_view_v1_0_0`, `VR_Crews_view_v1_0_0`, `VR_COS_view_v1_0_0`, `VR_Explore_view_v1_0_0`, `VR_Grading_view_v1_0_0` - `v1_0_1`, `VR_Stems_view_v1_0_0` - `v1_0_2` (1.0.0 Bad_NotFound on the title; 1.0.1 thousands separators), `analytics_valuerecovery_code_v1_0_0` - `v1_0_1` (now 1.1.0 of 2026-10-20_A). Not project knowledge. |
| COS NEW auto superseded files (2026-10-12_B) | The 1.0.0 package `KPP_COS_NewAuto_v1_0_0` - `_103_COS_NewAuto_v1_0_0`, `_100_COS_ConveyorControl_v1_3_0`, `_110_LogStopConvControl_v1_2_0`, `_055_COS_InfeedConveyor_v1_2_0`, `_260_COSWatch_v1_3_0`, `_261_COSMoves_v1_1_0`, `KPP_COS_NewAuto_Tags_v1_0_0`, the 1.0.0 views, `KPP_COS_LogStopPositioning_view_v1_3_0`, `KPP_COS_NewAuto_Install_v1_0_0` (NEVER IMPORT - tags-only L5X, braking to 2000, the stall and spring-back faults); `KPP_COS_NewAuto_LiveCheck_v1_0_0` (counts not rates, re-seats and restarts mixed), `KPP_PA_P2_CutTiming_v1_0_0`, `KPP_PA_COS_DB_apply_v0_1_1`, `PA_Page_view_v0_1_1`. Do not import or run. |
| `DashboardandPLC_Knowledge_Index_v1_55_0` | Superseded by **v1.56.0** (2026-10-12_B registered). Remove (root and claude/ copies). |
| `DashboardandPLC_Knowledge_Index_v1_56_0` | Superseded by **v1.57.0** (2026-10-22_A registered). Remove (claude/ copy). |
| `DashboardandPLC_Knowledge_Index_v1_57_0` | Superseded by **v1.58.0** (2026-10-23_A registered). Remove (claude/ copy). |
| Operator KPI superseded files (2026-10-23_A) | `Operator_KPI_Scorecard_Design_v3.13.xlsx` (12 errors - Design v3_14_0), `OperatorKPI` 1.8.0, `TrainingReview` 1.7.0 view and `operator.trainingreview` 1.4.0 (KPI values lost on Save), `BusinessSideMenu` 1.6.0, `BusinessHome` 2.5.0, `DebarkerStemPressure` 1.4.x, `DebarkerDetail` 1.0.3, `Stem Gap Histogram` NQ 1 (no booth filter). Replace on install. |
| Visitor Sign In superseded files (2026-10-22_A) | `Hubheader_view_v1_6_0` (its pill shows on the Menu - labels ignore `props.style.display`), `VisitorUserVerification_view_v1_1_0` - `v1_1_2` (1.1.0 the hint never hides; 1.1.2 the glow cut square). Do not import. |

---

*Rules for writing into any of these → `DashboardandPLC_Knowledge_Standard`.*
