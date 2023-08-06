import inspect
from pathlib import Path
from typing import Union


# TODO: remove this api, unify to flattened args
def func_receive_dict_inputs(func):
    """to decide if a func could recieve dict inputs or not

    Args:
        func (class): the target function to be inspected

    Returns:
        bool: if func only has one arg ``input`` or ``inputs``, return True, else return False
    """
    full_args_spec = inspect.getfullargspec(func)
    varargs = full_args_spec.varargs
    varkw = full_args_spec.varkw
    if not (varargs is None and varkw is None):
        return False

    args = full_args_spec if full_args_spec else []
    args.pop(0) if (args and args[0] in ['self', 'cls']) else args

    if len(args) == 1 and args[0] in ['input', 'inputs']:
        return True

    return False





def read_file(path):

    with open(path, 'r') as f:
        text = f.read()
    return text



def ensure_dir(dirname: Union[str, Path]) -> Path:
    """
    ensure dir path is exist,if not exist,make it
    Args:
        dirname: 文件夹 路径

    Returns:
    """
    dirname = Path(dirname)
    if not dirname.is_dir():
        dirname.mkdir(parents=True, exist_ok=False)
    return dirname
