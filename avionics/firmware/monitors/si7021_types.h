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

#ifndef AVIONICS_FIRMWARE_MONITORS_SI7021_TYPES_H_
#define AVIONICS_FIRMWARE_MONITORS_SI7021_TYPES_H_

#include <stdint.h>

#include "avionics/firmware/drivers/si7021_types.h"

typedef struct {
  int32_t monitor;
  Si7021Config config;
} Si7021Monitor;

typedef struct {
  uint32_t populated;
  int32_t num_devices;
  const Si7021Monitor *device;
} Si7021Monitors;

#endif  // AVIONICS_FIRMWARE_MONITORS_SI7021_TYPES_H_
