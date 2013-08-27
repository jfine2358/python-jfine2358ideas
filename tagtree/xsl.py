'''Core for xsl tags
'''

__metaclass__ = type

import lxml.etree

from .core import OPTIONAL
from .core import REQUIRED
from .core import tagtype
from .core import tagdecoratorfactory
from .core import complextag
from .core import complextagbase
from .core import simpletagbase


class xsltagtype(tagtype):

    # Properties of an xsltag, even when not instantiated.
    # TODO: These need to be kept in sync with wibble (ugh).
    @property
    def xml(tag):
        return tag().xml

    @property
    def xml_pp(tag):
        return tag().xml_pp


class xsltagbase(complextagbase):

    metaclass = xsltagtype

    NAMESPACE = 'http://www.w3.org/1999/XSL/Transform'

    @staticmethod
    def translate_name(name):
        '''Return QName associated to Python name.

        >>> doit = xsltagbase.translate_name
        >>> doit('abc')
        'abc'
        >>> doit('if_')
        'if'
        >>> doit('ns__name')
        'ns:name'

        >>> doit('long_compound_name')
        'long-compound-name'

        >>> doit('ns__ns__name')
        'ns:ns--name'
        '''
        # TODO: Translate first '

        if name.endswith('_'):
            name = name[:-1]

        seq = name.split('__', 1)
        if len(seq) == 2:
            name = ':'.join(seq)

        return name.replace('_', '-')

    @property
    def xml_tag(self):

        ns = self.NAMESPACE
        name = self.__class__.__name__
        # Remove one trailing underscore, if present.
        if name.endswith('_'):
            name = name[:-1]
        # Replace underscore by hyphen.
        name = name.replace('_', '-')
        return '{{{0}}}{1}'.format(ns, name)

    def make_attrib(self, args):

        return dict(
            (self.translate_name(name), unicode(value))
            for name, value in self.head.items()
            # TODO: Test suppress when value is None.
            if value is not OPTIONAL
            )

    @property
    def xml_pp(self):
        '''Return XML pretty print of a tag.
        '''

        # Wrap self to suppress namespace.
        @xsltag
        def wrap():
            return locals()
        xml = wrap[self,].xml              # TODO: Remove comma.

        s = lxml.etree.tostring(xml, pretty_print=True)
        lines = s.split('\n')
        s2 = '\n'.join(line[2:] for line in lines[1:-2])
        return s2


# This is just what I want.  It's so simple.
xsltag = tagdecoratorfactory(xsltagbase)



if __name__ == '__main__':

    import doctest
    print(doctest.testmod())
