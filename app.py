from flask import Flask, request, jsonify, render_template, session
from flask_mysqldb import MySQL
import mysql.connector
import numpy as np
import pickle
import os


# Import the 'os' module for file path handling
app = Flask(__name__)


# Configuration for MySQL connection
app.secret_key = "xyzsdfg"
db_config = {
    "host": "ZAMRY-PC",  # MySQL server hostname
    "user": "root",  # MySQL username
    "password": "root",  # MySQL password
    "database": "heartdiseasedb",  # MySQL database name
}

with mysql.connector.connect(
    host="ZAMRY-PC",
    user="root",
    password="root",
    database="heartdiseasedb"

) as conn:
    cursor = conn.cursor()


# Create a MySQL connection
conn = mysql.connector.connect(**db_config)

# Define the path to the model file
model_file_path = 'model.pkl'

# Add error handling to open the file
try:
    model = pickle.load(open(model_file_path, 'rb'))
except FileNotFoundError:
    # Handle the case where the file is not found
    model = None
    print(f"Error: The file '{model_file_path}' was not found.")
except Exception as e:
    # Handle other exceptions that may occur during file opening
    model = None
    print(f"Error: An exception occurred while opening '{model_file_path}': {str(e)}")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/adminloginform')
def admin_login_form():
    return render_template('adminlogin.html')


@app.route('/heartpredictor')
def heartpredictor():
    return render_template('HeartDiseasePredictionSystem.html')


@app.route('/patientdetails')
def patientdetails():
    return render_template('patientdetails.html')


@app.route('/adminhome')
def adminhome():
    return render_template('adminpanel.html')


mysql = MySQL(app)


@app.route('/details')
def details():
    cur = conn.cursor()
    cur.execute("SELECT * FROM heartdata")
    data = cur.fetchall()
    return render_template('patientdetails.html', heartdata=data)


@app.route('/loginadmin', methods=['POST'])
def loginadmin():
    if request.method == 'POST':  # Check if the request method is POST
        username = request.form.get('username')
        password = request.form.get('password')

        # Query the database to check user credentials (replace with your own query)
        cur = conn.cursor()
        cur.execute("SELECT * FROM admindetails WHERE username = %s AND password = %s",
                    (username, password))
        admindetails = cur.fetchone()

        cur.close()

        if admindetails:
            # Store user information in a session
            session['username'] = admindetails[0]
            return render_template('adminpanel.html', username=session['username'])

    return "Login failed. Please check your credentials."


@app.route('/loginform')
def login_form():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':  # Check if the request method is POST
        username = request.form.get('username')
        password = request.form.get('password')

        # Query the database to check user credentials (replace with your own query)
        cur = conn.cursor()
        cur.execute("SELECT * FROM userdetails WHERE username = %s AND password = %s",(username, password))
        userdetails = cur.fetchall()

        cur.close()

        if userdetails:
            # Store user information in a session
            session['username'] = userdetails[0]
            return render_template('userpanel.html', username=session['username'])

    return "Login failed. Please check your credentials."


@app.route('/registration')
def registration_form():
    return render_template('registration.html')


@app.route('/register', methods=['GET', 'POST'])
def process_registration():
    result = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        try:
            username = request.form.get('username')
            password = request.form.get('password')
            email = request.form.get('email')  # Add email field in the form

            # Connect to the database
            cur = conn.cursor()

            # Insert the new user into the database with email
            cur.execute('INSERT INTO userdetails (username, password, email) ''VALUES (%s, %s, %s)', (username, password, email))
            conn.commit()
            result = 'Registration successful!'
        except Exception as e:
            # Handle registration errors (e.g., username or email already exists)
            result = f'Error: {e}'
        finally:
            cur.close()  # Change 'cursor' to 'cur'

    return render_template('registration.html', result=result)


@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        # Handle the case where the model is not available
        return jsonify({'error': 'Model not available'})
    # Get input data from POST request
    age = int(request.form.get('Age'))
    sex = int(request.form.get('sex'))
    chestpaintypes = int(request.form.get('chestPainTypes'))
    trestbps = int(request.form.get('trestBps'))
    serumcholesterol = int(request.form.get('SerumCholesterol'))
    fastingbloodsugar = int(request.form.get('FastingBloodSugar'))
    ecgresults = int(request.form.get('ecg_results'))
    maximumheartrate = int(request.form.get('MaximumHeartRate'))
    exerciseangina = int(request.form.get('exercise_angina'))
    stdepression = float(request.form.get('stDepression'))

    stslope = int(request.form.get('st_slope'))
    majorvessels = int(request.form.get('major_vessels'))
    thalassemia = int(request.form.get('thalassemia'))

    # Create input array for prediction
    input_query = np.array([[age, sex, chestpaintypes, trestbps, serumcholesterol, fastingbloodsugar,

    ecgresults,maximumheartrate, exerciseangina, stdepression, stslope, majorvessels, thalassemia]])

    # Make prediction
    prediction = model.predict(input_query)

    if isinstance(prediction, (list, np.ndarray)) and len(prediction) > 0:
        if prediction[0] == 0:
            result = 'The Person does not have Heart Disease'
        else:
            result = 'The Person has Heart Disease'
    else:
        result = 'Invalid prediction data'

    return render_template('HeartDiseasePredictionSystem.html', result=result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
