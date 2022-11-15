from typing import List

from domain import Entity
from exceptii import *


class Pattern(Entity):
    def __eq__(self, other):
        if len(self.__kwargs) != len(other.__kwargs):
            return False
        for p1, p2 in zip(self.__kwargs, other.__kwargs):
            if p1 != p2:
                return False
        return True

    def ok(self, entity: Entity):
        for key in self:
            if type(entity[key]) != self[key]:
                return False
        return True

    @classmethod
    def from_entity(cls, entity: Entity):
        kwargs = {}
        for field_name, field_value in entity:
            kwargs[field_name] = type(field_value)
        return cls(**kwargs)


class Repository:
    def __init__(self, pattern: Pattern = None):
        self._entities = []
        self._pattern = pattern

    @property
    def pattern(self) -> Pattern:
        return self._pattern

    @pattern.setter
    def pattern(self, val: Pattern):
        self._pattern = val

    # CRUD
    def add(self, obj: Entity) -> None:
        if obj in self._entities:
            raise RepoException("Element duplicat!")
        if self._pattern is None:
            self._entities.append(obj)
            # create the pattern
            pattern = Pattern()
            for key in obj:
                pattern[key] = type(obj[key])
            self._pattern = pattern
            return
        if not self._pattern.ok(obj):
            raise RepoException("Pattern mismatch!")
        self._entities.append(obj)

    def remove(self, obj: Entity) -> None:
        if obj not in self._entities:
            raise RepoException("Elementul nu a fost gasit!")
        self._entities.remove(obj)

    def modify(self, obj1: Entity, obj2: Entity) -> None:
        if Pattern.from_entity(obj1) != Pattern.from_entity(obj2):
            raise RepoException("Pattern mismatch!")
        if obj1 in self._entities:
            i = self._entities.index(obj1)
            self._entities[i] = obj2
        else:
            raise RepoException("Elementul nu a fost gasit!")

    def find(self, *lambdas, **kwargs) -> List[Entity]:
        rez = []
        for fct in lambdas:
            if callable(fct):
                for elem in self._entities:
                    if fct(elem):
                        if elem not in rez:
                            rez.append(elem)

        for key, value in kwargs.items():
            for elem in self._entities:
                if elem[key] == value:
                    rez.append(elem)
        return rez

    def __len__(self) -> int:
        return len(self._entities)

    def __iter__(self):
        return iter(self._entities)

    def to_list(self) -> List[Entity]:
        return self._entities[:]


class FileRepository(Repository):
    def __init__(self, filename, pattern=None):
        self.__path = filename
        super().__init__(pattern)

    @property
    def pattern(self):
        self.__read()
        return self._pattern

    def __read(self) -> None:
        self._entities.clear()
        with open(self.__path, "r") as f:
            for line in f:
                if line != "":
                    obj = Entity.from_str(line)
                    if self._pattern is None or len(self._pattern) == 0:
                        self._entities.append(obj)
                        # create the pattern
                        pattern = Pattern()
                        for key in obj:
                            pattern[key] = type(obj[key])
                        self._pattern = pattern
                        continue
                    elif not self._pattern.ok(obj):
                        raise RepoException("Pattern mismatch!")
                    else:
                        self._entities.append(obj)
                    # self._entities.append(obj)

    def __write(self) -> None:
        with open(self.__path, "w") as f:
            for elem in self._entities:
                f.write(repr(elem) + "\n")

    def add(self, obj: Entity) -> None:
        self.__read()
        super(FileRepository, self).add(obj)
        self.__write()

    def remove(self, obj: Entity) -> None:
        self.__read()
        super().remove(obj)
        self.__write()

    def modify(self, obj1: Entity, obj2: Entity) -> None:
        self.__read()
        super().modify(obj1, obj2)
        self.__write()

    def find(self, *lambdas, **kwargs) -> List[Entity]:
        self.__read()
        return super().find(*lambdas, **kwargs)

    def __len__(self) -> int:
        self.__read()
        return super().__len__()

    def __iter__(self) -> iter:
        self.__read()
        return super().__iter__()

    def to_list(self) -> List[Entity]:
        self.__read()
        return super().to_list()
