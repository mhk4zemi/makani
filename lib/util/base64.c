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

#include "lib/util/base64.h"

#include <stdint.h>
#include <glib.h>

void Base64Free(void *str) {
  g_free((gchar *)str);
}

char *Base64Encode(const void *buf, uint32_t len) {
  gsize sz = (gsize)len;
  return g_base64_encode((const guchar *)buf, sz);
}

void *Base64Decode(const char *buf, uint32_t *len) {
  gsize sz;
  guchar *decode = g_base64_decode((const gchar *)buf, &sz);
  *len = (uint32_t)sz;
  return decode;
}
