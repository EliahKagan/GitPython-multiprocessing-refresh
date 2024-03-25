"""See how globally calling GitPython's git.refresh() interacts with multiprocessing."""

__all__ = ["main"]

import git

from . import _demo

git.refresh("/usr/bin/git")  # TODO: Somehow avoid hard-coding this path.


def main() -> None:
    """The global refresh already occurred, so run the experiment."""
    _demo.run_experiment()
