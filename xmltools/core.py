'''Core XML tools


>>> @tagclass
... class aaa: pass
>>> @tagclass
... class bbb: pass

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

Here's a more complex example.
>>> doit(aaa['rst', bbb, 'uvw', bbb[aaa,]])
'<aaa>rst<bbb/>uvw<bbb><aaa/></bbb></aaa>'

Use make_args to give custom argument processing. Here's how to
provide default values, and map positional to named arguments.
>>> @tagclass
... class ccc:
...     @staticmethod
...     def make_args(a=0, b=1, c=2):
...         return (), locals()

>>> doit(ccc)
'<ccc a="0" c="2" b="1"/>'

>>> doit(ccc(5, b=7))
'<ccc a="5" c="2" b="7"/>'

This example also provides some error checking.
>>> ccc(1, 2, 3, 4)
Traceback (most recent call last):
TypeError: make_args() takes at most 3 arguments (4 given)

>>> ccc(d=5)
Traceback (most recent call last):
TypeError: make_args() got an unexpected keyword argument 'd'
'''

import lxml.etree

__metaclass__ = type


# TODO: Move to jfine.functools.
def return_args(*argv, **kwargs):
    '''Return pair (argv, kwargs).'''
    return argv, kwargs


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

    args = None                 # Set to (tuple, dict) by tag(...).
    body = None                 # Set to a tuple by tag(...)[...].

    make_args = return_args  # Subclass can override.


    def __init__(self, *argv, **kwargs):
        '''Read the source for init to see what it does.'''

        self.args = self.make_args(*argv, **kwargs)


    def __getitem__(self, body):
        '''Return self, mutated by self.body = body.'''

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
        kwargs = self.args[1]
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

                value.append(child.xml)

        return value


if __name__ == '__main__':

    import doctest
    print(doctest.testmod())
