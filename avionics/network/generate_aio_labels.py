#!/usr/bin/python
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


"""Generate the aio_labels.[ch] and aio_labels_test.cc files."""

import os
import re
import sys
import textwrap

from makani.avionics.network import network_config
from makani.lib.python import string_util


def _GetLabelNames(config, label_name):
  """Gets a bunch of useful strings and names associated with a label.

  Args:
    config: A NetworkConfig.
    label_name: The kind name in snake_case.
  Returns:
    Dict { 'labels': A sorted list of label names.
           'nodes': A sorted list of AioNode names.
           'camel_suffixes': A sorted list of camel-cased short names.
           'force_signed_label': 'kFooLabelForceSigned' for kind 'foo'.
           'label_count': 'kNumFoos' for kind 'foo'.
           'camel_name': The name of kind in CamelCase.
           'snake_name': The name of kind in snake_case.
         }
  """

  camel_name = string_util.SnakeToCamel(label_name)
  label_count = 'kNum%s' % string_util.GetPlural(camel_name)
  force_signed_label = 'k%sLabelForceSigned' % camel_name

  instances = config.GetAioNodesByLabel(label_name)
  if next(iter(instances)).snake_name.startswith(label_name):
    snake_prefix = label_name
  else:
    snake_prefix = os.path.commonprefix([n.snake_name for n in instances])
  camel_prefix = string_util.SnakeToCamel(snake_prefix)
  snake_suffixes = [n.snake_name[len(snake_prefix):] for n in instances]
  camel_suffixes = [string_util.SnakeToCamel(s) for s in snake_suffixes]
  if any(not x for x in camel_suffixes):
    # This only happens on unique items.
    assert len(camel_suffixes) == 1
    camel_suffixes = [camel_prefix]
    nodes = ['kAioNode%s' % camel_prefix]
    labels = ['k%s' % camel_prefix]
  else:
    nodes = []
    labels = []
    for i in range(len(camel_suffixes)):
      camel = camel_suffixes[i]
      nodes.append('kAioNode%s%s' % (camel_prefix, camel))
      labels.append('k%s%s' % (camel_name, camel))
  return {'labels': labels,
          'nodes': nodes,
          'camel_suffixes': camel_suffixes,
          'force_signed_label': force_signed_label,
          'label_count': label_count,
          'camel_name': camel_name,
          'snake_name': label_name,
         }


def _WriteAioLabelsHeader(script_name, file_without_extension, rel_path,
                          config):
  """Write aio_labels.h.

  Args:
    script_name: This script's filename.
    file_without_extension: The full path to the output file, missing the '.h'.
    rel_path: The relative path from the autogenerated files root to our output
              file.
    config: A NetworkConfig.
  """
  header_guard = re.sub('[/.]', '_', rel_path.upper()) + '_H_'
  parts = [textwrap.dedent("""
      #ifndef {guard}
      #define {guard}

      // Generated by {name}; do not edit.

      #include "avionics/network/aio_node.h"

      #ifdef __cplusplus
      extern "C" {{
      #endif
      """[1:]).format(name=script_name, guard=header_guard)]

  for label in config.aio_labels:
    if label == 'unknown':
      continue
    info = _GetLabelNames(config, label)
    parts.append('typedef enum {')
    parts.append('  %s = -1,' % info['force_signed_label'])
    for label in info['labels']:
      parts.append('  %s,' % label)
    parts.append('  %s' % info['label_count'])
    parts.append('} %sLabel;\n' % info['camel_name'])

  for label in config.aio_labels:
    if label == 'unknown':
      continue
    parts.append(textwrap.dedent("""
        AioNode {0}LabelTo{0}AioNode({0}Label {1}_label);
        {0}Label {0}AioNodeTo{0}Label(AioNode {1}_node);"""[1:]).format(
            string_util.SnakeToCamel(label), label))

  for label in config.aio_labels:
    if label == 'unknown':
      continue
    parts.append(textwrap.dedent("""
        const char *{0}LabelToString({0}Label {1}_label);"""[1:]).format(
            string_util.SnakeToCamel(label), label))

  parts.append(textwrap.dedent("""
      #ifdef __cplusplus
      }}  // extern "C"
      #endif

      #endif  // {guard}
      """[1:]).format(guard=header_guard))

  with open(file_without_extension + '.h', 'w') as f:
    f.write('\n'.join(parts))


def _WriteAioLabelsSource(script_name, file_without_extension, rel_path,
                          config):
  """Write aio_labels.c.

  Args:
    script_name: This script's filename.
    file_without_extension: The full path to the output file, missing the '.c'.
    rel_path: The relative path from the autogenerated files root to our output
              file.
    config: A NetworkConfig.
  """
  parts = [textwrap.dedent("""
      // Generated by {name}; do not edit.

      #include "{header}"

      #include <assert.h>
      #include <stdbool.h>

      #include "avionics/network/aio_node.h"
      """[1:]).format(name=script_name, header=rel_path + '.h')]

  for label in config.aio_labels:
    if label == 'unknown':
      continue
    info = _GetLabelNames(config, label)
    snake_name = info['snake_name']
    camel_name = info['camel_name']
    label_count = info['label_count']
    first_node = config.GetAioNodesByLabel(label)[0].enum_name

    parts.append(textwrap.dedent("""
        AioNode {name}LabelTo{name}AioNode({name}Label {snake_name}_label) {{
          if ({snake_name}_label >= 0 &&
              {snake_name}_label < {label_count}) {{
            return (AioNode)({first_node} + {snake_name}_label);
          }}
          return kAioNodeUnknown;
        }}

        {name}Label {name}AioNodeTo{name}Label(AioNode {snake_name}_node) {{
          assert(Is{name}Node({snake_name}_node));
          return ({name}Label)({snake_name}_node - {first_node});
        }}
        """[1:]).format(name=camel_name, snake_name=snake_name,
                        first_node=first_node, label_count=label_count))

    parts.append(textwrap.dedent("""
        const char *{name}LabelToString({name}Label {snake_name}_label) {{
          switch ({snake_name}_label) {{"""[1:]).format(name=camel_name,
                                                        snake_name=snake_name))
    for label, short_name in zip(info['labels'], info['camel_suffixes']):
      parts.append('    case %s:' % label)
      parts.append('      return "%s";' % short_name)

    parts.append(textwrap.dedent("""
            default:
            case {force_signed_label}:
            case {label_count}:
              assert(false);
              return "<Unknown>";
          }}
        }}
        """[1:]).format(force_signed_label=info['force_signed_label'],
                        label_count=label_count))

  with open(file_without_extension + '.c', 'w') as f:
    f.write('\n'.join(parts))


def _WriteAioLabelsTest(script_name, file_name, rel_path, config):
  """Write aio_labels_test.cc.

  Args:
    script_name: This script's filename.
    file_name: The full path to the output file.
    rel_path: The relative path from the autogenerated files root to our output
              file's header.
    config: A NetworkConfig.
  """
  parts = [textwrap.dedent("""
      // Generated by {name}; do not edit.

      #include <gtest/gtest.h>

      #include <functional>
      #include <vector>

      #include "{header}"
      #include "avionics/network/aio_node.h"

      namespace {{
      template <uint32_t size, typename T, typename U>
      void ExpectConversionEq(const std::array<T, size> &ts,
                              const std::array<U, size> &us,
                              const std::function<T(U)> &u_to_t,
                              const std::function<U(T)> &t_to_u) {{
        for (uint32_t i = 0; i < size; ++i) {{
          EXPECT_EQ(ts[i], u_to_t(us[i]));
          EXPECT_EQ(us[i], t_to_u(ts[i]));
        }}
      #ifndef NDEBUG
        EXPECT_DEATH(u_to_t((U)((int32_t)us[0] + size)), "");
        EXPECT_DEATH(u_to_t((U)(-1)), "");
      #endif  // NDEBUG
        EXPECT_EQ(kAioNodeUnknown, t_to_u((T)(-1)));
        EXPECT_EQ(kAioNodeUnknown, t_to_u((T)(size)));
      }}
      }}  // namespace
      """[1:]).format(name=script_name, header=rel_path)]

  for label in config.aio_labels:
    if label == 'unknown':
      continue
    info = _GetLabelNames(config, label)
    camel_name = info['camel_name']
    nodes = ''
    labels = ''
    count = len(info['labels'])
    for i in range(count):
      nodes += info['nodes'][i]
      labels += info['labels'][i]
      if i < count - 1:
        nodes += (',')
        labels += (',')
        if i % 4 == 3:
          nodes += ('\n       ')
          labels += ('\n       ')
        else:
          nodes += (' ')
          labels += (' ')

    parts.append(textwrap.dedent("""
        TEST({name}, All) {{
          ExpectConversionEq<{label_count}, {name}Label, AioNode>(
              {{{labels}}},
              {{{nodes}}},
              {name}AioNodeTo{name}Label,
              {name}LabelTo{name}AioNode);
        }}
        """[1:]).format(name=camel_name, labels=labels,
                        nodes=nodes, label_count=info['label_count']))

  parts.append(textwrap.dedent("""
      int main(int argc, char **argv) {
        ::testing::InitGoogleTest(&argc, argv);
        return RUN_ALL_TESTS();
      }
      """[1:]))

  with open(file_name, 'w') as f:
    f.write('\n'.join(parts))


def _WriteAioLabels(autogen_root, output_dir, script_name, config):
  aio_labels_without_extension = os.path.join(output_dir, 'aio_labels')
  rel_path = os.path.relpath(aio_labels_without_extension, autogen_root)
  aio_labels_test_file = os.path.join(output_dir, 'aio_labels_test.cc')

  _WriteAioLabelsHeader(script_name, aio_labels_without_extension, rel_path,
                        config)
  _WriteAioLabelsSource(script_name, aio_labels_without_extension, rel_path,
                        config)
  _WriteAioLabelsTest(script_name, aio_labels_test_file, rel_path + '.h',
                      config)


def main(argv):
  flags, argv = network_config.ParseGenerationFlags(argv)

  config = network_config.NetworkConfig(flags.network_file)
  script_name = os.path.basename(argv[0])
  _WriteAioLabels(flags.autogen_root, flags.output_dir, script_name,
                  config)

if __name__ == '__main__':
  main(sys.argv)
