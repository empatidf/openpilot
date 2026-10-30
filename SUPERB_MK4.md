# Škoda Superb Mk4 on stock openpilot (branch `op`)

This branch is **comma.ai openpilot master, unchanged**, with one difference: the `opendbc`
submodule points at [empatidf/opendbc](https://github.com/empatidf/opendbc) branch `op`, which is
commaai/opendbc master plus a single commit adding the Škoda Superb Mk4 (MQB Evo, 2024+).

> **Untested on the car.** Not supported or reviewed by comma.ai. Use at your own risk, keep your
> hands on the wheel and be ready to take over at any time.

## What the car port does
- Car: Škoda Superb Mk4 (chassis `NZ`, MQB Evo, 2024+), camera install with a VW C / MFK-C harness,
  CAN FD device (comma 3X / comma four).
- Identified automatically by its radar firmware (the only ECU that answers from the camera
  connector).
- **Steering only.** The car's own ACC keeps gas, brake and AEB. openpilot engages when you engage
  ACC and disengages with it (stock openpilot behaviour; there is no steering without ACC).
- Lateral tuning measured on this car: curvature gain above 60 km/h, EPS correction at town speed,
  stronger integrator from 29 km/h.
- Known behaviour: the steering rack briefly releases about once per second unless the car's own
  Travel Assist is engaged; rarely this latches "LKAS Fault" in a loaded curve. Engaging the car's
  Travel Assist together with ACC avoids it.

## Changes 2026-10-30
Made from drives `0000002f` and `00000032`:
- **Stop-and-go "Cruise Fault":** the radar's `AWV_Unavailable` bit flickers for 0.1-2 s during
  Front Assist warning phases in dense traffic; openpilot treated it as a fault, disengaged and
  cancelled ACC. It now has to persist for 5 s.
- **Highway left-right weave:** the curvature controller's P gain is a third of the MEB value
  (it amplified wheel-angle sensor steps); the P/I error uses the plan from one steering delay ago.
- **Lane changes:** a wheel nudge no longer resets the learned steering bias (integrator); the
  integrator is frozen during lane changes and bounded to 1 m/s^2.
- Still open: during each lane change the car's Travel Assist pauses for ~3-8 s and the rack
  releases briefly once per second in that window.

## Changes 2026-10-30 (drive 00000044)
- **Slow lane changes:** the smoothing filter ran after the jerk limit and cut the steering rate
  to a fifth; it now runs before it.
- **Wheel vibration in curves:** with the car's Travel Assist active, the rack follows the camera's
  own lane centering and only a few percent of openpilot's corrections. openpilot's integrator
  wound up against it (up to 20e-4 1/m) and the two requests fought (~10 Hz vibration). The
  integrator is now frozen and bled off while Travel Assist is active
  (`CarState.lateralStockAssistActive`).
- Important: **with Travel Assist active, the car's own Travel Assist does most of the steering**;
  openpilot mainly steers when Travel Assist is off or paused (e.g. lane changes).

## Install
`installer.comma.ai/empatidf/op`

## Updating to newer openpilot
```sh
# 1. openpilot: take comma's latest master
git fetch https://github.com/commaai/openpilot.git master
NEW_DBC=$(git ls-tree FETCH_HEAD opendbc_repo | awk '{print $3}')   # opendbc commit comma pins
git merge FETCH_HEAD            # conflicts only possible in .gitmodules / opendbc_repo: keep ours

# 2. opendbc: replay the single Superb commit onto the opendbc commit comma pins
cd opendbc_repo
git fetch https://github.com/commaai/opendbc.git master
git rebase $NEW_DBC
git push origin HEAD:op --force-with-lease

# 3. openpilot: point at the rebased opendbc commit
cd .. && git add opendbc_repo && git commit -m "bump opendbc (Superb Mk4)" && git push origin op
```
