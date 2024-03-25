"""See how locally calling git.refresh() interacts with multiprocessing."""

__all__ = ["main"]

import git

from . import _demo


def main() -> None:
    """Refresh to get a correct git path, and run the experiment."""
    git.refresh("/usr/bin/git")  # TODO: Somehow avoid hard-coding this path.
    _demo.run_experiment()
