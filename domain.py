import jsonpickle


class Entity:
    def __init__(self, **kwargs):
        self.__kwargs = kwargs

    def __getitem__(self, item: str):
        return self.__kwargs[item]

    def __setitem__(self, key: str, value) -> None:
        self.__kwargs[key] = value

    def __delitem__(self, key: str) -> None:
        del self.__kwargs[key]

    def __contains__(self, item: str) -> bool:
        return item in self.__kwargs

    def __len__(self) -> int:
        return len(self.__kwargs)

    def __str__(self) -> str:  # ui
        rez = ""
        for name, value in self.__kwargs.items():
            rez += f"{name}: {value}, "
        return rez[:-2]

    def __repr__(self) -> str:  # fisiere
        json_obj = jsonpickle.encode(self)
        return str(json_obj)

    def __eq__(self, other) -> bool:
        if len(self.__kwargs) != len(other.__kwargs):
            return False
        if "id" in self.__kwargs:
            return self.__kwargs['id'] == other.__kwargs['id']
        for p1, p2 in zip(self.__kwargs, other.__kwargs):
            if p1 != p2:
                return False
        return True

    def __hash__(self) -> int:
        if "id" in self.__kwargs:
            return self.__kwargs['id']
        else:
            return hash(tuple(self.__kwargs.values()))

    def __iter__(self):
        return iter(self.__kwargs)

    @classmethod
    def from_str(cls, sir: str):
        obj = jsonpickle.decode(sir)
        return obj
