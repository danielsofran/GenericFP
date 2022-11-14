# Generic FP
Generic class, repository, service and console UI builder for quick storing entities.

# Dependencies
This library requiers *jsonpickle* python package.
```pip install jsonpickle```, or
```python -m pip install jsonpickle```

# Classes

## 1. Entity
Represents an abstractized entity.

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

#### Static functions
* ```fromStr(cls, sir: str)```: creates the object based on a string coded by *__repr__*

Example: ```assert entity == Entity.fromStr(repr(entity))```

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
