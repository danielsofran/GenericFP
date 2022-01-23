from domain import Entity
from exceptii import ValidatorException


class Validator(Entity):
    def __init__(self, **kwargs):
        for _, val in kwargs.items():
            if str(type(val)) != "<class 'function'>":
                kwargs.pop(_)
        super().__init__(**kwargs)

    def __call__(self, entity: Entity):
        for name in self:
            if name in entity:
                if self[name](entity[name]) == False:
                    raise ValidatorException(f"validare falsa {name} {entity[name]}")


# fct_id_ok = lambda elem: elem>0
# Validator(id = lambda: fct_id_ok(1), nume = )
