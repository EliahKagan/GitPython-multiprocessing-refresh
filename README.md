# GitPython-multiprocessing-refresh

This investigates the interaction between:

- GitPython's "refresh" functionality that sets global state about the `git`
  executable to be used.
- The Python standard library's `multiprocessing` feature, which GitPython
  attempts to be compatible with (such as by making objects picklable).
