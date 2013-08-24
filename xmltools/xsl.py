'''XLS elements

>>> import lxml.etree

>>> def doit(elt):
...     print(lxml.etree.tostring(elt.xml, pretty_print=True)[:-1])


>>> doit(choose)
<xsl:choose xmlns:xsl="http://www.w3.org/1999/XSL/Transform"/>

Here's a populated choose element.
>>> elt = choose[
...     when('condition1'),
...     when('condition2'),
...     otherwise,
... ]

>>> doit(elt)
<xsl:choose xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:when test="condition1"/>
  <xsl:when test="condition2"/>
  <xsl:otherwise/>
</xsl:choose>

It's an error to give choose an argument.
>>> choose(a=1)
Traceback (most recent call last):
ValueError: this element class has no parameters
'''

__metaclass__ = type
from .core import elementclass


class XslBase:

    NAMESPACE = 'http://www.w3.org/1999/XSL/Transform'

    @property
    def xml_tag(self):

        ns = self.NAMESPACE
        name = self.__class__.__name__
        return '{{{0}}}{1}'.format(ns, name)

class NoArgs:

    @staticmethod
    def make_args(*argv, **kwargs):

        if argv or kwargs:
            raise ValueError('this element class has no parameters')
        return argv, kwargs


@elementclass
class choose(XslBase, NoArgs):
    '''choose[ when +, otherwise ?]
    '''

@elementclass
class when(XslBase):

    # TODO: have elementclass promote make_args to staticmethod?
    @staticmethod
    def make_args(test):
        return (), dict(test=test)


@elementclass
class otherwise(XslBase, NoArgs):
    pass



if __name__ == '__main__':

    import doctest
    print(doctest.testmod())
