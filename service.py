from domain import Entity


class Service:
    def __init__(self, validator, repo):
        self.__validator = validator
        self.__repo = repo

    def adauga(self, *args):
        pattern = self.__repo.pattern
        dct = {}
        for i, _ in enumerate(pattern):
            dct[_] = args[i]
        obj = Entity(**dct)
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
