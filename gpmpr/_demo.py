"""See how GitPython's git.refresh() interacts with multiprocessing.

This is imported by the public ``gpmpr.mplocal`` and ``gpmpr.mpglobal`` modules.
"""

__all__ = ["run_experiment"]

import concurrent.futures
import multiprocessing

import git


def _get_version(g: git.Git) -> str:
    """Call ``g.version()``. This helps since ``g.version`` is an unpicklable lambda."""
    return g.version()


def run_experiment() -> None:
    """Use ``Git.version`` here and also by the three multiprocessing start methods."""
    g = git.Git()
    ver = _get_version(g)
    print(f"In parent process: {ver}")

    for method in "fork", "spawn", "forkserver":
        with concurrent.futures.ProcessPoolExecutor(
            max_workers=1,
            mp_context=multiprocessing.get_context(method),
        ) as executor:
            ver = executor.submit(_get_version, g).result()
            print(f"In child process ({method}): {ver}")
