import pytest
from app import app
from flask.testing import FlaskClient


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    response = client.get('/')
    assert b"Heart Disease Prediction System | Homepage" in response.data
    assert response.status_code == 200


def test_admin_login_form(client):
    response = client.get('/adminloginform')
    assert b"Admin Login" in response.data
    assert response.status_code == 200


def test_heartpredictor(client):
    response = client.get('/heartpredictor')
    assert b"Heart Disease Prediction Using ML" in response.data
    assert response.status_code == 200


def test_patientdetails(client):
    response = client.get('/patientdetails')
    assert b"Patient Data" in response.data
    assert response.status_code == 200


def test_adminhome(client):
    response = client.get('/adminhome')
    assert b"Admin Functionalities" in response.data
    assert response.status_code == 200


def test_details(client):
    response = client.get('/details')
    assert b"Patient Details" in response.data
    assert response.status_code == 200


def test_loginadmin(client):
    response = client.post('/loginadmin', data={'username': 'invalid_username',
                                                'password': 'invalid_password'})
    assert b"Login failed. Please check your credentials" in response.data
    assert response.status_code == 200


def test_login_form(client):
    response = client.get('/loginform')
    assert b"Login" in response.data
    assert response.status_code == 200


def test_login(client):
    response = client.post('/login', data={'username': 'testuser', 'password':
        'incorrect_password'})
    assert b"Login failed. Please check your credentials" in response.data
    assert response.status_code == 200  # Or use the correct status code for login failure


def test_registration_form(client):
    response = client.get('/registration')
    assert b"Registration Page" in response.data
    assert response.status_code == 200


def test_process_registration(client):
    response = client.get('/register')
    assert b"Registration Page" in response.data
    assert response.status_code == 200


def test_predict(client):
    response = client.post('/predict', data={'Age': '63', 'sex': '1', 'chestPainTypes': '3',
                                             'trestBps': '145',
                         'serumcholesterol': '233', 'fastingbloodsugar': '1', 'ecgresults': '0',
                         'maximumheartrate': '150', 'exerciseangina': '0', 'stdepression': '2.3',
                        'stslope': '0', 'majorvessels': '0', 'thalassemia': '1'})
    assert b'{"error":"Model not available"}\n' in response.data



if __name__ == "__main__":
    pytest.main([__file__])
