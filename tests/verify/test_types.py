"""Result contract for M2 (plan §7.1 wave 0): the types encode the honesty rules."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from caxgauge.verify.types import (
    NECESSARY_NOT_SUFFICIENT,
    BrowserResult,
    CheckResult,
    PreflightResult,
    RenderedView,
    RenderResult,
    Status,
)


def _result(*statuses: Status) -> PreflightResult:
    return PreflightResult(
        checks=tuple(
            CheckResult(name=f"check_{i}", status=s, detail="d") for i, s in enumerate(statuses)
        )
    )


def test_all_pass_is_green_but_labelled_necessary_not_sufficient():
    result = _result(Status.PASS, Status.PASS)
    assert result.green
    assert not result.hard_fail
    assert "necessary" in NECESSARY_NOT_SUFFICIENT.lower()
    assert "not sufficient" in NECESSARY_NOT_SUFFICIENT.lower()
    assert "verified" not in NECESSARY_NOT_SUFFICIENT.lower()


def test_any_fail_is_a_hard_fail_and_not_green():
    result = _result(Status.PASS, Status.FAIL, Status.SKIP)
    assert result.hard_fail
    assert not result.green


def test_skip_never_counts_toward_green():
    result = _result(Status.PASS, Status.SKIP)
    assert not result.hard_fail
    assert not result.green


def test_skipped_names_which_checks_had_no_bound():
    result = PreflightResult(
        checks=(
            CheckResult(name="watertight", status=Status.PASS, detail="closed"),
            CheckResult(name="bbox", status=Status.SKIP, detail="no --envelope given"),
            CheckResult(name="volume", status=Status.SKIP, detail="no --volume-band given"),
        )
    )
    assert [c.name for c in result.skipped] == ["bbox", "volume"]
    assert "--envelope" in result.skipped[0].detail


def test_no_checks_is_not_green():
    assert not PreflightResult(checks=()).green


def test_results_are_immutable():
    check = CheckResult(name="bbox", status=Status.PASS, detail="d")
    with pytest.raises(ValidationError):
        check.status = Status.FAIL  # type: ignore[misc]


def test_browser_result_fails_on_any_captured_error_class():
    clean = BrowserResult(status=Status.PASS, detail="loaded")
    assert not clean.hard_fail
    for field in ("console_errors", "page_errors", "network_failures"):
        dirty = BrowserResult(status=Status.FAIL, detail="x", **{field: ("boom",)})
        assert dirty.hard_fail


def test_browser_result_rejects_pass_with_captured_errors():
    with pytest.raises(ValidationError):
        BrowserResult(status=Status.PASS, detail="x", page_errors=("SyntaxError",))


def test_browser_skip_when_tooling_absent_is_not_a_fail():
    skipped = BrowserResult(status=Status.SKIP, detail="polyfetch/Chromium absent")
    assert not skipped.hard_fail


def test_render_result_pass_with_one_view_per_requested():
    result = RenderResult(
        status=Status.PASS,
        detail="2 view(s) captured",
        requested_views=("front", "iso"),
        views=(
            RenderedView(name="front", path=Path("front.png")),
            RenderedView(name="iso", path=Path("iso.png")),
        ),
    )
    assert not result.hard_fail
    assert [v.name for v in result.views] == ["front", "iso"]


def test_render_result_pass_rejects_partial_views():
    with pytest.raises(ValidationError):
        RenderResult(
            status=Status.PASS,
            detail="only one captured",
            requested_views=("front", "iso"),
            views=(RenderedView(name="front", path=Path("front.png")),),
        )


def test_render_result_pass_rejects_wrong_or_reordered_names():
    with pytest.raises(ValidationError):
        RenderResult(
            status=Status.PASS,
            detail="mismatched",
            requested_views=("front", "iso"),
            views=(
                RenderedView(name="iso", path=Path("iso.png")),
                RenderedView(name="front", path=Path("front.png")),
            ),
        )


def test_render_result_fail_is_hard_fail_and_may_carry_partial_views():
    result = RenderResult(
        status=Status.FAIL,
        detail="render failed: top: exit 1: boom",
        requested_views=("front", "top"),
        views=(RenderedView(name="front", path=Path("front.png")),),
    )
    assert result.hard_fail
    assert "verified" not in result.detail.lower()


def test_render_result_skip_when_polyfetch_absent_is_not_a_fail():
    skipped = RenderResult(
        status=Status.SKIP,
        detail="no render: polyfetch unavailable",
        requested_views=("front", "iso", "top", "right"),
    )
    assert not skipped.hard_fail
    assert skipped.views == ()


def test_render_result_is_immutable():
    result = RenderResult(status=Status.FAIL, detail="d", requested_views=("front",), views=())
    with pytest.raises(ValidationError):
        result.status = Status.PASS  # type: ignore[misc]
