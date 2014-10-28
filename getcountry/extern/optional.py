import abc
import types
import collections




class Optional(object):
    """Simple implementation of an 'Optional' data type.
    @todo: Look at the implementations:
        Lingospot
        fn.py
        Haskell
        Rust
    """
    def __init__(self, default=None, execute=None):
        self.default, self.execute = self._validate(default, execute)

    def _validate(self, default=None, execute=None):
        #execute must be None or callable
        assert(isinstance(execute, (type(None), collections.Callable))), (
            "'execute' must be NoneType or Callable."
        )
        
        if callable(execute):
            assert(isinstance(default, type(None))), (
                "If 'execute' is provided, then default must be not provided or None."
            )
        
        return default, execute        
    @property
    def value(self):
        if callable(self.execute):
            return self.execute()
        else:
            return self.default
    def get(self):
        return self.value
    def __repr__(self):
        return "Optional({0})".format(repr(self.value))

def deoption(obj, default=None, execute=None):
    if isinstance(obj, Optional):
        return obj.value
    elif isinstance(obj, type(None)):
        return Optional(default=default, execute=execute).value
    else:
        return obj

class Nullish(object):
    """ABC for None-like objects.
    If this turns out to be usefull...
    @todo: Make this replicate the behavior of the builtin None.
    """
    __metaclass__ = abc.ABCMeta
Nullish.register(types.NoneType)
Nullish.register(Optional)




if __name__ == "__main__":
    


    def myfunc(first, second=None, third=Optional(5), fourth=Optional(execute=list)):
        
        #Equivalent: second = deoption(second, 5)
        if isinstance(second, type(None)):
            second = 5
        
        third = deoption(third)
        fourth = deoption(fourth)
        
        return first, second, third, fourth

    expected = ('a', 5, 5, [])
    assert(myfunc('a') == expected)
    assert(myfunc('a', 5) == expected)
    assert(myfunc('a', second=5) == expected)
    assert(myfunc('a', 5, 5) == expected)
    assert(myfunc('a', fourth=[]) == expected)