"""See how GitPython's git.refresh() interacts with multiprocessing."""

__all__ = ["main"]

import concurrent.futures
import multiprocessing

import git


def main() -> None:
    git.refresh("/usr/bin/git")  # TODO: Somehow avoid hard-coding this.
    g = git.Git()
    ver = g.version()
    print(f"In parent process: {ver}")

    for method in "fork", "spawn", "forkserver":
        with concurrent.futures.ProcessPoolExecutor(
            max_workers=1,
            mp_context=multiprocessing.get_context(method),
        ) as executor:
            ver = executor.submit(g.version).result()
            print(f"In child process ({method}): {ver}")
