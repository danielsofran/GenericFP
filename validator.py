from domain import Entity
from exceptii import ValidatorException


class Validator(Entity):
    def __init__(self, **kwargs):
        for _, val in kwargs.items():
            if not isinstance(val, type(lambda x: True)):
                kwargs.pop(_)
        super().__init__(**kwargs)

    def __call__(self, entity: Entity):
        for name in self:
            if name in entity:
                if self[name](entity[name]) is False:
                    raise ValidatorException(f"validare falsa {name} {entity[name]}")
