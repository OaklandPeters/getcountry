from ..extern.pyzipcode import ZipCodeDatabase

class GetZipCodes(object):
    def __new__(cls, *args, **kwargs):
        return cls.__call__(*args, **kwargs)
    @classmethod
    def __call__(cls, state, city):
        """If not found, returns None"""
        return cls.zcdb.find_zip(city, state)
    # Constructed once - shared between calls
    zcdb = ZipCodeDatabase()