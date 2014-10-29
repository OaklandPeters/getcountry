import os
import csv

#zcta_county_rel_10.csv
# INput: zip (column 'GEOID')
# output: state_id, county_id

#
# Input: state_id, county_id
# Output: 


class GetCountyID(object):
    # Build database or hash
    datafile = 'zcta_county_rel_10.csv'
    data = list(csv_dict_rows(datafile))
    
    def __new__(cls, *args, **kwargs):
        return cls.__call__(*args, **kwargs)
    @classmethod
    def __call__(cls, zips, state):
        """Which file does this come from?"""
        # This needs to be able to accept zip as either single value, or sequence of zips
        zips, state = cls.validate(zips, state)

        nested_rows = (find_location_rows(zip, state) for zip in zips)
        rows = list(flatten(nested_rows))
        
        county_ids = [row[] for row in rows]
        state_ids = [rows[] for row in rows]

        return county_ids, state_ids
    
    @classmethod
    def validate(cls, zips, state):
        if isinstance(zips, collections.Sequence) and not isinstance(zips, basestring):
            zips = [zips]
        # ensure zips are... int or str?
        
        if not isinstance(state, basestring):
            raise TypeError("'state' must be a basestring.")

        return zips, state
    
    @classmethod
    def find_location_rows(cls, zip, state):
        """Operates on a single zip code."""
        matching_rows = [
            row for row in cls.data
            if row[''] == state
            and row[''] == zip
        ]
        
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

if __name__ == "__main__":
    load_hash()