'''Rewrite of core.py to make it simpler.

>>> tag = simpletagtype('tag', (), {})
>>> a = tag(aaa=1, bbb=2)
>>> b = a[1, 2, 3]
>>> c = tag[1, 2, 3]
>>> tag == type(a) == type(b) == type(c)
True
>>> a == b
True

>>> type(tag) == simpletagtype
True

>>> a.head
{'aaa': 1, 'bbb': 2}


>>> deco = tagdecoratorfactory(simpletagtype, (wobble,))

>>> @deco
... def wibble(a=REQUIRED, b=2, c=None):
...     'docstring'
...     return locals()

>>> a = wibble(a=1)
>>> sorted(a.head.items())
[('a', 1), ('b', 2)]

>>> print(a.pp_xml[:-1])
<wibble a="1" b="2"/>

>>> @deco
... def td(): return{}

>>> @deco
... def tr(): return{}

>>> print(tr[td['aaa',], td['bbb',]].pp_xml[:-1])
<tr>
  <td>aaa</td>
  <td>bbb</td>
</tr>

>>> a = wibble(b=1, c=2)
Traceback (most recent call last):
ValueError: missing keys: a

>>> type(wibble) == simpletagtype
True
>>> wibble.__doc__
'docstring'

'''

import lxml.etree

__metaclass__ = type

# DONE: Able to create classes and instances.
# DONE: Able to mutate instances.

OPTIONAL = object()             # Sentinel.
REQUIRED = object()             # Sentinel.

# Naming convention
# Type, BaseClass, Decorator
# simpletagtype, simpletagbase, simpletag
# htmltagtype, htmltagbase, htmltag
# xsltagtype, xsltagbase, xsltag

class tagbase:

    def __getitem__(self, body):
        '''Return self, mutated by self.body.extend(body).

        We treat tag()[node] as tag()[node,]. This fails if item is
        already a tuple, which is a markup abuse, except possibly when
        item is the empty tuple.
        '''
        if self.got_item:
            raise ValueError('tag[node][node] error')

        if type(body) != tuple:
            body = (body,)

        self.body.extend(body)
        self.got_item = True
        return self

    def __init__(*argv, **kwargs):

        # Remove self from argv.
        self = argv[0]          # In trouble if this fails.
        argv = argv[1:]

        self.head = None
        self.body = []          # Start as list, to be extended.
        self.got_item = False   # Don't allow tag()[node][node].

        # First make_args, and then use_args.
        # TODO: Move make_args to the tagtype?
        args = self.make_args(argv, kwargs)
        self.use_args(args)


class tagtype(type):
    '''
    '''

    # TODO: This is a basic class modifier - manipulate type and
    # bases.
    def __new__(cls_type, name, bases, cls_dict):

        bases = bases + (simpletagbase,)
        return type.__new__(cls_type, name, bases, cls_dict)


    def __getitem__(self, body):
        '''Returns self()[body], to permit elt[...].
        '''
        return self()[body]


class simpletagbase(tagbase):

    # All tags of same type should have same make_args.  Provides
    # basic properties.
    @classmethod
    def make_args(cls, argv, kwargs):
        if argv:
            raise ValueError
        return cls.process_args(**kwargs)

    # Usually, the processing of arguments will differ.
    @staticmethod
    def process_args(**kwargs):
        return kwargs

    # All tags of the same type should have the same use_args.
    def use_args(self, args):
        self.head = args


class simpletagtype(tagtype):
    pass


def tagfactory(metaclass, bases, fn):
    '''Return tag with fn(**kwargs) as processor.
'
    '''
    # TODO: doctest fn.__name__.
    process_args = staticmethod(fn)
    tag = metaclass(fn.__name__, bases, dict(process_args = process_args))
    fn.__name__ = fn.__name__ + '__process_args'
    tag.__doc__ = fn.__doc__

    return tag


def tagdecoratorfactory(tagtype, bases, doc=None):

    def deco(fn):
        return tagfactory(tagtype, bases, fn)

    # TODO: Test __doc__
    deco.__doc__ = doc
    return deco


class wobble:

    # TODO: is there a need for a metaclassmethod?
    @classmethod
    def make_args(cls, argv, kwargs):

        if argv:
            raise ValueError
        return cls.process_args(**kwargs)

    @staticmethod
    def filter_dict(arg_dict):
        '''Return (valid, invalid) dicts from arg_dict.
        '''

        valid = {}
        invalid = {}
        for k, v in arg_dict.items():

            if v is None:
                pass
            elif v is REQUIRED:
                invalid[k] = v
            else:
                valid[k] = v

        return valid, invalid


    # TODO: tags in same collection to have same use_args.
    def use_args(self, args):

        head, errors = self.filter_dict(args)

        if errors:
            msg = "missing keys: {0}"
            missing_keys = ','.join(errors)
            raise ValueError(msg.format(missing_keys))

        self.head = head
        # self.body is a list which can be extended.

    @property
    def xml_tag(self):
        '''Return class name, for use as the xml_tag.'''
        return self.__class__.__name__

    @staticmethod
    def make_attrib(args):

        return dict(
            (name, unicode(value))
            for name, value in args.items()
            # TODO: Test suppress when value is None.
            if value is not None
            )

    @property
    def xml(self):

        # TODO: More tests.
        elt = lxml.etree.Element(self.xml_tag)
        elt.attrib.update(self.make_attrib(self.head))

        if self.body:
            for child in self.body:

                # TODO: What if successive text nodes?
                # TODO: Allow custom processing of special children
                if isinstance(child, str):
                    # TODO: Is len redundant?
                    if len(elt):
                        elt[-1].tail = child
                    else:
                        elt.text = child
                    continue

                elt.append(child.xml)

        return elt


    @property
    def pp_xml(self):

        s = lxml.etree.tostring(self.xml, pretty_print=True)
        return s


if __name__ == '__main__':

    import doctest
    print(doctest.testmod())
