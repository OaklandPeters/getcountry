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
import collections

from getcountry.pipeline.getcountyid import GetCountyID
from getcountry.pipeline.getcountyname import GetCountyName
from getcountry.pipeline.getzipcode import GetZipCode
from getcountry.pipeline.serviceman import ServiceMan




def csv_rows(infile):
    assert(isinstance(infile, basestring))
    assert(os.path.exists(infile))
    assert(os.path.isfile(infile))
    
    with open(infile, mode='rb') as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            yield row

def soldiers(infile):
    rows = csv_rows(infile)
    rows.next() #Remove first row -- headers
    for row in rows:
        yield ServiceMan(row)

def embelish_soldier(soldier):
    soldier.zip = GetZipCode(soldier.state, soldier.city)
    soldier.county_id = GetCountyID(soldier.zip, soldier.state)
    soldier.county = GetCountyName(soldier.county_id)
    return soldier

def embelish(infile):
    for soldier in soldiers(infile):
        yield embelish_soldier(soldier)



