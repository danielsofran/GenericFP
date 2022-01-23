from console import Console
from domain import *
from repository import *
from service import Service
from validator import *

def afisare(l):
    for elem in l:
        print(elem)

pattern = Pattern(id=int, nume=str, bani=float)
r = FileRepository("repo.txt", pattern)
v = Validator(id=lambda id: id>0)

s = Service(v, r)
c = Console(s)
c.menu()
