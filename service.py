from typing import List

from domain import Entity
from exceptii import NoPatternException, ServiceException
from repository import Repository, Pattern
from validator import Validator


class Service:
    def __init__(self, validator: Validator, repo: Repository):
        self._validator = validator
        self._repo = repo

    @property
    def pattern(self) -> Pattern:
        return self._repo.pattern

    def _list_of_fields_to_entity(self, lst) -> Entity:
        pattern = self._repo.pattern
        if pattern is None:
            raise NoPatternException
        dct = {}
        for i, _ in enumerate(pattern):
            dct[_] = lst[i]
        return Entity(**dct)

    def add(self, *args) -> None:
        obj = self._list_of_fields_to_entity(args)
        self._validator(obj)
        self._repo.add(obj)

    def remove(self, *lambdas, **kwargs) -> None:
        for fct in lambdas:
            if callable(fct):
                for elem in self._repo:
                    if fct(elem):
                        self._repo.remove(elem)
        for key, value in kwargs.items():
            if key in self._repo.pattern:
                to_erase = []
                for elem in self._repo:
                    if elem[key] == value:
                        to_erase.append(elem)
                for elem in to_erase:
                    self._repo.remove(elem)

    def modify(self, *args) -> None:
        if len(args) != 2*len(self.pattern):
            raise ServiceException("Invalid number of arguments!")
        obj1 = self._list_of_fields_to_entity(args[:len(args) // 2])
        obj2 = self._list_of_fields_to_entity(args[len(args) // 2:])
        self._validator(obj1)
        self._validator(obj2)
        self._repo.modify(obj1, obj2)

    def modify_firstfield(self, *args) -> None:  # cautam obiectul dupa primul camp si modificam celelalte campuri
        obj = self._list_of_fields_to_entity(args)
        # after creating obj
        firstfield = None
        for field in obj:
            firstfield = field
            break
        pattern = self._repo.pattern
        for field in pattern:
            if firstfield != field:
                raise ServiceException("Mismatch pattern in search by first field!")
            break
        objfound = self._repo.find(**{firstfield: obj[firstfield]})[0]
        self._repo.modify(objfound, obj)

    def find(self, *lambdas, **kwargs) -> List[Entity]:
        return self._repo.find(*lambdas, **kwargs)

    def get_elements(self) -> List[Entity]:
        return self._repo.to_list()
