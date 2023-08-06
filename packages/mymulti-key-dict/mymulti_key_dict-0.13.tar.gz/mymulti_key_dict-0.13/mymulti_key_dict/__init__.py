import operator
from collections import UserDict, defaultdict
from functools import reduce
from pprint import pformat
from copy import deepcopy


def nested_dict():
    return defaultdict(nested_dict)


def convert_to_default_dict(di):
    if isinstance(di, dict):
        ndi = nested_dict()
        for k, v in di.items():
            ndi[k] = convert_to_default_dict(v)
        return ndi
    return di


def convert_to_normal_dict_simple(di):
    if isinstance(di, defaultdict):
        di = {k: convert_to_normal_dict_simple(v) for k, v in di.items()}
    return di


class MultiKeyDict(UserDict):
    """
    A dictionary class that allows nested access and modification of dictionary elements.
    The class extends the UserDict class and provides additional functionality.

    Methods:
        __init__(self, initialdata=None, **kwargs):
            Initializes the MultiKeyDict object with optional initial data.

        __getitem__(self, key):
            Retrieves the value associated with the given key(s) from the nested dictionary.

        __setitem__(self, key, value):
            Sets the value associated with the given key(s) in the nested dictionary.

        __str__(self):
            Returns a string representation of the nested dictionary.

        __repr__(self):
            Returns a string representation of the nested dictionary.

        get(self, key, default=None):
            Retrieves the value associated with the given key(s) from the nested dictionary,
            or returns the default value if the key(s) is not found.

        pop(self, key, default=None):
            Removes and returns the value associated with the given key(s) from the nested dictionary,
            or returns the default value if the key(s) is not found.

        __delitem__(self, key):
            Removes the key(s) and its associated value(s) from the nested dictionary.

        setdefault(self, key, default=None):
            Raises a TypeError indicating that 'setdefault' is not allowed for the MultiKeyDict class.

        to_dict(self):
            Converts the nested dictionary to a normal dictionary and returns it.

        copy(self):
            Creates a deep copy of the MultiKeyDict object and returns it.

        items(self):
            Returns a list of key-value pairs from the nested dictionary.

        keys(self):
            Returns a list of keys from the nested dictionary.

        values(self):
            Returns a list of values from the nested dictionary.

        update(self, other=(), **kwds):
            Updates the nested dictionary with the key-value pairs from another dictionary.

        clear(self):
            Clears all the elements from the nested dictionary.

        reversed(self):
            Returns a reversed iterator of the keys in the nested dictionary.
    """

    def __init__(self, dict=None, /, **kwargs):
        super().__init__(dict,**kwargs)
        self.data = convert_to_default_dict(self.data)

    def __getitem__(self, key, /):
        if isinstance(key, list):
            v = self._get_from_original_iter(keys=key)
            if isinstance(v, defaultdict):
                return convert_to_normal_dict_simple(v)
            return v
        if isinstance(v := self.data[key], defaultdict):
            return convert_to_normal_dict_simple(v)
        return v

    def __setitem__(self, key, value):
        if isinstance(key, list):
            self._set_in_original_iter(key, value)
        else:
            self.data[key] = value

    def __str__(self):
        return pformat(convert_to_normal_dict_simple(self.data), width=1)

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def _convert2dict(d):
        try:
            return convert_to_normal_dict_simple(d)
        except Exception:
            return d

    def get(self, key, default=None):
        v = default
        if not isinstance(key, list):
            if key in self.data:
                v = self.data[key]
        else:
            v = self._get_from_original_iter(key)
        v = self.__class__._convert2dict(v)
        return v

    def pop(self, key, default=None):
        if not isinstance(key, list):
            v = super().pop(key, default)
            v = self.__class__._convert2dict(v)
            return v
        else:
            return self._convert2dict(self._del_and_return(key))

    def _del_and_return(self, key):
        newkey = key[:-1]
        delkey = key[-1]
        h = reduce(operator.getitem, newkey, self.data)
        value1 = h[delkey]
        del h[delkey]
        return value1

    def __delitem__(self, key):
        if not isinstance(key, list):
            super().__delitem__(key)
        else:
            _ = self._del_and_return(key)

    def setdefault(self, key, default=None):
        raise TypeError("setdefault not allowed!")

    def to_dict(self):
        return convert_to_normal_dict_simple(self.data)

    def copy(self):
        return self.__class__(deepcopy(self.data))

    def items(self):
        return self.to_dict().items()

    def keys(self):
        return self.to_dict().keys()

    def values(self):
        return self.to_dict().values()

    def update(self, other=(), /, **kwds):
        super().update(other, **kwds)
        self.data = convert_to_default_dict(self.data)

    def _get_from_original_iter(self, keys):
        return reduce(operator.getitem, keys, self.data)

    def _set_in_original_iter(self, keys, value):
        self._get_from_original_iter(keys[:-1])[keys[-1]] = value

    def clear(self):
        self.data = convert_to_default_dict({})

    def reversed(self):
        return reversed(list(iter(self.keys())))

