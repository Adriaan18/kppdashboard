# kppdashboard

KPP Dashboard & PLC: the Ignition Perspective reporting suite, capture engines and HMI views for KPP and MLY (Kaingaroa Tipu), plus the Rockwell PLC and Delta motion side.
This private repo is the off-PK home for project knowledge and source extracts.

- **Clone:** `C:\dropbox\kppdashboard`, branch `main`.
- **Author:** `Adriaan <Riaan18.rp@gmail.com>`.
- **Stack:** gateway `TL-KPPWS01`, project `MainSCADA_Timberlands`, PostgreSQL `KPP_production`, Studio 5000 v35 (`COS_PLC_1756CPU`).
- **Workmate Dev** (the CMMS rebuild) lives in `workmate-scada`, not here.

## Layout
| Path | What it holds |
|---|---|
| `docs\` | The mirror of the claude.ai project knowledge (PK) of the "KPP Dashboard & PLC" Project, at the same versioned filenames, flat. Files that PK keeps under `claude/` drop the prefix here. |
| `docs\reference\<slice>\` | Source extracts per slice: view JSONs, gateway and console scripts, NQ SQL, PLC L5X, builders, harnesses, previews and superseded versions. Large or rarely needed files live here, not in PK. |
| `docs\PK_MIRROR.md` | Which PK docs are mirrored so far. |

## Rules
- **Never overwrite.** Every change is a new versioned file (`..._vX_Y_Z.ext`), and old versions stay in git history.
- **One commit per release or housekeeping pass.** The message names the slice and the versions.
- **Plain hyphens only** in every file, never an em or en dash.
- **Dropbox:** only this PC works in this clone. GitHub is the backup; pull and push, and never edit `.git` from a second machine through Dropbox.
