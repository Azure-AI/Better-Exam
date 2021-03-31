import app
import unittest

test_app = app.create_app()

class AppTest(unittest.TestCase):
    def setUp(self) -> None:
        test_app.config['TESTING'] = True
        self.app = test_app.test_client()

    def test_index(self) -> None:
        r = self.app.get('/test')
        self.assertEqual(r.data, b'Server is Working')
        
if __name__ == '__main__':
    unittest.main()