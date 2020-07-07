;; Copyright 2020 Makani Technologies LLC
;;
;; Licensed under the Apache License, Version 2.0 (the "License");
;; you may not use this file except in compliance with the License.
;; You may obtain a copy of the License at
;;
;;      http://www.apache.org/licenses/LICENSE-2.0
;;
;; Unless required by applicable law or agreed to in writing, software
;; distributed under the License is distributed on an "AS IS" BASIS,
;; WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
;; See the License for the specific language governing permissions and
;; limitations under the License.

(add-to-list 'load-path (format "%s/%s"
                                (getenv "MAKANI_HOME")
                                "lib/scripts/style"))
(require 'google-c-style)
(defun apply-google-style ()
  "Format the whole buffer."
  ;; Treat all .h and .cc files as C++ files.
  (unless (string= (file-name-extension buffer-file-name) "c")
    (c++-mode))
  (google-set-c-style)
  (untabify (point-min) (point-max))
  (indent-region (point-min) (point-max) nil)
  (princ (buffer-substring-no-properties (point-min) (point-max))))
