'''XLS elements

>>> import lxml.etree

>>> def doit(elt):
...     print(lxml.etree.tostring(elt.xml, pretty_print=True)[:-1])


>>> pp_elt(text(' abc '))
<xsl:text> abc </xsl:text>

>>> pp_elt(choose)
<xsl:choose/>

Here's a populated choose element.
>>> elt = choose[
...     when('condition1')[text('first'),],
...     when('condition2')[text('second'),],
...     otherwise[text('default'),],
... ]

>>> pp_elt(elt)
<xsl:choose>
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

# Copied from testtools.py so can avoid import, make own version.
def pp_elt(elt):

    # Start hack to suppress names spaces in output.
    @elementclass
    class wrap(XslBase):
        pass

    wrapper = wrap[elt,]
    xml = wrapper.xml
    s = lxml.etree.tostring(xml, pretty_print=True)

    lines = s.split('\n')
    s2 = '\n'.join(line[2:] for line in lines[1:-2])
    print(s2)


class XslBase:

    NAMESPACE = 'http://www.w3.org/1999/XSL/Transform'

    @property
    def xml_tag(self):

        ns = self.NAMESPACE
        name = self.__class__.__name__
        # Replace underscore by hyphen.
        name = name.replace('_', '-')
        return '{{{0}}}{1}'.format(ns, name)

class NoArgs:

    @staticmethod
    def make_args(*argv, **kwargs):

        if argv or kwargs:
            raise ValueError('this element class has no parameters')
        return argv, kwargs


# Keep the element classes in alphabetical order.

@elementclass
class apply_templates(XslBase):
    '''
    >>> pp_elt(apply_templates(mode='abc'))
    <xsl:apply-templates mode="abc" select="*"/>
    '''
    @staticmethod
    def make_args(select='*', mode=None):
        return (), locals()


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
        return (), locals()

    @property
    def xml(self):

        elt = lxml.etree.Element(self.xml_tag)
        elt.text = self.args[1]['text']
        return elt

@elementclass
class param(XslBase):
    '''
    >>> pp_elt(param('width'))
    <xsl:param name="width"/>
    >>> pp_elt(param('width', '*'))
    <xsl:param name="width" select="*"/>
    '''
    @staticmethod
    def make_args(name, select=None):
        return (), locals()


@elementclass
class when(XslBase):

    # TODO: have elementclass promote make_args to staticmethod?
    @staticmethod
    def make_args(test):
        return (), locals()


if __name__ == '__main__':

    import doctest
    print(doctest.testmod())
