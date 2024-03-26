# GitPython-multiprocessing-refresh

This investigates the interaction between:

- GitPython's "refresh" functionality that sets global state about the `git`
  executable to be used.
- The Python standard library's `multiprocessing` feature, which GitPython
  attempts to be compatible with (such as by making objects support pickling).

## License

The contents of this repository, including the code and this readme, are
licensed under [0BSD](https://spdx.org/licenses/0BSD.html), a "public domain
equivalent" license that imposes no restrictions. This is the same license that
is (as of this writing) used for code examples in Python's documentation. See
[**`LICENSE`**](LICENSE) for details.

## Background

Python supports three *start methods* for multiprocessing:

- `fork`: Extensive state from the parent process is in workers automatically.
- `spawn`: The interpreter is rerun from the beginning and imports modules.
- `forkserver`: A separate process with minimal state (the "server") is
  maintained and caused to fork off subprocesse as needed.

`fork` is the default method on GNU/Linux systems as of this writing, but that
is planned to change to `spawn` in Python 3.14 because of its incompatibility
with threading (that is, with multithreading being used *at all*). `spawn` is
already the default on macOS, where `fork` does not work well, and on Windows,
where `fork` and `forkserver` are unavailable since Windows has no *fork*
system call.

All three methods should be expected to work with the automatic `git.refresh`
when it defaults to the command name `"git"` or uses a path or other command
name it finds as the value of the `GIT_PYTHON_GIT_EXECUTABLE` environment
variable. However, another way to provide a path to use for the git command
is to pass it as an arugment to `git.refresh`.

## The question

The question is, when...

1. The desired git executable path is given to GitPython by calling
   `git.refresh(<path>)`.
2. Then `multiprocessing` is used (incuding via higher level abstractions such
   as `concurrent.futures.ProcessPoolExecutor`) to create one or more worker
   processes.
3. The worker processes use GitPython.

*...does GitPython in the worker processes have the `<path>` that was passed to
`git.refresh`?*

## The answer

This does not always happen. Broadly speaking, and barring special effort to
get the desired state into the worker process, it happens when *either*:

- The `fork` start method is used.
- Another start method is used, but the worker process imports a module where
  setting the desired value occurs as a result of running the module's
  top-level code.

With the `fork` start method, most program state is duplicated, including the
class attributes of GitPython's `git.cmd.Git` class, such as the
`GIT_PYTHON_GIT_EXECUTABLE` attribute that holds the path chosen in
`git.refresh`.

Otherwise, most program state is not duplicated, and instead worker processes
import the modules they need. Although this does cause `git.refresh` to be
called in the worker process, that sets `Git.GIT_PYTHON_GIT_EXECUTABLE` (and
associated state) either to the default value of `"git"` or to a string gotten
from the `GIT_PYTHON_GIT_EXECUTABLE` environment variable.

A `git.refresh(<path>)` is thus lost unless it is run again as well. Besides
special efforts to set the state—such as explicitly running it in as part of
the worker process's task, or possibly using a custom preload when `forkserver`
is used—this happens:

- When the worker process must import a module that makes the call.

It does not happen:

- When the call is local to a function (that is not called at import time).
- When the call is global, but in a module the worker doesn't need to import.
  It may be unintuitive that this can include the module that sets up
  multiprocessing, submits work to worker processes, and retrieves their
  results. For example, if the function submitted for the worker to call is
  defined in another module, the worker will need to import that module, but
  will not typically need to import the module that submitted the work.

Finally, note that:

- The state set by refreshing is global. Local state, such as `Git` instances,
  support pickle serialization and deserialization and can be passed to worker
  processes. But that does not affect whether the effect of `git.refresh` is
  reflected in operations carried out through them.

- This is essentially unrelated to how separate processes in multiprocessing
  do not automatically share global state with each other and all have separate
  global variables and class attributes. That's a fundamental point of how
  multiprocessing works, but the topic being investigated here is *what state
  that is* in worker processes.

## The code

This repository contains scripts that test out various scenarios with
`git.refresh(<path>)` and multiprocessing.

Most systems don't have multiple `git` commands, so this also includes a fake
`git` script that supports `git version`—revealing itself to be fake and giving
a bogus version number—but no other commands. When the code is installed in a
Python virtual environment, that virtual environment's `git` entry point will
take precedence over the actual `git` command on the system.

At least for now, the scripts hard-code `/usr/bin/git` as the "real" git
command to be used as `<path>` in `git.refresh(<path>)` calls.

This code only works on systems where Python supports all three of the
multiprocesing start methods—`fork`, `spawn`, and `forkserver`—and where
they all work. This excludes Windows, which only has `spawn`, and macOS where,
of the others, at least `fork` does not to work correctly in multiprocessing.
This is only tested on GNU/Linux.

## How to run

The top-level `runall` shell script automates running `poetry install` and then
running each of the experiment scripts. It can be run as:

```sh
./runall
```

This requires `poetry` to be installed.

(These instructions or the script would have to be adapted if they were to
support attempting the experiments on Windows, but since the code itself does
not support Windows, that may not be a priority.)

## Results

Results of running `./runall` on an Ubuntu 22.04.4 LTS system running Python
3.12.2 are saved as [`results.txt`](results.txt).
