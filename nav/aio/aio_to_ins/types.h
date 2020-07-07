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

#ifndef NAV_AIO_AIO_TO_INS_TYPES_H_
#define NAV_AIO_AIO_TO_INS_TYPES_H_

#include <stdbool.h>
#include <stdint.h>

#include "avionics/network/aio_node.h"
#include "nav/ins/messages/message_types.h"
#include "nav/ins/messages/messages.h"

// Called for each new InsMessage.
typedef void (* const NewInsMessageFunction)(const InsMessage *m, void *arg);

typedef struct {
  // Label type is specific to the InsMessageType. For example,
  // kInsMessageTypeInertial references the InsImuLabel enum.
  int32_t label[kNumInsMessageTypes][kNumAioNodes];
  bool valid[kNumInsMessageTypes][kNumAioNodes];
} AioSourceToInsLabelMap;

#endif  // NAV_AIO_AIO_TO_INS_TYPES_H_
