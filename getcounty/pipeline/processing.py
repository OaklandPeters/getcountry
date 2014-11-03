"""
Build Plan:
    Setup dummy function for unified processing
    Setup pipeline 
    Write-out at end
    Hand test
    Setup pipeline unittest

    
    
    Create value to fill in for values which were not found
    IE when parts of the pipeline fail
    class NotFound()

"""
from __future__ import absolute_import
import csv
import os

from .getlocationids.GetLocationIDs import GetLocationIDs
from getcounty.pipeline.getcountyname.GetCountyName import GetCountyName
from .getzipcodes import GetZipCodes
from .serviceman import ServiceMan
from ..shared import csv_io
from ..extern import unroll



def soldiers(infile):
    rows = csv_io.read_csv_rows(infile)
    rows.next() #Remove first row -- headers
    for row in rows:
        yield ServiceMan(row)

def embelish_soldier(soldier):
    """Add County data to soldier."""
#     soldier.zips = GetZipCodes(soldier.state, soldier.city)
#     soldier.county_id, soldier.state_id = GetLocationIDs(soldier.zips, soldier.state)
#     soldier.county = GetCountyName(soldier.county_id, soldier.state_id)
#     return soldier

    zips = GetZipCodes(soldier.state, soldier.city)
    county_id, state_id = GetLocationIDs(zips, soldier.state)
    county = GetCountyName(county_id, state_id)
    soldier.county = county
    return soldier

def find_county(state, city):
    zips = GetZipCodes(state, city)
    county_id, state_id = GetLocationIDs(zips, state)
    county = GetCountyName(county_id, state_id)
    return county



def embelish(infile):
    for soldier in soldiers(infile):
        if soldier.county in ['', None, 'None']:
            # Only process entries missing county data
#            yield embelish_soldier(soldier)
            soldier.county = find_county(soldier.state, soldier.city)
            yield soldier
        else:
            yield soldier


@unroll.unroll(list)
def soldier_to_row(soldier, headers):
    for column in headers:
        value = soldier.data[column]
        if value is not None:
            yield value
        else:
            yield ""

def pipeline(infile, outfile):
    """
    This should output two files:
    (1) Same columns as input - but with the county filled in
    (2) All intermediate columns written
    
    @todo: Write a 2nd file: one with only the original columns included

    """
    
    original_headers = csv_io.get_headers(infile)
    
    # Get soldier objects - as generator
    soldiers = embelish(infile)
    # Transform soldiers to output rows
    rows = (soldier_to_row(soldier, original_headers)
        for soldier in soldiers
    )
    # Write output rows to outfile
    csv_io.write_csv_rows(outfile, rows, headers=original_headers)

def find_unfilled(filepath, header):
    for row in csv_io.read_csv_dict_rows(filepath):
        if row[header] in ['', None, 'None']:
            yield row

def count_unfilled(filepath, header):
    return len(list(find_unfilled(filepath, header)))

