"""`caxgauge check` — the documented command M3 adopts against (plan §7.1 wave 4, §7.3)."""

import json
from pathlib import Path

import pytest
import trimesh

from caxgauge import cli
from caxgauge.verify.substrate import POLYFETCH_ENV

FIXTURES = Path(__file__).parent / "fixtures"
GOOD = FIXTURES / "good.stl"  # 20 x 15 x 10 box, volume 3000


@pytest.fixture(autouse=True)
def _no_polyfetch(monkeypatch: pytest.MonkeyPatch) -> None:
    """Stub mode (plan §7.3 #8): no browser in unit tests, so browser + render SKIP."""
    monkeypatch.delenv(POLYFETCH_ENV, raising=False)


def _report(out: Path) -> dict[str, object]:
    return json.loads((out / "report.json").read_text())


def test_bounded_good_part_is_review_exit_0(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    code = cli.main(
        ["check", str(GOOD), "--envelope", "21,16,11", "--volume-band", "2990,3010",
         "--out", str(tmp_path)]
    )  # fmt: skip
    assert code == 0
    assert _report(tmp_path)["verdict"] == "review"
    out = capsys.readouterr().out
    assert "review" in out
    assert "necessary, not sufficient" in out.lower()
    assert "verified" not in out.lower()


def test_headline_silent_fusion_loss_fails_through_the_cli(tmp_path: Path):
    intended = trimesh.load(FIXTURES / "feature_absorbed_intended.stl", file_type="stl")
    assert isinstance(intended, trimesh.Trimesh)
    low, high = intended.volume * 0.99, intended.volume * 1.01
    code = cli.main(
        ["check", str(FIXTURES / "feature_absorbed_buggy.stl"),
         "--volume-band", f"{low},{high}", "--out", str(tmp_path)]
    )  # fmt: skip
    assert code == 1
    report = _report(tmp_path)
    assert report["verdict"] == "fail"
    volume = next(c for c in report["checks"] if c["name"] == "volume")  # type: ignore[union-attr]
    assert volume["status"] == "fail"


def test_unbounded_run_names_the_absent_bounds_and_is_not_green(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
):
    code = cli.main(["check", str(GOOD), "--out", str(tmp_path)])
    assert code == 0
    assert {"bbox", "volume"} <= set(_report(tmp_path)["skipped"])  # type: ignore[arg-type]
    out = capsys.readouterr().out
    assert "--envelope" in out
    assert "--volume-band" in out


def test_no_render_skips_the_browser_legs_without_running_them(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    def boom(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("must not run with --no-render")

    monkeypatch.setattr(cli, "render_views", boom)
    monkeypatch.setattr(cli, "browser_load_check", boom)
    assert cli.main(["check", str(GOOD), "--no-render", "--out", str(tmp_path)]) == 0
    checks = {c["name"]: c for c in _report(tmp_path)["checks"]}  # type: ignore[union-attr]
    assert checks["render"]["status"] == "skip"
    assert "--no-render" in checks["render"]["detail"]


def test_without_polyfetch_the_render_is_skipped_loudly(tmp_path: Path):
    cli.main(["check", str(GOOD), "--out", str(tmp_path)])
    assert "No render" in (tmp_path / "report.html").read_text()


@pytest.mark.parametrize(
    "args",
    [
        ["check", str(GOOD), "--envelope", "1,2"],
        ["check", str(GOOD), "--envelope", "a,b,c"],
        ["check", str(GOOD), "--volume-band", "10,1"],
        ["check", "does-not-exist.stl"],
        [],
    ],
)
def test_usage_errors_exit_2(args: list[str], tmp_path: Path):
    with pytest.raises(SystemExit) as exc:
        cli.main([*args, "--out", str(tmp_path)] if args else args)
    assert exc.value.code == 2
