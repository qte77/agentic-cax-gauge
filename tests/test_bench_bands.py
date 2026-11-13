"""Every brief's volume band, recomputed from its closed form (plan §5 BENCH-3 item 1).

Each bounded brief declares `volume:` in its front matter: the part's exact volume as an
arithmetic expression (numbers, + - * / **, and `pi`), hidden from the agent like the rest of
the front matter. This test evaluates it and checks three things:

- the number the brief's `Bounds:` line states matches the expression (prose and formula
  can't drift apart, the way 5 of 12 expected values did in another repo's ground truth);
- the band contains the exact volume;
- the band's edges match the tolerance the `Bounds:` line states, when it states one exactly.

The volumes are closed-form, so no contestant's mesh is the oracle.
"""

import ast
import math
import operator
import re
from collections.abc import Callable
from pathlib import Path

import pytest

BRIEFS = Path(__file__).resolve().parent.parent / "bench" / "briefs"

_BINARY: dict[type[ast.operator], Callable[[float, float], float]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}


def _evaluate(expr: str) -> float:
    """Evaluate a closed-form volume: numbers, + - * / **, unary minus and `pi` only."""

    def walk(node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return walk(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, int | float):
            return float(node.value)
        if isinstance(node, ast.Name) and node.id == "pi":
            return math.pi
        if isinstance(node, ast.BinOp) and type(node.op) in _BINARY:
            return _BINARY[type(node.op)](walk(node.left), walk(node.right))
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -walk(node.operand)
        msg = f"not allowed in a volume expression: {ast.dump(node)}"
        raise ValueError(msg)

    return walk(ast.parse(expr, mode="eval"))


def _brief(path: Path) -> tuple[dict[str, str], str]:
    _, front, body = path.read_text().split("---", 2)
    fields: dict[str, str] = {}
    for line in front.splitlines():
        key, sep, value = line.partition(":")
        if sep:
            fields[key.strip()] = value.strip()
    bounds = body[body.index("Bounds:") :]
    return fields, " ".join(bounds.split())


BANDED = [p for p in sorted(BRIEFS.glob("*.md")) if "volume_band" in _brief(p)[0]]


def test_the_evaluator_refuses_anything_but_arithmetic():
    assert _evaluate("40*40*5 + pi*5**2*8") == pytest.approx(8628.3, abs=0.05)
    with pytest.raises(ValueError, match="not allowed"):
        _evaluate("__import__('os').getcwd()")


def test_every_banded_brief_declares_its_closed_form():
    missing = [p.stem for p in BANDED if "volume" not in _brief(p)[0]]
    assert missing == []
    assert len(BANDED) == 18


@pytest.mark.parametrize("path", BANDED, ids=lambda p: p.stem)
def test_band_matches_the_closed_form(path: Path):
    fields, bounds = _brief(path)
    exact = _evaluate(fields["volume"])
    low, high = (float(v) for v in fields["volume_band"].split(","))

    # The prose states the same number the formula gives, to its printed precision.
    stated = re.search(r"(?:=|→|volume)\s*([0-9][0-9.]*(?:e[0-9]+)?)\s*mm³", bounds)
    assert stated is not None, f"{path.stem}: no stated volume in its Bounds line"
    printed = stated.group(1)
    decimals = len(printed.split(".")[1]) if "." in printed and "e" not in printed else 0
    tolerance = float(printed) * 5e-4 if "e" in printed else 0.5 * 10**-decimals
    assert exact == pytest.approx(float(printed), abs=tolerance)

    assert low < exact < high

    # Where the Bounds line states the tolerance exactly, the edges follow from it.
    if "−1.5 % / +1 %" in bounds:  # noqa: RUF001 — the briefs print a real minus sign
        expected = (exact * 0.985, exact * 1.01)
    elif m := re.search(r"\(band ±([0-9.]+) %", bounds):
        pct = float(m.group(1)) / 100
        expected = (exact * (1 - pct), exact * (1 + pct))
    else:  # "band ≈ ±N %": approximate by its own words, so containment is all we check
        return
    assert (low, high) == pytest.approx(expected, rel=2e-4)
