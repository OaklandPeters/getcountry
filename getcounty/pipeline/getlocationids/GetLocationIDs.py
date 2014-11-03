"""
#zcta_county_rel_10.csv
# INput: zipcode (column 'GEOID')
# output: state_id, county_id

#
# Input: state_id, county_id
# Output: 

"""
import os
import csv
import itertools
import collections

from ...extern import rich_core
from ...extern import unroll
from ...extern.pyzipcode import ZipCode
from ...shared.errors import NotFoundException
from ...shared import csv_io

#==============================================================================
#    Local Utility
#==============================================================================
# def csv_dict_rows(infile):
#     #State    State ANSI    County ANSI    County Name    ANSI Cl
#     
#     assert(isinstance(infile, basestring))
#     assert(os.path.exists(infile))
#     assert(os.path.isfile(infile))
#     
#     with open(infile, mode='rb') as csvfile:
#         rows = csv.DictReader(csvfile)
#         for row in rows:
#             yield row
            
def flatten(seqOfSequences):
    "Flatten one level of nesting"
    return itertools.chain.from_iterable(seqOfSequences)



#==============================================================================
#    Main function
#==============================================================================
class GetLocationIDs(object):
    """Operator-style function-class (ie stateless).
    Represents a single step of procesing.
    """
    
    def __new__(cls, zips, state):
        return cls.__call__(zips, state)
    @classmethod
    def __call__(cls, zips, state):
        """
        ?? Is the state name information actually necessary?
        Dooesn't zipcode uniquely determine state?
        """
        # This needs to be able to accept zipcode as either single value, or sequence of zips
        zips, state = cls.validate(zips, state)

        nested_rows = (cls.find_location_rows(zipcode) for zipcode in zips)
        
        try:
            first = first_nonempty(nested_rows)
        except NotFoundException:
            return None, None
        
        try:
            return first['COUNTY'], first['STATE']
        except KeyError:
            return None, None
    
    @classmethod
    def validate(cls, zips, state):
        """
        Convert zips to a list of integers.
        """
        zips = cls.validate_zips(zips)
        if not isinstance(state, basestring):
            raise TypeError("'state' must be a basestring.")

        return zips, state    
    
    @classmethod
    @unroll.unroll(tuple)
    def validate_zips(cls, zips):
        """Returns zips as a tuple of strings."""
        for i, zipcode in enumerate(rich_core.ensure_tuple(zips)):
            if isinstance(zipcode, ZipCode):
                yield int(zipcode.zip)
            elif isinstance(zipcode, basestring):
                yield int(zipcode)
            elif isinstance(zipcode, int):
                yield zipcode
            elif zipcode is None:
                continue
            else:
                raise TypeError(str.format(
                    "Element #{0} of 'zips' is type {1}, but should be type "
                    "ZipCode, basestring or int.",
                    i, type(zipcode).__name__
                ))
            
            
    @classmethod
    def find_location_rows(cls, zipcode):
        """Operates on a single zipcode code."""
        return [
            row for row in cls.data
            if int(row['ZCTA5']) == zipcode
        ]

    @classmethod
    def all_states_equal(cls, state_ids):
        #state_ids should be NonStringSequence
        assert(isinstance(state_ids, collections.Sequence)
               and not isinstance(state_ids, basestring))
        return all_equal(state_ids)


    #--------------------------------------------------------------------------
    #    Build database or hash
    #--------------------------------------------------------------------------
    # Data file assumed to be in directory with this code file.
    datafile = os.path.join(
        os.path.split(__file__)[0],
        'zcta_county_rel_10.csv'
    )
    data = list(csv_io.read_csv_dict_rows(datafile))
#     @rich_core.ClassProperty
#     def data(self):
#         if not hasattr(self, '_data'):
#             self._data = list(csv_io.read_csv_dict_rows(self.datafile))
#         return self._data




#------------------------------------------------------------------------------
#    Local Utility Functions
#------------------------------------------------------------------------------
def all_equal(iterable):
    try:
        iterator = iter(iterable)
        first = next(iterator)
        return all(first == rest for rest in iterator)
    except StopIteration:
        return True

def first_nonempty(iterable):
    for elm in iterable:
        if isinstance(elm, collections.Sequence) and not isinstance(elm, basestring):
            if len(elm) != 0:
                return elm[0]
    # No non-empty found
    raise NotFoundException("No non-empty entry found.")



