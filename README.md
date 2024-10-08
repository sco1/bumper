# bumper
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sco1-bumper/0.1.0?logo=python&logoColor=FFD43B)](https://pypi.org/project/sco1-bumper/)
[![PyPI](https://img.shields.io/pypi/v/sco1-bumper?logo=Python&logoColor=FFD43B)](https://pypi.org/project/sco1-bumper/)
[![PyPI - License](https://img.shields.io/pypi/l/sco1-bumper?color=magenta)](https://github.com/sco1/bumper/blob/main/LICENSE)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/sco1/bumper/main.svg)](https://results.pre-commit.ci/latest/github/sco1/bumper/main)

Automatically increment the project's version number.

Heavily inspired by [`bump2version`](https://github.com/c4urself/bump2version) and [`bumpversion`](https://github.com/peritus/bumpversion). While [`bump-my-version`](https://github.com/callowayproject/bump-my-version) is an excellent modern fork this functionality, I'd like a pared down version of the offered feature set for my personal projects.

## Configuration
`bumper` searches for its configuration options first in a `.bumper.toml` file, then in `pyproject.toml`; preference is given to whichever configuration is located first.
### Required Fields
#### `tool.bumper`
* `current_version` - The current software version. This is automatically incremented when bumping.

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
