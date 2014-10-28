import collections
from ..extern.clsproperty import VProperty

__all__ = ['ServiceMan']



class ServiceMan(collections.MutableMapping):
    """Convenience class around CSV entry. Has fixed fields."""
    def __init__(self, fields):
        assert(len(fields) == len(self.titles)), (
            "Length of fields must be {0}.".format(len(self.titles))
        )
        self.data = dict(zip(self.titles, fields))

    #--------------------------------------------------------------------------
    # Fields used as input to pipeline functions
    #--------------------------------------------------------------------------
    @VProperty
    class city(object):
        """Column 'Home of Record City'."""
        def _get(self):
            return self.data['Home of Record City']
    @VProperty
    class county(object):
        """Column 'Home of Record County'."""
        def _get(self):
            return self.data['Home of Record County']
        def _set(self, value):
            self.data['Home of Record County']
    @VProperty
    class state(object):
        """Column 'Home of Record State'."""
        def _get(self):
            return self.data['Home of Record State']
    
    #--------------------------------------------------------------------------
    # Fields used as output to pipeline functions
    #--------------------------------------------------------------------------
    @VProperty
    class zip(object):
        """Zip-code. Column not found in raw data."""
        def _get(self):
            return self.data['ZIP Code']
        def _set(self, value):
            self.data['ZIP Code'] = value
    
    @VProperty
    class county_id(object):
        """ID Code for a county. Column not found in raw data."""
        def _get(self):
            return self.data['Code for Home of Record County']
        def _set(self, value):
            self.data['Code for Home of Record County'] = value

    
    # Required MagicMethods
    def __getitem__(self, key):
        return self.data[key]
    def __setitem__(self, key, value):
        self.data[key] = value
    def __delitem__(self, key):
        del self.data[key]
    def __len__(self):
        return len(self.data)
    def __iter__(self):
        return iter(self.data)
    def keys(self):
        return self.data.keys()
    def values(self):
        return self.data.values()
    def items(self):
        return self.data.items()
    def __repr__(self):
        return repr(self.data)
    def __str__(self):
        return str(self.data)

    
    # Fixed Values
    titles = [
        'Service',
        'Component',
        'Name  (Last, First M)',
        'Rank',
        'Pay Grade',
        'Date of Death (yyyy/mm/dd)',
        'Age',
        'Gender',
        'Home of Record City',
        'Home of Record County',
        'Home of Record State',
        'Home of Record Country',
        'Unit',
        'Incident Geographic Code',
        'Casualty Geographic Code',
        'Casualty Country',
        'City of Loss'
    ]