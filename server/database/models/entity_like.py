from typing import Any, Callable


class EntityLikeMixin:
    __common_fields_with_entity__: list[str]
    __entity__: Any
    __attrs_to_entity__: dict[str, Callable]
    __attrs_from_entity__: dict[str, Callable]

    @classmethod
    def from_entity(cls, entity):
        model = cls()
        for field in cls.__common_fields_with_entity__:
            model.__setattr__(field, entity.__getattribute__(field))
        for key, value in cls.__attrs_from_entity__.items():
            model.__setattr__(key, value(entity.__getattribute__(key)))
        return model

    def as_entity(self):
        args = {
            field: self.__getattribute__(field)
            for field in self.__common_fields_with_entity__
        }
        for key, value in self.__attrs_to_entity__.items():
            args[key] = value(self.__getattribute__(key))
        return self.__entity__(**args)
