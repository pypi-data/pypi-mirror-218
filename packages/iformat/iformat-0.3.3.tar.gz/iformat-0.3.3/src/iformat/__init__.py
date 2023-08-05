"""iformat is a simple package that prints basic data structures in an indented and readable format. The main `iprint` function supports changing the indent size and expansion threshold, as well as all vanilla `print` arguments. The included `iformat` function provides more customization, and returns a string that has been indented and formatted. An `.iformat` method (returning a string) can be added to any class for that class to be printed with custom formatting.

https://github.com/FinnE145/iprint

https://pypi.org/project/iformat"""


# Copyright (C) 2023  Finn Emmerson

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# finne014@gmail.com

# ----------- iPrint ---------- #
from inspect import isfunction as _if, isbuiltin as _ib, ismethod as _im
from re import match as _match
_iters = [dict, list, tuple, set]        # NOTE: 'dict' must be first, because it has special cases. Other allowed iterable types can be added after item 0. They will by default have no brackets accociated with them, but will otherwise be treated as iterables

def _length(i):
    return (sum([_length(k) + _length(v) + (3 if len(i.keys()) <= 1 else (2 if len(i.keys()) <= 0 else 4)) for k, v in i.items()]) + 1) if type(i) == dict else (sum([_length(x) + 2 for x in i]) if type(i) in _iters else (len(i.__class__.__name__) + _length(i.__dict__) + len(i.__dict__.keys()) - 1 if hasattr(i, "__dict__") else len(str(i))))

def _brackets(datatype, newline = False, indentAmount = 0):
    return [("[" if datatype == list else "(" if datatype == tuple else "{" if datatype in [set, dict] else "") + ("\n" if datatype in _iters and newline else "") + (" " * indentAmount), ("\n" if datatype in _iters and newline else "") + (" " * indentAmount) + ("]" if datatype == list else ")" if datatype == tuple else "}" if datatype in [set, dict] else "")]

def _indent(indentLevel, indentDepth):
    return " " * (indentLevel * indentDepth)

def _isfunctionish(i):
    return _if(i) or _ib(i) or _im(i)

def iformat(i, indentLevel = 0, indentDepth = 4, expansionThreshold = 0, excludedAttrs = r"__.+__"):
    il, id, et, ea = indentLevel, indentDepth, expansionThreshold, excludedAttrs
    length = _length(i)
    if type(i) in _iters:
        return (_brackets(type(i), True if length > et and len(i) > 0 else False, ((il + 1) * id) if length > et and len(i) > 0 else False)[0]\
            + ((",\n" + _indent(il + 1, id)) if length > et and len(i) > 0 else (", ")).join(\
                    [f"{iformat(k, il + 1, id, et, ea)}: {iformat(v, il + 1, id, et, ea)}" for k, v in i.items()]\
                if type(i) == dict else\
                    [iformat(x, il + 1, id, et, ea) for x in i])\
            + _brackets(type(i), True if length > et and len(i) > 0 else False, (il * id) if length > et else 0)[-1])
    if _isfunctionish(i):
        return f"<function {i.__name__}>"
    if "iformat" in dir(i):
        return i.iformat(il, id, et, ea)
    if hasattr(i, "__dict__"):
        return (f"{icn if (icn := i.__class__.__name__) != 'type' else i.__name__}({', '.join([f'{k} = {iformat(v, il, id, et, ea)}' for k, v in i.__dict__.items() if (k not in ea if type(ea) in _iters[1:] else not _match(ea, k))])})")
    return str(i)

def iprint(*args, indentDepth = 4, expansionThreshold = 0, excludedAttrs = r"__.+__", sep = " ", end = "\n", file = None, flush = False):
    print(*[iformat(x, 0, indentDepth, expansionThreshold = expansionThreshold, excludedAttrs = excludedAttrs) for x in args], sep = sep, end = end, file = file, flush = flush)