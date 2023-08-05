# iformat

iformat is a simple package that prints basic data structures in an indented and readable way. The main `iprint` function supports changing the indent size and expansion threshold, as well as all vanilla `print` arguments. The included `iformat` function provides more customization, and returns a string that has been indented and formatted. An `.iformat` method (returning a string) can be added to any class for that class to be printed with custom formatting, and classes are otherwise printed with all their methods.

## Parameters:
**`indentDepth`:** *(`iprint` and `iformat`)*\
Specifies how many spaces should be inserted as one indent level. Default `4`.

**`expansionThreshold`**: *(`iprint` and `iformat`)*\
Specifies how long an object must be when printed before it is shown in a muilti-line format. Default `0`.\
Ex:
```py
iprint([1, 2, 3], expansionThreshold = 10)
# [1, 2, 3]

iprint([1, 2, 3], expansionThreshold = 0)
# [
#   1,
#   2,
#   3
# ]
```

**`excludedAttrs`**: *(`iprint` and `iformat`)*\
Specifies class attributes that should not be printed. Should be a list or tuple of strings OR a regex pattern. Default `r"__.+__"`.

## `.iformat` method for classes:
You can add a `.iformat` method to any class to show the return value of that method instead of the default iformat output for classes. It must accept positional arguments `indentLevel`, `indentDepth`, `expansionThreshold`, and `excludedAttrs`, which will be passed the same values as those passed to the `iformat` function call that calls the method. It is reccomended that you add whitespace in front of the output corresponding to `indentLevel * indentDepth`, and that you call `iformat`, with the same passed args (maybe with `indentDepth + 1`) on any values that are part of the outputted string.

**`indentLevel`:** *(`iformat` only)*\
Specifies the indent level of the returned output string. Default `0`.

https://github.com/FinnE145/iprint

https://pypi.org/project/iformat