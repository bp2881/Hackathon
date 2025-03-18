from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import csv
import json
import os
from chatbot import get_chatbot_response  # Import chatbot logic

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config['WTF_CSRF_ENABLED'] = False

# Paths to data files
data_path = "./static/aqi_data.csv"
location_path = "./static/location_details.json"
stationaries_path = "./static/stationaries.json"
users_path = "./static/users.json"
feedbacks_path = "./static/feedbacks.json"

# Function to fetch AQI data from local CSV (kept for other routes)
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

# Function to get the city name from location_details.json (kept for other routes)
def get_city_from_location():
    try:
        with open(location_path, 'r') as file:
            location_data = json.load(file)
            return location_data.get("city", "")
    except Exception as e:
        return ""

# Function to load users from the JSON file
def load_users():
    if os.path.exists(users_path):
        with open(users_path, 'r') as file:
            return json.load(file)
    return {}

# Function to save users to the JSON file
def save_users(users):
    with open(users_path, 'w') as file:
        json.dump(users, file, indent=4)

# Function to load feedbacks from JSON
def load_feedbacks():
    if os.path.exists(feedbacks_path):
        with open(feedbacks_path, 'r') as file:
            return json.load(file)
    return []

# Function to save feedbacks to JSON
def save_feedbacks(feedbacks):
    with open(feedbacks_path, 'w') as file:
        json.dump(feedbacks, file, indent=4)

# Home route with leaderboard
@app.route('/')
def home():
    users = load_users()
    leaderboard = sorted(users.items(), key=lambda x: x[1].get('streak', 0), reverse=True)
    return render_template('home.html', leaderboard=leaderboard)

# AQI route
@app.route('/aqi', methods=['GET'])
def aqi():
    city = request.args.get('city', get_city_from_location())
    if not city:
        return jsonify({"error": "Could not determine city from location."})
    return jsonify(get_aqi_data(city))

# About Us route
@app.route('/about-us')
def about():
    return render_template('aboutus.html')

# Login route with streak increment
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users and users[username]['password'] == password:
            session['username'] = username
            users[username]['streak'] = users[username].get('streak', 0) + 1
            save_users(users)
            return redirect(url_for('user_home', user=username))
        return "Invalid credentials, please try again."
    return render_template('login.html')

# Signup route with streak initialization
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users:
            return "Username already exists."
        users[username] = {'password': password, 'streak': 0}
        save_users(users)
        return redirect(url_for('login'))
    return render_template('signup.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

# Contact Us route
@app.route('/contactus')
def contact():
    return render_template('contactus.html')

# Feedback route
@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

# Submit Feedback route
@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    feedback_text = request.form.get('feedback')
    if feedback_text:
        feedbacks = load_feedbacks()
        feedbacks.append({
            "username": session.get('username', 'Anonymous'),
            "feedback": feedback_text,
            "timestamp": "2025-03-18"
        })
        save_feedbacks(feedbacks)
    return render_template('feedback_submitted.html')

# Eco Tips route
@app.route('/eco-tips')
def ecotips():
    return render_template('eco-tips.html')

# Eco Location route
@app.route('/eco-location')
def ecolocation():
    return render_template('eco-location.html')

# Polluted Areas route
@app.route('/pollutedareas')
def pollutedarea():
    city = get_city_from_location()
    aqi_data = get_aqi_data(city) if city else {"error": "Could not determine city from location."}
    return render_template('polluted_areas.html', aqi_data=aqi_data)

# Stores route
@app.route('/stores')
def stores():
    return render_template('getapi.html')

# Chatbot route
@app.route('/chatbot')
def chatbot():
    return render_template("chatbot.html")

# Chatbot message endpoint
@app.route('/chatbot/message', methods=['POST'])
def chatbot_message():
    message = request.json.get('message', '')
    username = session.get('username')
    response = get_chatbot_response(message, username)  # Use imported function
    return jsonify({"response": response})

# User-specific home route with streak and leaderboard
@app.route('/home/<user>')
def user_home(user):
    if 'username' not in session or session['username'] != user:
        return redirect(url_for('login'))
    user_initial = user[0].upper()
    users = load_users()
    streak = users.get(user, {}).get('streak', 0)
    leaderboard = sorted(users.items(), key=lambda x: x[1].get('streak', 0), reverse=True)
    return render_template('afterlogin.html', user_initial=user_initial, username=user, streak=streak, leaderboard=leaderboard)

if __name__ == '__main__':
    app.run(debug=True)