"""
See how locally calling git.refresh() interacts with multiprocessing, with everything
in one module except the payload to invoke.
"""

__all__ = ["main"]

import concurrent.futures
import multiprocessing

import git

from . import _payload

git.refresh("/usr/bin/git")  # TODO: Somehow avoid hard-coding this path.


def _run_experiment() -> None:
    """Use ``Git.version`` here and also by the three multiprocessing start methods."""
    g = git.Git()
    ver = _payload.get_version(g)
    print(f"In parent process: {ver}")

    for method in "fork", "spawn", "forkserver":
        with concurrent.futures.ProcessPoolExecutor(
            max_workers=1,
            mp_context=multiprocessing.get_context(method),
        ) as executor:
            ver = executor.submit(_payload.get_version, g).result()
            print(f"In child process ({method}): {ver}")


def main() -> None:
    """Run the experiment."""
    _run_experiment()
