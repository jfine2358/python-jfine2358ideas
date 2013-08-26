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

        if len(argv) != 1:
            # TODO: Revise and doctest this.
            name = type(self).__name__
            # TypeError: f() takes exactly 0 arguments (1 given)
            msg = '{0}() does not take positional arguments ({1} given)'
            raise TypeError(msg.format(name, len(argv) - 1))


class tagtype(type):
    '''
    >>> tag = tagtype('tag', (), {})
    >>> a = tag(aaa='1', bbb='2')
    >>> b = a[1, 2, 3]
    >>> c = tag[1, 2, 3]
    >>> tag == type(a) == type(b) == type(c)
    True
    >>> a == b
    True

    >>> type(tag) == tagtype
    True
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


if __name__ == '__main__':

    import doctest
    print(doctest.testmod())
