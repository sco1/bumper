# bumper
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sco1-bumper/2.0.0?logo=python&logoColor=FFD43B)](https://pypi.org/project/sco1-bumper/)
[![PyPI](https://img.shields.io/pypi/v/sco1-bumper?logo=Python&logoColor=FFD43B)](https://pypi.org/project/sco1-bumper/)
[![PyPI - License](https://img.shields.io/pypi/l/sco1-bumper?color=magenta)](https://github.com/sco1/bumper/blob/main/LICENSE)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/sco1/bumper/main.svg)](https://results.pre-commit.ci/latest/github/sco1/bumper/main)

Automatically increment the project's version number.

Heavily inspired by [`bump2version`](https://github.com/c4urself/bump2version) and [`bumpversion`](https://github.com/peritus/bumpversion). While [`bump-my-version`](https://github.com/callowayproject/bump-my-version) is an excellent modern fork this functionality, I'd like a pared down version of the offered feature set for my personal projects.

## Supported Versioning Schemes
* [Semantic Versioning (SemVer)](https://semver.org/#semantic-versioning-200)
  * Assumes `<MAJOR>.<MINOR>.<PATCH>`
* [Calendar Versioning (CalVer)](https://calver.org/)
  * Assumes `<YYYY>.<0M>.<MICRO>`

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
    f"```\n$ bumper --help\n{out.stdout.rstrip()}\n```"
)
]]] -->
```
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
* `versioning_type` - Versioning type to be used, accepted values are `"semver"` and `"calver"`

#### `tool.bumper.files`
* `file` - Path to target file relative to the repository root
* `search` - Replacement string to search for in the target file. Must contain a `{current_version}` tag if you want something to happen.

### Example Configuration
The basic configuration looks something like the following:

#### SemVer
```toml
[tool.bumper]
current_version = "0.1.0"
versioning_type = "semver"

[[tool.bumper.files]]
file = "./pyproject.toml"
search = 'version = "{current_version}"'
```

#### CalVer
```toml
[tool.bumper]
current_version = "2025.01.0"
versioning_type = "calver"

[[tool.bumper.files]]
file = "./pyproject.toml"
search = 'version = "{current_version}"'
```

Multiple replacements within the same file can also be specified:

```toml
[tool.bumper]
current_version = "0.1.0"
versioning_type = "semver"

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
    f"```\n$ bumper bump --help\n{out.stdout.rstrip()}\n```"
)
]]] -->
```
$ bumper bump --help
Usage: bumper bump [OPTIONS] BUMP_BY:{major|minor|patch|date}

  Bump the requested version component.

  Allowable `BUMP_BY` values differ based on the project's specified
  versioning type: SemVer - (major, minor, patch), CalVer - (date)

  When using CalVer, if the user's current UTC month is the same as the
  current project version, then the Micro component is incremented. Otherwise,
  the date components are bumped to the user's current UTC month and Micro
  reset to `0`.

  If `dry_run` is `True`, the requested diff will be displayed in the terminal
  & no file modifications will take place.

Arguments:
  BUMP_BY:{major|minor|patch|date}
                                  [required]

Options:
  --dry-run / --no-dry-run  Preview the requested diff.  [default: no-dry-run]
  --help                    Show this message and exit.
```
<!-- [[[end]]] -->

### `bumper init`
A small helper to initialize a starter `.bumper.toml` file that bumps the `version` field of your project's `pyproject.toml` file.

**NOTE:** Be sure to update the sample version with your current version number before bumping with bumper.

<!-- [[[cog
import cog
from subprocess import PIPE, run
out = run(["bumper", "init", "--help"], stdout=PIPE, encoding="ascii")
cog.out(
    f"```\n$ bumper init --help\n{out.stdout.rstrip()}\n```"
)
]]] -->
```
$ bumper init --help
Usage: bumper init [OPTIONS]

  Generate a default bumper configuration file.

  If the `--ignore_existing` flag is set, any existing `.bumper.toml` file
  will be overwritten; this action is not reversible. Otherwise, the existing
  configuration will be preserved.

Options:
  --versioning-type [semver|calver]
                                  [default: semver]
  --ignore-existing / --no-ignore-existing
                                  [default: no-ignore-existing]
  --help                          Show this message and exit.
```
<!-- [[[end]]] -->
