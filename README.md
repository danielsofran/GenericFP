# Generic FP
Generic class, repository, service and console UI builder for quick storing entities.

# Dependencies
This library requiers *jsonpickle* python package. It can be installed using 
```pip install jsonpickle```, or
```python -m pip install jsonpickle``` commands.

# Classes

## 1. Entity
Represents an abstracted entity.

> Important! <br>
> If the entity has a unique identifier, it's recommended to name it ***'id'*** and put it as ***the first field*** in the entity.

> Important! <br>
> As python allows to dinamically add attributes to an object or change its type,
> *Entity* class allows these operations aswell.

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
  
    def setId(self, value):
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

### Constructor
* ```Entity(**kwargs)```: creates an entity with the given fields and values

### Public Member Functions
* ```__getitem__(self, field: str)```, ```__setitem__(self, field: str, value)```: defines the getters and the setters for all fields
* ```__str__(self)```: automate conversion to string that is supposed to be read by a user
* ```__repr__```: converts the entity to a string in the purpose of storing the data
* ```__eq__(self, other)```: checks if two entities are equal, meaning they have the same field names and values
* ```__hash__(self)```: returns the entity's hash code
* ```__iter__(self)```: iterates over the field names and its instance values
* ```__len__(self)```: returns the number of fields

Example
```python3
for field_name, field_value in entity:
    print(field_name, field_value)  # do stuff...
```

### Static functions
* ```from_str(cls, sir: str)```: creates the object based on a string coded by *__repr__*

Example

```python3
assert entity == Entity.from_str(repr(entity))
```

## 2. Pattern
Pattern represents the class definition as the association between the names of the fields and their types.
A pattern it's basically an entity where the value of a field is its type.
Pattern allows users to check if an entity 'follows' a pattern.

Example
```python3
pattern=Pattern(id=int, name=str, age=int)
assert pattern.ok(entity) == True  # the previously declared entity follows this pattern
```

### Constructor
* ```Pattern(**kwargs)```: creates a pattern with the given fields and types

### Public Member Functions
* all the functions from *Entity* class, as *Pattern* is inherited from *Entity*
* ```ok(self, entity: Entity)```: checks if the given entity follows the pattern

### Static functions
* ```from_entity(cls, entity: Entity)```: creates a pattern based on an entity

## 3. Repository
Represents the way to store a set of entities ***in memory***. It implements *CRUD* methods like *add*, *remove*, *modify* and *find*, but it can be inherited and added more functions, even though it's not a recommended practice. It can store ***only entities with similar pattern***.

> Note: <br>
> If the pattern is not specified, the repository will store all entities with the same pattern as the first entity inserted or read.

### Constructor
* ```Repository(pattern: Pattern = None)```: creates a repository with the given pattern

### Protected Fields
* ```_entities```: stores the entities
* ```_pattern```: stores the pattern

### Public Member Functions
* ```add(self, obj: Entity)```: Adds an entity in the repository. Raises *RepoException* if the entity already exists(it's a duplicate), or if the entity's pattern does not match the pattern of the entities from the repository.
* ```remove(self, obj: Entity)```: Removes the entity from the repository. Raises *RepoException* if the entity could not be found.
* ```modify(self, obj1: Entity, obj2: Entity)```: Replaces the first occurance of *obj1* with *obj2*. Raises *RepoException* if their pattern doesn't match the repository's pattern.
* ```find(self, *lambdas, **kwargs)```: Returns a list of all entities that has the field values that are in kwargs *OR* returnes true for the predicates that are evaluated as *True*.
* ```__len__(self)```: Returns the number of entities stored in the repository.
* ```__iter__(self)```: Allows the user to iterate over the entities stored in the repository.
* ```toList(self)```: Creates and returns a copy of the list of entities.

Example

```python3
person1 = Entity(id=1, name='Name1', age=20)
person2 = Entity(id=2, name='Name2', age=18)
person3 = Entity(id=3, name='Name3', age=32)

pattern = Pattern(id=int, name=str, age=int)
r = Repository(pattern)  # the pattern is optional, but it's not recommended to omit it
r.add(person1)
r.add(person2)
r.add(person3)
assert len(r) == 3


def filter1(entity):
    return entity['id'] > 1


def filter2(entity):
    return entity['age'] > 18


# returns all the entities filtered by filterl OR filter2 OR the inline function OR have the id equals to 1
r.find(filter1, filter2, lambda e: 'Name' in e['name'], id=1)
r.find(id=1, name='Name2')  # returns all the entities that have the id equals to 1 or the name 'Name2'
r.find(filter1)

r.remove(person3)
r.modify(person2, person3)

for person in r:
    print(r)
```

## 4. FileRepository
Represents the way to store a set of entities ***in a file***. It implements *CRUD* methods like *add*, *remove*, *modify* and *find*, but it can be inherited and added more functions, even though it's not a recommended practice. It can store ***only entities with similar pattern***.

### Constructor
* ```FileRepository(filename: str, pattern: Pattern = None)```: creates a repository with the given pattern and filename. If the pattern is not given, it will be read from the file.

### Public Member Functions
* all the functions from *Repository* class, as *FileRepository* is inherited from *Repository*

## 5. Exceptions
* ```BaseAutoGeneratingException(Exception)```: the base class for all exceptions
* ```RepoException```: raised when an error occurs in the repository
* ```ValidException```: raised when an error occurs in the validator
* ```ServiceException```: raised when an error occurs in the service
* ```NoPatternException```: raised when a service is created for a repository with no pattern.

## 6. Validator
Validator is a class that checks if an entity is valid. It's used by the service to check if an entity is valid before using it.

### Constructor
* ```Validator(**kwargs)```: assigns the given functions to the fields

All the given values for the name of the fields must be predicates, or functions that take one parameter and return a boolean value.
The other data will be ignored.

Example
```python3
# the validator will check if the id is a positive integer, the name is a string and the age is greater or equal to 0
validator = Validator(id=lambda x: x > 0, name=lambda x: len(x) > 0, age=lambda x: x >= 0)
```

### Public Member Functions
* ```__call__(self, entity: Entity)```: checks if the entity is valid. Raises *ValidatorException* otherwise.

Example
```python3
validator(Entity(id=1, name='Name', age=20)) # no exception is raised
validator(Entity(id=-1, name='Name', age=20)) # raises ValidatorException as the id is not valid
validator(Entity(id=-1, name='', age=20)) # raises ValidatorException as the id is not valid
```

## 7. Service
Service is a class that allows the user to interact with the repository. It's used to add, remove, modify and find entities in the repository. It's also used to check if an entity is valid before performing any operation on it.

> Important: <br>
> Service provides **only the basic CRUD** operations. If you want to add more operations, you can inherit from it and add more functions.<br>
> Note that the functions that are added shouldn't be as generic as the predefined ones 

### Constructor
* ```Service(validator: Validator, repo: Repository)```: creates a service with the given repository and validator

### Protected Member Functions
* ```_list_of_fields_to_entity(self, fields)```: converts a list of fields to the entity specified by the repository's pattern

### Public Member Functions
* ```add(self, *args)```: Creates an entity with the given arguments and the pattern specified by the repository and adds it to the repository
* ```remove(self, **kvargs)```: removes the entities that satisfies the function given or has the given value from the repository
* ```modify(self, *args)```: modifies the first entity having the values given in the first half with the entity having the values given in the second half
* ```modify_firstfield(self, *args)```: modifies the first entity having the first field as given by setting the other fields to the given values. This function is used when the first field is the unique identifier of the entity, such as ```id```.
* ```find(self, *lambdas, **kwargs)```: returns a list of all entities that has the field values that are in kwargs *OR* returns true for the predicates that are evaluated as *True*.
* ```get_elements(self)```: returns a list with all the entities stored in the repository

Example
```python3
service = Service(validator, repo)
service.add(1, 'Name1', 20)
service.add(2, 'Name2', 18)
service.add(3, 'Name3', 32)
service.modify(1, 'Name1', 20, 1, 'Name1', 18) # modifies the age of the entity with id 1 to 18
service.modify_firstfield(1, 'Name1', 18) # the same as above
service.remove(id=1) # removes the entity with id 1
assert len(service) == 1

# removes all the entities with age greater than 18 or name containing '3'
service.remove(lambda e: e['age'] > 18, lambda e: '3' in e['name']) # the last entity is removed
service.find(id=1) # returns the entity with id 1
service.find(lambda e: e['age'] > 18) # empty list returned
```

## 8. Console
Console is a class that allows the user to interact with the service. It has a default menu to add, remove, modify and find entities in the repository.

> Note: <br>
> Console provides **only the basic CRUD** operations. If you want to add more operations, the best way is to inherit from it and add more functions.<br>

### Constructor
* ```Console(service: Service)```: creates a console with the given service

### Public Member Functions
* ```create_form(self, *field_names)```: creates a form with the given arguments. The arguments must be strings, and they will be used as the names of the fields. The form will be displayed in the console and will return the list of given inputs.
* ```menu(self, menu: str = None, cmd: str = None, **actions)```: creates a menu with the given actions. The actions must be functions that take the service as parameter. The menu will be displayed in the console.

Legend:
* *menu*: the menu title to be displayed. If it's not given, the default ***'Menu'*** will be displayed
* *cmd*: the command to be displayed. If it's not given, the default ***'Enter the command'*** will be displayed
* *actions*: the associations between the command and the function to be executed. The command must be a string, and the function must take the service as parameter.

Example
```python3
console=Console(service)
console.menu()
```
