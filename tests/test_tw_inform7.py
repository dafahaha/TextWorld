# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT license.

"""Tests for the Inform7 wrapper helpers."""

import sys
from unittest import mock

# Jericho imports cleanly on Linux/macOS but not on every platform.
# The parsing helpers tested here do not use it, so stub it out when
# the real package cannot be loaded.
try:
    import jericho  # noqa: F401
except Exception:  # pragma: no cover - platform dependent
    sys.modules["jericho"] = mock.MagicMock()
    sys.modules["jericho.jericho"] = mock.MagicMock()

from textworld.envs.wrappers.tw_inform7 import _detect_extra_infos


def test_detect_extra_infos_with_multiple_commands():
    # Several commands on one line (e.g. "go north. go east.") make the
    # Inform7 interpreter print one set of extra-info tags per command.
    text = (
        "You head north.\n"
        "<score>\n0\n</score>\n"
        "<moves>\n1\n</moves>\n"
        "You head east.\n"
        "<score>\n0\n</score>\n"
        "<moves>\n2\n</moves>\n"
    )
    matches, cleaned = _detect_extra_infos(
        text, tracked_infos=["score", "moves"]
    )

    # The value from the last command is the one that reflects the
    # current game state.
    assert matches["score"] == "0"
    assert matches["moves"] == "2"
    assert "<score>" not in cleaned
    assert "<moves>" not in cleaned


def test_detect_extra_infos_single_command():
    text = (
        "You head north.\n"
        "<score>\n0\n</score>\n"
        "<moves>\n1\n</moves>\n"
    )
    matches, cleaned = _detect_extra_infos(
        text, tracked_infos=["score", "moves"]
    )
    assert matches["score"] == "0"
    assert matches["moves"] == "1"
    assert "<score>" not in cleaned
    assert "<moves>" not in cleaned
