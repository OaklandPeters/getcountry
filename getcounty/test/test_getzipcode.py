import unittest
from getcounty.extern.pyzipcode import ZipCodeDatabase






class GetZipCodeTests(unittest.TestCase):
    def setUp(self):
        self.zdbc = ZipCodeDatabase()
    def test_basic(self):
        city = 'Washington'
        state = 'DC'
        results = self.zdbc.find_zip(city, state)
        
        zips = [int(elm.zip) for elm in results]
        for zip in dc_zips:
            self.assert_(zip in zips)
        

# A few zip codes in DC
dc_zips = [
    20001, 20002, 20003, 20004, 20005, 20006, 20007, 20008, 20009, 20010,
    20064, 20065, 20066, 20067, 20068, 20069, 20070, 20071, 20073, 20074,
    20412, 20413, 20414, 20415, 20416, 20418, 20419, 20420, 20421, 20422
]

if __name__ == "__main__":
    unittest.main()



