from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import csv
import json
import os

app = Flask(__name__)

data_path = "./static/aqi_data.csv"
location_path = "./static/location_details.json"
stationaries_path = "./static/stationaries.json"
users_path = "./static/users.json"

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
