from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import csv
import json
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

data_path = "./static/aqi_data.csv"  # Path to the AQI data file
location_path = "./static/location_details.json"  # Path to the location details file
stationaries_path = "./static/stationaries.json"  # Path to the stationaries data file
users_path = "./static/users.json"  # Path to the user data file

def get_aqi_data(city_name):
    try:
        with open(data_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                city = row['City'].strip("()'")
                if city.lower() == city_name.lower():
                    return {
                        "City": city_name,
                        "AQI": row['AQI Value'],
                        "CO AQI Category": row['CO AQI Category'],
                        "Ozone AQI Category": row['Ozone AQI Category']
                    }
        return {"error": "City not found in AQI database."}
    except Exception as e:
        return {"error": str(e)}

def get_city_from_location():
    try:
        with open(location_path, 'r') as file:
            location_data = json.load(file)
            return location_data.get("city", "")
    except Exception as e:
        return ""

def get_stationaries():
    try:
        with open(stationaries_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        return {"error": str(e)}

def load_users():
    if os.path.exists(users_path):
        with open(users_path, 'r') as file:
            return json.load(file)
    return {}

def save_users(users):
    with open(users_path, 'w') as file:
        json.dump(users, file, indent=4)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/aqi', methods=['GET'])
def aqi():
    city = request.args.get('city', get_city_from_location())
    if not city:
        return jsonify({"error": "Could not determine city from location."})
    return jsonify(get_aqi_data(city))

@app.route('/pollutedareas')
def pollutedarea():
    city = get_city_from_location()
    aqi_data = get_aqi_data(city) if city else {"error": "Could not determine city from location."}
    return render_template('polluted_areas.html', aqi_data=aqi_data)

@app.route('/stationaries', methods=['GET'])
def stationaries():
    return jsonify(get_stationaries())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('home'))
        return "Invalid credentials, please try again."
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users:
            return "Username already exists."
        users[username] = {'password': password}
        save_users(users)
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
