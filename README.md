# openpilot for the Škoda Superb Mk4 (2024+, MQB Evo)

Steering support for the **Škoda Superb Mk4** (4th generation, 2024+, MQB Evo GEN2, chassis code `NZ`)
on a comma device. openpilot steers; the car's own ACC keeps gas, brake and emergency braking.

> **Experimental, not supported or reviewed by comma.ai.** Keep your hands on the wheel and be ready to
> take over at any time. You use this software at your own risk.

## Which branch to install

| Branch | What it is | Install |
|---|---|---|
| **`op`** (use this) | comma.ai openpilot 0.11.3 with the Superb Mk4 port in [empatidf/opendbc](https://github.com/empatidf/opendbc) branch `op` | `installer.comma.ai/empatidf/op` |
| `master` | Earlier port on a sunnypilot base. No longer the active branch; kept for reference | — |
| `superb-long` | Experimental openpilot longitudinal attempt. **Do not use** (see open issues) | — |
| `op-superb-fix` | Old test branch, merged into `op`. Can be deleted | — |

The current `op` build has the same code as `4210b83`, the build confirmed on the car as the best working
steering so far. Its parameters and the reasons behind them are in `SUPERB_MK4_BEST_LATERAL.md` on the
`op` branch (search for `BEST WORKING LATERAL MODEL`); `SUPERB_MK4.md` there lists every change.

## Requirements

- comma four or comma 3X (the car uses CAN FD).
- VW C / MFK-C camera harness at the windscreen camera.
- The car is identified by its radar firmware (`1N3907567B`, ECU `0x757`); the VIN cannot be read from the
  camera connector.

## How to drive with it

1. Turn on the car's ACC and engage the car's own **Travel Assist** (steering-wheel button, green
   steering-wheel icon in the cluster). openpilot engages together with ACC.
2. With Travel Assist engaged the steering rack does not release once per second, and the "LKAS Fault"
   seen in earlier versions has not occurred in the logged drives.
3. Lane changes: signal and nudge the wheel; openpilot changes lane.

## What the port does

- Steering by curvature (`HCA_03`), with tuning measured on this car over ~20 logged drives:
  - speed-dependent gain on the command (the rack carries out less of the command above ~100 km/h),
  - a smoothed command at speed, filtered before the legal acceleration/jerk limits,
  - a gentle feedback controller (low proportional gain against highway weave; an integrator that is kept
    through wheel nudges, frozen during lane changes and bled off while Travel Assist steers).
- Stock ACC stays in charge of speed. Short Front Assist warning phases in dense traffic
  (`AWV_03.AWV_Unavailable` for 0.1–2 s) no longer count as a cruise fault.

## Open issues

- **Rack releases once per second without Travel Assist.** When the car's Travel Assist is not engaged,
  the rack drops openpilot's steering request for 10–20 ms every second (felt as a small ping). Under load
  with the driver steering, such a release can end in "LKAS Fault: Restart the Car". This also happens
  during lane changes, because Travel Assist pauses for about 3–8 s when you signal.
- **With Travel Assist engaged, the car's own lane centering does most of the steering.** The rack follows
  only a small part of openpilot's corrections; openpilot steers alone when Travel Assist pauses, e.g.
  during lane changes.
- **Rare stock-ACC shut-off at standstill.** Once in a while the car's ACC switches itself off after a few
  seconds at a stop (reversible fault with a warning sound) and openpilot disengages with it. The likely
  cause is openpilot's second copy of the steering wheel's hands-on message (`KLR_01`) colliding with the
  car's own frame on the car-side bus. A fix was tested and is reverted for now, because the build without
  it drove more reliably; still under investigation.
- **Car errors at some ignitions.** On some start-ups the car shows several assistance-system errors. The
  panda's camera-side bus records bus-off errors around ignition on/off, never while driving. Not solved.
- **Small steering-wheel dither below ~15 km/h** comes from the driving model's plan; a fine 10–17 Hz buzz
  felt in some curves is generated inside the rack.
- **No openpilot longitudinal control.** The radar sits on the car-side bus, outside the camera harness, so
  its acceleration requests cannot be replaced without silencing the whole ADAS unit (which also removes
  emergency braking and Travel Assist). A gateway (J533) harness could make it possible; not tried.

## License

openpilot is released under the MIT license; see [`LICENSE`](LICENSE). Any user of this software shall
indemnify and hold harmless Comma.ai, Inc. and its directors, officers, employees, agents, stockholders,
affiliates, subcontractors and customers from and against all allegations, claims, actions, suits, demands,
damages, liabilities, obligations, losses, settlements, judgments, costs and expenses (including without
limitation attorneys' fees and costs) which arise out of, relate to or result from any use of this software
by user.

**THIS IS ALPHA QUALITY SOFTWARE FOR RESEARCH PURPOSES ONLY. THIS IS NOT A PRODUCT. YOU ARE RESPONSIBLE FOR
COMPLYING WITH LOCAL LAWS AND REGULATIONS. NO WARRANTY EXPRESSED OR IMPLIED.**
