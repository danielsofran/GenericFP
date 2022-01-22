from domain import Entity
from exceptii import *

class Repository:
    def __init__(self, pattern = None):
        self._l = []
        self._pattern = pattern

    @property
    def pattern(self):
        return self._pattern

    @pattern.setter
    def pattern(self, val):
        self._pattern = val

    # CRUD
    def adauga(self, obj: Entity):
        if obj in self._l:
            raise RepoException("Element duplicat!")
        if len(self) == 0:
            self._l.append(obj)
            return
        for k1 in obj:
            if not k1 in self.pattern:
                raise RepoException("Pattern mismatch!")

    def stergere(self, obj: Entity):
        if not obj in self._l:
            raise RepoException("Elementul nu a fost gasit!")
        self._l.remove(obj)

    def modificare(self, obj1: Entity, obj2: Entity):
        if obj1.pattern != obj2.pattern:
            raise RepoException("Pattern mismatch!")
        if obj1 in self._l:
            i = self._l.index(obj1)
            self._l[i] = obj2
        else: raise RepoException("Elementul nu a fost gasit!")

    def cautare(self, *lambdas, **kwargs):
        rez = []
        for fct in lambdas:
            for elem in self._l:
                if fct(elem):
                    if not elem in rez:
                        rez.append(elem)

        for key, value in kwargs.items():
            for elem in self._l:
                if elem[key] == value:
                    rez.append(elem)
        return rez

    def __len__(self):
        return len(self._l)

    def __iter__(self):
        return iter(self._l)

    def toList(self):
        return self._l[:]

class FileRepository(Repository):
    def __init__(self, filename, pattern = None):
        self.__path = filename
        super().__init__(pattern)

    def __read(self):
        self._l = []
        with open(self.__path, "r") as f:
            for line in f:
                if line!="":
                    obj = Entity.fromStr(line)
                    self._l.append(obj)

    def __write(self):
        with open(self.__path, "w") as f:
            for elem in self._l:
                f.write(repr(elem)+"\n")

    def adauga(self, obj: Entity):
        self.__read()
        super(FileRepository, self).adauga(obj)
        self.__write()

    def stergere(self, obj: Entity):
        self.__read()
        super().stergere(obj)
        self.__write()

    def modificare(self, obj1: Entity, obj2: Entity):
        self.__read()
        super().modificare(obj1, obj2)
        self.__write()

    def cautare(self, *lambdas, **kwargs):
        self.__read()
        return super().cautare(*lambdas, **kwargs)

    def __len__(self):
        self.__read()
        return super().__len__()

    def __iter__(self):
        self.__read()
        return super().__iter__()

    def toList(self):
        self.__read()
        return super().toList()
