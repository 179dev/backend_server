from typing import Any


class EntityLikeMixin:
    __common_fields_with_entity__: list[str]
    __entity__: Any

    @classmethod
    def from_entity(cls, entity):
        model = cls()
        for field in cls.__common_fields_with_entity__:
            model.__setattr__(field, entity.__getattribute__(field))
        return model

    def as_entity(self):
        args = {
            field: self.__getattribute__(field)
            for field in self.__common_fields_with_entity__
        }
        return self.__entity__(**args)
