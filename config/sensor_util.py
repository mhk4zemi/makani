# Copyright 2020 Makani Technologies LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Utility functions for constructing sensor parameters."""

import numpy as np


def MakeEncoderParams(bias=0.0, steps_per_revolution=8192,
                      noise_level_counts=0.0, scale=1.0):
  quantization = 2.0 * np.pi / float(steps_per_revolution)
  return {
      'bias': bias,
      'scale': scale,
      'noise_level': quantization * noise_level_counts,
      'bound_low': -np.pi,
      'bound_high': np.pi,
      'quantization': quantization
  }
