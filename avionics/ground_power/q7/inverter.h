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

#ifndef AVIONICS_GROUND_POWER_Q7_INVERTER_H_
#define AVIONICS_GROUND_POWER_Q7_INVERTER_H_

#include <modbus.h>
#include <stdbool.h>

#include "avionics/ground_power/q7/inverter_types.h"

typedef struct {
  uint8_t id;
  modbus_t *mb;
  bool mb_status;
} Inverter;

typedef struct {
  int32_t size;
  Inverter inverter_array[kNumInverters];
} InverterBank;

typedef struct {
  uint16_t modbus_register;
  uint16_t modbus_datalen;
} InverterModbusReadParam;

void InverterBankInit(InverterBank *inverters);
void *InverterCommunication(void *inverter_arg);
#endif  // AVIONICS_GROUND_POWER_Q7_INVERTER_H_
