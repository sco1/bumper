# bumper
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sco1-bumper/0.1.0?logo=python&logoColor=FFD43B)](https://pypi.org/project/sco1-bumper/)
[![PyPI](https://img.shields.io/pypi/v/sco1-bumper?logo=Python&logoColor=FFD43B)](https://pypi.org/project/sco1-bumper/)
[![PyPI - License](https://img.shields.io/pypi/l/sco1-bumper?color=magenta)](https://github.com/sco1/bumper/blob/main/LICENSE)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/sco1/bumper/main.svg)](https://results.pre-commit.ci/latest/github/sco1/bumper/main)

Automatically increment the project's version number.

Heavily inspired by [`bump2version`](https://github.com/c4urself/bump2version) and [`bumpversion`](https://github.com/peritus/bumpversion). While [`bump-my-version`](https://github.com/callowayproject/bump-my-version) is an excellent modern fork this functionality, I'd like a pared down version of the offered feature set for my personal projects.

## Installation
Install from PyPi with your favorite `pip` invocation, e.g.:

```bash
$ pip install sco1-bumper
```

You can confirm proper installation via the `bumper` CLI:
<!-- [[[cog
import cog
from subprocess import PIPE, run
out = run(["bumper", "--help"], stdout=PIPE, encoding="ascii")
cog.out(
    f"```bash\n$ bumper --help\n{out.stdout.rstrip()}\n```"
)
]]] -->
```bash
$ bumper --help
Usage: bumper [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  bump  Bump the requested version component.
  init  Generate a default bumper configuration file.
```
<!-- [[[end]]] -->

## Configuration
`bumper` searches for its configuration options first in a `.bumper.toml` file, then in `pyproject.toml`; preference is given to whichever configuration is located first.
### Required Fields
#### `tool.bumper`
* `current_version` - The current software version. This is automatically incremented when bumping.
  * **NOTE:** Only SemVer is supported

#### `tool.bumper.files`
* `file` - Path to target file relative to the repository root
* `search` - Replacement string to search for in the target file. Must contain a `{current_version}` tag if you want something to happen.

### Example Configuration
The basic configuration looks something like the following:

```toml
[tool.bumper]
current_version = "0.1.0"

[[tool.bumper.files]]
file = "./pyproject.toml"
search = 'version = "{current_version}"'
```

Multiple replacements within the same file can also be specified:

```toml
[tool.bumper]
current_version = "0.1.0"

[[tool.bumper.files]]
file = "./pyproject.toml"
search = 'version = "{current_version}"'

[[tool.bumper.files]]
file = "./README.md"
search = "sco1-bumper/{current_version}"

[[tool.bumper.files]]
file = "./README.md"
search = "rev: v{current_version}"
```

## CLI
### `bumper bump`
Bump your project's version number using your defined configuration.

<!-- [[[cog
import cog
from subprocess import PIPE, run
out = run(["bumper", "bump", "--help"], stdout=PIPE, encoding="ascii")
cog.out(
    f"```bash\n$ bumper bump --help\n{out.stdout.rstrip()}\n```"
)
]]] -->
```bash
$ bumper bump --help
Usage: bumper bump [OPTIONS] BUMP_BY:{major|minor|patch}

  Bump the requested version component.

  If `dry_run` is `True`, the requested diff will be displayed in the terminal
  & no file modifications will take place.

Arguments:
  BUMP_BY:{major|minor|patch}  [required]

Options:
  --dry-run / --no-dry-run  Preview the requested diff.  [default: no-dry-run]
  --help                    Show this message and exit.
```
<!-- [[[end]]] -->

### `bumper init`
A small helper to initialize a starter `.bumper.toml` file that bumps the `version` field of your project's `pyproject.toml` file.

**NOTE:** This starter file is initialized at version `0.1.0`, so be sure to update this value with your current version number before using bumper.

<!-- [[[cog
import cog
from subprocess import PIPE, run
out = run(["bumper", "init", "--help"], stdout=PIPE, encoding="ascii")
cog.out(
    f"```bash\n$ bumper init --help\n{out.stdout.rstrip()}\n```"
)
]]] -->
```bash
$ bumper init --help
Usage: bumper init [OPTIONS]

  Generate a default bumper configuration file.

  If the `--ignore_existing` flag is set, any existing `.bumper.toml` file
  will be overwritten; this action is not reversible. Otherwise, the existing
  configuration will be preserved.

Options:
  --ignore-existing / --no-ignore-existing
                                  [default: no-ignore-existing]
  --help                          Show this message and exit.
```
<!-- [[[end]]] -->
