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

        # GOTCHA: Not doing this was raising many exceptions.
        @staticmethod
        def process_args():
            return {}, None

    wrapper = wrap[elt,]
    xml = wrapper.xml
    s = lxml.etree.tostring(xml, pretty_print=True)

    lines = s.split('\n')
    s2 = '\n'.join(line[2:] for line in lines[1:-2])
    print(s2)


def translate_name(name):
    '''Return QName associated to Python name.

    >>> doit = translate_name
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

class XslBase:

    NAMESPACE = 'http://www.w3.org/1999/XSL/Transform'

    @property
    def xml_tag(self):

        ns = self.NAMESPACE
        name = self.__class__.__name__
        # Replace underscore by hyphen.
        name = name.replace('_', '-')
        return '{{{0}}}{1}'.format(ns, name)


    def make_attrib(self, args):

        return dict(
            (translate_name(name), unicode(value))
            for name, value in self.head.items()
            # TODO: Test suppress when value is None.
            if value is not None
            )


class NoArgs:

    @staticmethod
    def process_args(*argv, **kwargs):

        if argv or kwargs:
            raise ValueError('this element class has no parameters')
        return {}, None


def process_parameters(cls, parameters):
    '''Return body consisting of cls elements.

    The parameters are always in alphabetical order.
    '''
    body = []
    for name, value in sorted(parameters.items()):
        body.append(cls(name, value))
    return body


class mode(str):
    '''Use mode('ns:name') pass a mode argument.
    '''

class namespace(str):
    '''Use namespace('http://example.org') pass a namespace argument.
    '''

class qname(str):
    '''Use mode('ns:name') pass a name argument.
    '''

###################################################
# Keep the element classes in alphabetical order. #
###################################################

@elementclass
class apply_imports(XslBase, NoArgs):
    '''
    >>> pp_elt(apply_imports)
    <xsl:apply-imports/>
    '''

def head_from_argv(argv):

    # GOTCHA: map class to name, not vice-versa.
    name_for = {
        mode: 'mode',
        str: 'select',
        }

    pairs = [(name_for[type(arg)], arg) for arg in argv]
    head = dict(pairs)

    if len(pairs) != len(head):
        raise ValueError    # TODO: Test this.

    return head


@elementclass
class apply_templates(XslBase):
    '''
    Use trailing underscore to access 'tag parameters'.
    >>> pp_elt(apply_templates(mode('abc')))
    <xsl:apply-templates mode="abc" select="*"/>

    >>> elt = apply_templates(
    ...    'author|title',
    ...    mode('abc'),
    ...    wibble = 'an-expression',
    ...    wobble = [text('template body'),],
    ... )

    >>> pp_elt(elt)
    <xsl:apply-templates mode="abc" select="author|title">
      <xsl:with-param name="wibble" select="an-expression"/>
      <xsl:with-param name="wobble">
        <xsl:text>template body</xsl:text>
      </xsl:with-param>
    </xsl:apply-templates>
    '''
    @staticmethod
    def process_args(*argv, **parameters):

        head = dict(select='*')
        head.update(head_from_argv(argv))

        body = process_parameters(with_param, parameters)
        return head, body


@elementclass
class attribute(XslBase):
    '''
    The rules for what happens here are a bit odd (see Kay's book).
    It would be good to clean this up by revising the interface.  From
    the information set point of view, what's required is a (uri,
    ncname) pair.

    >>> pp_elt(attribute('wibble'))
    <xsl:attribute name="wibble"/>

    >>> pp_elt(attribute('wibble', 'http://example.org'))
    <xsl:attribute namespace="http://example.org" name="wibble"/>
    '''

    # GOTCHA: typed process_arguments, not warned.
    @staticmethod
    def process_args(name, namespace=None):

        return locals(), None

@elementclass
class attribute_set(XslBase):
    '''
    >>> pp_elt(attribute_set('padding'))
    <xsl:attribute-set name="padding"/>

    >>> pp_elt(attribute_set('padding', 'wibble wobble'))
    <xsl:attribute-set name="padding" use-attribute-sets="wibble wobble"/>

    '''
    @staticmethod
    def process_args(name, use_attribute_sets=None):
        return locals(), None


@elementclass
class call_template(XslBase):
    '''
    >>> pp_elt(call_template('aaa'))
    <xsl:call-template name="aaa"/>

    Here's what we write.
    >>> elt = call_template('aaa',
    ...    wibble = 'an-expression',
    ...    wobble = [text('template body'),],
    ... )

    Here's what we get.
    >>> pp_elt(elt)
    <xsl:call-template name="aaa">
      <xsl:with-param name="wibble" select="an-expression"/>
      <xsl:with-param name="wobble">
        <xsl:text>template body</xsl:text>
      </xsl:with-param>
    </xsl:call-template>
    '''

    @staticmethod
    def process_args(_name, **parameters):
        body = process_parameters(with_param, parameters)
        return dict(name=_name), body


@elementclass
class choose(XslBase, NoArgs):
    '''choose[ when +, otherwise ?]
    '''

@elementclass
class otherwise(XslBase, NoArgs):
    pass


@elementclass
class param(XslBase):
    '''
    >>> pp_elt(param('width'))
    <xsl:param name="width"/>
    >>> pp_elt(param('width', '*'))
    <xsl:param name="width" select="*"/>
    '''

    # Keep same as xsl.with_param.
    @staticmethod
    def process_args(name, select=None):

        if isinstance(select, list):
            return dict(name=name), select

        else:
            return locals(), None


@elementclass
class template(XslBase):
    '''
    >>> elt = template(
    ...    __match ='aa',
    ...    wibble = 'an-expression',
    ...    wobble = [text('template body'),],
    ... )[
    ...    text('TEMPLATE BODY'),
    ... ]

    >>> pp_elt(elt)
    <xsl:template match="aa">
      <xsl:param name="wibble" select="an-expression"/>
      <xsl:param name="wobble">
        <xsl:text>template body</xsl:text>
      </xsl:param>
      <xsl:text>TEMPLATE BODY</xsl:text>
    </xsl:template>
    '''

    # TODO: Allow template to have name, mode and match.
    allow_extension = True

    @staticmethod
    def process_args(**parameters):

        # Allow xsl.template to have match etc parameters, via __match
        # (a bit of a hack)

        # TODO: Clean up and refactor this __ hack for template
        # attributes.

        # There might be head items in the parameters.
        # Make list of items to move.
        move_pairs = tuple(
            (key[2:], key)
            for key in parameters
            if key.startswith('__')
            )

        # Move the items.
        head = {}
        for k1, k2 in move_pairs:
            head[k1] = parameters[k2]
            del parameters[k2]

        # Check the head dictionary.
        def check_head(match=None, name=None, priority=None, mode=None):
            pass
        check_head(**head)

        # Almost done.  Now create the body and return (head, body).
        body = process_parameters(param, parameters)
        return head, body


# An element that has a custom xml property.
@elementclass
class text(XslBase):

    @staticmethod
    def process_args(text):
        return locals(), None

    @property
    def xml(self):

        elt = lxml.etree.Element(self.xml_tag)
        elt.text = self.head['text']
        return elt


@elementclass
class stylesheet(XslBase):
    '''
    >>> elt = stylesheet(
    ...    wibble = 'an-expression',
    ...    wobble = [text('template body'),],
    ...    woozle = '',
    ... )[
    ...     template(),
    ...  ]

    TODO: Note that params output in alphabetic order.
    >>> pp_elt(elt)
    <xsl:stylesheet version="1.0">
      <xsl:param name="wibble" select="an-expression"/>
      <xsl:param name="wobble">
        <xsl:text>template body</xsl:text>
      </xsl:param>
      <xsl:param name="woozle" select=""/>
      <xsl:template/>
    </xsl:stylesheet>
    '''

    # TODO: Allow stylesheet to import.
    allow_extension = True

    @staticmethod
    def process_args(**parameters):
        body = process_parameters(param, parameters)
        return dict(version='1.0'), body

@elementclass
class value_of(XslBase):
    '''
    >>> pp_elt(value_of('abc'))
    <xsl:value-of select="abc"/>
    '''
    # Keep same as xsl.param etc.
    @staticmethod
    def process_args(select=None):

        if isinstance(select, list):
            return dict(name=name), select
        else:
            return locals(), None

@elementclass
class when(XslBase):

    # TODO: have elementclass promote process_args to staticmethod?
    @staticmethod
    def process_args(test):
        return locals(), None


@elementclass
class with_param(XslBase):
    '''
    >>> pp_elt(with_param('wibble'))
    <xsl:with-param name="wibble"/>

    TOOD: In this case, forbid adding to body.
    >>> pp_elt(with_param('wibble', 'an-expression'))
    <xsl:with-param name="wibble" select="an-expression"/>

    >>> pp_elt(with_param('wibble', [text('template-body')]))
    <xsl:with-param name="wibble">
      <xsl:text>template-body</xsl:text>
    </xsl:with-param>
    '''

    # Keep same as xsl.param.
    @staticmethod
    def process_args(name, select=None):

        if isinstance(select, list):
            return dict(name=name), select

        else:
            return locals(), None


if __name__ == '__main__':

    import doctest
    # Ensure the we have xmltools.xsl.mode, not __main__.mode' etc.
    import xmltools.xsl as this_module
    print(doctest.testmod(this_module))
