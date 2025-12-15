# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Utilities for transcription text handling."""

PUNCTUATION_CHARS = {'.', '!', '?', ';', ':', "'"}


def join_fragment(existing_tx: str, new_chunk: str) -> str:
  """Join transcription fragments preserving proper spacing.

  Handles three special cases:
  - Leading punctuation on the new chunk (attach without space).
  - Leading apostrophe followed by 's' (contraction, attach without space).
  - Leading apostrophe followed by other letters (plural possessive):
    move apostrophe to end of existing and insert a space before remainder.

  Also avoids introducing double spaces when `existing` already ends
  with whitespace.
  """
  new_stripped = new_chunk.strip()
  if not new_stripped:
    return existing_tx

  # If the existing text ends with an apostrophe and the new fragment
  # starts with 's' (continuation of a contraction), attach without
  # a space: "That'" + "s great" -> "That's great".
  if existing_tx.rstrip().endswith("'") and new_stripped[0].lower() == 's':
    return existing_tx.rstrip() + new_stripped

  # Leading apostrophe handling when the new fragment itself starts
  # with an apostrophe (e.g. "'s great" or "'job?").
  if new_stripped[0] == "'" and len(new_stripped) > 1:
    remainder = new_stripped[1:]
    # contraction like "'s": attach directly (That's)
    if remainder[0].lower() == 's':
      # If existing already ends with an apostrophe, don't add another.
      if existing_tx.rstrip().endswith("'"):
        return existing_tx.rstrip() + remainder
      return existing_tx.rstrip() + "'" + remainder
    # possessive like "'job": attach apostrophe to previous word,
    # then add a space before the remainder (parents' job)
    base = existing_tx.rstrip()
    if not base.endswith("'"):
      base = base + "'"
    return base + ' ' + remainder

  # Leading punctuation attaches without a space (e.g. ? , !)
  if new_stripped[0] in PUNCTUATION_CHARS:
    return existing_tx.rstrip() + new_stripped

  # Default: add a space if existing doesn't already end with whitespace
  if existing_tx and not existing_tx.endswith((' ', '\t', '\n')):
    return existing_tx + ' ' + new_stripped
  return existing_tx + new_stripped
