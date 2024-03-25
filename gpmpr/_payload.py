"""Module with ``get_version`` for separate-payload tests."""

__all__ = ["get_version"]

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import git


def get_version(g: "git.Git") -> str:
    """Call ``g.version()``."""
    return g.version()
