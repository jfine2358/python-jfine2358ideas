'''Core XML tools


>>> @elementclass
... class aaa: pass
>>> @elementclass
... class bbb: pass

The four partial and full instantiations of a element.
>>> e0 = aaa
>>> e1 = aaa['abc',]
>>> e2 = aaa(a=1, b=2)
>>> e3 = aaa(a=1, b=2)['abc',]

You cannot reassign the body.
>>> e1['def',]
Traceback (most recent call last):
AttributeError: element already has body

Elements can be converted to xml.
>>> def doit(t, pp=False):
...     return lxml.etree.tostring(t.xml, pretty_print=pp)

>>> doit(e0)
'<aaa/>'
>>> doit(e1)
'<aaa>abc</aaa>'
>>> doit(e2)
'<aaa a="1" b="2"/>'
>>> doit(e3)
'<aaa a="1" b="2">abc</aaa>'

Here's a more complex example.
>>> doit(aaa['rst', bbb, 'uvw', bbb[aaa,]])
'<aaa>rst<bbb/>uvw<bbb><aaa/></bbb></aaa>'

Use xml_tag to override the default value.
>>> @elementclass
... class template:
...    xml_tag = '{http://www.w3.org/1999/XSL/Transform}template'

>>> @elementclass
... class html:
...    pass

TODO: Clean up the test code.
>>> print(doit(template(match='poem')[html,], pp=True)[:-1])
<xsl:template xmlns:xsl="http://www.w3.org/1999/XSL/Transform" match="poem">
  <html/>
</xsl:template>

Use process_args to give custom argument processing. Here's how to
provide default values, and map positional to named arguments.
>>> @elementclass
... class ccc:
...     @staticmethod
...     def process_args(a=0, b=1, c=2):
...         return ((), locals()), None

>>> doit(ccc)
'<ccc a="0" c="2" b="1"/>'

>>> doit(ccc(5, b=7))
'<ccc a="5" c="2" b="7"/>'

This example also provides some error checking.
>>> ccc(1, 2, 3, 4)
Traceback (most recent call last):
TypeError: process_args() takes at most 3 arguments (4 given)

>>> ccc(d=5)
Traceback (most recent call last):
TypeError: process_args() got an unexpected keyword argument 'd'


Use make_attrib to give custom conversion of the args into an
attributes dictionary.  Here's how to replace underscored by hyphens
in XML attribute names.  Each set of element classes might have its
own conversion, which could be given using a lookup table.  The
mapping could also add namespaces.

>>> @elementclass
... class ddd:
...     @staticmethod
...     def make_attrib(args):
...         return dict(
...             (name.replace('_', '-'), value)
...             for name, value in args[1].items()
...          )

>>> doit(ddd(keep_alive='true'))
'<ddd keep-alive="true"/>'
'''

import lxml.etree

__metaclass__ = type


# TODO: Move to jfine.functools.
def return_args(*argv, **kwargs):
    '''Return pair (argv, kwargs).'''
    return argv, kwargs


class elementclass(type):

    def __new__(type_, cls):

        name = cls.__name__
        # This is a hack to avoid:
        # TypeError: Cannot create a consistent method resolution
        # order (MRO) for bases object, ElementBase
        bases = tuple(
            c for c in cls.__bases__
            if c is not object
            ) + (ElementBase,)
        attrib = dict(cls.__dict__)

        new_cls = type.__new__(type_, name, bases, attrib)
        return new_cls


    def __getitem__(self, body):
        '''Returns self()[body], to permit elt[...].
        '''
        return self()[body]


    @property
    def xml(self):
        return self().xml


class ElementBase:

    head = None                 # Set to (tuple, dict) by elt(...).
    body = None                 # Set to a tuple by elt(...)[...].

    def process_args(*argv, **kwargs):
        '''Return initial values for (head, body).

        Subclass can, and probably should, override.
        '''
        return (argv, kwargs), None


    def __init__(self, *argv, **kwargs):
        '''Read the source for init to see what it does.'''

        self.head, self.body = self.process_args(*argv, **kwargs)


    def __getitem__(self, body):
        '''Return self, mutated by self.body = body.'''

        # Forbid elt(...)[...][...].
        if self.body is not None:
            raise AttributeError('element already has body')

        # TOOD: Make this optional? Place in element class bases.
        if not isinstance(body, tuple):
            raise ValueError('Expecting tuple, missing comma perhaps')

        self.body = body
        return self


    @staticmethod
    def make_attrib(args):

        return dict(
            (name, unicode(value))
            for name, value in args[1].items()
            # TODO: Test suppress when value is None.
            if value is not None
            )


    # TODO: Can I define this as a classproperty?
    @property
    def xml_tag(self):
        '''Return class name, for use as the xml_tag.'''
        return self.__class__.__name__


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


if __name__ == '__main__':

    import doctest
    print(doctest.testmod())
