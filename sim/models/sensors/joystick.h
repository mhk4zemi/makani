/*
 * Copyright 2020 Makani Technologies LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#ifndef SIM_MODELS_SENSORS_JOYSTICK_H_
#define SIM_MODELS_SENSORS_JOYSTICK_H_

#include <stdint.h>

#include <stack>

#include "common/macros.h"
#include "control/system_types.h"
#include "sim/models/sensors/sensor.h"
#include "sim/sim_messages.h"

class Joystick : public Sensor {
  friend class JoystickTest;

 public:
  explicit Joystick(const JoystickParams &joystick_params,
                    const SimJoystickParams &joystick_sim_params);
  ~Joystick() {}

  void UpdateSensorOutputs(SimSensorMessage *sensor_message,
                           TetherUpMessage * /*tether_up*/) const override;
  void Publish() const override;

 private:
  void DiscreteStepHelper(double t) override;

  double throttle() const { return throttle_.val(); }
  double roll() const { return roll_.val(); }
  double pitch() const { return pitch_.val(); }
  double yaw() const { return yaw_.val(); }
  JoystickSwitchPositionLabel tri_switch() const { return tri_switch_.val(); }
  JoystickSwitchPositionLabel momentary_switch() const {
    return momentary_switch_.val();
  }

  const JoystickParams &joystick_params_;
  const SimJoystickParams joystick_sim_params_;
  const AioNode joystick_node_;
  std::stack<const SimJoystickUpdate *> updates_;

  DiscreteState<double> throttle_, roll_, pitch_, yaw_;
  DiscreteState<JoystickSwitchPositionLabel> tri_switch_;
  DiscreteState<JoystickSwitchPositionLabel> momentary_switch_;

  DISALLOW_COPY_AND_ASSIGN(Joystick);
};

#endif  // SIM_MODELS_SENSORS_JOYSTICK_H_
