'''XLS elements

>>> import lxml.etree

>>> def doit(elt):
...     print(lxml.etree.tostring(elt.xml, pretty_print=True)[:-1])


>>> doit(text(' abc '))
<xsl:text xmlns:xsl="http://www.w3.org/1999/XSL/Transform"> abc </xsl:text>

>>> doit(choose)
<xsl:choose xmlns:xsl="http://www.w3.org/1999/XSL/Transform"/>

Here's a populated choose element.
>>> elt = choose[
...     when('condition1')[text('first'),],
...     when('condition2')[text('second'),],
...     otherwise[text('default'),],
... ]

>>> doit(elt)
<xsl:choose xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:when test="condition1">
    <xsl:text>first</xsl:text>
  </xsl:when>
  <xsl:when test="condition2">
    <xsl:text>second</xsl:text>
  </xsl:when>
  <xsl:otherwise>
    <xsl:text>default</xsl:text>
  </xsl:otherwise>
</xsl:choose>

It's an error to give choose an argument.
>>> choose(a=1)
Traceback (most recent call last):
ValueError: this element class has no parameters
'''

import lxml.etree
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


# Keep the element classes in alphabetical order.
@elementclass
class choose(XslBase, NoArgs):
    '''choose[ when +, otherwise ?]
    '''

@elementclass
class otherwise(XslBase, NoArgs):
    pass


# An element that has a custom xml property.
@elementclass
class text(XslBase):

    @staticmethod
    def make_args(text):
        return (), dict(text=text)

    @property
    def xml(self):

        elt = lxml.etree.Element(self.xml_tag)
        elt.text = self.args[1]['text']
        return elt


@elementclass
class when(XslBase):

    # TODO: have elementclass promote make_args to staticmethod?
    @staticmethod
    def make_args(test):
        return (), dict(test=test)


if __name__ == '__main__':

    import doctest
    print(doctest.testmod())
