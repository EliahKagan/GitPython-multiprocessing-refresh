"""Fake broken git command for testing automatic git.refresh() on import."""

__all__ = ["main"]

import sys
from typing import NoReturn


def main() -> NoReturn:
    if sys.argv[1:] == ["version"]:
        print("FAKE git 99.999.9")
        sys.exit(0)

    print("error: fake git only supports 'git version'")
    sys.exit(1)
