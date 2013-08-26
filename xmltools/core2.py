'''Rewrite of core.py to make it simpler.

'''

# import lxml.etree

__metaclass__ = type

# DONE: Able to create classes and instances.
# DONE: Able to mutate instances.

class _TagBase:

    def __getitem__(self, body):
        '''Return self, mutated by self.body = body.'''

        self.body = body
        return self

    def __init__(*argv, **kwargs):

        self = argv[0]          # In trouble if this fails.

        # TODO: Refactor and doctest this.
        if len(argv) != 1:
            name = type(self).__name__
            # TypeError: f() takes exactly 0 arguments (1 given)
            msg = '{0}() does not take positional arguments ({1} given)'
            raise TypeError(msg.format(name, len(argv) - 1))

        self.head = self.process_args(**kwargs)

    @staticmethod
    def process_args(**kwargs):

        return kwargs


class tagtype(type):
    '''
    >>> tag = tagtype('tag', (), {})
    >>> a = tag(aaa=1, bbb=2)
    >>> b = a[1, 2, 3]
    >>> c = tag[1, 2, 3]
    >>> tag == type(a) == type(b) == type(c)
    True
    >>> a == b
    True

    >>> type(tag) == tagtype
    True

    >>> a.head
    {'aaa': 1, 'bbb': 2}

    '''

    # TODO: This is a basic class modifier - manipulate type and
    # bases.
    def __new__(cls_type, name, bases, cls_dict):

        bases = bases + (_TagBase,)
        return type.__new__(cls_type, name, bases, cls_dict)


    def __getitem__(self, body):
        '''Returns self()[body], to permit elt[...].
        '''
        return self()[body]


def basictag(fn):
    '''Return tag with fn(**kwargs) as processor.
    >>> @basictag
    ... def wibble(a=1, b=2, c=None):
    ...     'docstring'
    ...     return locals()

    >>> type(wibble) == tagtype
    True
    >>> wibble.__doc__
    'docstring'

    >>> a = wibble()
    >>> sorted(a.head.items())
    [('a', 1), ('b', 2), ('c', None)]
    '''

    process_args = staticmethod(fn)
    tag = tagtype(fn.__name__, (), dict(process_args = process_args))
    tag.__doc__ = fn.__doc__

    return tag





if __name__ == '__main__':

    import doctest
    print(doctest.testmod())
