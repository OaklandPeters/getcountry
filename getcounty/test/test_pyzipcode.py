from __future__ import absolute_import
import unittest

from getcounty.extern.pyzipcode import ZipCodeDatabase

class PyZipCodeTests(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_basic(self):
        zcdb = ZipCodeDatabase()
        
        zipcode = zcdb[54115]
        self.assertEqual(zipcode.zip, u'54115')
        self.assertEqual(zipcode.city, u'De Pere')
        self.assertEqual(zipcode.state, u'WI')
        self.assertEqual(zipcode.longitude, -88.078959999999995)
        self.assertEqual(zipcode.latitude, 44.42042)
        self.assertEqual(zipcode.timezone, -6)
        
    def test_for_zipcodes(self):

        zcdb = ZipCodeDatabase()
        self.assertEqual(
            len(zcdb.find_zip(city="Oshkosh")),
            7
        )

if __name__ == "__main__":
    unittest.main()