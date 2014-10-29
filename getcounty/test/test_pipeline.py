from __future__ import absolute_import
import unittest
import os
import collections

#Set current directory to being this file
fdir, fname = os.path.split(__file__)
os.chdir(fdir)
from getcounty.pipeline import processing



        
        
class PipelineTests(unittest.TestCase):
    def setUp(self):
#         self.infile = os.path.abspath(
#             os.path.join("..", "input", "dummy_data.csv")
#         )
#        assert(os.path.exists(self.infile))
        self.infile = os.path.join("..", "input", "dummy_data.csv")
        
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
        rows = processing.csv_rows(self.infile)
        headers = rows.next()
        self.assertEqual(headers, self.expected_headers)
        first = rows.next()
        self.assertEqual(first, self.expected_first_columns)

    def test_serviceman(self):
        soldiers = processing.soldiers(self.infile)
        first = soldiers.next()
        self.assertEqual(first, self.expected_first_dict)
    
    def test_embelish(self):
        
        soldiers = processing.embelish(self.infile)
        first = soldiers.next()

        self.assert_(isinstance(first, processing.ServiceMan))
        # Zip code
        self.assert_(isinstance(first.zips, collections.MutableSequence))
        zips_title = processing.ServiceMan.zips.title
        self.assert_(isinstance(first[zips_title], collections.MutableSequence))
        self.assertEqual(len(first.zips), 1)
        self.assertEqual(first.zips[0].zip, u'98240')
        
        self.assertEqual(first.county_id, self.NotFoundValue)
        self.assertEqual(first.county, self.NotFoundValue)
        
        county_id_title = processing.ServiceMan.county_id.title
        county_title = processing.ServiceMan.county.title

        self.assertEqual(first[county_id_title], self.NotFoundValue)
        self.assertEqual(first[county_title], self.NotFoundValue)
    

    
if __name__ == "__main__":
    unittest.main()


