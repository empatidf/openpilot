# openpilot for the Škoda Superb Mk4 (2024+, MQB Evo)

This `master` branch is built on **[comma.ai openpilot](https://github.com/commaai/openpilot)** (0.11.3) and adds
steering support for the **Škoda Superb Mk4** (4th generation, 2024+, MQB Evo GEN2, chassis code `NZ`).
openpilot steers; the car's own ACC keeps gas, brake and emergency braking.

> **Experimental, not supported or reviewed by comma.ai.** Keep your hands on the wheel and be ready to
> take over at any time. You use this software at your own risk.

## Where the code comes from

- **openpilot:** comma.ai openpilot, with small Volkswagen changes to the curvature controller
  (`openpilot/selfdrive/controls`, see [`SUPERB_MK4.md`](SUPERB_MK4.md)).
- **opendbc (car code):** the `opendbc_repo` submodule points at
  [empatidf/opendbc](https://github.com/empatidf/opendbc) branch `master`. That is comma.ai opendbc plus the
  Superb Mk4 port. **The MQB Evo message definitions (`_vw_mqbevo_common.dbc`, `vw_mqbevo_2024.dbc`, unchanged)
  and the MQB Evo platform approach are taken from
  [infiniteCable2/opendbc](https://github.com/infiniteCable2/opendbc)**; the Superb Mk4 platform, its tuning and
  the fixes listed below were added on top.

## What you need

| Item | Notes |
|---|---|
| Car | Škoda Superb Mk4 (2024+) with **ACC** and **Travel Assist**. Other MQB Evo cars are not supported by this port. |
| comma device | **comma four** or **comma 3X**. The car uses CAN FD; older devices do not work. |
| Harness | **VW C harness**: [xnor.shop/products/vw-c-harness](https://xnor.shop/products/vw-c-harness). It goes between the windscreen camera and its connector. |

The comma device and harness are not sold for this car by comma.ai; check fit and plugs before you install.

## Installation from scratch

1. **Harness:** with the car off, open the cover around the windscreen camera (behind the rear-view mirror),
   unplug the camera connector, and plug the VW C harness in between camera and car, following the harness
   instructions. Connect the harness to the comma device and mount the device on the windscreen.
2. **Software:** start the comma device. During setup choose **Custom Software** and enter:

   `installer.comma.ai/empatidf/master`

3. **First start:** switch the car on. openpilot reads the radar firmware to recognise the car (the VIN
   cannot be read from the camera connector). The supported radar firmware is `1N3907567B` (ECU `0x757`).
   If the device shows **"Car Unrecognized"** or dashcam mode, your car has different firmware: open an issue
   with your route, the firmware can then be added.
4. **Calibration:** drive above 24 km/h on straight roads until calibration reaches 100 % (a few minutes).
   openpilot cannot engage before that.
5. **Settings on the device:** make sure openpilot is enabled (Settings → Toggles). Uploading drives to
   comma connect is recommended; logs are the only way to find problems.

### Driving

1. Turn on the car's **ACC** and engage the car's own **Travel Assist** (steering-wheel button, green
   steering-wheel icon in the cluster). openpilot engages together with ACC and disengages when ACC
   switches off; there is no steering without ACC.
2. Keep Travel Assist engaged: without it the steering rack releases openpilot's request for a moment once
   per second, and under load this can end in "LKAS Fault: Restart the Car" (a restart clears it).
3. Lane changes: signal and nudge the wheel; openpilot changes lane.
4. Keep your hands on the wheel. Braking, gas or a firm steering input overrides openpilot.

### Updating and removing

- The device updates by itself when the car is off and it has internet; Settings → Software checks by hand.
  A device installed from the old `op` branch: Settings → Software → target branch → `master`.
- To return the car to stock, unplug the harness and plug the camera connector back in.

## Branches

| Branch | What it is |
|---|---|
| **`master`** (use this) | comma.ai openpilot with the Superb Mk4 port |
| `chestnut` | Newer comma.ai openpilot (the source of `nightly-chestnut`) with the same Superb Mk4 port, for use with the comma Chestnut GPU |
| `chestnut-ta` (test) | `chestnut` plus openpilot's own Travel Assist status message, so openpilot steers alone without the rack's one-second release. Drive it with the car's Travel Assist switched off; see below |
| `sunnypilot` | Earlier port on a sunnypilot base; kept for reference, not developed further |

The current code is the build confirmed on the car as the best working steering so far. Its parameters and
the reasons behind them are in [`SUPERB_MK4_BEST_LATERAL.md`](SUPERB_MK4_BEST_LATERAL.md) (search for
`BEST WORKING LATERAL MODEL`); [`SUPERB_MK4.md`](SUPERB_MK4.md) lists every change and how to update to newer
comma.ai openpilot.

### Using the comma Chestnut GPU (`chestnut` branch)

[Chestnut](https://comma.ai/shop/chestnut) is comma's external GPU for the comma four. It runs a much larger
driving model than the device can. comma ships it on `nightly-chestnut`, which is built from comma's `master`.
The `chestnut` branch here is that same comma `master` merged with this port (the Superb Mk4 opendbc code and the
steering changes), so the car steers with the big model:

1. Plug in Chestnut as comma describes (USB-C to the device, 12 V power).
2. Install `installer.comma.ai/empatidf/chestnut` (Settings > Software > Uninstall, then Custom Software), or
   switch branch to `chestnut` under Settings > Software.
3. The first start builds openpilot and downloads the big model (about 760 MB), so give it time on Wi-Fi.
4. With Chestnut connected, openpilot loads the big model on its own; without it, it falls back to the normal
   model. Chestnut alerts (not detected, overheated, power) show on the home screen as in comma's build.

Notes:

- `chestnut` follows comma's development code, which is newer and less tested than `master` here. If it
  misbehaves, go back to `installer.comma.ai/empatidf/master`.
- The opendbc submodule points at the `chestnut` branch of
  [empatidf/opendbc](https://github.com/empatidf/opendbc/tree/chestnut), which is the same Superb port merged
  with the opendbc version comma's `master` uses.
- The steering tune was set on `master` with the normal model; the big model plans differently, so report how
  it drives (routes with bookmarks help).

### Test branch `chestnut-ta`: openpilot steers alone

**What was found.** Two things in the car decide how openpilot can steer (logs of 24 Nov 2026):

- While the car's own Travel Assist is **active**, the car's lane centering sets where the car sits in the lane.
  openpilot's sustained requests are not executed, and a position the driver steered to is kept (0.5 m right of
  centre for 75 s after a 4 s push on the wheel).
- While Travel Assist is **not active**, the rack ends every steering request after exactly 1.00 s and accepts
  it again one frame later. In turns that is a jolt in the wheel and a pulse towards straight ahead once a second.

**What this branch changes.**

- openpilot re-sends the camera's Travel Assist status message (`TA_01`) and reports Travel Assist as active
  while it steers, as comma's MEB port with openpilot longitudinal does. The frame is the one the camera itself
  sends in that state on this car, byte for byte. The panda blocks the camera's copy and lets "active" through
  only while openpilot is engaged.
- While the car's own Travel Assist is not active, the steering command is no longer multiplied by the speed gain
  table (it was measured with Travel Assist steering along).
- When you steer, openpilot follows your steering and hands back over one second after you let go, instead of
  holding its plan against you and swinging back on release. Lane changes are unchanged.

**How to drive it.**

1. Install `installer.comma.ai/empatidf/chestnut-ta`, or switch branch under Settings > Software.
2. In the car, switch **Travel Assist off** and drive with ACC only. If the car's Travel Assist is active, the
   branch behaves like `chestnut`.
3. The instrument cluster may show Travel Assist as active while openpilot steers; that is the message above.
4. First drive: an empty road, hands on the wheel, below about 100 km/h. Above that speed the steering gain is not
   measured yet for this mode and the car may steer too little in curves.
5. Bookmark anything odd and share the route. Go back with `installer.comma.ai/empatidf/chestnut`.

Not verified on the car yet: that the rack keeps accepting openpilot continuously with this message, and that no
other control unit objects to it.

## What the port does

- Steering by curvature (`HCA_03`), tuned on this car over ~20 logged drives:
  - speed-dependent gain on the command (the rack carries out less of the command above ~100 km/h),
  - a smoothed command at speed, filtered before the legal acceleration/jerk limits,
  - a gentle feedback controller (low proportional gain against highway weave; an integrator that is kept
    through wheel nudges, frozen during lane changes and bled off while Travel Assist steers).
- Stock ACC stays in charge of speed. Short Front Assist warning phases in dense traffic no longer count as a
  cruise fault.

## Open issues

- **Keeps too close to the right lane line.** With the car's Travel Assist active, the car's own lane
  centering holds the lane position and keeps a position the driver steered to; openpilot cannot pull it back.
  The `chestnut-ta` test branch is the attempt to fix it. On unmarked town roads the driving model itself keeps
  to the right and takes right-hand bends close to the kerb.
- **Short opposite-direction steering pulses in turns, once a second.** Confirmed: with Travel Assist not
  active the rack ends each steering request after 1.00 s and accepts it again one frame later. The
  `chestnut-ta` test branch is the attempt to fix it.
- **Sensors drop out briefly and openpilot disengages.** The car's assistance sensors go away for a moment,
  openpilot switches off, the sensors come back right after and openpilot can be engaged again. Not fixed;
  it is linked to a timing clash of CAN messages (openpilot's copy of the steering wheel's hands-on message
  `KLR_01` colliding with the car's own frame).
- **Sensors missing after a short stop.** When the car is switched off for a short break and started again,
  the assistance sensors sometimes do not come up, and the car has to be switched off and on once more. Not
  fixed.
- **Small left-right steering oscillation at low speed.** Will be addressed in coming versions.

### Limitations

- With Travel Assist engaged, the car's own lane centering does most of the steering; openpilot steers alone
  when Travel Assist pauses, e.g. during lane changes (Travel Assist pauses for about 3–8 s when you signal).
- No openpilot longitudinal control: the radar sits on the car-side bus, outside the camera harness, so its
  acceleration requests cannot be replaced without silencing the whole ADAS unit (which also removes
  emergency braking and Travel Assist).

## License

openpilot is released under the MIT license; see [`LICENSE`](LICENSE). Any user of this software shall
indemnify and hold harmless Comma.ai, Inc. and its directors, officers, employees, agents, stockholders,
affiliates, subcontractors and customers from and against all allegations, claims, actions, suits, demands,
damages, liabilities, obligations, losses, settlements, judgments, costs and expenses (including without
limitation attorneys' fees and costs) which arise out of, relate to or result from any use of this software
by user.

**THIS IS ALPHA QUALITY SOFTWARE FOR RESEARCH PURPOSES ONLY. THIS IS NOT A PRODUCT. YOU ARE RESPONSIBLE FOR
COMPLYING WITH LOCAL LAWS AND REGULATIONS. NO WARRANTY EXPRESSED OR IMPLIED.**
