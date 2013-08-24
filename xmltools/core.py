'''Core XML tools


>>> @tagclass
... class aaa: pass

The four partial and full instantiations of a tag.
>>> t0 = aaa
>>> t1 = aaa['abc',]
>>> t2 = aaa(a=1, b=2)
>>> t3 = aaa(a=1, b=2)['abc',]

You cannot reassign the body.
>>> t1['def',]
Traceback (most recent call last):
AttributeError: element already has body

Tags can be converted to xml.
>>> def doit(t): return lxml.etree.tostring(t.xml)

>>> doit(t0)
'<aaa/>'
>>> doit(t1)
'<aaa>abc</aaa>'
>>> doit(t2)
'<aaa a="1" b="2"/>'
>>> doit(t3)
'<aaa a="1" b="2">abc</aaa>'
'''

import lxml.etree

__metaclass__ = type


class tagclass(type):

    def __new__(type_, cls):

        name = cls.__name__
        bases = (TagBase,)
        attrib = dict(cls.__dict__)

        new_cls = type.__new__(type_, name, bases, attrib)
        return new_cls


    def __getitem__(self, body):
        '''Returns self()[body], to permit tag[...].
        '''
        return self()[body]


    @property
    def xml(self):
        return self().xml


class TagBase:

    argv = None                 # Set to a tuple by tag(...).
    kwargs = None               # Set to a dict by tag(...).
    body = None                 # Set to a tuple by tag(...)[...].

    def __init__(self, *argv, **kwargs):

        # TODO: Allow subclass to process args.
        self.argv = argv
        self.kwargs = kwargs


    def __getitem__(self, body):
        '''Return self, mutated by self.body = body.
        '''

        # Forbid tag(...)[...][...].
        if self.body is not None:
            raise AttributeError('element already has body')

        # TOOD: Make this optional? Place in tag bases.
        if not isinstance(body, tuple):
            raise ValueError('Expecting tuple, missing comma perhaps')

        self.body = body
        return self


    @property
    def xml(self):

        # TODO: More tests.
        # TODO: Custom mapping of args.
        name = self.__class__.__name__
        kwargs = self.kwargs
        value = lxml.etree.Element(name)
        value.attrib.update(
            (key, unicode(value))
            for key, value in kwargs.items()
            )

        if self.body:
            for child in self.body:

                # TODO: What if successive text nodes?
                # TODO: Allow custom processing of special children
                if isinstance(child, str):
                    # TODO: Is len redundant?
                    if len(value):
                        value[-1].tail = child
                    else:
                        value.text = child
                    continue

                # TODO: Remove this wart.
                if isinstance(child, tagtype):
                    child = child()
                value.append(child.xml)

        return value


if __name__ == '__main__':

    import doctest
    print(doctest.testmod())
