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
        self.title_test(processing.ServiceMan.zip, False)
        self.title_test(processing.ServiceMan.county_id, False)
        
#         city_title = processing.ServiceMan.city.title
#         self.assertEqual(city_title, "Home of Record City")
#         self.assertEqual(
#             soldier[city_title], self.expected_first_dict[city_title]
#         )
        
        
class PipelineTests(unittest.TestCase):
    def setUp(self):
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
        self.assertEqual(first.zip, self.NotFoundValue)
        self.assertEqual(first.county_id, self.NotFoundValue)
        self.assertEqual(first.county, self.NotFoundValue)
        
        zip_title = processing.ServiceMan.zip.title
        county_id_title = processing.ServiceMan.county_id.title
        county_title = processing.ServiceMan.county.title
        self.assertEqual(first[zip_title], self.NotFoundValue)
        self.assertEqual(first[county_id_title], self.NotFoundValue)
        self.assertEqual(first[county_title], self.NotFoundValue)
    
if __name__ == "__main__":
    unittest.main()


