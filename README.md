# Zippity - dum lil CLI to collect TODOs for ChatGPT to use.

# Zippity - dum lil CLI to collect TODOs for ChatGPT to use.

[![PyPI version](https://badge.fury.io/py/zippity.svg)](https://badge.fury.io/py/zippity)
[![Build Status](https://travis-ci.com/ChatGPT/zippity.svg?branch=master)](https://travis-ci.com/ChatGPT/zippity)
[![codecov](https://codecov.io/gh/ChatGPT/zippity/branch/master/graph/badge.svg)](https://codecov.io/gh/ChatGPT/zippity)
[![Documentation Status](https://readthedocs.org/projects/zippity/badge/?version=latest)](https://zippity.readthedocs.io/en/latest/?badge=latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This is a Python command-line interface (CLI) package developed using Poetry.

## Installation

```shell
pipx install zippity-py
```

## Usage

After installation, you can use the CLI by running:

```bash


> zippity --help

Usage: zippity [OPTIONS] [SOURCE_DIRECTORY]

Options:
  -e, --extensions TEXT (Default: '.py,.js,.ts')
  -r, --result_file PATH  (Default: 'ZIPPITYDO.md')
  -t, --template_file PATH
  --help    
```

## Template

Templates are jinja markdown files, that get passed an list of these:

```python
FileTodos = TypedDict(
    "FileTodos",
    {
        "todos": List[Todo],
        "content": str,
        "language": str,
        "mimetype": str,
        "name": str,
    },
)
```

Each `FileTodo` will have a list of todos, like this:

```python
Todo = TypedDict(
    "Todo",
    {
        "line_number": int,
        "text": str,
    },
)
```

The default template is in [template/template.md](zippity/template/default.md.jinja); once compiled it looks like this:

![Screenshot](screenshot.pngpng>)

## Contributing

Contributions are welcome. Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)