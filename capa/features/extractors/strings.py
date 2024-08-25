# strings code from FLOSS, https://github.com/mandiant/flare-floss
#
# Copyright (C) 2020 Mandiant, Inc. All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
# You may obtain a copy of the License at: [package root]/LICENSE.txt
# Unless required by applicable law or agreed to in writing, software distributed under the License
#  is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

import re
import contextlib
from collections import namedtuple

ASCII_BYTE = r" !\"#\$%&\'\(\)\*\+,-\./0123456789:;<=>\?@ABCDEFGHIJKLMNOPQRSTUVWXYZ\[\]\^_`abcdefghijklmnopqrstuvwxyz\{\|\}\\\~\t".encode(
    "ascii"
)
DEFAULT_LENGTH = 4
ASCII_RE_DEFAULT = re.compile(b"([%s]{%d,})" % (ASCII_BYTE, DEFAULT_LENGTH))
UNICODE_RE_DEFAULT = re.compile(b"((?:[%s]\x00){%d,})" % (ASCII_BYTE, DEFAULT_LENGTH))
REPEATS = [b"A", b"\x00", b"\xfe", b"\xff"]
SLICE_SIZE = 4096

String = namedtuple("String", ["s", "offset"])


def buf_filled_with(buf, character):
    dupe_chunk = character * SLICE_SIZE
    for offset in range(0, len(buf), SLICE_SIZE):
        new_chunk = buf[offset : offset + SLICE_SIZE]
        if dupe_chunk[: len(new_chunk)] != new_chunk:
            return False
    return True


def extract_ascii_strings(buf, min_len=DEFAULT_LENGTH):
    """
    Extract ASCII strings from the given binary data.

    :param buf: A bytestring.
    :type buf: str
    :param min_len: The minimum length of strings to extract.
    :type min_len: int
    :rtype: Sequence[String]
    """

    if not buf:
        return

    if (buf[0] in REPEATS) and buf_filled_with(buf, buf[0]):
        return

    r = None
    if min_len == DEFAULT_LENGTH:
        r = ASCII_RE_DEFAULT
    else:
        reg = b"([%s]{%d,})" % (ASCII_BYTE, min_len)
        r = re.compile(reg)
    for match in r.finditer(buf):
        yield String(match.group().decode("ascii"), match.start())


def extract_unicode_strings(buf, min_len=DEFAULT_LENGTH):
    """
    Extract naive UTF-16 strings from the given binary data.

    :param buf: A bytestring.
    :type buf: str
    :param min_len: The minimum length of strings to extract.
    :type min_len: int
    :rtype: Sequence[String]
    """

    if not buf:
        return

    if (buf[0] in REPEATS) and buf_filled_with(buf, buf[0]):
        return

    if min_len == DEFAULT_LENGTH:
        r = UNICODE_RE_DEFAULT
    else:
        reg = b"((?:[%s]\x00){%d,})" % (ASCII_BYTE, min_len)
        r = re.compile(reg)
    for match in r.finditer(buf):
        with contextlib.suppress(UnicodeDecodeError):
            yield String(match.group().decode("utf-16"), match.start())
