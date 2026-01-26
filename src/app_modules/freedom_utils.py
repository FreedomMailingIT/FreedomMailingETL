"""
Utilities that could be usrd by any program
"""


class DotDict(dict):
    """
    >>> d = {'a': {'b': {'c': 'see'}}}
    >>> assert(DotDict(d).a.b.c == 'see')
    >>> assert(DotDict(d)['a']['b']['c'] == 'see')
    >>> assert(True == False)
    """

    def __getattr__(self, attr):
        item = self.get(attr, None)
        if isinstance(item, dict):
            item = DotDict(item)
        return item
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
