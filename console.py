from domain import Entity
from exceptii import BaseAutoGeneratingException
from service import Service


class Console:
    def __init__(self, service: Service):
        self.__srv = service

    @property
    def pattern(self):
        return self.__srv.pattern

    """
        read the entity from the console
        :param field_names: the field_names to be read
        :return: the entity field values
    """
    def create_form(self, *field_names) -> list:
        results = []
        for fieldname in self.pattern:
            if len(field_names)==0 or fieldname in field_names:
                results.append(self.pattern[fieldname](input(f"{fieldname}: ")))
        return results

    def menu(self, menu: str = None, cmd: str = None, **actions) -> None:
        if menu is None:
            menu = """Menu
1. Add
2. Remove
3. Modify
4. Find
e. Exit\n"""
        if cmd is None:
            cmd = "Enter the command: "
        if len(actions) == 0:
            def cauta(srv):
                print("Introduceti metoda de cautare dintre urmatoarele: ",
                      *[f"{name}," for name in self.pattern])
                s = input()
                fdict = {}
                for token in s.split():
                    if token in self.pattern:
                        fdict[token] = self.pattern[token](input(token+": "))
                    else:
                        print(f"{token} nu se afla printre proprietatile unui element din aceasta colectie!")
                        return
                rez = srv.find(**fdict)
                for elem in rez:
                    print(elem, sep = " ")
                print()
            actions = {
                "1": lambda srv: srv.add(*self.create_form()),
                "2": lambda srv: srv.remove(id=self.create_form("id")[0]),
                "3": lambda srv: srv.modify_firstfield(*self.create_form()),
                "4": lambda srv: cauta(srv),
                "e": lambda srv: exit(0)
            }

        while True:
            print(menu)
            cmd = input("Introduceti comanda: ")
            if cmd in actions:
                try: actions[cmd](self.__srv)
                except BaseAutoGeneratingException as me: print(str(me))

