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
| `sunnypilot` | Earlier port on a sunnypilot base; kept for reference, not developed further |

The current code is the build confirmed on the car as the best working steering so far. Its parameters and
the reasons behind them are in [`SUPERB_MK4_BEST_LATERAL.md`](SUPERB_MK4_BEST_LATERAL.md) (search for
`BEST WORKING LATERAL MODEL`); [`SUPERB_MK4.md`](SUPERB_MK4.md) lists every change and how to update to newer
comma.ai openpilot.

## What the port does

- Steering by curvature (`HCA_03`), tuned on this car over ~20 logged drives:
  - speed-dependent gain on the command (the rack carries out less of the command above ~100 km/h),
  - a smoothed command at speed, filtered before the legal acceleration/jerk limits,
  - a gentle feedback controller (low proportional gain against highway weave; an integrator that is kept
    through wheel nudges, frozen during lane changes and bled off while Travel Assist steers).
- Stock ACC stays in charge of speed. Short Front Assist warning phases in dense traffic no longer count as a
  cruise fault.

## Open issues

- **Keeps too close to the right lane line in town.** Cause not found yet.
- **Short opposite-direction steering pulses in turns, at a regular rhythm.** Source not found yet; it is
  most likely the car itself (the rack's once-per-second release), but the logs have not confirmed it.
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
