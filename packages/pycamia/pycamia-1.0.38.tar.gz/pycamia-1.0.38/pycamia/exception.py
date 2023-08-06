
from .manager import info_manager

__info__ = info_manager(
    project = "PyCAMIA",
    package = "<main>",
    author = "Yuncheng Zhou",
    create = "2021-12",
    fileinfo = "File to handle the exceptions.",
    help = "Handle the exceptions. `touch` swallow the error, `crashed` to see if there is an erro, `avouch` to assert with text, `Error` to create new error types. "
)

__all__ = """
    touch
    touch_func
    crashed
    avouch
    Error
    void
""".split()

from .environment import get_args_expression, get_environ_vars, update_locals_by_environ
from .functions import const_function
from .strop import is_snakename, tokenize

def touch(v, default=None, error_type=Exception):
    """
    Touch a function or an expression `v`, see if it causes exception in `error_type`. 
    If not, output the result, otherwise, output `default`. 
    
    Params:
        v [callable or str]: The expression to touch/run. 
        default [callable]: The function (error) -> return to cope with exceptions. 
            Use `default = pycamia.functions.identity_function` (or write one yourself)
            to return the exception object.
        error_type [Exception]: The exceptions to be caught. All exceptions by default. 
    
    Example:
    ----------
    >>> a = 0
    >>> touch(lambda: 1/a, default = 'fail')
    fail
    """
    if not callable(default):
        default = const_function(default)
    if isinstance(v, str):
        update_locals_by_environ()
        try: return eval(v)
        except error_type as e: return default(e)
    else:
        try: return v()
        except error_type as e: return default(e)

def touch_func(v, default=None, *input, error_type=Exception):
    """
    Touch a function with inputs, if it causes exception in `error_type`. 
    If not, output the result, otherwise, output `default`. 
    
    Params:
        v [callable or str]: The expression to touch/run. 
        default [callable]: The function (error) -> return to cope with exceptions. 
            Use `default = pycamia.functions.identity_function` (or write one yourself)
            to return the exception object.
        input [any]: The input of v and default. 
        error_type [Exception]: The exceptions to be caught. All exceptions by default. 
    
    Example:
    ----------
    >>> touch(lambda a: 1/a, default = lambda a: f'failed for {a}', 0)
    failed for 0
    """
    if len(input) == 0:
        input = (default,)
        default = None
    if isinstance(v, str):
        update_locals_by_environ()
        try: return eval(v)(*input)
        except error_type: return default(*input)
    else:
        try: return v(*input)
        except error_type: return default(*input)

def avouch(v: bool, txt=""):
    """
    Assert with text. 
    
    Inputs:
        v[bool]: the expression to be validated.
        txt[str]: the assertion message when the test fails.
    """
    if not v:
        if not txt:
            expr = tokenize(get_args_expression(), sep=',')[0].strip()
            if (expr is not None):
                txt = f"Failure in assertion '{expr}'"
        txt = ' '.join(txt.split())
        raise AssertionError(txt)

def crashed(func):
    """
    Validate whether a function `func` would crash. 
    """
    try:
        func()
    except:
        return True
    return False

def Error(name: str):
    """
    Create a temporary error by text. 

    Inputs:
        name[str]: the name of the error; It is used to identify the error type. 

    Example:
    ----------
    >>> try:
    >>>     raise Error("TEST")()
    >>> except Error("TEST"):
    >>>     print('caught')
    ... 
    caught
    >>> raise Error('Type')("description")
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    pycamia.exception.TESTError: description
    """
    if not is_snakename(name):
        raise TypeError(f"Invalid name '{name}' for an error: it should be alphabets/digits/underlines without spaces (as long as all other symbols). ")
    v = get_environ_vars().globals
    error_name = f"{name}Error"
    if error_name in v: return v[error_name]
    exec(f"class {error_name}(Exception): pass")
    v[error_name] = eval(error_name)
    return eval(error_name)

void = []
