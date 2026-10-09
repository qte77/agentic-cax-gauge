"""Result contract shared by preflight, browser, report and CLI (plan §7.1 wave 0).

The types encode the honesty rules (`.claude/rules/verification-honesty.md`): a `SKIP` never
counts toward green, and green is only ever *necessary, not sufficient*.
"""

from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, model_validator

NECESSARY_NOT_SUFFICIENT = (
    "Green is necessary, not sufficient: these checks cannot see local defects. "
    "Look at the render and decide."
)


class Status(StrEnum):
    """Outcome of one check. `SKIP` means nothing was checked — never a pass."""

    PASS = "pass"  # noqa: S105 — a check outcome, not a credential
    FAIL = "fail"
    SKIP = "skip"


class CheckResult(BaseModel):
    """One check's outcome; `detail` says what was measured, or why it was skipped."""

    model_config = ConfigDict(frozen=True)

    name: str
    status: Status
    detail: str


class PreflightResult(BaseModel):
    """All deterministic checks for one mesh."""

    model_config = ConfigDict(frozen=True)

    checks: tuple[CheckResult, ...]

    @property
    def hard_fail(self) -> bool:
        """Whether any check failed."""
        return any(c.status is Status.FAIL for c in self.checks)

    @property
    def skipped(self) -> tuple[CheckResult, ...]:
        """Checks that ran without a bound, so checked nothing."""
        return tuple(c for c in self.checks if c.status is Status.SKIP)

    @property
    def green(self) -> bool:
        """Whether every check passed. A `SKIP` or an empty result is never green."""
        return bool(self.checks) and all(c.status is Status.PASS for c in self.checks)


class BrowserResult(BaseModel):
    """Headless load check: did the mesh parse and render at all (plan §9.2)."""

    model_config = ConfigDict(frozen=True)

    status: Status
    detail: str
    console_errors: tuple[str, ...] = ()
    page_errors: tuple[str, ...] = ()
    network_failures: tuple[str, ...] = ()

    @model_validator(mode="after")
    def _no_pass_with_errors(self) -> Self:
        if self.status is Status.PASS and (
            self.console_errors or self.page_errors or self.network_failures
        ):
            msg = "a load with captured errors cannot be a pass"
            raise ValueError(msg)
        return self

    @property
    def hard_fail(self) -> bool:
        """Whether the load failed."""
        return self.status is Status.FAIL
