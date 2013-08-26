'''Rewrite of core.py to make it simpler.

'''

# import lxml.etree

__metaclass__ = type

# DONE: Able to create classes and instances.
# DONE: Able to mutate instances.

REQUIRED = object()             # Sentinel.

class _TagBase:

    def __getitem__(self, body):
        '''Return self, mutated by self.body = body.'''

        self.body = body
        return self

    def __init__(*argv, **kwargs):

        # Remove self from argv.
        self = argv[0]          # In trouble if this fails.
        argv = argv[1:]

        # TODO: I now think this code is a bad idea.
        if 0:
            # TODO: Refactor and doctest this.
            if len(argv) != 1:
                name = type(self).__name__
                # TypeError: f() takes exactly 0 arguments (1 given)
                msg = '{0}() does not take positional arguments ({1} given)'
                raise TypeError(msg.format(name, len(argv) - 1))

        args = self.make_args(argv, kwargs)
        self.use_args(args)


    # TODO: tags in same collection to have same make_args.
    # TODO: is there a need for a metaclassmethod?
    @classmethod
    def make_args(cls, argv, kwargs):

        if argv:
            raise ValueError

        return cls.process_args(**kwargs)

    # TODO: tags in same collection to have same use_args.
    # TODO: Migrate this, perhaps to basictag.
    def use_args(self, args):

        self.head = args


    # TODO: This is particular to the tag.
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


def tagfactory(bases, fn):
    '''Return tag with fn(**kwargs) as processor.
    >>> def wibble(a=REQUIRED, b=2, c=None):
    ...     'docstring'
    ...     return locals()

    >>> wibble = tagfactory((wobble,), wibble)


    >>> a = wibble(a=1)
    >>> sorted(a.head.items())
    [('a', 1), ('b', 2)]

    >>> a = wibble(b=1, c=2)
    Traceback (most recent call last):
    ValueError: missing keys: a

    >>> type(wibble) == tagtype
    True
    >>> wibble.__doc__
    'docstring'
    '''
    # TODO: doctest fn.__name__.
    fn.__name__ = fn.__name__ + '__process_args'
    process_args = staticmethod(fn)
    tag = tagtype(fn.__name__, bases, dict(process_args = process_args))
    tag.__doc__ = fn.__doc__

    return tag


class wobble:

    # TODO: is there a need for a metaclassmethod?
    @classmethod
    def make_args(cls, argv, kwargs):

        if argv:
            raise ValueError
        return cls.process_args(**kwargs)

    # TODO: tags in same collection to have same use_args.
    def use_args(self, args):

        head = {}
        errors = {}
        for k, v in args.items():

            if v is None:
                pass
            elif v is REQUIRED:
                errors[k] = v
            else:
                head[k] = v

        if errors:
            msg = "missing keys: {0}"
            missing_keys = ','.join(errors)
            raise ValueError(msg.format(missing_keys))

        self.head = head



if __name__ == '__main__':

    import doctest
    print(doctest.testmod())
