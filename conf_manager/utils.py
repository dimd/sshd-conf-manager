import re
from itertools import ifilter


def split_on_first_whitespace(line):
    return line.split(None, 1)


def cleaned_up_conf(iterable):
    no_comments_and_empty_lines = re.compile(r' *\w+(?:\s+)\w+')
    return ifilter(
            no_comments_and_empty_lines.match,
            iterable)
