# Generic FP
Generic class, repository, service and console UI builder for quick storing entities.

# Dependencies
This library requiers *jsonpickle* python package. It can be installed using 
```pip install jsonpickle```, or
```python -m pip install jsonpickle``` commands.

# Classes

## 1. Entity
Represents an abstractized entity.

##### Important! If the entity has an unique identifier, it's recommended to name it 'id'

Example: the following code
```python3
class Entity:
  def __init__(self):
    self.__id = 1
    self.__name = 'Name'
    self.__age = 20
  
  def getId(self): 
    return self.__id
  
  def getName(self):
    return self.__name
  
  def getAge(self):
    return self.__age
  
  def setId(self):
    self.__id = value
  
  def setName(self, value):
    self.__name = value
  
  def setAge(self, value):
    self.__age = value
    
entity = Entity()
entity.setAge(30)
print(entity.getAge())
```
can be easily written as
```python3
entity=Entity(id=1, name='Name', age=20) 
entity['age']=30
print(entity['age'])
```

#### Member functions
* ```__getitem__(self, field: str)```, ```__setitem__(self, field: str, value)```: defines the getters and the setters for all fields
* ```pattern(self)```: returns the list with the names of the fields
* ```__str__(self)```: automate conversion to string that is supposed to be read by a user
* ```__repr__```: converts the entity to a string in the purpose of storing the data
* ```__eq__(self, other)```: checks if two entities are equal, meaning they have the same field names and values
* ```__hash__(self)```: returns the entity's hash code
* ```__iter__(self)```: iterates over the field names and its instance values

Example
```python3
for field_name, field_value in entity:
  # do stuff...
```

#### Static functions
* ```fromStr(cls, sir: str)```: creates the object based on a string coded by *__repr__*

Example
```python3
assert entity == Entity.fromStr(repr(entity))
```

## 2. Pattern
Pattern represents the class definition as the association between the names of the fields and their types.
A pattern it's basically an entity where the value of a field is its type.
Patterns allows users to check if an entity 'follows' a pattern.

Example
```python3
pattern=Pattern(id=int, name=str, age=int)
assert pattern.ok(entity) == True  # the previously declared entity follows this pattern
```

## 3. Repository
Represents the way to store a set of entities ***in memory***. It implements *CRUD* methods like *add*, *remove*, *modify* and *find*, but it can be inherited and added more functions, even though it's not a recommended practice. It can store ***only entities with similar pattern***.

### Member functions
* ```adauga(self, obj: Entity)```: Adds an entity in the repository. Raises *RepoException* if the entity already exists(it's a duplicate), or if the entity's pattern does not match the pattern of the entities from the repository.
* ```stergere(self, obj: Entity)```: Removes the entity from the repository. Raises *RepoException* if the entity could not be found.
* ```modificare(self, obj1: Entity, obj2: Entity)```: Replaces the first occurance of *obj1* with *obj2*. Raises *RepoException* if their pattern doesn't match the repository's pattern.
* ```cautare(self, *lambdas, **kwargs)```: Returns a list of all entities that has the field values that are in kwargs *OR* returnes true for the predicates that are evaluated as *True*.
* ```__len__(self)```: Returns the number of entities stored in the repository.
* ```__iter__(self)```: Allows the user to iterate over the entities stored in the repository.
* ```toList(self)```: Creates and returns a copy of the list of entities.

Example
```python3
person1=Entity(id=1, name='Name1', age=20)
person2=Entity(id=2, name='Name2', age=18)
person3=Entity(id=3, name='Name3', age=32)

pattern=Pattern(id=int, name=str, age=int)
r = Repository(pattern) # the pattern is optional, but it's not recommended to omit it
r.adauga(person1)
r.adauga(person2)
r.adauga(person3)

def filtru1(entity):
  return entity['id'] > 1
  
de filtru2(entity):
  return entity['age'] > 18

r.cautare(filtru1, filtru2, lambda e: 'Name' in e['name'], id=1) # returneaza entitatile care respecta filtru1 SAU filtru2 SAU functia inline SAU are id-ul egal cu 1
```
