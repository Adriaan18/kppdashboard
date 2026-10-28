# DashboardandPLC Raw Log - 2026-10-28 B

**Version:** 1.0.0 - **Author:** Adriaan - **Layer:** RAW - append-only, never rewritten
**Session:** the same chat as 2026-10-28 A, from 18:57 (NZDT); lettered B because A (1.1.0) is at the size the project
knowledge still takes (about 24 KB free of 2 MB).
**Sources:** the Script Console output of `forensics.hydPump.rebase()` (18:42 on 1.0.5; 19:08 and 19:10 on 1.0.6); the
`Safety.zip` export of `Application/Safety` (19:14) and a screenshot of the old COS safety map.
**Design of record:** this log; `KPP_HydPumpWatch_Design` 1.2.0 for the pump watch.

---

## 1. Scope (NZDT, Wed 28 Oct)

- **18:57** - `rebase()` on 1.0.5 (18:42) stopped at the second pump: the Designer gave up on DB P2's whole-history read
  ("Idle timeout expired: 60010/60000 ms"). Nothing was written by it - the writes come after every pump is read.
- **19:08 / 19:10** - on 1.0.6 the dry run and the live run read all 18 pumps: "rebase: none" - the references were
  already set (a 1.0.5 `rebase(False)` went through): DB P1 - P3 22 May - 19 Jun, DB P6 26 Sep - 24 Oct (used from 5 Dec),
  GRA P1 2 - 30 May, GRA P3 28 May - 25 Jun. Every pump NORMAL (DB P5 index 49, GRA P1 26).
- **19:14** - "we have removed the safety visual representation for the devices in Safety - add a small visual in the new
  SafetyDiag popup for the areas".

## 2. Findings

- **DB P4 and DB P6 read the same pressure every month from April to September** (131.5, 128.8, 131.8, 132.5/132.6,
  138.0, 131.1 bar): both tags read one transmitter until DB P6 stepped on 25 Sep (now 110.9, level with DB P5 at
  109.7 - HydUnit2). DB P6's "-18 bar since Apr" was that, not wear. DB P4's last 14 days read 137.2 against 130.5 for
  October - it moved about +7 bar in mid-October (under the 8 bar rebase line, card normal).
- DB P1 - P3 all stepped up on 21 May (126 - 129 -> 137 - 138) - one change for the three, likely a setting or scaling
  change, rebased.
- DB P5 (index 49): its temperature is judged against DB P6 (peer, no tank sensor on HydUnit2) - DB P6's transmitter
  change moved DB P5's T by +3.1 degC. TNB P4 +7.0 bar from July (107 -> 114.5), under the line.
- **The old safety map** is `Application/Safety/Zone` (818 KB): per area its map view with the safety layer only
  (`Application/COS/COS Map`, `Grading/GRA Map`, `Debarker/SDB Map`, `TNB/TNB Map`, `Hogger/HOG Map`, `Chippers & Refuse/CHP
  Map` - params Safety true, the other layers false) and the isolation-group outlines over it (41 labels, each reading
  three IG tags of its own). The Zone's map box is 1420 x 456 px at its default size (Chippers drawn for 1.65:1). DDB has
  no map. The maps carry live buttons (TNB "Regrade Next Log", sweep setpoints).

## 3. Built (not installed)

- **`forensics.hydPump` 1.0.6** (18:59): `rebase()` reads the table a month at a time, each read tried 3 times 3 s
  apart; a pump still not read is listed NOT READ with its cause and the others go on (nothing written for it);
  `only=[...]`. Nothing else changes.
- **SafetyDiag popup 1.3.0** (gen_safetydiag_map 1.0.0 from 1.2.1): a **Map** chip in the devices head (not on DDB)
  swaps the device list for the area map - the Zone's own map view with the safety layer (loaded only while shown; the
  map takes no taps - its old popups and buttons stay out of reach) and the Zone's group outlines redrawn in the popup's
  colours from the popup's model (energized green, isolated yellow, ready to reset blue, stopped orange, fault red;
  "IG n" on each group; one picked = the others grey). Tap an outline to pick the group (again, or outside, for all);
  the tooltip names the group and its state. The map box keeps the Zone's ratio (100 % x 322 px; Chippers 693 x 420).
  The chip's choice holds for the session (`session.custom.safetyDiagMap`). The outlines read no tags of their own (the
  Zone's read 123).

## 4. Decisions

1. The map is the plant's own area maps as the Zone showed them, not a new drawing - the crews know it, and it stays
   right when the maps change.
2. The map replaces the device list on a chip, not beside it - the 1002 px panel has room for one at a legible size.

## 5. Proof before delivery

- 1.0.6: the 1.0.5 tests again (FAILS 0) plus a read failing once (tried again, nothing lost), DB P2 never readable
  (NOT READ with the time-out, the 17 others read, the four rebases written, DB P2 not), every read 30 days at most,
  `only=` reading just its pump.
- 1.3.0: 173 new expressions balanced and on declared props, 50 new scripts Python 2 grammar, scope G; the chip, the
  startup read, an outline tap, the outside tap and the colour transform run in the stand-in; every outline names a
  group `booth.safety` knows; every map path exists in the export; the outlines drawn per area at the box sizes (no
  Perspective here - the map under them is as the Zone showed it).

## 6. Deliverables

- `forensics_hydPump_v1_0_6.py` -> `forensics/hydPump` [1.0.5]
- `BoothSafetyDiag_view_v1_3_0.json` -> `Application/Booth/Popups/SafetyDiag` [1.2.1] - into an empty view
- This log.

## 7. Open

1. Check the map against the Zone on one area (the outlines over the right places); if one is off, the box ratio for
   that area is the knob (`gen_safetydiag_map` BOX_H / BOX_W).
2. DB P4's mapping (moved +7 bar mid-October); `rebase(False, force=["DB P5"])` if its peer temperature should restart.
3. The project knowledge is near its limit - old Knowledge Index copies to clear before the next index.
