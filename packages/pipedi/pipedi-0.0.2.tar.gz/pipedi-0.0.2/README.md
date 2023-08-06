# Pipedi

A simple Python package that enables piping iterables to functions with the pipe `|` character like in a shell.

```python
with open('input.txt', 'r') as input_file:
    res = list(input_file \
                | strip('\n') \
                | tail(10) \
                | rev() \
                | grep('x', invert=True) \
                | cut(delimiter=';', fields=[1, 0, 3]) \
                | sort(delimiter=';', fields=[2, 1]) \
                | tac()
            )
    print(res)

```

## Install

```
pip install pipedi
```

## Usage

It provides two decorators that enable a function to be used in a pipe.

```python
from pipedi import piped, pipable
```

Use the `pipable` decorator for simple functions that edit items in the stream (i.e. don't remove or add items). These functions must take an items as the first parameter. Rest of the parameters can be anything.

```python
@pipable
def wrap(item, pre, post):
    return pre + item + post
```


Use the `piped` decorator for functions that edit the stream (e.g. filter, add, or enumerate items). These functions must take an iterable as the first parameter. The rest can be anything.

```python
@piped
def grep(iterable, regex):
    for line in iterable:
        if re.search(regex, line) is not None:
            yield line
```

```python
@piped
def duplicate(iterable):
    for i, line in enumerate(iterable):
        yield line
        yield line
```

```python
@piped
def enum(iterable):
    for i, line in enumerate(iterable):
        yield (i, line)
```

When used in a pipe, the first parameters (item or iterable) are omitted. Rest of the arguments are provided to the function.
```python
['apple', 'banana', 'cocos'] | grep('^.[aeiouy]') | wrap('[', ']')
```

See more examples in the tests directory and the src/pipedi/util directory.

The result of a pipe is a normal iterable, so you can use existing tools on it.

For example to duplicate a stream, you can use `itertools.dup`.

```python
from itertools import dup

with open('input.txt', 'r') as input_file:
    lines = input_file | strip('\n')

    input1, input2 = dup(lines)

    lines_with_x = input1 | grep('x')
    lines_without_x = input2 | grep('x', invert=True)

```


## Building

```bash
# Clone this repository
$ git clone git@github.com:akupar/pipedi.git
$ cd pipedi
# Create virtual environment
.../pipedi$ python -m venv venv
# Activate virtual environment
.../pipedi$ . venv/bin/activate
# Install requirements
(venv) .../pipedi$ pip install -r requirements.txt
# Install the pipedi package in editable mode
(venv) .../pipedi$ pip install -e .
# Run tests
(venv) .../pipedi$ python -m pytest
# Preview readme
(venv) .../pipedi$ grip -b README.md
# Build package
(venv) .../pipedi$ python -m build

``´