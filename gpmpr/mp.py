"""See how GitPython's git.refresh() interacts with multiprocessing."""

__all__ = ["main"]

from concurrent.futures import ProcessPoolExecutor
import multiprocessing

import git


def main() -> None:
    git.refresh("/usr/bin/git")  # FIXME: Somehow avoid hard-coding this.
    g = git.Git()
    print(g.version())
