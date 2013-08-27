import lxml.etree
from tagtree.xsl_tags import *
from tagtree.core import complextag

__metaclass__ = type


def ppp(elt):
    print(lxml.etree.tostring(elt.xml, pretty_print=True))

def pp2(elt):
    print(lxml.etree.tostring(elt, pretty_print=True))


htmltag = complextag
datatag = complextag


# HTML elements.
@htmltag
def body(**kwargs):
    return kwargs

@htmltag
def html(**kwargs):
    return kwargs

@htmltag
def table(**kwargs):
    return kwargs

@htmltag
def tr(**kwargs):
    return kwargs

@htmltag
def td(**kwargs):
    return kwargs


# Data elements.
@datatag
def author(**kwargs):
    return kwargs

@datatag
def book(**kwargs):
    return kwargs

@datatag
def books(**kwargs):
    return kwargs

@datatag
def price(**kwargs):
    return kwargs

@datatag
def title(**kwargs):
    return kwargs


# Data.  Based on Kay's XSLT book.
data = books[

    book(category='reference')[
        author['Nigel Rees'],
        title['Sayings of the century'],
        price['9.95'],
        ],

    book(category='fiction')[
        author['Evelyn Waugh'],
        title['Sword of Honour'],
        price['12.99'],
        ],

    book(category='fiction')[
        author['Hermann Melville'],
        title['Moby Dick'],
        price['8.99'],
        ],

    book(category='fiction')[
        author['J. R. R. Tolkien'],
        title['The Lord of the Rings'],
        price['22.99'],
        ],
    ]


# Stylesheet.  Based on Kay's XSLT book.
my_xsl = stylesheet[

    template(match = 'books')[
        html[
            body[
                table(width='640')[
                    apply_templates
                    ]
                ]
            ]
        ],

    template(match = 'book')[
        tr[
            td[number],
            apply_templates,
            ]
        ],

    template(match = 'author|title|price')[
        td[value_of(select='.')
           ]
        ],
    ]


if __name__ == '__main__':

    # Run everything.
    ppp(data)
    ppp(my_xsl)

    fn = lxml.etree.XSLT(my_xsl.xml)
    result = fn(data.xml, profile_run=True)

    pp2(result)
    pp2(result.xslt_profile)
