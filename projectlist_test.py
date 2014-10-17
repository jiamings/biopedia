import unittest
from projectlist import save_project
from datetime import date

class ProjectListTestCase(unittest.TestCase):
    """
    Tests all the functions in projectlist.py.
    """
    def test_save_project(self):
        obj = save_project(
            name='MetaTongue',
            environment='Human',
            site='Oral',
            sequence_type='WGS',
            project_id='MGP-D001',
            num_of_total_sequences=50000,
            num_of_orfs=15000,
            num_of_samples=183,
            read_length=1500,
            platform='Illumina Hiseq 2000',
            create_date={"year": 2014, "month": 8, "day": 12},
            update_date={"year": 2014, "month": 10, "day": 16},
        )
        self.assertEquals(obj, True)


def suite():
    return unittest.makeSuite(ProjectListTestCase)


if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())