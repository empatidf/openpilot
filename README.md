## ✍ To install this fork use installer.comma.ai/empatidf/master (Comma Four compatible)

## ⚠️ Untested branch — Škoda Superb Mk4 (2024+) port in progress

This fork is based on [infiniteCable2/openpilot](https://github.com/infiniteCable2/openpilot) and adds
**experimental, untested** support for the **Škoda Superb Mk4** (4th generation, 2024+, MQB Evo,
VIN chassis code `NZ`).

**It has not been driven or validated on a real car yet.** Do not rely on it. If you install it:

- Keep your hands on the wheel and be ready to take over at all times.
- Test first with the car stationary, then on an empty road — never in traffic on a first run.
- Expect CAN errors, an "unidentified vehicle" message, or steering that does not engage.
- Do not enable alpha longitudinal: on a camera-harness install it disables the stock radar and
  with it the car's stock automatic emergency braking (AEB).

You use this software at your own risk.

### What was changed for the Superb Mk4

All car-specific changes are in the opendbc submodule, which now points to
[empatidf/opendbc](https://github.com/empatidf/opendbc) instead of infiniteCable2/opendbc:

| File | Change |
|---|---|
| `opendbc/car/volkswagen/values.py` | New platform `SKODA_SUPERB_MK4`: MQB Evo, chassis code `NZ`, Škoda WMI `TMB`, mass 1678 kg, wheelbase 2.84 m, flag `MQB_EVO_GEN2` (2024 DBC and checksum variant) |
| `opendbc/car/volkswagen/fingerprints.py` | Placeholder firmware entry (the car's firmware versions are not known yet) |
| `opendbc/car/torque_data/substitute.toml` | Uses the Golf Mk8 torque values, as the Octavia Mk4 does |
| `opendbc/car/tests/routes.py` | Listed under `non_tested_cars` (no test route yet) |
| `opendbc/sunnypilot/car/car_list.json` | Adds "Škoda Superb 2024-25" to the vehicle selector |

Steering, safety and CAN handling reuse the existing MQB Evo code; no other code was changed.

### Status after the first installed-car logs (2026-10-09)

- **Identification:** the car identifies by its radar firmware (`1N3907567B`, ECU `0x757`). The VIN
  cannot be read from the camera connector on this car, so firmware matching is the only automatic
  path. If it still shows "Car Unrecognized", select **"Škoda Superb 2024-25"** manually
  (Settings → fingerprint).
- **`MQB_EVO_GEN2` is measured, not assumed:** `ESC_51` is 64 bytes, `Motor_51` 48 bytes, and the
  2024 message definitions validate every checksum on recorded frames.
- **`SMLS_01` is present** on this car. **`EA_01`/`EA_02` are not**, so the Emergency-Assist read
  is now only done when the fingerprint saw them.
- Verified offline only: recorded frames replayed through the car interface give a valid car state
  (gear, cruise available, steering angle, no faults). **Not yet driven with openpilot engaged.**
- **The car's own lane-centering command is not on this CAN.** A 13-minute drive with stock
  Travel Assist actively steering (EPS reporting `QFK_01.LatCon_HCA_Status = active`) never showed
  `HCA_03` (0x303) or any other new message on the camera-connector bus. The camera most likely
  steers over Automotive Ethernet. Whether the gateway/EPS accept openpilot's `HCA_03` sent on this
  CAN is therefore **unverified until the first engagement**.
- **Before testing openpilot steering, switch the car's own Lane Assist / Travel Assist off** in
  the infotainment. openpilot cannot block the stock command, so both must never run at once.
- Stock ACC, blinkers, capacitive steering-wheel touch, gear and set-speed all decode correctly
  from the recorded drive.
- Requires a CAN FD capable device (comma 3X / comma four) and a VW C / MFK-C camera harness.

![](https://user-images.githubusercontent.com/47793918/233812617-beab2e71-57b9-479e-8bff-c3931347ca40.png)

## 🌞 What is sunnypilot?
[sunnypilot](https://github.com/sunnyhaibin/sunnypilot) is a fork of comma.ai's openpilot, an open source driver assistance system. sunnypilot offers the user a unique driving experience for over 300+ supported car makes and models with modified behaviors of driving assist engagements. sunnypilot complies with comma.ai's safety rules as accurately as possible.

## 💭 Join our Community Forum
Join the official sunnypilot community forum to stay up to date with all the latest features and be a part of shaping the future of sunnypilot!
* https://community.sunnypilot.ai/

## Documentation
https://docs.sunnypilot.ai/ is your one stop shop for everything from features to installation to FAQ about the sunnypilot

## 🚘 Running on a dedicated device in a car
First, check out this list of items you'll need to [get started](https://community.sunnypilot.ai/t/getting-started-using-sunnypilot-in-your-supported-car/251).

## Installation
Next, refer to the sunnypilot community forum for [installation instructions](https://community.sunnypilot.ai/t/read-before-installing-sunnypilot/254), as well as a complete list of [Recommended Branch Installations](https://community.sunnypilot.ai/t/recommended-branch-installations/235).

## 🎆 Pull Requests
We welcome both pull requests and issues on GitHub. Bug fixes are encouraged.

Pull requests should be against the most current `master` branch.

## 📊 User Data

By default, sunnypilot uploads the driving data to comma servers. You can also access your data through [comma connect](https://connect.comma.ai/).

sunnypilot is open source software. The user is free to disable data collection if they wish to do so.

sunnypilot logs the road-facing camera, CAN, GPS, IMU, magnetometer, thermal sensors, crashes, and operating system logs.
The driver-facing camera and microphone are only logged if you explicitly opt-in in settings.

By using this software, you understand that use of this software or its related services will generate certain types of user data, which may be logged and stored at the sole discretion of comma. By accepting this agreement, you grant an irrevocable, perpetual, worldwide right to comma for the use of this data.

## Licensing

sunnypilot is released under the [MIT License](LICENSE). This repository includes original work as well as significant portions of code derived from [openpilot by comma.ai](https://github.com/commaai/openpilot), which is also released under the MIT license with additional disclaimers.

The original openpilot license notice, including comma.ai’s indemnification and alpha software disclaimer, is reproduced below as required:

> openpilot is released under the MIT license. Some parts of the software are released under other licenses as specified.
>
> Any user of this software shall indemnify and hold harmless Comma.ai, Inc. and its directors, officers, employees, agents, stockholders, affiliates, subcontractors and customers from and against all allegations, claims, actions, suits, demands, damages, liabilities, obligations, losses, settlements, judgments, costs and expenses (including without limitation attorneys’ fees and costs) which arise out of, relate to or result from any use of this software by user.
>
> **THIS IS ALPHA QUALITY SOFTWARE FOR RESEARCH PURPOSES ONLY. THIS IS NOT A PRODUCT.
> YOU ARE RESPONSIBLE FOR COMPLYING WITH LOCAL LAWS AND REGULATIONS.
> NO WARRANTY EXPRESSED OR IMPLIED.**

For full license terms, please see the [`LICENSE`](LICENSE) file.

## 💰 Support sunnypilot
If you find any of the features useful, consider becoming a [sponsor on GitHub](https://github.com/sponsors/sunnyhaibin) to support future feature development and improvements.


By becoming a sponsor, you will gain access to exclusive content, early access to new features, and the opportunity to directly influence the project's development.


<h3>GitHub Sponsor</h3>

<a href="https://github.com/sponsors/sunnyhaibin">
  <img src="https://user-images.githubusercontent.com/47793918/244135584-9800acbd-69fd-4b2b-bec9-e5fa2d85c817.png" alt="Become a Sponsor" width="300" style="max-width: 100%; height: auto;">
</a>
<br>

<h3>PayPal</h3>

<a href="https://paypal.me/sunnyhaibin0850" target="_blank">
<img src="https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif" alt="PayPal this" title="PayPal - The safer, easier way to pay online!" border="0" />
</a>
<br></br>

Your continuous love and support are greatly appreciated! Enjoy 🥰

<span>-</span> Jason, Founder of sunnypilot
