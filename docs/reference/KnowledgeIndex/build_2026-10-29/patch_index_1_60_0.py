# builds the final DashboardandPLC_Knowledge_Index_v1_60_0.md from the 16:04 draft (which registered 2026-10-28_A 1.0.0 only)
import sys
src, out = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()

def rep(a, b):
    global s
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b)

# 1. date + changelog entry
rep('**Status:** Active · **Date:** 2026-10-28 · **Author:** Adriaan',
    '**Status:** Active · **Date:** 2026-10-29 · **Author:** Adriaan')
a0 = s.index('- v1.60.0 - REGISTRATION')
a1 = s.index('- v1.59.0 - REGISTRATION')
s = s[:a0] + '''- v1.60.0 - REGISTRATION for the 2026-10-28_A and 2026-10-28_B session (HMI alarm history, the one-press RESET ALL
  IGs, PUMP WATCH rebased after the transmitter swaps, the area map in the SafetyDiag popup; one chat, Wed 28 Oct 15:12
  - 20:36, closed out Thu 29 Oct with the first GitHub pass; built on 1.59.0). Raw Logs `2026-10-28_A` 1.1.0 and
  `2026-10-28_B` 1.1.0 added. **(1) Findings (L5K `KPP_COS_V20T` of 27 Oct, the 28 Oct export, the Script Console):**
  the group reset is the release edge of a reset button, blocked while the TOF fault-reset pulse is on; the fault reset
  is a 3 s hold; the pulse is 500 ms on every group except Grading (GRA_IG1-3 2000 ms), so a fixed "3.5 s then 0.2 s"
  loses Grading resets (61 of 100 modelled); HMI reset reach per area (COS also resets T&B IG1-5 and CHP IG7; DDB has
  none); `_102_COS_IG2` shares `ONSAux[0].7` between the COS HMI reset and CHP_RB_08 (PLC, not touched); the booth
  alarm tables cannot acknowledge. Pumps: pressure transmitters were swapped (Adriaan) - DB P4 and DB P6 read one
  transmitter Apr - Sep, DB P6 stepped 25 Sep; DB P1 - P3 stepped together 21 May; DB P4 +7 bar mid-Oct, TNB P4 +7 bar
  July (under the line). The 2020 Material icons (`health_and_safety`, `restart_alt`) are not on this gateway - a
  component error box. The Designer's RPC gives up a runQuery after 60 s idle. The old safety map is
  `Application/Safety/Zone` (the area maps with the safety layer + 41 IG outlines). **(2) Built and installed:**
  `booth.safetyreset` 1.0.0, `forensics.alarmHistory` 1.0.0 (`alarm.hmi_history`, timer `AlarmHistory_FixedDelay`),
  `shared.purge` 1.2.0 (30 days); Booth Alarms popup 1.1.0, AlarmPanel 1.3.0, MessageAckButton 1.1.0, AreaSafetyCard
  1.5.0, SafetyPlantOverview 1.25.1 (verified_user), SafetyDiag popup 1.3.0 (area map, installed and confirmed);
  `forensics.hydPump` 1.0.6 (`rebase()` month by month) - references set on site: DB P1 - P3 22 May - 19 Jun, DB P6
  26 Sep - 24 Oct (long check from 5 Dec), GRA P1 2 - 30 May, GRA P3 28 May - 25 Jun; all 18 pumps NORMAL.
  **Delivered, install pending:** SafetyDiag 1.3.1 (the picked group bright - fill, 4 px line, glow, on top).
  `KPP_HydPumpWatch_Design` 1.1.0 -> **1.2.0** (rebase, section 15). **(3) CORRECTIONS banked:** the Diag tile icons
  (1.25.1 / 1.2.1); `rebase()` 1.0.5 timed out on DB P2's whole-history read - 1.0.6 (nothing was written by the
  failed run). **(4) Staged, not compiled:** `KPP_Platform_Rules`, `KPP_Domain_Data_Reference` - Raw Log 2026-10-28_A
  sections 5 and 14. **(5) Repo:** `Adriaan18/kppdashboard` PR #1 merged 29 Oct (`9572282`) - the session's
  deliverables, builders and tests under `docs\\reference\\` (BoothHMI, HydPumpWatch, Shared, TestBench) and the
  session's PK docs mirrored; `PK_MIRROR` 1.1.0. Index copies 1.53.0, 1.54.0 (root and claude/), 1.56.0, 1.58.0
  removed from PK (all in the repo, `docs\\`). **(6) OPEN:** SafetyDiag 1.3.1 install; the map against the Zone per
  area; DB P4 mapping; `rebase(False, force=["DB P5"])` optional; 33 alarms active over 30 days in the history; the COS
  IG2 shared ONS for the next safety unlock; the old Zone / MapCards reset buttons; a read-only login for the AI box;
  the full PK mirror - Raw Log 2026-10-28_A section 18, 2026-10-28_B section 7.
''' + s[a1:]

# 2. compiled doc row
rep('| `KPP_HydPumpWatch_Design` | 1.1.0 | Anything PUMP WATCH',
    '| `KPP_HydPumpWatch_Design` | 1.2.0 | Anything PUMP WATCH')
rep('the install and the tests, open items. Session record: Raw Log 2026-10-17_A sections 3-7. |',
    'the install and the tests, open items; from 1.2.0 `rebase()` after a transmitter swap or pump change (section 15) and references taken at the next refresh. Session record: Raw Log 2026-10-17_A sections 3-7; Raw Log 2026-10-28_A sections 10-16 and 2026-10-28_B. |')

# 3. raw log series entry
old = ('`2026-10-28_A` (HMI alarm history and the one-press RESET ALL IGs, 28 Oct: the safety PLC\'s reset rungs read from the L5K - '
       'release-edge group reset blocked by the fault-reset pulse, Grading\'s 2 s pulse, HMI reset reach per area, the COS IG2 shared ONS; '
       '`booth.safetyreset` 1.0.0, `forensics.alarmHistory` 1.0.0 with `alarm.hmi_history`, `shared.purge` 1.2.0; Booth Alarms popup 1.1.0 '
       'HISTORY tab, SafetyDiag 1.2.0, AreaSafetyCard 1.5.0, SafetyPlantOverview 1.25.0)**')
new = old[:-3] + ('; 1.1.0: the Diag tile icons, `forensics.hydPump` 1.0.5 `rebase()` after the transmitter swaps), '
       '`2026-10-28_B` (the same chat from 18:57: `forensics.hydPump` 1.0.6 - rebase read month by month, the references set on site, '
       'DB P4 / DB P6 one transmitter Apr - Sep; SafetyDiag 1.3.0 the area map from `Application/Safety/Zone`, 1.1.0: 1.3.1 the picked group bright)**')
rep(old, new)

# 4. deliverables row
rep('`SafetyPlantOverview_view_v1_25_0.json` (`Application/Safety/SafetyPlantOverview`). Detail in Raw Log 2026-10-28_A sections 3 and 9. |',
    '`SafetyPlantOverview_view_v1_25_0.json` (`Application/Safety/SafetyPlantOverview`). Then `SafetyPlantOverview_view_v1_25_1.json` and '
    '`BoothSafetyDiag_view_v1_2_1.json` (icons), `BoothSafetyDiag_view_v1_3_0.json` (area map, installed) and `BoothSafetyDiag_view_v1_3_1.json` '
    '(picked group bright, to install - into an empty view). PUMP WATCH: `forensics_hydPump_v1_0_5.py`, `forensics_hydPump_v1_0_6.py` -> '
    '`forensics/hydPump` (1.0.6 installed; `rebase()` then `rebase(False)` run). All in `kppdashboard` `docs\\reference\\` with their builders and '
    'tests. Detail in Raw Log 2026-10-28_A sections 3, 9, 12 and 17, 2026-10-28_B sections 3, 6 and 8. |')

# 5. section 2: the repo
rep('| `Workmate_Memory_Export` | Re-seeding Claude memory - the 30 delivery rules. |\n',
    '| `Workmate_Memory_Export` | Re-seeding Claude memory - the 30 delivery rules. |\n'
    '| GitHub `Adriaan18/kppdashboard` (`C:\\dropbox\\kppdashboard`, branch `main`) | The off-PK home: `docs\\` mirrors PK at the same filenames (flat, `claude/` dropped), `docs\\reference\\<slice>\\` holds source extracts, builders and tests; `docs\\PK_MIRROR.md` lists what is there. Look here for a superseded index or a session\'s builders before asking. |\n')

# 6. retired rows
anchor = '\n\n---\n\n*Rules for writing into any of these'
assert s.count(anchor) == 1
rows = '''
| `DashboardandPLC_Knowledge_Index_v1_53_0`, `v1_54_0`, `v1_56_0`, `v1_58_0` | Removed from PK 29 Oct 2026 (root 1.53.0 and 1.54.0, claude/ 1.54.0, 1.56.0, 1.58.0) - in the repo, `docs\\`. |
| `DashboardandPLC_Knowledge_Index_v1_59_0` | Superseded by **v1.60.0** (2026-10-28_A and B registered). Remove (claude/ copy) - in the repo, `docs\\`. |
| `KPP_HydPumpWatch_Design_v1_1_0` | Superseded by **v1.2.0** (rebase, 28 Oct). Remove (root and claude/ copies). |
| `DashboardandPLC_Raw_Log_2026-10-28_A_v1_0_0`, `_B_v1_0_0` | Superseded by **v1.1.0** of each (append-only - the 1.1.0 holds all of 1.0.0). Remove (claude/ copies). |
| Booth / Safety / PUMP WATCH superseded files (2026-10-28) | `SafetyPlantOverview_view_v1_25_0` and `BoothSafetyDiag_view_v1_2_0` (2020 Material icons - a component error), `BoothSafetyDiag_view_v1_2_1`, `v1_3_0` (replaced by 1.3.1), `forensics_hydPump_v1_0_5` (`rebase()` times out in the Designer). Not project knowledge; in the repo. |'''
s = s.replace(anchor, rows + anchor)

assert '\\u2013' not in s
assert '\u2013' not in s and '\u2014' not in s
open(out, 'w', encoding='utf-8').write(s)
print('ok', len(s.encode('utf-8')))
