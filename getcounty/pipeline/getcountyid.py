

class GetCountyID(object):
    def __new__(cls, *args, **kwargs):
        return cls.__call__(*args, **kwargs)
    @classmethod
    def __call__(cls, *args, **kwargs):
        return NotImplemented