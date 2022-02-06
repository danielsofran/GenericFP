from exceptii import MyException
from service import Service


class Console:
    def __init__(self, service: Service):
        self.__srv = service

    @property
    def pattern(self):
        return self.__srv.pattern

    def createForm(self, *elements):
        results = []
        for name in self.pattern:
            if len(elements)==0 or name in elements:
                results.append(self.pattern[name](input(f"{name}: ")))
        return results

    def menu(self, meniu=None, cmd=None, **actions):
        if meniu is None:
            #nonlocal meniu, actions
            meniu = """Meniu
1. Adauga
2. Sterge
3. Modifica
4. Cauta
e. Exit\n"""
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
                rez = srv.cautare(**fdict)
                for elem in rez:
                    print(elem, sep = " ")
                print()
            actions = {
                "1": lambda srv: srv.adauga(*self.createForm()),
                "2": lambda srv: srv.stergere(id=self.createForm("id")[0]),
                "3": lambda srv: srv.modificare_id(*self.createForm()),
                "4": cauta,
                "e": lambda srv: exit(0)
            }
            cmd = "Introduceti comanda: "

        while True:
            print(meniu)
            cmd = input("Introduceti comanda: ")
            if cmd in actions:
                try: actions[cmd](self.__srv)
                except MyException as me: print(str(me))

