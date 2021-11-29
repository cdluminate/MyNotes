'''
doc for module ``foo``
'''

class Foo(object):
    '''
    class doc for ``foo.Foo``

    ``id`` is the universal ID, ``locx`` denotes the *x* component of its
    location.
    '''
    def __init__(self, id: int, name: str, locx: float, locy: float):
        '''this will be emitted.
        '''
        pass

    def bar(self, abc: int) -> int:
        '''
        instance method ``bar``
        '''
        pass

def foobar(x: int) -> int:
    '''function doc

    .. note::
        let's see wether this works.
    '''
    pass
