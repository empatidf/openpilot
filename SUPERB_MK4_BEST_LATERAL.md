# BEST WORKING LATERAL MODEL — Škoda Superb Mk4

Reference builds that drove well, newest first. Search for `BEST WORKING LATERAL MODEL` or `best-lateral`.

```
BEST WORKING LATERAL MODEL - Skoda Superb Mk4 (MQB Evo GEN2), 2026-10-30

Keywords: best-lateral, best working lateral model, superb-mk4, mqb-evo, reference build

Confirmed on the car by the owner as one of the best working lateral steering
builds so far. Use this tag as the reference point to compare or roll back to.

  openpilot  empatidf/openpilot  op  4210b83  (comma openpilot 0.11.3 base)
  opendbc    empatidf/opendbc    op  7251ca3f
  Install:   installer.comma.ai/empatidf/op  (or check out this tag)

CAR SETUP
- Skoda Superb Mk4 (chassis NZ, 2024+), MQB Evo GEN2, CAN FD, camera harness
  (VW C / MFK-C), comma four. Identified by radar FW 1N3907567B (ECU 0x757).
- Stock ACC keeps gas/brake/AEB; openpilot steers only, by curvature (HCA_03).

LATERAL PARAMETERS IN THIS BUILD
- Curvature PID: kpBP [10, 40] m/s, kpV [0, 0.5] (MEB default 1.45);
  kiBP [8, 12, 40], kiV [0, 0.4, 0.4]; kf 1.0. steerActuatorDelay 0.3 s,
  steerRatio 16.5.
- P/I error uses the plan from one actuator delay ago (expected curvature).
- Integrator: kept through wheel nudges (no PID reset), frozen during
  overrides, lane changes, safety limiting and below 5 m/s, bounded to
  1 m/s^2 lateral accel, bled off (2 s) while the car's Travel Assist steers.
- Speed gain on the command: 1.0 / 1.12 / 1.2 / 2.0 / 2.3 at
  60 / 80 / 95 / 105 / 120 km/h (EPS reduced-authority map).
- EPS correction (rack minus measured curvature) faded out 50-60 km/h.
- Command low-pass: 0 below 30 km/h, 80 ms from 45 km/h, applied BEFORE the
  ISO lateral accel/jerk limits.
- AWV_03.AWV_Unavailable counts as a cruise fault only after 5 s.

WHAT WE LEARNED (from ~20 logged drives, 100 Hz CAN)
1. Rack 1 Hz supervision drop: while the car's own Travel Assist is NOT active
   (TA_01.Travel_Assist_Status != 4) the rack drops openpilot's HCA to "ready"
   for 10-20 ms exactly once per second (felt as a ~1 Hz ping). Every "LKAS
   Fault: Restart the Car" (QFK_01 status 6, latched) started on one of these
   drops while the driver was steering hard. With TA active: ~0 drops, no faults.
2. With Travel Assist active the rack mostly follows the camera's own lane
   centering: only 3-7 % of openpilot's deviations from the plan are executed
   (TA off: ~72 %). Travel Assist pauses (status 4 -> 2) for 3-8 s at every
   openpilot lane change, so openpilot steers alone during lane changes.
3. CAN map (camera bus): TA_01.Travel_Assist_Status 0 off / 2 ready / 4 active;
   LDW_02.LDW_Lernmodus 0 Lane Assist off / 1 on / 3 steering;
   ACC_18.ACC_Status_ACC 2 standby (6 briefly at start-up);
   QFK_01.LatCon_HCA_Status 2 ready / 4 active / 6 fault;
   0x318 camera status ...03 starting -> ...07 ready ~5-9 s after ignition.
4. Stop-and-go "Cruise Fault": AWV_03.AWV_Unavailable flickers 0.1-2 s during
   Front Assist warning/prefill phases; upstream treated it as a fault,
   disengaged and cancelled ACC. Fixed by the 5 s persistence check.
5. Highway left-right weave: the P term fed back 0.1 deg wheel-angle steps and
   the speed gain doubled them; the old gain went unstable in a closed-loop
   rack model. kp 1.45 -> 0.5 halved wheel motion at 90-140 km/h.
6. Drift after lane changes: the wheel nudge that confirms a lane change reset
   the PID and threw away the learned bias. Integrator now kept and frozen.
7. Wheel vibration (~10 Hz) in curves: the kept integrator wound up against
   Travel Assist (up to 20e-4 1/m) and the two steering requests fought;
   vibration grew 4.6x with the gap. Fixed by bleeding it off while TA steers.
8. Slow/late lane changes and near lane departure: the low-pass ran after the
   jerk limit and cut the steering rate to a fifth (0.7 vs 3.6 m/s^3); the
   command lagged 0.5-1.2 s. Filter now runs before the limits.
9. Updates: a submodule pointer must name an existing opendbc commit; devices
   cloned with --recurse-submodules check every intermediate commit, so one
   bad pointer in history blocks all updates ("failed to update").

STILL OPEN / NOT DONE
- Spoofing TA_01 "active" to stop the 1 Hz drop without Travel Assist was not
  implemented (it defeats a factory supervision check).
- 1 Hz drops still occur during lane changes while Travel Assist pauses.
- Low-speed (<15 km/h) model plan jitter; 10-17 Hz rack buzz is internal.
```
