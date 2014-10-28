from __future__ import absolute_import
import unittest
import os
from getcountry.pipeline import pipeline

class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.infile = os.path.join("..", "input", "dummy_data.csv")
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
        rows = pipeline.csv_rows(self.infile)
        headers = rows.next()
        self.assertEqual(headers, self.expected_headers)
        first = rows.next()
        self.assertEqual(first, self.expected_first_columns)

    def test_serviceman(self):
        soldiers = pipeline.soldiers(self.infile)
        first = soldiers.next()
        self.assertEqual(first, self.expected_first_dict)
    
    def test_embelish(self):
        soldiers = pipeline.embelish(self.infile)
        first = soldiers.next()
        
        print()
        print()
    
if __name__ == "__main__":
    unittest.main()