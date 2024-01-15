# Zippity

[![PyPI version](https://badge.fury.io/py/zippity-pi.svg)](https://badge.fury.io/py/zippity=pi)
[![codecov](https://codecov.io/gh/lumpenspace/zippity/branch/master/graph/badge.svg)](https://codecov.io/gh/lumpenspace/zippity)
[![Documentation Status](https://readthedocs.org/projects/zippity-pi/badge/?version=latest)](https://zippity-pi.readthedocs.io/en/latest/?badge=latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

 dum lil CLI to collect TODOs for ChatGPT

## Warns

I'm currently preparing the companion GPT; you are welcome to use it in the meantime but it's going to be disappointing.

![alt text](cover.png)

## Installation

```shell
pipx install zippity_py
```

## Usage

After installation, you can use the CLI by running:

```bash


> zpt --help

Usage: zpt [OPTIONS] [SOURCE_DIRECTORY]

Options:
  -e, --extensions TEXT (Default: '.py,.js,.ts')
  -r, --result_file PATH  (Default: 'ZIPPITYDO_EXAMPLE.md')
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

![Screenshot](screenshot.png)

## Contributing

Contributions are welcome. Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
