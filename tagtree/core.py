'''Core code for tag trees

A tag tree is a particular sort of tree.  More abstractly, it is a
notation for specifying such a tree.  The non-data nodes of the tree
are called tags.  Tags are organised into families, such as HTML, SVG
and XSL.  All the tags in a family have a lot in common.  They differ only
in the way that they process the tag arguments.

Every tag has a head and a body.  (This is a small white lie.) The
body is a possibly empty list.  The head stores tag attributes as in
XML, or something similar.  The tag arguments determine the head, and
can sometimes also contribute to the body.

The argument processing interface depends on the tag family. Simple
tags have only keyword arguments, and are created using the simpletag
decorator.

>>> @simpletag
... def tag(**kwargs):
...     return kwargs

Here is a tag with an empty head and a body.
>>> bo = tag['the', 'body']
>>> bo.head, bo.body
({}, ['the', 'body'])


Here is a tag with a head and an empty body.
>>> ho = tag(the='head')
>>> ho.head, ho.body
({'the': 'head'}, [])

Here is a tag with both head and body.
>>> hb = tag(the='head')['the body']
>>> hb.head, hb.body
({'the': 'head'}, ['the body'])


Here is a tag without either head or body.  It's a little odd.
>>> no_hb = tag
>>> no_hb.head, no_hb.body
({}, [])

The no-head no-body instance of a tag is the tag itself.  It has empty
head and body to provide a consistent interface.  For empty tags the
head and body should be treated as read-only.

TODO And in a future release they will be.

TODO: Simple tag with positional arguments.

TOOD: Simple tag with restricted range of arguments.

TODO: Simple tag with default values.

TODO: Simple tag with optional values (but no default).

TODO: Maybe remove REQUIRED, OPTIONAL.

This shows the types.
>>> a = tag()
>>> b = a[1, 2, 3]
>>> c = tag[1, 2, 3]
>>> tag == type(a) == type(b) == type(c)
True
>>> a == b
True

>>> type(tag) == simpletagtype
True

The complextag has different processing.  Give tag type control over
error handling.  Useful for low-level mapping of tags to XML schema,
and thus for XML generation.

TODO: Rename to xmltag and require that values be strings.  Also
provide namespace support.

>>> @complextag
... def wibble(a=REQUIRED, b=2, c=OPTIONAL):
...     'docstring'
...     return locals()

>>> a = wibble(a=1)
>>> sorted(a.head.items())
[('a', 1), ('b', 2)]

>>> print(a.pp_xml[:-1])
<wibble a="1" b="2"/>

>>> @complextag
... def td(): return{}

>>> @complextag
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

# For Python3 compatibility.
try:
    unicode
except NameError:
    def unicode(arg):
        return arg

import lxml.etree

__metaclass__ = type

# Naming convention
# Type, BaseClass, Decorator
# simpletagtype, simpletagbase, simpletag
# htmltagtype, htmltagbase, htmltag
# xsltagtype, xsltagbase, xsltag

# TODO: rename simpletag to basictag (or valuetag?).
# TODO: rename complextag to xmltag.
# TODO: provide element('name', attribute='value').
# TODO: provide element('name', namespace, attribute='value').

class tagtype(type):
    '''Base type (not class) for all tags.

    Provides exactly the methods shared by all no-head no-body tags.

    * tag[node] calls and return tag()[body].
    * tag.head property gives empty dict - treat as read-only.
    * tag.body property gives empty list - treat as read-only.

    Subclass tagtype to provide additional methods on a tag family.
    '''
    def __getitem__(self, body):
        '''Returns self()[body], to permit elt[...].
        '''
        return self()[body]

    # TODO: Best would be to make head and body ordinary attributes,
    # namely a read-only dictionary and list respectively.
    # TODO: self not used, but don't see how to remove it.
    @property
    def head(self):
        '''Treat as read-only.'''
        return {}

    @property
    def body(self):
        '''Treat as read-only.'''
        return []


class tagbase:
    '''Base class for all tags.

    Every tag inherits from tagbase, which provide __init__ and
    __getitem__.  Subclasses should supply

    * a static function args = make_args(argv, kwargs)
    * an instance method self.use_args(args)

    All tags in the same family should share the same conventions
    regarding the nature of args.

    There should be no need, except for logging and the like, for a
    tag provide it's own __init__ and __getitem__ methods.

    TODO: Abstract Base Class? New in 2.6.
    '''

    metaclass = tagtype

    def __init__(*argv, **kwargs):

        # Remove self from argv.
        self = argv[0]          # In trouble if this fails.
        argv = argv[1:]

        self.head = {}          # Start as dict, to be updated.
        self.body = []          # Start as list, to be extended.
        # TODO: Rename to allow_getitem.
        self.got_item = False   # Don't allow tag()[node][node].

        # First make_args, and then use_args.
        # TODO: Move make_args to the tagtype?
        args = self.make_args(argv, kwargs)
        self.use_args(args)


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


# TODO: Rename to tagdecorator?
# TOOD: Allow baseclass to be class or tuple of classes.
def tagdecoratorfactory(baseclass, doc=None):

    def deco(fn):

        metaclass = baseclass.metaclass

        process_args = staticmethod(fn)
        tag = metaclass(fn.__name__, (baseclass,), dict(process_args = process_args))
        fn.__name__ = fn.__name__ + '__process_args'
        tag.__doc__ = fn.__doc__

        return tag

    # TODO: Test __doc__
    deco.__doc__ = doc
    return deco


simpletagtype = tagtype

class simpletagbase(tagbase):

    metaclass = tagtype

    # All tags of same type should have same make_args.  Provides
    # basic properties.
    @classmethod
    def make_args(cls, argv, kwargs):
        if argv:
            raise ValueError
        return cls.process_args(**kwargs)

    # All tags of the same type should have the same use_args.
    def use_args(self, args):
        self.head = args

    # Usually, the processing of arguments will differ.
    @staticmethod
    def process_args(**kwargs):
        return kwargs



# This is just what I want.  It's so simple.
simpletag = tagdecoratorfactory(simpletagbase)

######################################################################

OPTIONAL = object()             # Sentinel.
REQUIRED = object()             # Sentinel.

class complextagbase(simpletagbase):


    @staticmethod
    def filter_dict(arg_dict):
        '''Return (valid, invalid) dicts from arg_dict.
        '''

        valid = {}
        invalid = {}
        for k, v in arg_dict.items():

            if v is OPTIONAL:
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
            # TODO: Test suppress when value is OPTIONAL.
            if value is not OPTIONAL
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

complextag = tagdecoratorfactory(complextagbase)

if __name__ == '__main__':

    import doctest
    print(doctest.testmod())
