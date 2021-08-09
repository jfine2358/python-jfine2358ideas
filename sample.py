import lxml.etree
from xmltools.xsl import *
from xmltools.core import elementclass

__metaclass__ = type


def ppp(elt):
    return lxml.etree.tostring(elt.xml, pretty_print=True)

def pp2(elt):
    return lxml.etree.tostring(elt, pretty_print=True)


# HTML elements.
@elementclass
class body: pass

@elementclass
class html: pass

@elementclass
class table: pass

@elementclass
class tr: pass

@elementclass
class td: pass


# Data elements.
@elementclass
class author: pass

@elementclass
class book: pass

@elementclass
class books: pass

@elementclass
class price: pass

@elementclass
class title: pass


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

    template(__match = 'books',
             )[
        html[
            body[
                table(width='640')[
                    apply_templates
                    ]
                ]
            ]
        ],

    template(__match = 'book')[
        tr[
            td['1'],
            apply_templates,
            ]
        ],

    template(__match = 'author|title|price')[
        td[value_of('.')
           ]
        ],
    ]


if __name__ == '__main__':

    # Run everything.

    fn = lxml.etree.XSLT(my_xsl.xml)
    result = fn(data.xml, profile_run=True)

    for item in [ppp(data), ppp(my_xsl), pp2(result), pp2(result.xslt_profile)]:

        print()
        print(item.decode())
