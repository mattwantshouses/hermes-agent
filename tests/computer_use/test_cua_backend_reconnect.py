"""Tests for `_CuaDriverSession`'s reconnect-on-failure classification.

2026-07-07 incident: the daemon (`cua-driver serve`) was healthy, but the
Hermes-side stdio proxy (`cua-driver mcp`) was wedged — its transport
neither closed cleanly nor responded, so every `call_tool` timed out at 30s
via `concurrent.futures.TimeoutError` from `_AsyncBridge.run`. The reconnect
path only fired on "closed" exceptions (ClosedResourceError etc.), not on
TimeoutError, so the wedge never self-healed; it took a manual
`pkill -f 'cua-driver mcp'` + gateway restart to recover. These tests pin
`_is_closed_session_error` to also treat TimeoutError as recoverable.
"""

from __future__ import annotations

import concurrent.futures

from tools.computer_use.cua_backend import _CuaDriverSession


class TestIsClosedSessionError:
    def test_concurrent_futures_timeout_error_is_recoverable(self):
        assert _CuaDriverSession._is_closed_session_error(
            concurrent.futures.TimeoutError()
        )

    def test_builtin_timeout_error_is_recoverable(self):
        assert _CuaDriverSession._is_closed_session_error(TimeoutError())

    def test_broken_pipe_error_is_recoverable(self):
        assert _CuaDriverSession._is_closed_session_error(BrokenPipeError())

    def test_eof_error_is_recoverable(self):
        assert _CuaDriverSession._is_closed_session_error(EOFError())

    def test_unrelated_value_error_is_not_recoverable(self):
        assert not _CuaDriverSession._is_closed_session_error(ValueError("boom"))
