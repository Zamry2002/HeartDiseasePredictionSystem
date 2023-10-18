import unittest
from app import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Heart Disease Prediction System | Homepage', response.data)

    def test_admin_login_form(self):
        response = self.app.get('/adminloginform')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Admin Login', response.data)

    def test_heartpredictor(self):
            response = self.app.get('/heartpredictor')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Heart Disease Prediction Using ML', response.data)

    def test_patientdetails(self):
            response = self.app.get('/patientdetails')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Patient Data', response.data)

    def test_adminhome(self):
            response = self.app.get('/adminhome')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Admin Functionalities', response.data)

    def test_details(self):
            response = self.app.get('/details')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Patient Data', response.data)

    def test_loginadmin(self):
            response = self.app.get('/loginadmin')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Admin Functionalities', response.data)

    def test_login_form(self):
        response = self.app.get('/loginform')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_login(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User Page', response.data)

    def test_registration_form(self):
        response = self.app.get('/registration')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration Page', response.data)

    def test_process_registration(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration Page', response.data)

    def test_predict(self):
        response = self.app.get('/predict')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Heart Disease Prediction Using ML', response.data)


if __name__ == '__main__':
    unittest.main()
