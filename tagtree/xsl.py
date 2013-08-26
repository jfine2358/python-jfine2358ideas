'''Tags for xslt stylesheets

>>> def doit(tag): print(tag.xml_pp)
>>> doit(apply_templates())
<xsl:apply-templates/>

Use tag.xml_pp to get pretty-printed form of tag.

>>> doit(apply_templates)
<xsl:apply-templates/>

>>> doit(apply_templates(select='the-selection', mode='the-mode'))
<xsl:apply-templates mode="the-mode" select="the-selection"/>

TODO: translate under to hyphen.
>>> doit(sort(data_type='number'))
<xsl:sort data_type="number"/>
'''

__metaclass__ = type

import lxml.etree

from .core import REQUIRED      # And optional to follow.
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
    def xml_pp(tag):
        return tag().xml_pp


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


xsltag = tagdecoratorfactory(xsltagtype, (XslBase, wobble))


#################################################
# Here are the xsl tags, in alphabetical order. #
#################################################

OPTIONAL = None


@xsltag
def apply_imports():
    return locals()

@xsltag
def apply_templates(select=OPTIONAL, mode=OPTIONAL):
    '''
    TODO: This is not being picked up by doctest.
    >>> aaa
    '''
    return locals()

@xsltag
def attribute(name=REQUIRED, namespace=OPTIONAL):
    return locals()

@xsltag
def attribute_set(name=REQUIRED, use_attribute_sets=OPTIONAL):
    return locals()

@xsltag
def call_template(name=REQUIRED):
    return locals()

@xsltag
def choose():
    return locals()

@xsltag
def comment():
    return locals()

@xsltag
def copy(use_attribute_sets=OPTIONAL):
    return locals()

@xsltag
def copy_of(select=REQUIRED):
    return locals()

@xsltag
def decimal_format(
    name=None,
    decimal_separator=None,
    grouping_separator=None,
    infinity=None,          # An odd line of code.
    minus_sign=None,
    Nan=None,
    percent=None,
    per_mille=None,
    zero_digit=None,
    digit=None,
    pattern_separator=None
    ):
    return locals()

@xsltag
def element(
    name=REQUIRED,
    namespace=OPTIONAL,
    use_attribute_sets=OPTIONAL):
    return locals()

@xsltag
def fallback():
    return locals()

@xsltag
def for_each(select=REQUIRED):
    return locals()

@xsltag
def if_(test=REQUIRED):
    return locals()

@xsltag
def import_(href=REQUIRED):
    return locals()

@xsltag
def include(href=REQUIRED):
    return locals()

@xsltag
def key(name=REQUIRED, match=REQUIRED, use=REQUIRED):
    return locals()

@xsltag
def message(terminate=OPTIONAL):
    return locals()

@xsltag
def namespace_alias(
    stylesheet_prefix=REQUIRED,
    result_prefix=REQUIRED
    ):
    return locals()

@xsltag
def number(
    level = OPTIONAL,
    count = OPTIONAL,
    from_ = OPTIONAL,
    value = OPTIONAL,
    format = OPTIONAL,
    lang = OPTIONAL,
    letter_value = OPTIONAL,
    grouping_separator = OPTIONAL,
    grouping_size = OPTIONAL,
    ):
    return locals()

@xsltag
def otherwise():
    return locals()

@xsltag
def output(
    method = OPTIONAL,
    version = OPTIONAL,
    encoding = OPTIONAL,
    omit_xml_declaration = OPTIONAL,
    standalone = OPTIONAL,
    doctype_public = OPTIONAL,
    doctype_system = OPTIONAL,
    cdata_section_elements = OPTIONAL,
    indent = OPTIONAL,
    media_type = OPTIONAL
    ):
    return locals()

@xsltag
def param(name=REQUIRED, select=OPTIONAL):
    return locals()

@xsltag
def preserve_space(elements=REQUIRED):
    return locals()

@xsltag
def processing_instruction(name=REQUIRED):
    return locals()

@xsltag
def sort(
    select = OPTIONAL,
    order = OPTIONAL,
    case_order = OPTIONAL,
    lang = OPTIONAL,
    data_type = OPTIONAL
    ):
    return locals()

@xsltag
def strip_space(elements=REQUIRED):
    return locals()

@xsltag
def stylesheet(
    id = OPTIONAL,              # Also a Python builtin.
    version = OPTIONAL,
    extension_element_prefixes = OPTIONAL,
    exclude_result_prefixes = OPTIONAL
    ):
    return locals()

@xsltag
def template(
    match = OPTIONAL,
    name = OPTIONAL,
    priority = OPTIONAL,
    mode = OPTIONAL
    ):
    # If no match then name is required.
    return locals()

# Copy of stylesheet.
@xsltag
def transform(
    id = OPTIONAL,              # Also a Python builtin.
    version = OPTIONAL,
    extension_element_prefixes = OPTIONAL,
    exclude_result_prefixes = OPTIONAL
    ):
    return locals()

@xsltag
def text(disable_output_escaping=OPTIONAL):
    return locals()

@xsltag
def value_of(
    select = REQUIRED,
    disable_output_escaping = OPTIONAL
    ):
    return locals()

@xsltag
def variable(name=REQUIRED, select=OPTIONAL):
    return locals()

@xsltag
def when(test=REQUIRED):
    return locals()

@xsltag
def with_param(name=REQUIRED, select=OPTIONAL):
    return locals()

if __name__ == '__main__':

    import doctest
    print(doctest.testmod())
