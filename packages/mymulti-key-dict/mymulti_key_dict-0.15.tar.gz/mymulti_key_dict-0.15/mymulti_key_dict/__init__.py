import operator
from pprint import pformat


def convert_to_normal_dict_simple(di):
    if isinstance(di, MultiKeyDict):
        di = {k: convert_to_normal_dict_simple(v) for k, v in di.items()}
    return di


class MultiKeyDict(dict):

    def __init__(self, seq=None, **kwargs):
        if seq:
            super().__init__(seq, **kwargs)

        def convert_dict(di):
            if (isinstance(di, dict) and not isinstance(di, self.__class__)) or (
                    (hasattr(di, "items") and hasattr(di, "keys") and hasattr(di, "keys"))
            ):
                ndi = self.__class__({}, )
                for k, v in di.items():
                    ndi[k] = convert_dict(v)
                return ndi
            return di

        for key in self:
            self[key] = convert_dict(self[key])

    def __str__(self):
        return pformat({k: v for k, v in super().items()}, width=1)

    def __missing__(self, key):
        self[key] = self.__class__({})
        return self[key]

    def __repr__(self):
        return self.__str__()

    def __delitem__(self, i):
        if isinstance(i, list):
            if len(i) > 1:
                lastkey = i[-1]
                i = i[:-1]
                it = iter(i)
                firstkey = next(it)
                value = self[firstkey]
                for element in it:
                    value = operator.itemgetter(element)(value)
                del value[lastkey]
            else:
                super().__delitem__(i[0])
        else:
            super().__delitem__(i)

    def __getitem__(self, key, /):
        if isinstance(key, list):
            if len(key) > 1:
                it = iter(key)
                firstkey = next(it)
                value = self[firstkey]
                for element in it:
                    value = operator.itemgetter(element)(value)
                return value
            else:
                return super().__getitem__(key[0])
        else:
            return super().__getitem__(key)

    def __setitem__(self, i, item):
        if isinstance(i, list):
            if len(i) > 1:
                lastkey = i[-1]
                i = i[:-1]
                it = iter(i)
                firstkey = next(it)
                value = self[firstkey]
                for element in it:
                    value = operator.itemgetter(element)(value)
                value[lastkey] = item
            else:
                return super().__setitem__(i[0], item)
        else:
            return super().__setitem__(i, item)

    def to_dict(self):
        return convert_to_normal_dict_simple(self)

    def update(self, other, /, **kwds):
        other = self.__class__(other)
        super().update(other, **kwds)

    def get(self, key, default=None):
        v = default
        if not isinstance(key, list):
            return super().get(key, default)
        else:
            if len(key) > 1:
                it = iter(key)
                firstkey = next(it)
                value = self[firstkey]
                for element in it:
                    if element in value:
                        value = operator.itemgetter(element)(value)
                    else:
                        return default
            else:
                return super().get(key[0], default)
            return value

    def pop(self, key, default=None):
        if not isinstance(key, list):
            return super().pop(key, default)

        elif len(key) == 1:
            return super().pop(key[0], default)
        else:
            return self._del_and_return(key, default)

    def _del_and_return(self, key, default=None):
        newkey = key[:-1]
        delkey = key[-1]
        it = iter(newkey)
        firstkey = next(it)
        value = self[firstkey]
        for element in it:
            if element in value:
                value = operator.itemgetter(element)(value)
            else:
                return default

        value1 = value[delkey]
        del value[delkey]
        return value1

    def reversed(self):
        return reversed(list(iter(self.keys())))
