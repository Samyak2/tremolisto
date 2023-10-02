import inspect
import os
from pathlib import Path
from typing import Callable, Concatenate, ParamSpec, TypeVar

from pydantic import BaseModel, TypeAdapter

_MODULE_DIR = Path(os.path.dirname(os.path.realpath(__file__)))

RetType = TypeVar("RetType", bound=BaseModel)
InputType = TypeVar("InputType", bound=BaseModel)
ParamType = ParamSpec("ParamType")


def cached(
    func: Callable[Concatenate[InputType, ParamType], RetType]
) -> Callable[Concatenate[InputType, ParamType], RetType]:
    annots = inspect.get_annotations(func, eval_str=True)
    ret_type = annots["return"]

    func_id = func.__qualname__

    cache_file = _MODULE_DIR / f".cache.{func_id}.json"
    cache_file_bkp = _MODULE_DIR / f".cache.{func_id}.backup.json"

    def wrapper(
        input: InputType, *args: ParamType.args, **kwargs: ParamType.kwargs
    ) -> RetType:
        cache_file.touch()
        with open(cache_file) as f:
            data = f.read()

        cache_key = input.model_dump_json()

        cache_type = TypeAdapter(dict[str, ret_type])
        cache = cache_type.validate_json(data) if data else {}

        if cache_key in cache:
            return cache[cache_key]
        else:
            ret = func(input, *args, **kwargs)
            cache[cache_key] = ret

            cache_file_bkp.touch()
            with open(cache_file) as f_orig, open(cache_file_bkp, "a") as f_bkp:
                f_bkp.write("\n")
                f_bkp.write(f_orig.read())

            with open(cache_file, "w") as f:
                f.write(cache_type.dump_json(cache).decode())

            return ret

    return wrapper
