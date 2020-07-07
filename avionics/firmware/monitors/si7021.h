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

#ifndef AVIONICS_FIRMWARE_MONITORS_SI7021_H_
#define AVIONICS_FIRMWARE_MONITORS_SI7021_H_

#include <stdbool.h>
#include <stdint.h>

#include "avionics/firmware/drivers/si7021.h"
#include "avionics/firmware/drivers/si7021_types.h"
#include "avionics/firmware/monitors/si7021_types.h"

// Si7021MonitorPoll() calls a function with this prototype for each SI7021
// device update. The 'device' argument corresponds to the Si7021Monitor.device
// member field, not the 'device_index' passed to Si7021MonitorPoll().
typedef void (* const Si7021OutputFunction)(int32_t device,
                                            const Si7021OutputData *raw);

// Si7021MonitorInit() initializes an array of SI7021 devices.
void Si7021MonitorInit(int32_t num_devices, Si7021 *devices);

// Si7021MonitorPoll() polls all SI7021 devices in the given configuration,
// and calls 'output_function' for each update. The 'device_index' input/output
// argument is used by Si7021MonitorPoll() to track the internal state. The
// caller should initialize 'device_index' to zero before the first call to
// Si7021MonitorPoll() then not set it again. It's value should not be used
// outside of calls to Si7021MonitorPoll(). This function returns true when
// the I2C bus returns to idle and it is safe to call another monitoring
// function.
bool Si7021MonitorPoll(const Si7021Monitors *config,
                       Si7021OutputFunction output_function,
                       uint32_t *device_index, Si7021 *devices);

#endif  // AVIONICS_FIRMWARE_MONITORS_SI7021_H_
