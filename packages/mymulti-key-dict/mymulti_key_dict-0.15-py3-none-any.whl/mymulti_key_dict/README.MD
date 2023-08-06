# Access nested dict elements as d[[1,2,3]] instead of d[1][2][3] - compatible with dict() - no requirements

## pip install mymulti-key-dict 

#### Tested against Windows 10 / Python 3.10 / Anaconda 


The MultiKeyDict class is a special type of dictionary that allows you to use lists 
as keys to access and modify nested elements within the dictionary. 
This feature sets it apart from regular dictionaries and provides additional
flexibility in working with hierarchical data structures.

Using lists as keys in the MultiKeyDict allows you to traverse multiple levels of nesting 
in a single operation. For example, if you have a nested dictionary d and you want to 
access the value at **d\[1\]\[2\]\[3\]**, you can simply pass the list **\[1, 2, 3\]** 
as the key ( **d\[\[1, 2, 3\]\]** )
to retrieve the desired value. This makes it easier to work with complex nested 
structures and eliminates the need for multiple indexing operations.

Furthermore, the MultiKeyDict class provides methods for converting the nested dictionary to 
a normal dictionary, making a deep copy of the dictionary, retrieving items, keys, and values, 
updating the dictionary with another dictionary, clearing the dictionary, and more. 
These methods make it convenient to perform common dictionary operations 
while preserving the nested structure.

By extending the dict class, the MultiKeyDict class inherits the basic dictionary functionality 
and adds the ability to handle nested keys. 
It also overrides certain methods, such as **\_\_getitem\_\_**, **\_\_setitem\_\_**, **\_\_delitem\_\_**, and others, 
to enable the list key functionality and provide the expected behavior for accessing 
and modifying nested elements.


```python

from mymulti_key_dict import MultiKeyDict
dict2 = {2: {"c": 222}, 3: {"d": {3, 6}}}
d = MultiKeyDict(dict2)

d[[1, 3, 4, 5, 67]] = 100
print(d[[1, 3]])
dd = {2: {"c": 222}, 3: {"d": {3, 6}}}
print(f"{list(d)=}")
print(f"{len(d)=}")
print(f"{d[1]=}")
print(f"{d[1][3]=}")
print(f"{d[[1,3]]=}")
d[[23, 4, 5, 323]] = "x"
print(f"""d[[23,4,5,323]] = 'x'={d}""")
print(f"{23 in d=}")
del d[[1, 3]]
print(f"""del d[[1,3]]={d}""")
del d[1]
print(f"""del d[1]={d}""")
di2 = d.copy()
print(f"{di2 == d=}")
print(f"{di2 is d=}")
di2.clear()
print(f"""di2.clear()={di2}""")
print(f"{list(iter(d))=}")
print(f"{d.get(2)=}")
print(f"{d.get([23,4,5])=}")
print(f"{d.items()=}")
print(f"{d.keys()=}")
print(f"{d.pop(3)=}")
print(f"{d.pop([23,4,5])=}")
print(f"""{d.popitem()=}""")
print(f"""after d.popitem={d}""")
dict2 = {2: {"c": 222}, 3: {"d": {3, 6}}, 4: 3, 33: {33: 2}}
d = MultiKeyDict(dict2)
print(f"""{list(d.reversed())=}""")
d.update({4: {44: 4}})
print(f"""d.update...={d}""")
d5 = d | {3: 4}
d |= {3: 4}
print(f"""d |= {{3:4}}={d}""")
print(f'{d.to_dict()=}')





{4: {5: {67: 100}}}
list(d)=[2, 3, 1]
len(d)=3
d[1]={3: {4: {5: {67: 100}}}}
d[1][3]={4: {5: {67: 100}}}
d[[1,3]]={4: {5: {67: 100}}}
d[[23,4,5,323]] = 'x'={1: {3: {4: {5: {67: 100}}}},
 2: {'c': 222},
 3: {'d': {3,
           6}},
 23: {4: {5: {323: 'x'}}}}
23 in d=True
del d[[1,3]]={1: {},
 2: {'c': 222},
 3: {'d': {3,
           6}},
 23: {4: {5: {323: 'x'}}}}
del d[1]={2: {'c': 222},
 3: {'d': {3,
           6}},
 23: {4: {5: {323: 'x'}}}}
di2 == d=True
di2 is d=False
di2.clear()={}
list(iter(d))=[2, 3, 23]
d.get(2)={'c': 222}
d.get([23,4,5])={323: 'x'}
d.items()=dict_items([(2, {'c': 222}), (3, {'d': {3, 6}}), (23, {4: {5: {323: 'x'}}})])
d.keys()=dict_keys([2, 3, 23])
d.pop(3)={'d': {3, 6}}
d.pop([23,4,5])={323: 'x'}
d.popitem()=(2, {'c': 222})
after d.popitem={23: {4: {}}}
list(d.reversed())=[33, 4, 3, 2]
d.update...={2: {'c': 222},
 3: {'d': {3,
           6}},
 4: {44: 4},
 33: {33: 2}}
d |= {3:4}={2: {'c': 222},
 3: 4,
 4: {44: 4},
 33: {33: 2}}
d.to_dict()={2: {'c': 222}, 3: 4, 4: {44: 4}, 33: {33: 2}}

```