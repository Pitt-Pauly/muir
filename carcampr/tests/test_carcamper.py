import os
import carcampr
import unittest
import tempfile


class CarCamprTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, carcampr.app.config['DATABASE'] = tempfile.mkstemp()
        carcampr.app.config['TESTING'] = True
        self.app = carcampr.app.test_client()
        with carcampr.app.app_context():
            carcampr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(carcampr.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/locations')
        assert b'No entries here so far' in rv.data


if __name__ == '__main__':
    unittest.main()
