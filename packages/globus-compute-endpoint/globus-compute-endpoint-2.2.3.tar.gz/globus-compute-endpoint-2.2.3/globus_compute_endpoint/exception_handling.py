"""
This module provides helpers for constructing the internal dict objects which get passed
around and ultimately converted into funcx_common.messagepack.Result objects

IDEALLY this would be refactored to produce and return Result objects directly, which
could then be passed around internally instead of raw dicts
but we don't have time to do that (even though it would be better (a lot better))
"""

from __future__ import annotations

import sys
import traceback
import types
import typing as t

from globus_compute_endpoint.exceptions import CouldNotExecuteUserTaskError
from globus_compute_sdk.errors import MaxResultSizeExceeded

INTERNAL_ERROR_CLASSES: tuple[type[Exception], ...] = (
    CouldNotExecuteUserTaskError,
    MaxResultSizeExceeded,
)


def _typed_excinfo(
    exc: Exception | None = None,
) -> tuple[type[Exception], Exception, types.TracebackType]:
    if exc:
        return type(exc), exc, exc.__traceback__  # type: ignore
    return t.cast(
        t.Tuple[t.Type[Exception], Exception, types.TracebackType],
        sys.exc_info(),
    )


def _inner_traceback(tb: types.TracebackType, levels: int = 2) -> types.TracebackType:
    while levels > 0:
        tb = tb.tb_next if tb.tb_next is not None else tb
        levels -= 1
    return tb


def get_error_string(*, exc: t.Any | None = None, tb_levels: int = 2) -> str:
    exc_info = _typed_excinfo(exc)
    exc_type, exc, tb = exc_info
    if isinstance(exc, INTERNAL_ERROR_CLASSES):
        return repr(exc)
    return "".join(
        traceback.format_exception(
            exc_type, exc, _inner_traceback(tb, levels=tb_levels)
        )
    )


def get_result_error_details(exc: BaseException | None = None) -> tuple[str, str]:
    _, error, _ = _typed_excinfo(exc)  # type: ignore
    # code, user_message
    if isinstance(error, INTERNAL_ERROR_CLASSES):
        return type(error).__name__, f"remote error: {error}"
    return (
        "RemoteExecutionError",
        "An error occurred during the execution of this task",
    )
