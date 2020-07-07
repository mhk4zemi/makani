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

#include "avionics/fc/firmware/monitor.h"

#include <assert.h>
#include <stdbool.h>
#include <stdint.h>

#include "avionics/fc/firmware/output.h"
#include "avionics/firmware/identity/identity.h"
#include "avionics/firmware/monitors/aio.h"
#include "avionics/firmware/monitors/fc.h"
#include "avionics/firmware/serial/aio_serial_params.h"
#include "avionics/firmware/serial/board_serial.h"
#include "avionics/firmware/serial/fc_serial_params.h"
#include "common/macros.h"

// This file defines the flight computer hardware monitoring configuration.

static FcMonitorData* g_fc_monitor;
static AioModuleMonitorData* g_aio_monitor;

static bool PollFc(void) {
  return FcMonitorPoll(kFcHardwareRevBa, g_fc_monitor);
}

void FcMonInit(FcMonitorData* fc_monitor, AioModuleMonitorData* aio_monitor) {
  AioMonitorInit();
  FcMonitorInit();
  g_fc_monitor = fc_monitor;
  g_aio_monitor = aio_monitor;
}

void FcMonPoll(void) {
  switch (BootConfigGetHardwareType()) {
    case kHardwareTypeAio:
      AioMonitorPollStack(GetBoardHardwareRevision(), g_aio_monitor, PollFc);
      break;
    case kHardwareTypeFc:
      // TODO: The rev -000AB flight computer function as the main
      // board and uses an instrumentation board to interface to the sensors.
      // Remove when fully deprecated.
      FcMonitorPoll(kFcHardwareRevAb, g_fc_monitor);
      break;
    case kHardwareTypeCs:
    case kHardwareTypeMotor:
    case kHardwareTypeServo:
    case kHardwareTypeUnknown:
    default:
      assert(false);
      break;
  }
}
