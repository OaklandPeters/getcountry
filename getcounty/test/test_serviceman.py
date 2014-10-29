from __future__ import absolute_import
import unittest
import os

from getcounty.pipeline import processing

class ServiceManTests(unittest.TestCase):
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
    def test_instance(self):
        soldier = processing.ServiceMan(self.expected_first_columns)
        self.assertEqual(soldier, self.expected_first_dict)

    def title_test(self, property_obj, exists=True):
        soldier = processing.ServiceMan(self.expected_first_columns)
        title = property_obj.title

        self.assertEqual(title in soldier.keys(), exists)            
        if title in soldier.keys():
            self.assertEqual(soldier[title], self.expected_first_dict[title])
        
        
    def test_titles(self):
        self.title_test(processing.ServiceMan.city, True)
        self.title_test(processing.ServiceMan.county, True)
        self.title_test(processing.ServiceMan.state, True)
        #Do not initially exist
        self.title_test(processing.ServiceMan.zips, False)
        self.title_test(processing.ServiceMan.county_id, False)

if __name__ == "__main__":
    unittest.main()
