'''Tags for xslt stylesheets

>>> def doit(tree): print(tree.pp_xml[:-1])
>>> doit(apply_templates())
<apply_templates/>


TODO: Add xml etc to the metaclass to avoid

>>> doit(apply_templates)
Traceback (most recent call last):
TypeError: 'property' object is unsubscriptable

'''

__metaclass__ = type


from .core import tagtype
from .core import tagdecoratorfactory
from .core import wobble        # TODO: rename, refactor.


class xsltagtype(tagtype):
    pass

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
