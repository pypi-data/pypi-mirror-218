# MultiKeyIterDict enhances the capabilities of the standard dictionary by supporting multiple keys, nested searches, and operations such as updates and merges (without loosing data) on dicts

## pip install multikeyiterdict 

### Support for Multiple Keys: 

MultiKeyIterDict enhances the capabilities of the standard dictionary 
by supporting multiple keys, nested searches, and operations such as
 updates and merges (without loosing data) on nested data structures. 
It is particularly beneficial when working with complex nested 
dictionaries or hierarchical data.

### Nested Search: 

MultiKeyIterDict provides methods such as nested_value_search 
and nested_key_search that allow you to search for values or 
keys within the nested structure of the dictionary. 
These methods can simplify searching and retrieval of 
specific values or keys within complex nested dictionaries.

### Nested Update and Merge: 

The nested_update and nested_merge methods enable updating and 
merging of dictionaries with nested key-value pairs. 
These methods handle the merging of nested data structures seamlessly, providing a convenient way to update or combine 
dictionaries with complex hierarchical data.

### Iterable Keys and Values: 

The nested_keys, nested_values, and nested_items 
methods generate iterable results for the nested keys, 
values, and items in the dictionary. 
This can be useful when you need to iterate over 
or process the nested elements of the dictionary.






```python
from multikeyiterdict import MultiKeyIterDict

dict2 = {2: {"c": 222}, 3: {"d": {3, 6}}}
d = MultiKeyIterDict(dict2)
d[[1, 3, 4, 5, 67]] = 100
print(d[[1, 3]])
dd = {2: {"c": 222}, 3: {"d": {3, 6}}}
print(f"\n\n-----------------------\n{list(d)=}")
print(f"\n\n-----------------------\n{len(d)=}")
print(f"\n\n-----------------------\n{d[1]=}")
print(f"\n\n-----------------------\n{d[1][3]=}")
print(f"\n\n-----------------------\n{d[[1,3]]=}")
d[[23, 4, 5, 323]] = "x"
print(f"\n\n-----------------------\n" "d[[23,4,5,323]] = 'x'={d}" "")
print(f"\n\n-----------------------\n{23 in d=}")
del d[[1, 3]]
print(f"\n\n-----------------------\n" "del d[[1,3]]={d}" "")
del d[1]
print(f"\n\n-----------------------\n" "del d[1]={d}" "")
di2 = d.copy()
print(f"\n\n-----------------------\n{di2 == d=}")
print(f"\n\n-----------------------\n{di2 is d=}")
di2.clear()
print(f"\n\n-----------------------\n" "di2.clear()={di2}" "")
print(f"\n\n-----------------------\n{list(iter(d))=}")
print(f"\n\n-----------------------\n{d.get(2)=}")
print(f"\n\n-----------------------\n{d.get([23,4,5])=}")
print(f"\n\n-----------------------\n{d.items()=}")
print(f"\n\n-----------------------\n{d.keys()=}")
print(f"\n\n-----------------------\n{d.pop(3)=}")
print(f"\n\n-----------------------\n{d.pop([23,4,5])=}")
print(f"\n\n-----------------------\n{d.popitem()=}")
print(f"\n\n-----------------------\nafter d.popitem={d}")
dict2 = {2: {"c": 222}, 3: {"d": {3, 6}}, 4: 3, 33: {33: 2}}
d = MultiKeyIterDict(dict2)
print(f"\n\n-----------------------\n{list(d.reversed())=}")
d.update({4: {44: 4}})
print(f"\n\n-----------------------\nd.update...={d}")
d5 = d | {3: 4}
d |= {3: 4}
print(f"\n\n-----------------------\nd |= {{3:4}}={d}")
print(f"\n\n-----------------------\n{d.to_dict()=}")

#########################################
print(f"\n\n-----------------------\n{list(d.nested_items())=}")
print(f"\n\n-----------------------\n{list(d.nested_values())=}")
print(f"\n\n-----------------------\n{list(d.nested_keys())=}")
print(f"\n\n-----------------------\n{list(d.nested_value_search(4))=}")
d[[1, 3, 4, 5, 67]] = 100
for key in d.nested_key_search(67):
    print(key)

for key in d.nested_key_search(4):
    print(key)

d7 = d.nested_merge({221: 2, 3: 4})
print(f"\n\n-----------------------\nafter nested merge {d7=}")

d.nested_update({221: 2, 3: 4})
print(f"\n\n-----------------------\nafter nested update {d=}")
#########################################



{4: {5: {67: 100}}}
-----------------------
list(d)=[2, 3, 1]
-----------------------
len(d)=3
-----------------------
d[1]={3: {4: {5: {67: 100}}}}
-----------------------
d[1][3]={4: {5: {67: 100}}}
-----------------------
d[[1,3]]={4: {5: {67: 100}}}
-----------------------
d[[23,4,5,323]] = 'x'={d}
-----------------------
23 in d=True
-----------------------
del d[[1,3]]={d}
-----------------------
del d[1]={d}
-----------------------
di2 == d=True
-----------------------
di2 is d=False
-----------------------
di2.clear()={di2}
-----------------------
list(iter(d))=[2, 3, 23]
-----------------------
d.get(2)={'c': 222}
-----------------------
d.get([23,4,5])={323: 'x'}
-----------------------
d.items()=dict_items([(2, {'c': 222}), (3, {'d': {3, 6}}), (23, {4: {5: {323: 'x'}}})])
-----------------------
d.keys()=dict_keys([2, 3, 23])
-----------------------
d.pop(3)={'d': {3, 6}}
-----------------------
d.pop([23,4,5])={323: 'x'}
-----------------------
d.popitem()=(2, {'c': 222})
-----------------------
after d.popitem={23: {4: {}}}
-----------------------
list(d.reversed())=[33, 4, 3, 2]
-----------------------
d.update...={2: {'c': 222},
 3: {'d': {3,
           6}},
 4: {44: 4},
 33: {33: 2}}
-----------------------
d |= {3:4}={2: {'c': 222},
 3: 4,
 4: {44: 4},
 33: {33: 2}}
-----------------------
d.to_dict()={2: {'c': 222}, 3: 4, 4: {44: 4}, 33: {33: 2}}
-----------------------
list(d.nested_items())=[([2, 'c'], 222), ([3], 4), ([4, 44], 4), ([33, 33], 2)]
-----------------------
list(d.nested_values())=[222, 4, 4, 2]
-----------------------
list(d.nested_keys())=[[2, 'c'], [3], [4, 44], [33, 33]]
-----------------------
list(d.nested_value_search(4))=[[3]]
([1, 3, 4, 5, 67], 100)
([4], {44: 4})
([1, 3, 4], {5: {67: 100}})
-----------------------
after nested merge d7={2: {'c': 222}, 3: [4, 4], 4: {44: 4}, 33: {33: 2}, 1: {3: {4: {5: {67: 100}}}}, 221: 2}
-----------------------
after nested update d={1: {3: {4: {5: {67: 100}}}},
 2: {'c': 222},
 3: [4,
     4],
 4: {44: 4},
 33: {33: 2},
 221: 2}


```