from domain import *
from repository import *
from service import Service
from validator import *

def afisare(l):
    for elem in l:
        print(elem)

pattern = Pattern(id=int, nume=str, bani=float)
r = FileRepository("repo.txt")
#print(pattern.ok(r.toList()[0]))

v = Validator(id=lambda id: id>0)

s = Service(v, r)
#s.adauga(-3, "grigore", 10.0)
#s.stergere(id=1, nume="2")
#s.modificare(3, "ninja", 11.0, 3, "grigore", 10.0)
#s.modificare_id(3, "ninja", 11.0)
afisare(r)

