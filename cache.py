import inspect
import os
from pathlib import Path
from typing import Callable, Concatenate, ParamSpec, TypeVar

from pydantic import BaseModel, TypeAdapter

_MODULE_DIR = Path(os.path.dirname(os.path.realpath(__file__)))
_CACHE_FILE = _MODULE_DIR / ".music_cache.json"
_CACHE_FILE_BKP = _MODULE_DIR / ".music_cache.backup.json"

RetType = TypeVar("RetType", bound=BaseModel)
InputType = TypeVar("InputType", bound=BaseModel)
ParamType = ParamSpec("ParamType")


def cached(
    func: Callable[Concatenate[InputType, ParamType], RetType]
) -> Callable[Concatenate[InputType, ParamType], RetType]:
    annots = inspect.get_annotations(func, eval_str=True)
    input_type = list(annots.values())[0]
    ret_type = annots["return"]

    def wrapper(
        input: InputType, *args: ParamType.args, **kwargs: ParamType.kwargs
    ) -> RetType:
        _CACHE_FILE.touch()
        with open(_CACHE_FILE) as f:
            data = f.read()

        cache_key = input.model_dump_json()

        cache_type = TypeAdapter(dict[input_type, ret_type])
        cache = cache_type.validate_python(data) if data else {}

        if cache_key in cache:
            return cache[cache_key]
        else:
            ret = func(input, *args, **kwargs)
            cache[cache_key] = ret

            _CACHE_FILE_BKP.touch()
            with open(_CACHE_FILE) as f_orig, open(_CACHE_FILE_BKP, "a") as f_bkp:
                f_bkp.write("\n")
                f_bkp.write(f_orig.read())

            with open(_CACHE_FILE, "w") as f:
                f.write(cache_type.dump_json(cache).decode())

            return ret

    return wrapper
