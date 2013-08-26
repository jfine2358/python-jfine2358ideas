'''Tags for xslt stylesheets

>>> print(apply_templates().pp_xml)
<xsl:apply-templates/>

TODO: Is .xml_pp better - the xml pretty printed.
>>> print(apply_templates.pp_xml)
<xsl:apply-templates/>

'''

__metaclass__ = type

import lxml.etree

from .core import tagtype
from .core import tagdecoratorfactory
from .core import wobble        # TODO: rename, refactor.


class xsltagtype(tagtype):

    # Properties of an xsltag, even when not instantiated.
    # TODO: These need to be kept in sync with wibble (ugh).
    @property
    def xml(tag):
        return tag().xml

    @property
    def pp_xml(tag):
        return tag().pp_xml


class XslBase:

    NAMESPACE = 'http://www.w3.org/1999/XSL/Transform'

    @property
    def xml_tag(self):
        return

    @property
    def xml_tag(self):

        ns = self.NAMESPACE
        name = self.__class__.__name__
        # Replace underscore by hyphen.
        name = name.replace('_', '-')
        return '{{{0}}}{1}'.format(ns, name)

    @property
    def pp_xml(self):

        # Wrap self to suppress namespace.
        @xsltag
        def wrap():
            return locals()
        xml = wrap[self,].xml              # TODO: Remove comma.

        s = lxml.etree.tostring(xml, pretty_print=True)
        lines = s.split('\n')
        s2 = '\n'.join(line[2:] for line in lines[1:-2])
        return s2


xsltag = tagdecoratorfactory(xsltagtype, (XslBase, wobble))


@xsltag
def apply_templates(select=None, mode=None):
    '''
    TODO: This is not being picked up by doctest.
    >>> aaa
    '''

    return locals()

if __name__ == '__main__':

    import doctest
    print(doctest.testmod())
