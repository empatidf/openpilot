import math
import numpy as np
from collections import deque

from openpilot.cereal import log
from openpilot.common.pid import PIDController
from openpilot.selfdrive.controls.lib.latcontrol import LatControl
from openpilot.selfdrive.controls.lib.drive_helpers import MAX_CURVATURE

LAT_ACCEL_SATURATION_THRESHOLD = 0.5  # m/s^2
VW_INTEGRATOR_MAX_LAT_ACCEL = 1.0  # m/s^2


class LatControlCurvature(LatControl):
  def __init__(self, CP, CI, dt):
    super().__init__(CP, CI, dt)
    self.sat_check_min_speed = 5.
    if CP.lateralTuning.which() == 'pid':
      ct = CP.lateralTuning.pid
      self.pid = PIDController((ct.kpBP, ct.kpV), (ct.kiBP, ct.kiV),
                               pos_limit=MAX_CURVATURE, neg_limit=-MAX_CURVATURE, rate=1 / dt)
      self.kf = ct.kf
    else:
      self.pid = None
      self.kf = 1.
    self.desired_curvature_buffer_len = int(1. / self.dt)
    self.desired_curvature_buffer = deque([0.] * self.desired_curvature_buffer_len, maxlen=self.desired_curvature_buffer_len)
    # Volkswagen (MEB / MQB Evo): compare the measured curvature with the plan from one actuator delay ago, keep the
    # learned integrator through driver overrides, and hold it during lane changes (set by controlsd)
    self.vw_feedback = CP.brand == "volkswagen"
    self.hold_integrator = False

  def reset(self):
    super().reset()
    if self.pid is not None:
      self.pid.reset()

  def update(self, active, CS, VM, params, steer_limited_by_safety, desired_curvature, curvature_limited, lat_delay):
    curvature_log = log.ControlsState.LateralCurvatureState.new_message()
    actual_curvature = -VM.calc_curvature(math.radians(CS.steeringAngleDeg - params.angleOffsetDeg), CS.vEgo, params.roll)
    error = desired_curvature - actual_curvature
    self.desired_curvature_buffer.append(desired_curvature)
    delay_frames = int(np.clip(lat_delay / self.dt + 1, 1, self.desired_curvature_buffer_len))
    expected_curvature = self.desired_curvature_buffer[-delay_frames]

    if not active:
      output_curvature = 0.0
      curvature_log.active = False
      if self.pid is not None:
        self.pid.reset()
    elif self.pid is not None and self.vw_feedback:
      # A wheel nudge (e.g. confirming a lane change) used to reset the PID, dropping the integrator that holds the
      # car's steady steering bias (up to ~6e-4 1/m at highway speed on the Superb Mk4) and pushing the car off centre
      # for seconds afterwards. Keep it, without P, during overrides; freeze it while steering is overridden, lane
      # changing or limited by safety, so it does not wind up on errors the controller is not meant to remove.
      freeze = CS.steeringPressed or self.hold_integrator or steer_limited_by_safety or CS.vEgo < 5.
      vw_error = 0. if CS.steeringPressed else expected_curvature - actual_curvature
      output_curvature = self.pid.update(vw_error, speed=CS.vEgo, feedforward=self.kf * desired_curvature,
                                         freeze_integrator=freeze)
      # bound the kept integrator to 1 m/s^2 of lateral acceleration (steady bias seen: ~0.6 m/s^2)
      i_max = VW_INTEGRATOR_MAX_LAT_ACCEL / max(CS.vEgo, 5.) ** 2
      if abs(self.pid.i) > i_max:
        self.pid.i = float(np.clip(self.pid.i, -i_max, i_max))
        output_curvature = self.pid.p + self.pid.i + self.pid.f
      curvature_log.p = float(self.pid.p)
      curvature_log.i = float(self.pid.i)
      curvature_log.f = float(self.pid.f)
      curvature_log.active = True
    elif self.pid is None or CS.steeringPressed:
      # no PID or override: feedforward only
      if self.pid is not None:
        self.pid.reset()
      output_curvature = self.kf * desired_curvature
      curvature_log.active = True
    else:
      output_curvature = self.pid.update(error, speed=CS.vEgo, feedforward=self.kf * desired_curvature)
      curvature_log.p = float(self.pid.p)
      curvature_log.i = float(self.pid.i)
      curvature_log.f = float(self.pid.f)
      curvature_log.active = True

    curvature_log.error = float(error)
    curvature_log.actualCurvature = float(actual_curvature)
    curvature_log.desiredCurvature = float(desired_curvature)
    curvature_log.output = float(output_curvature)
    curvature_log.saturated = bool(self._check_saturation(abs(expected_curvature - actual_curvature) * CS.vEgo ** 2 > LAT_ACCEL_SATURATION_THRESHOLD, CS,
                                                          False, curvature_limited))
    return 0.0, float(output_curvature), curvature_log
