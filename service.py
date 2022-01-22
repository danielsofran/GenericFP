from domain import Entity
from exceptii import NoPatternException, ServiceException


class Service:
    def __init__(self, validator, repo):
        self.__validator = validator
        self.__repo = repo

    def __list_to_obj(self, l, pattern):
        if pattern is None:
            raise NoPatternException
        dct = {}
        for i, _ in enumerate(pattern):
            dct[_] = l[i]
        return Entity(**dct)

    def adauga(self, *args):
        pattern = self.__repo.pattern
        obj = self.__list_to_obj(args, pattern)
        self.__validator(obj)
        self.__repo.adauga(obj)

    def stergere(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.__repo.pattern:
                to_erase = []
                for elem in self.__repo:
                    if elem[key] == value:
                        to_erase.append(elem)
                for elem in to_erase:
                    self.__repo.stergere(elem)

    def modificare(self, *args):
        pattern = self.__repo.pattern
        obj1 = self.__list_to_obj(args[:len(args)//2], pattern)
        obj2 = self.__list_to_obj(args[len(args)//2:], pattern)
        self.__validator(obj1)
        self.__validator(obj2)
        self.__repo.modificare(obj1, obj2)

    def modificare_id(self, *args): # cautam obiectul dupa primul camp si modificam celelalte campuri
        pattern = self.__repo.pattern
        obj = self.__list_to_obj(args, pattern)
        # after creating obj
        firstfield = None
        for field in obj:
            firstfield = field
            break
        pattern = self.__repo.pattern
        for field in pattern:
            if firstfield != field:
                raise ServiceException("Mismatch pattern in search by first field!")
            break
        objfound = self.__repo.cautare(**{firstfield: obj[firstfield]})[0]
        self.__repo.modificare(objfound, obj)

    def cautare(self, *lambdas, **kwargs):
        return self.__repo.cautare(*lambdas, **kwargs)



