"""Package metadata: the version has a single source of truth (pyproject.toml)."""

from importlib.metadata import version

import caxgauge


def test_version_matches_installed_distribution():
    assert caxgauge.__version__ == version("agentic-cax-gauge")
