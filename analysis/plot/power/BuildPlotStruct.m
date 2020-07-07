% Copyright 2020 Makani Technologies LLC
%
% Licensed under the Apache License, Version 2.0 (the "License");
% you may not use this file except in compliance with the License.
% You may obtain a copy of the License at
%
%      http://www.apache.org/licenses/LICENSE-2.0
%
% Unless required by applicable law or agreed to in writing, software
% distributed under the License is distributed on an "AS IS" BASIS,
% WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
% See the License for the specific language governing permissions and
% limitations under the License.

function [s] = BuildPlotStruct(message_type, plot_function, plot_type, title_string, ...
               var_name, y_string, math_cell, deal_plots, labels, s)
%BuildPlotStruct Creates and appends a plot record
%
% [s] = BuildPlotStruct(data_source, plot_function, plot_type, title_string, ...
%               var_name, y_string, math_cell, deal_plots, labels, s)
% BuildPlotStruct creates a plot description to be used by PlotStacking.  If a
% math description is included, it will also create a description of a new data
% element that will be generated by GenerateDerivedValue within PlotStacking.
%
% Arguments
%
% message_type: kMessageType for this plot
% plot_function: Name of function to plot with:
%                         'PlotMotorData' - Standard plot
%                         'PlotMotorSumData' - Various forms of summed data
%                         'PlotMotorDiffData' - Plot pair difference
%                         'PlotMotorTempData' - Plot temperature data
%                         'PlotMotorArrayData' - Plot data stored in array
% plot_type: Optional (use [] to ignore) sub plot specifier
% title_string: String to put on plot title
% var_name: Variable to plot - use cell array to plot multiple items together
% y_string: String to use on y axis
% math_cell: Cell array describing a new variable to create ([] to ignore):
%                         {1}: String of anonymous function
%                         {2}: Input variables, consistent with input number
%                         {3}: New variable name
%                         {4}: Alternate header if variable is not in message
% deal_plots: True/False.  Dealt plots will generate one plot per motor
% labels: Alternative legend, used in array plots
% s: Structure to add data to
%
% Return values
%
% s: Structure containing directives for PlotStacking
%
% Required toolboxes: None.
    snew = struct('message_type', message_type, 'plot_function', plot_function, ...
      'plot_type', plot_type, 'title_string', title_string, ...
      'var_name', {var_name}, 'y_string', y_string, 'labels', {labels});

    snew.deal_plots = logical(deal_plots);

    if isempty(math_cell)
      snew.var_math = [];
    else
      snew.var_math = struct('math', math_cell{1}, 'input', {math_cell{2}}, ...
                          'output', math_cell{3}, 'header', math_cell{4});
    end

    s = [s,snew];
end
