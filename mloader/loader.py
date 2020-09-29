import importlib
import inspect
from copy import deepcopy
from typing import Optional, Any, List

def _get_calling_module():
    caller = inspect.stack()[2]
    module = inspect.getmodule(caller.frame)
    return module

class Loader:
    _config: Optional[dict] = None
    config: Optional[dict] = None

    def __init__(self, _config: dict):
        self._config = _config
        self.config = deepcopy(_config)

    def _get_value(self, compound_key: str) -> Any:
        keys = compound_key.split(".")

        anchor: Any = self._config

        while len(keys) > 0:
            key = keys.pop(0)

            if not key in anchor:
                return None

            anchor = anchor[key]

        return anchor

    def load(
        self, key: str, as_class: bool = False, package: Optional[str] = None
    ) -> Any:
        obj = self._get_value(key)

        if as_class:
            module: Any = None
            if isinstance(obj, str):
                class_path = obj
                params = {}
            elif isinstance(obj, dict):
                class_path_key = f"{key}_name"

                if class_path_key not in obj:
                    raise KeyError(f"please specify {key}_name for instantiation")

                class_path = obj.pop(class_path_key)
                params = obj

                for key, param in params.items():
                    if isinstance(param, dict) and "load" in param and param["load"]:
                        param.pop("load")
                        if package is None:
                            module = _get_calling_module()
                            package = module.__name__

                        params[key] = self.load(key=param["key"], as_class=param.get("as_class", False), package=package)

            class_parts = class_path.split(".")
            class_name = class_parts.pop()

            if len(class_parts) > 0:
                module = importlib.import_module(".".join(class_parts))
            elif package is not None:
                if package.startswith("."):
                    module = _get_calling_module()
                    package = module.__package__ + package
                module = importlib.import_module(package) # type: ignore

            if module is None:
                module = _get_calling_module()

            class_instantiator = getattr(module, class_name)

            return class_instantiator(**params)

        return obj