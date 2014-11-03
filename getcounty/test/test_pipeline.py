from __future__ import absolute_import
import unittest
import os
import collections

#Set current directory to being same directory as this file
fdir, fname = os.path.split(__file__)
os.chdir(fdir)

from getcounty.pipeline import processing
from getcounty.shared import csv_io


from getcounty.pipeline.getzipcodes import GetZipCodes
from getcounty.pipeline.getlocationids.GetLocationIDs import GetLocationIDs
from getcounty.pipeline.getcountyname.GetCountyName import GetCountyName

        
        
class PipelineTests(unittest.TestCase):
    inname = "dummy_data.csv"
    infile = os.path.join("..", "input", inname)
    outfile = os.path.join("..", "output", inname)
    def setUp(self):        
        self.NotFoundValue = NotImplemented
        self.expected_headers = [
            'Service', 'Component', 'Name  (Last, First M)', 'Rank',
            'Pay Grade', 'Date of Death (yyyy/mm/dd)', 'Age', 'Gender',
            'Home of Record City', 'Home of Record County',
            'Home of Record State', 'Home of Record Country', 'Unit',
            'Incident Geographic Code', 'Casualty Geographic Code',
            'Casualty Country', 'City of Loss'
        ]
        self.expected_first_columns = [
            'ARMY',
            'ACTIVE DUTY',
            'AAMOT, AARON SETH',
            'SPC',
            'E04',
            '11/5/2009',
            '22',
            'MALE',
            'CUSTER',
            '',
            'WA',
            'US',
            ' COMPANY C, 1ST BATTALION, 17TH INFANTRY REGIMENT, 5 SBCT, 2 ID, FORT LEWIS, WA',
            'AF',
            'AF',
            'AFGHANISTAN',
            'JELEWAR'
        ]
        self.expected_first_dict = dict(zip(
            self.expected_headers, self.expected_first_columns
        ))


    def test_passthrough(self):
        rows = csv_io.read_csv_rows(self.infile)
        headers = rows.next()
        self.assertEqual(headers, self.expected_headers)
        first = rows.next()
        self.assertEqual(first, self.expected_first_columns)

    def test_serviceman(self):
        soldiers = processing.soldiers(self.infile)
        first = soldiers.next()
        self.assertEqual(first, self.expected_first_dict)
    
    def test_pipeline_parts(self):
        soldiers = processing.soldiers(self.infile)
        first = soldiers.next()

        self.assert_(isinstance(first, processing.ServiceMan))

        # Zip code
        first.zips = GetZipCodes(first.state, first.city)
        self.assert_(isinstance(first.zips, collections.MutableSequence))
        zips_title = processing.ServiceMan.zips.title
        self.assert_(isinstance(first[zips_title], collections.MutableSequence))
        self.assertEqual(len(first.zips), 1)
        self.assertEqual(first.zips[0].zip, u'98240')
        
        # County ID
        first.county_id, first.state_id = GetLocationIDs(first.zips, first.state)
        expected_county_id = '073'
        self.assert_(isinstance(first.county_id, collections.Sequence))
        self.assertEqual(first.county_id, expected_county_id)
        county_id_title = processing.ServiceMan.county_id.title
        self.assertEqual(first[county_id_title], expected_county_id)

        # County Name
        first.county = GetCountyName(first.county_id, first.state_id)
        expected_county_name = 'Whatcom County'
        self.assert_(isinstance(first.county, str))
        self.assertEqual(first.county, expected_county_name)
        county_title = processing.ServiceMan.county.title
        self.assertEqual(first[county_title], expected_county_name)

    def test_output(self):
        if os.path.exists(self.outfile):
            os.remove(self.outfile)
        # Write outfile
        self.assert_(not os.path.exists(self.outfile))
        processing.pipeline(self.infile, self.outfile)
        self.assert_(os.path.exists(self.outfile))
            


#==============================================================================
#    Local Utility Functions
#==============================================================================
def check_unfilled(infile, outfile):
    if not os.path.exists(outfile):
        #If output file doesn't exist - make it
        processing.pipeline(infile, outfile)
     
    unfilled = list(
        processing.find_unfilled(outfile, 'Home of Record County')
    )
    print("-----------")
    print("County of rows with no 'Home of Record County' found:   {0}".format(len(unfilled)))



if __name__ == "__main__":
    unittest.main()
    check_unfilled(PipelineTests.infile, PipelineTests.outfile)


