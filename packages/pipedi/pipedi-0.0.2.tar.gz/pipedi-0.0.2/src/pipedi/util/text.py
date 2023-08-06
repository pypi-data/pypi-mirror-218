import re
import collections

from .. import piped, pipable

@piped
def head(iterable, num):
    for line in iterable:
        if num == 0:
            break
        num -= 1
        yield line

@piped
def tail(iterable, num):
    queue = collections.deque(maxlen=num)
    for line in iterable:
        queue.append(line)

    return iter(queue)

@piped
def cut(iterable, delimiter=' ', fields=None, output_delimiter=None):
    output_delimiter = output_delimiter or delimiter

    for line in iterable:
        all_fields = line.split(delimiter)
        selection = all_fields if fields is None \
                               else [all_fields[i] for i in fields]
        yield output_delimiter.join(selection)

@piped
def grep(iterable, regex, invert=False):
    for line in iterable:
        found = (re.search(regex, line) is not None)
        if found ^ invert:
            yield line



def field_key(line, delimiter, fields):
    if fields is None:
        return line

    all_fields = line.split(delimiter)
    return tuple([all_fields[i] for i in fields])

@piped
def sort(iterable, fields=None, delimiter=" "):
    key = lambda line: field_key(line, delimiter, fields)
    return iter(sorted(iterable, key=key))

@piped
def tac(iterable, fields=None, delimiter=" "):
    return iter(reversed([x for x in iterable]))


@pipable
def strip(line: str, chars='\n'):
    return line.strip(chars)

@pipable
def rev(line: str):
    return str("".join(reversed(list(line))))
