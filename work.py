import lxml.etree
__metaclass__ = type

class meta(type):

    def __getitem__(self, body):
        return self()[body]

class Base:

    def __init__(self, *argv, **kwargs):

        argv, kwargs = self.process_args(*argv, **kwargs)
        self.argv = argv
        self.kwargs = kwargs
        self.body = None


    @staticmethod
    def process_args(*argv, **kwargs):
        return argv, kwargs


    def __getitem__(self, body):

        if not isinstance(body, tuple):
            raise ValueError('Expecting tuple, missing comma perhaps')

        self.body = body
        return self

    def toxml(self):

        name = self.__class__.__name__
        kwargs = self.kwargs
        value = lxml.etree.Element(name, **kwargs)

        if self.body:
            for child in self.body:

                if isinstance(child, str):
                    # GOTCHA: tree body and html body.
                    if len(value):
                        value[-1].tail = child
                    else:
                        value.text = child
                    continue

                if isinstance(child, meta):
                    child = child()
                value.append(child.toxml())

        return value


def wibble(cls):

    d = dict(cls.__dict__)
    name = cls.__name__
    new_cls = meta(name, (Base,), d)
    return new_cls


@wibble
class apple:

    @staticmethod
    def process_args(a=1, b=2, x=3):
        return (), dict(a=a, b=b, x=x)


x = apple(3, 4, x=5)[
    'abc',
lxml]

print(x.argv)
print(x.kwargs)
print(x.body)


y = apple[
    'fgh',
    'ijk',
]

print(y.argv)
print(y.kwargs)
print(y.body)


@wibble
class html:
    pass


@wibble
class body:
    pass

@wibble
class p:
    pass

@wibble
class div:
    pass

@wibble
class b:
    pass


pear_div = div(class_='pear')

page = html[
    body[
        div(class_='cherry')[
            p(id='ab5'),
            p,
            ],
        div(class_='wobble')[
            p['hello world',],
            p[
                'said',
                b['Peter',],
                'quietly',
                ],
            ],
        ],
    pear_div[p, p],
    pear_div[p, p],
]

print(lxml.etree.tostring(page.toxml(), pretty_print=True))
