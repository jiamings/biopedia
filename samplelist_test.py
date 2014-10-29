__author__ = 'yuanyuan'
import unittest
from samplelist import save_sample


class SampleListTestCase(unittest.TestCase):
    """
    Tests all the functions in samplelist.py.
    """

    def test_save_sample(self):
        obj = save_sample(
            elements={"project_name": 'MetaTongue',
                      "name": "XS-13", "insertSize": 417.138,
                      "rawReads": 44672924, "hostReads": 2851868,
                      "cleanReads": 41821056, "scaffoldsUp500bp": 42895,
                      "N50Length": 3645, "ORFs": 142224, "avgLength": 340.62,
                      "age": "NA", "sex": "NA", "tongueColor": "NA",
                      "tongueType": "NA", "BMI": "NA", }
        )
        self.assertEquals(obj, True)

    def test_save_sample_type_error(self):
        obj = save_sample(
            elements=[]
        )
        self.assertEquals(obj, False)

    def test_save_sample_num_error(self):
        obj = save_sample(
            elements={"project_name": 'MetaTongue',
                      "name": "XS-13", "insertSize": 417.138,
                      "rawReads": 44672924, "hostReads": 2851868,
                      "cleanReads": 41821056, "scaffoldsUp500bp": 42895,
                      "N50Length": 3645, "ORFs": 142224, "avgLength": 340.62,
                      "age": "NA", "sex": "NA", "tongueColor": "NA",
            }
        )
        self.assertEquals(obj, False)

    def test_save_sample_no_name(self):
        obj = save_sample(
            elements={"project_name": 'noSuchProject',
                      "name": "XS-13", "insertSize": 417.138,
                      "rawReads": 44672924, "hostReads": 2851868,
                      "cleanReads": 41821056, "scaffoldsUp500bp": 42895,
                      "N50Length": 3645, "ORFs": 142224, "avgLength": 340.62,
                      "age": "NA", "sex": "NA", "tongueColor": "NA",
                      "tongueType": "NA", "BMI": "NA", }
        )
        self.assertEquals(obj, False)


def suite():
    return unittest.makeSuite(SampleListTestCase)


if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())