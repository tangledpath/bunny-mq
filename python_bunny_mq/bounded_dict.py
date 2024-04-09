class BoundedDict(dict):
    def __init__(self, max_entries=10000, *args, **kwargs):
        self.update(*args, **kwargs)
        self.max_entries = max_entries

    def __getitem__(self, key):
        val = dict.__getitem__(self, key)
        print('GET', key)
        return val

    def __setitem__(self, key, val):
        print('SET', key, val)
        dict.__setitem__(self, key, val)

    def __repr__(self):
        dictrepr = dict.__repr__(self)
        return '%s(%s)' % (type(self).__name__, dictrepr)

    def __truncate(self):
        """ Remove entries from the beginning until we are at max_entries or less """
        while len(self) > self.max_entries:
            del self[self.keys()[0]]
