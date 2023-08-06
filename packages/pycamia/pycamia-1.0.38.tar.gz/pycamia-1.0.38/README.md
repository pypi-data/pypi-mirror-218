# pycamia

## Introduction

[`pycamia`](https://github.com/Bertie97/pycamia/tree/main/pycamia) is the base package affiliated to project [`PyCAMIA`](https://github.com/Bertie97/pycamia). It is a collection of different useful tools necessary in python programming. `pycamia` was designed for `python v3.6+`. It is consist of the following sub-packages. 

1. **environment** is a package containing functions to inspect the context. e.g. get the local variables in the context that calls a function. 
2. **strop** is a collection of advanced functions for strings. e.g. tokenize a string by spliting outside brackets OR find all indices for matched sub-strings.
3. **listop** is a collection of advanced functions for lists. e.g. flatten a nested list.
4. **manager** is a package to manage file and package infos. e.g. easily check the dependencies OR easy update the version. 
5. **functions** is a package of special (and commonly trivial) functions. e.g. empty functions. 
6. **exceptions** is a package to handle exceptions. e.g. touch a function and suppress the error OR assert with comment OR quickly create an Error.
7. **inout** is a package to extend the input/output. e.g. printing to a string OR suppressing the console output. 
8. **timing** is a package to time the executions. e.g. use `with` structure to record time spent for a set of commands. 
9. **more** is a collection of uncategorized functions, one need to import them from `pycamia.more`.

## Installation

This package can be installed by `pip install pycamia` or moving the source code to the directory of python libraries (the source code can be downloaded on [github](https://github.com/Bertie97/pycamia) or [PyPI](https://pypi.org/project/pyoverload/)). 

```shell
pip install pycamia
```

## Package `environment`

This package fetches the surrounding environment of the call. It is likely that no more functions would be added to it. If there's any suggestion, please contact the developer. 
1. Use `v = get_environ_locals()` or `v = get_environ_globals()` to get the dictionary of local or global variables in the parent environment. If the result is out of expectations, please contact the developer. 
2. Use `v['name']` to read variable `name` and `v['name'] = value` to add variable to the environment. 

## Package `strop`

This package cope with str objects. 
1. Use `str_len` to find the ASCII length for a string, with a length `2` for wide characters.
2. Use `str_slice` to slice a string by given indices.
3. Use `find_all` to obtain all the indices of a given string. `str_slice(s, find_all(s, k))` is equivalent to `s.split(k)`. 
4. Use `sorted_dict_repr` to create a repr string for a dictionary with ordered key.
5. Use `enclosed_object` to find the first object enclosed by brackets. 
6. Use `tokenize` to split a string without breaking enclosed objects. This is useful in breaking text of dictionary structures or arguments. e.g. one can use `tokenize(args, sep=[',', '='])[::2]` to find the argument names if `args` is a string in the format `key1=value1, key2 = value2, ...`.

## Package `listop`

This package cope with list objects. More useful functions will be added to it in the future. 
1. Use `argmin(list, domain)` to find the indices for the minimal value in list. The function only search in the indices `domain`. A list is output as there may be multiple entries. 
2. Use `argmax` to find the indices for the maximal value, similar to `argmin`. 
3. Use `flatten_list` to unwrap the list elements to create a list with no element in type `list`. 
4. Use `prod` to obtain the product of all numbers in the list. 
5. Use `item` to fetch the only element in the list. An error will be raised if there isn't any or are more than 1 elements. 

## Package `manager`

This package manages the info of packages and files. One can use it to organize the project. 
1. Use `__info__ = info_manager(project="PyCAMIA", ...)` to list the properties at the front of files. This serve as a brief introduction to readers.
2. Use `info_manager` at the beginning of `__init__.py`, `pack.py` uses it to create the portrait of a package. 
3. Use `__info__.check_requires()` to automatically check if the dependencies in attribute `requires` exist or not. This is commonly used in `__init__.py`. One can use `__info__ = info_manager(...).check()` to perform an in-place check.
4. Use `with __info__:` before importing required dependencies as well to perform a double check. 

## Package `functions`

This package contains simple functions. It is the simplest package in the project so far. 
1. Use `empty_function` for a function that does nothing. One can put any argument to the function but nothing would happen. 
2. Use `const_function(a)` for a function that accepts any argument but does nothing and always return `a`.

## Package `exceptions`

This package handles exceptions. 
1. Use `touch(function)` to try a function and suppress the error in the mean time. e.g. `touch(lambda: 1/a)` returns `None` to tell you that an exception occurs when `a=0`, but returns `1` when `a=1`. 
2. Use `crashed(function)` to check whether a function fails or not. 
3. Use `avouch(bool_to_be_tested, assertion_text)` to avouch that the given expression is true and output your designed `assertion_text` when the test fails. 
4. Use `Error("name")` to creat a new error type. It is the same as creating an Error tag by `class nameError(Exception): pass`.

## Package `inout`

This package manipulates the input/output. Currently, it only deal with print. Shell handler or other inout functions will be added here in the future. 
1. Use `with no_print:` to suppress the console output. Although not recommended, one can use `with no_print as out_stream:` and `output = str(out_stream)` inside the `with` structure to fetch the output. 
2. Use `sprint = SPrint()` to create a function `sprint` that collects the printed text. Use `out = sprint()` or `sprint.text` to get the results.

## Package `timing`

This package use the time spent of commands to perform useful inspection or organization of the codes.
1. Use `@time_this` to time a function.
2. Use `with Timer("name"):` to time a series of commands.
3. Use `with scope("name"):` to nest a series of commands. It is an alias of `Timer`. 
4. Use `with scope("name"), jump:` to jump a series of commands. 
5. Use `with scope("name"), Jump(False):` to disable the jump.
6. Use `wf = Workflow("step1", "step2")` and `with wf("step1(2)"), wf.jump:` before commands of "step1(2)" to create a workflow. One can change the arguments in the init function to decide which steps to run. 
7. Use `@periodic(seconds, max_repeat)` to run a function repeatedly. 

## Package `more`

Currently, only `once` is contained in the `more` package. 
Adding it in a function to check if the function is run once or not. 

## Waiting to Be Imroved

1. More functions will be added in the future, including path handler, tools for shell and so on. 
2. Contact us to make suggestions. 

## Acknowledgment

@Yuncheng Zhou: Developer