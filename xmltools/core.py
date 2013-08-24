'''Core XML tools


>>> @tagclass
... class aaa: pass

The four partial and full instantiations of a tag.
>>> t0 = aaa
>>> t1 = aaa['abc',]
>>> t2 = aaa(a=1, b=2)
>>> t3 = aaa(a=1, b=2)['abc',]
'''

__metaclass__ = type


class tagclass(type):

    def __new__(type_, cls):

        name = cls.__name__
        bases = (TagBase,)
        attrib = dict(cls.__dict__)

        new_cls = type.__new__(type_, name, bases, attrib)
        return new_cls


    def __getitem__(self, body):
        '''Returns self()[body], to permit tag[...].
        '''
        return self()[body]


class TagBase:


    def __init__(self, *argv, **kwargs):

        # TODO: Allow subclass to process args.
        self.argv = argv
        self.kwargs = kwargs


    def __getitem__(self, body):
        '''Return self, mutated by self.body = body.
        '''
        # TOOD: Make this optional? Place in tag bases.
        if not isinstance(body, tuple):
            raise ValueError('Expecting tuple, missing comma perhaps')

        self.body = body
        return self


if __name__ == '__main__':

    import doctest
    print(doctest.testmod())
