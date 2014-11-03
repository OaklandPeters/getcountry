from __future__ import absolute_import
import os
import csv

from ...extern import rich_core
from ...extern import unroll

__all__ = ['GetCountyName']


#==============================================================================
#    Local Utility
#==============================================================================
def csv_dict_rows(infile):
    #State    State ANSI    County ANSI    County Name    ANSI Cl
    
    assert(isinstance(infile, basestring))
    assert(os.path.exists(infile))
    assert(os.path.isfile(infile))
    
    with open(infile, mode='rb') as csvfile:
        rows = csv.DictReader(csvfile)
        for row in rows:
            yield row

def validate_string_int(obj, name="object"):
    if not isinstance(obj, basestring):
        print(obj, type(obj))
        raise TypeError("'{0}' must be a basestring.".format(name))
    int(obj)
    return obj

#==============================================================================
#    Main Function
#==============================================================================
class GetCountyName(object):
    """Operator-style state-less class function (IE no __init__).
    Input: county_id, state_id
    Output: county_name
    
    
    Clever Note: this should be based on national_county.csv
    Therefore: It should be able to handle inputs which are State 2 letter codes (WA)
        OR state id
    """
    
    def __new__(cls, county_ids, state):
        return cls.__call__(county_ids, state)
    
    @classmethod
    def __call__(cls, county_ids, state):
        """
        Input: county
        """
        # If None passed in - such as if a previous step could not find a county id
        if county_ids == [None] or county_ids is None or state is None:
            return None
        
        county_ids, state = cls.validate(county_ids, state)
        return cls.find_by_state_id(state, county_ids[0])

    @classmethod
    def validate(cls, county_ids, state):
        county_ids = cls.validate_county_ids(county_ids)
        state = cls.validate_state_id(state)
        return county_ids, state
    
    @classmethod
    def validate_state_id(cls, state):
        """Ensure state is a string of an integer."""
        if not isinstance(state, basestring):
            raise TypeError("State should be a basestring.")
        return validate_string_int(state, name="state")
    
    @classmethod
    def validate_state_code(cls, state):
        """Raise exception if state is not a two-letter state code.
        @todo: allow this to accept state_ids (integers, as int or string).
        """
        # 
        if not isinstance(state, basestring):
            raise TypeError("State should be a string")
        if not len(state) == 2:
            raise ValueError("State should be a 2-letter state code.")
        if not state.isalpha():
            raise ValueError("State must be alphabetic.")
        return state
    
    @classmethod
    def validate_county_ids(cls, county_ids):
        """Ensure that county_ids are a sequence of string codes.
        """
        # Iterate through county_ids
        # ensure_tuple(): handles case of single-value with no wrapping tuple/list
        county_ids = rich_core.ensure_tuple(county_ids)
        for i, county_id in enumerate(county_ids):
            validate_string_int(county_id, name="'county_id' #{0}".format(i))
        return county_ids
    
    @classmethod
    def find_by_state_id(cls, state_id, county_id):
        """Find county name from a row, based on a single state_id and county_id.
        
        @todo: Make GetCountyName.find_by_state_id  simply return the first matching
        @todo: GetCountyName.find_by_state_id: If not results found - return None
        """
        county_names = [
            row['County Name'] for row in cls.data
            if int(row['State ANSI']) == int(state_id)
            and int(row['County ANSI']) == int(county_id) 
        ]
        
        if len(county_names) == 1:
            return county_names[0]
        if len(county_names) > 1:
            # Should not happen
            return county_names[0]
        if len(county_names) == 0:
            #raise RuntimeError("No value found.")
            return None
        

    #--------------------------------------------------------------------------
    #    Build database or hash
    #--------------------------------------------------------------------------
    # Data file assumed to be in directory with this code file.
    datafile = os.path.join(
        os.path.split(__file__)[0],
        'national_county.csv'
    )
    data = list(csv_dict_rows(datafile))


