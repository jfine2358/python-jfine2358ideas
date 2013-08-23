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
            raise ValueError

        self.body = body
        return self


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
]

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
