"""agentic-cax-gauge: verification harness for agent-generated CAx."""

from importlib.metadata import version

# Reason: pyproject.toml is the single source of truth; bump-my-version edits only that file.
__version__ = version("agentic-cax-gauge")
