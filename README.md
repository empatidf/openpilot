# Škoda Superb Mk4 — earlier port on a sunnypilot base (branch `sunnypilot`)

> **This branch is kept for reference and is not developed further.**
> The active port is on **[`master`](https://github.com/empatidf/openpilot/tree/master)**, built on
> comma.ai openpilot: install it with `installer.comma.ai/empatidf/master`.

This branch is the first port of the **Škoda Superb Mk4** (2024+, MQB Evo GEN2, chassis code `NZ`), built on
[sunnypilot](https://github.com/sunnypilot/sunnypilot).

**Where the code comes from:** this branch continues
[infiniteCable2/openpilot](https://github.com/infiniteCable2/openpilot) (a sunnypilot-based fork with MEB and
MQB Evo support). Its car code is in [empatidf/opendbc](https://github.com/empatidf/opendbc) branch
`sunnypilot`, which **is taken from [infiniteCable2/opendbc](https://github.com/infiniteCable2/opendbc)** (MQB
Evo message definitions, MEB/MQB Evo control and safety code) with the Superb Mk4 platform and its tuning added
on top.

The findings from its test drives
(the rack's once-per-second release without the car's Travel Assist, the speed-dependent curvature gain, the
MQB Evo message map) carried over to `master`, where they are documented in `SUPERB_MK4.md` and
`SUPERB_MK4_BEST_LATERAL.md`.

If you still want to run this branch: `installer.comma.ai/empatidf/sunnypilot`. Experimental, not supported
or reviewed by comma.ai or sunnypilot; keep your hands on the wheel and be ready to take over at any time.

## License

This branch contains sunnypilot and comma.ai openpilot code, released under the MIT license; see
[`LICENSE`](LICENSE). Any user of this software shall indemnify and hold harmless Comma.ai, Inc. and its
directors, officers, employees, agents, stockholders, affiliates, subcontractors and customers from and
against all allegations, claims, actions, suits, demands, damages, liabilities, obligations, losses,
settlements, judgments, costs and expenses (including without limitation attorneys' fees and costs) which
arise out of, relate to or result from any use of this software by user.

**THIS IS ALPHA QUALITY SOFTWARE FOR RESEARCH PURPOSES ONLY. THIS IS NOT A PRODUCT. YOU ARE RESPONSIBLE FOR
COMPLYING WITH LOCAL LAWS AND REGULATIONS. NO WARRANTY EXPRESSED OR IMPLIED.**
