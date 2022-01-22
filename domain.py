class Entity:
    def __init__(self, **kwargs):
        self.__kwargs = kwargs

    def __getitem__(self, item: str):
        return self.__kwargs[item]

    def __setitem__(self, key:str, value) -> None:
        self.__kwargs[key] = value

    @property
    def pattern(self):
        return self.__kwargs.keys()

    def __str__(self): # ui
        rez = ""
        for name, value in self.__kwargs.items():
            rez+=f"{name}: {value}, "
        return rez[:-2]

    def __repr__(self): # fisiere
        rez = ""
        for name, value in self.__kwargs.items():
            rez += f"{type(value)}#{name}#{value}~"
        return rez

    def __eq__(self, other):
        if len(self.__kwargs) != len(other.__kwargs): return False
        if "id" in self.__kwargs:
            return self.__kwargs['id'] == other.__kwargs['id']
        for p1, p2 in zip(self.__kwargs, other.__kwargs):
            if p1 != p2:
                return False
        return True

    def __hash__(self):
        if "id" in self.__kwargs:
            return self.__kwargs['id']
        else: return hash(tuple(self.__kwargs.values())) # easy

    def __iter__(self):
        return iter(self.__kwargs)

    @classmethod
    def fromStr(cls, sir: str):
        obj = cls()
        for atr in sir.strip().split("~"):
            if atr != "":
                elem = atr.strip().split("#")
                tip = elem[0][elem[0].find("'")+1 : elem[0].rfind("'")]
                clas = None
                if tip=="int": clas=int
                elif tip=="str": clas=str
                elif tip=="float": clas=float
                elif tip=="list": clas=list
                elif tip=="tuple": clas=tuple
                elif tip=="set": clas=set
                obj[elem[1]] = clas(elem[2])
        return obj
