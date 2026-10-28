# PK mirror status

**Version:** 1.2.0 · **Date:** 2026-10-29 · **Author:** Adriaan

The PK of the claude.ai Project "KPP Dashboard & PLC" is mirrored into `docs\` byte for byte, at the same versioned filenames, in housekeeping passes. Once a large harness or builder is safe here, it is retired from PK and the PK index points to this repo.

**History**
- 1.2.0 2026-10-29 - Knowledge Index 1.53.0 - 1.60.0 (1.53.0, 1.54.0, 1.56.0, 1.58.0 then removed from PK); the 1.60.0 builder.
- 1.1.0 2026-10-29 - the 28 Oct session: its PK docs and its source extracts (BoothHMI, HydPumpWatch, Shared, TestBench).
- 1.0.0 2026-10-26 - repo set-up.

## Mirrored
| `docs\` | PK folder |
|---|---|
| `DashboardandPLC_Raw_Log_2026-10-28_A_v1_0_0.md` | `claude/` |
| `DashboardandPLC_Raw_Log_2026-10-28_A_v1_1_0.md` | `claude/` |
| `DashboardandPLC_Raw_Log_2026-10-28_B_v1_0_0.md` | `claude/` |
| `DashboardandPLC_Raw_Log_2026-10-28_B_v1_1_0.md` | `claude/` |
| `KPP_HydPumpWatch_Design_v1_2_0.md` | `claude/` |
| `DashboardandPLC_Knowledge_Index_v1_53_0.md` | root - removed from PK 29 Oct |
| `DashboardandPLC_Knowledge_Index_v1_54_0.md` | root and `claude/` (the two identical) - removed from PK 29 Oct |
| `DashboardandPLC_Knowledge_Index_v1_56_0.md` | `claude/` - removed from PK 29 Oct |
| `DashboardandPLC_Knowledge_Index_v1_58_0.md` | `claude/` - removed from PK 29 Oct |
| `DashboardandPLC_Knowledge_Index_v1_59_0.md` | `claude/` |
| `DashboardandPLC_Knowledge_Index_v1_60_0.md` | `claude/` |

Still to mirror: the rest of PK, up to `DashboardandPLC_Knowledge_Index_v1_59_0.md` (the full first pass). Some names sit in PK both at the root and under `claude/`, and a few root names twice - that pass compares each pair before the flat mirror keeps one.

## Reference extracts (`docs\reference\`)
Each slice holds its deliverables at their delivered filenames (`file -> Ignition resource [the version it replaces]`). `build_<date>\` holds that session's builders and tests as they ran; their paths are the session's (`/home/claude/out`, the scratchpad, the project export under `/home/claude/src`) - point them at these folders to run them again. The three dash checks in `BoothHMI\build_2026-10-28\` are written as Python unicode escapes here, not as the dash characters (the same code, AST identical).

### BoothHMI (28 Oct - Raw Log 2026-10-28 A and B)
- `booth_safetyreset_v1_0_0.py` -> `booth/safetyreset` [new]
- `forensics_alarmHistory_v1_0_0.py` -> `forensics/alarmHistory` [new]
- `BoothAlarmsPopup_view_v1_1_0.json` -> `Application/Booth/Popups/Alarms` [1.0.0]
- `BoothAlarmPanel_view_v1_3_0.json` -> `Application/Booth/Components/AlarmPanel` [1.2.0]
- `BoothMessageAckButton_view_v1_1_0.json` -> `Application/Booth/Components/MessageAckButton` [1.0.1]
- `BoothSafetyDiag_view_v1_2_0.json`, `_v1_2_1`, `_v1_3_0`, `_v1_3_1` -> `Application/Booth/Popups/SafetyDiag` [1.1.0] - each into an empty view
- `AreaSafetyCard_view_v1_5_0.json` -> `Application/Safety/Components/AreaSafetyCard` [1.4.1]
- `SafetyPlantOverview_view_v1_25_0.json`, `_v1_25_1` -> `Application/Safety/SafetyPlantOverview` [1.24.1]
- `BoothSafetyDiag_view_v1_3_0_preview.png` (the group outlines per area), `BoothSafetyDiag_view_v1_3_1_preview.png` (the picked group over the 20:22 screenshot)
- `build_2026-10-28\`: `gen_views_v1_0_0.py` / `_v1_0_1.py` (the six views, from the 28 Oct 14:22 export), `gen_safetydiag_map_v1_0_0.py` / `_v1_0_1.py` (SafetyDiag 1.3.0 / 1.3.1, from 1.2.1 and `Application/Safety/Zone`), `gson.py`; tests `test_reset`, `test_history`, `test_views`, `test_viewexec`, `test_map_view`, `test_map_view_131`, `measure_batch`

### HydPumpWatch (28 Oct - `KPP_HydPumpWatch_Design` 1.2.0)
- `forensics_hydPump_v1_0_5.py`, `_v1_0_6.py` -> `forensics/hydPump` [1.0.4] - 1.0.6 is the `rebase()` read a month at a time
- `build_2026-10-28\`: `hydPump_1_0_4.py` (1.0.4 as exported 28 Oct 14:22), `patch_1_0_5.py` (1.0.5 from it), `rebase_block.py` / `rebase_block_1_0_6.py` (the rebase code of 1.0.5 / 1.0.6); tests `test_rebase`, `test_rebase_106` and their output (`rebase_out.txt`, `rebase106_out.txt`)

### Shared (28 Oct)
- `shared_purge_v1_2_0.py` -> `shared/purge` [1.1.0] - adds the job "HMI alarm history" (30 days)

### KnowledgeIndex (29 Oct)
- `build_2026-10-29\`: `patch_index_1_60_0.py` - the final 1.60.0 from the 28 Oct draft (2026-10-28_A 1.0.0 only) - the whole session, the repo, the removals.

### TestBench (28 Oct)
- `build_2026-10-28\`: `harness.py` (an off-gateway stand-in for Ignition 8.3 / Jython 2.7: `java.*`, `system.*`, a virtual clock, `system.db` on a local PostgreSQL 16 - port 55432, `pg_up.sh` - and the project modules loaded from source through lib2to3), `plcsim.py` (a scan-level model of the isolation-group reset logic, parsed from `KPP_COS_V20T.L5K`), `py2check.py` (Python 2.7 grammar). The BoothHMI and HydPumpWatch tests of the same date import them.
