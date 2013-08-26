'''Tags for xslt stylesheets

>>> def doit(tree): print(tree.pp_xml[:-1])
>>> doit(apply_templates())
<apply_templates/>


>>> doit(apply_templates)
<apply_templates/>
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
    pass


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
