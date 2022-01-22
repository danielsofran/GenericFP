from domain import *
from repository import *
from service import Service
from validator import *

def afisare(l):
    for elem in l:
        print(elem)

r = FileRepository("repo.txt", ['id', 'nume', 'bani'])

v = Validator()

s = Service(v, r)
#s.adauga(1, "2", 3)
afisare(r)
s.stergere(cheie="")
afisare(r)
