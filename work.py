class Base:

    def __init__(self, *argv, **kwargs):

        self.argv = argv
        self.kwargs = kwargs
        self.body = None


    def __getitem__(self, body):

        if not isinstance(body, tuple):
            raise ValueError

        self.body = body

        return self




def wibble(cls):

    d = dict(cls.__dict__)
    name = cls.__name__


    new_cls = type(name, (Base,), {})

    return new_cls


@wibble
class apple:
    pass

x = apple(x=4, b=5)[
    'abc',
]

print(x.argv)
print(x.kwargs)
print(x.body)
