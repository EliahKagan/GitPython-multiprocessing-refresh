"""See how GitPython's git.refresh() interacts with multiprocessing."""

__all__ = ["main"]

import concurrent.futures
import multiprocessing

import git

git.refresh("/usr/bin/git")  # TODO: Somehow avoid hard-coding this path.


def get_version(g: git.Git) -> str:
    """Call ``g.version()``. This is like ``g.version`` but can be pickled."""
    return g.version()


def main() -> None:
    """Run the demo."""
    g = git.Git()
    ver = get_version(g)
    print(f"In parent process: {ver}")

    for method in "fork", "spawn", "forkserver":
        with concurrent.futures.ProcessPoolExecutor(
            max_workers=1,
            mp_context=multiprocessing.get_context(method),
        ) as executor:
            ver = executor.submit(get_version, g).result()
            print(f"In child process ({method}): {ver}")
