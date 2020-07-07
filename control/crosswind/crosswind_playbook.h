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

#ifndef CONTROL_CROSSWIND_CROSSWIND_PLAYBOOK_H_
#define CONTROL_CROSSWIND_CROSSWIND_PLAYBOOK_H_

#include "control/crosswind/crosswind_playbook_types.h"

#ifdef __cplusplus
extern "C" {
#endif

double AdjustHalfConeAziOffsetForElevation(const double half_cone_angle,
                                           const double elevation);

void GetPlaybookEntry(const Playbook *playbook, const PlaybookEntry *fallback,
                      double wind_speed, double fallback_crossfade,
                      PlaybookEntry *pb_entry_interp);

double GetPlaybookEntryAzimuthWithLimits(double wind_dir,
                                         const PlaybookEntry *playbook_entry);

#ifdef __cplusplus
}  // extern "C"
#endif

#endif  // CONTROL_CROSSWIND_CROSSWIND_PLAYBOOK_H_
