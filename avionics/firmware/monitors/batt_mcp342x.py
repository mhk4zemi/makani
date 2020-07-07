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

"""Batt MCP342X hardware monitor configuration."""

from makani.avionics.firmware.drivers import mcp342x_types
from makani.avionics.firmware.serial import batt_serial_params as rev

mcp342x_default = {
    'name': '',
    'address': 0x0,
    'channel': mcp342x_types.kMcp342xChannel1,
    'polarity': mcp342x_types.kMcp342xPolarityPositive,
    'mode': mcp342x_types.kMcp342xModeSingle,
    'sps': mcp342x_types.kMcp342xSps15,
    'gain': mcp342x_types.kMcp342xGain1X,
}

ch1_pos = dict(mcp342x_default, **{
    'channel': mcp342x_types.kMcp342xChannel1,
    'polarity': mcp342x_types.kMcp342xPolarityPositive,
})

ch2_pos = dict(mcp342x_default, **{
    'channel': mcp342x_types.kMcp342xChannel2,
    'polarity': mcp342x_types.kMcp342xPolarityPositive,
})

ch3_pos = dict(mcp342x_default, **{
    'channel': mcp342x_types.kMcp342xChannel3,
    'polarity': mcp342x_types.kMcp342xPolarityPositive,
})

ch4_pos = dict(mcp342x_default, **{
    'channel': mcp342x_types.kMcp342xChannel4,
    'polarity': mcp342x_types.kMcp342xPolarityPositive,
})

rev_all = [
    dict(ch1_pos, name='heat_plate_1', address=0x68),
    dict(ch2_pos, name='heat_plate_2', address=0x68),
    dict(ch3_pos, name='batteries_1', address=0x68),
    dict(ch4_pos, name='batteries_2', address=0x68),
]

mcp342x_config = (rev.BattHardware, {
    rev.BattHardware.SMALL_CELL15_V1: rev_all,
    rev.BattHardware.BIG_CELL18_V1: rev_all,
    rev.BattHardware.SMALL_CELL15_AA: rev_all,
    rev.BattHardware.BIG_CELL18_AA: rev_all,
    rev.BattHardware.SMALL_CELL15_AB: rev_all,
    rev.BattHardware.BIG_CELL18_AB: rev_all,
    rev.BattHardware.SMALL_CELL17_AB: rev_all,
    rev.BattHardware.SMALL_CELL15_AC: rev_all,
    rev.BattHardware.BIG_CELL18_AC: rev_all,
    rev.BattHardware.SMALL_CELL17_AC: rev_all,
    rev.BattHardware.SMALL_CELL17_AD: rev_all,
})
