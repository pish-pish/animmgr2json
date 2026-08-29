from typing import Any
from mashumaro.config import BaseConfig
from mashumaro.mixins.json import DataClassJSONMixin


# https://stackoverflow.com/questions/60978672/python-string-to-camelcase#60978847
def to_camel_case(text):
    s = text.replace("-", " ").replace("_", " ")
    s = s.split()
    if len(text) == 0:
        return text
    return s[0] + "".join(i.capitalize() for i in s[1:])


class CamelCaseModel(DataClassJSONMixin):
    class Config(BaseConfig):
        serialize_by_alias = True

    def __init_subclass__(cls, **kwargs: Any):
        generated_aliases = {}
        if hasattr(cls, "__annotations__"):
            for field_name in cls.__annotations__.keys():
                if not field_name.startswith("_"):
                    generated_aliases[field_name] = to_camel_case(field_name)

        cls.Config.aliases = generated_aliases

        super().__init_subclass__(**kwargs)
