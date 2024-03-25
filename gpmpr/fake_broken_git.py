"""Fake broken git command for testing automatic git.refresh() on import."""

__all__ = ["main"]

import sys
from typing import NoReturn


def main() -> NoReturn:
    sys.exit(1)
