import inspect
import os
from pathlib import Path
from typing import Callable, Concatenate, Generic, ParamSpec, Type, TypeVar

from pydantic import BaseModel, TypeAdapter

_MODULE_DIR = Path(os.path.dirname(os.path.realpath(__file__)))

RetType = TypeVar("RetType", bound=BaseModel)
InputType = TypeVar("InputType", bound=BaseModel)
ParamType = ParamSpec("ParamType")


_cache_file_cache = {}


V = TypeVar("V")


class KeyValueCache(Generic[V]):
    def __init__(self, cache_file: Path, value_type: Type[V]) -> None:
        cache_file.touch()
        with open(cache_file) as f:
            data = f.read()

        cache_type = TypeAdapter(dict[str, value_type])
        cache = cache_type.validate_json(data) if data else {}

        self._cache_type = cache_type
        self._cache: dict[str, V] = cache

        self._cache_file_path = cache_file
        self._bkp_file_path = cache_file.with_suffix(".backup.json")

    def __getitem__(self, key: str) -> V:
        return self._cache[key]

    def __setitem__(self, key: str, value: V):
        self._cache[key] = value

        self._bkp_file_path.touch()
        with (
            open(self._cache_file_path) as f_orig,
            open(self._bkp_file_path, "a") as f_bkp,
        ):
            f_bkp.write("\n")
            f_bkp.write(f_orig.read())

        with open(self._cache_file_path, "w") as f:
            f.write(self._cache_type.dump_json(self._cache).decode())

    def __contains__(self, key: str):
        return key in self._cache


def cached(
    func: Callable[Concatenate[InputType, ParamType], RetType],
) -> Callable[Concatenate[InputType, ParamType], RetType]:
    annots = inspect.get_annotations(func, eval_str=True)
    ret_type = annots["return"]

    func_id = func.__qualname__

    cache_file = _MODULE_DIR / f".cache.{func_id}.json"

    def wrapper(
        input: InputType, *args: ParamType.args, **kwargs: ParamType.kwargs
    ) -> RetType:
        cache_key = input.model_dump_json()

        if func_id in _cache_file_cache:
            cache = _cache_file_cache[func_id]
        else:
            cache = KeyValueCache(cache_file, ret_type)
            _cache_file_cache[func_id] = cache

        if cache_key in cache:
            return cache[cache_key]
        else:
            ret = func(input, *args, **kwargs)
            cache[cache_key] = ret

            return ret

    return wrapper
