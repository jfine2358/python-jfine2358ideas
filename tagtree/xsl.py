'''Tags for xslt stylesheets

>>> def doit(tree): print(tree.pp_xml[:-1])
>>> doit(apply_templates())
<xsl:apply-templates xmlns:xsl="http://www.w3.org/1999/XSL/Transform"/>

>>> doit(apply_templates)
<xsl:apply-templates xmlns:xsl="http://www.w3.org/1999/XSL/Transform"/>

'''

__metaclass__ = type


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
