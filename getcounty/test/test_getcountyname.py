import unittest
from getcounty.pipeline.getcountyname.GetCountyName import GetCountyName



class GetCountyName(unittest.TestCase):
    def setUp(self):
        pass
    def compare(self, county_ids, state_id, county_name):
        
        result = GetCountyName(county_ids, state_id)
        
        self.assertEqual(
            result,
            county_name
        )
    def test_basic(self):
        self.compare(('073',), '53', "Whatcom County")
        
        
        #self.compare(['3'], '1', "Baldwin County")
    def test_edge(self):
        self.compare(['03'], '1', "Baldwin County")
        self.compare(['3', '4'], '1', "Baldwin County")

if __name__ == "__main__":
    unittest.main()
