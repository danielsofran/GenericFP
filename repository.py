from domain import Entity
from exceptii import *

class Pattern(Entity):
    def __len__(self):
        count = 0
        for _ in self:
            count += 1
        return count
    def __eq__(self, other):
        if len(self.__kwargs) != len(other.__kwargs): return False
        for p1, p2 in zip(self.__kwargs, other.__kwargs):
            if p1 != p2:
                return False
        return True

    def ok(self, entity: Entity):
        for key in self:
            if type(entity[key]) != self[key]:
                return False
        return True

class Repository:
    def __init__(self, pattern: Pattern = None):
        self._l = []
        self._pattern = pattern

    @property
    def pattern(self):
        return self._pattern

    @pattern.setter
    def pattern(self, val: Pattern):
        self._pattern = val

    # CRUD
    def adauga(self, obj: Entity):
        if obj in self._l:
            raise RepoException("Element duplicat!")
        if self._pattern is None:
            self._l.append(obj)
            # create the pattern
            pattern = Pattern()
            for key in obj:
                pattern[key] = type(obj[key])
            self._pattern = pattern
            return
        if not self._pattern.ok(obj):
            raise RepoException("Pattern mismatch!")
        self._l.append(obj)

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

    @property
    def pattern(self):
        self.__read()
        return self._pattern

    def __read(self):
        self._l.clear()
        with open(self.__path, "r") as f:
            for line in f:
                if line!="":
                    obj = Entity.fromStr(line)
                    if self._pattern is None or len(self._pattern) == 0:
                        self._l.append(obj)
                        # create the pattern
                        pattern = Pattern()
                        for key in obj:
                            pattern[key] = type(obj[key])
                        self._pattern = pattern
                        continue
                    elif not self._pattern.ok(obj):
                        raise RepoException("Pattern mismatch!")
                    else: self._l.append(obj)
                    #self._l.append(obj)

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
