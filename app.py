from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import csv
import json
import os
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection for testing

# Paths to data files
data_path = "./static/aqi_data.csv"
location_path = "./static/location_details.json"
stationaries_path = "./static/stationaries.json"
users_path = "./static/users.json"
feedbacks_path = "./static/feedbacks.json"  # Added for feedback storage

# Function to fetch AQI data from local CSV
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

# Function to get the city name from location_details.json
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
    return []  # Return empty list if file doesn’t exist

# Function to save feedbacks to JSON
def save_feedbacks(feedbacks):
    with open(feedbacks_path, 'w') as file:
        json.dump(feedbacks, file, indent=4)

# Chatbot response logic (no API, local AQI data)
def get_chatbot_response(message, username=None):
    message_lower = message.lower().strip()
    
    # Greetings
    greeting_prefix = f"Hi {username}!" if username else "Hi there!"
    greetings = [
        f"{greeting_prefix} I’m Eco Buddy, your green guide. What’s sparking your eco-curiosity today?",
        f"{greeting_prefix} Welcome to the sustainability crew! How can I make your day greener?",
        f"{greeting_prefix} Hey, eco-warrior! Ready to chat about saving the planet?"
    ]
    if any(greet in message_lower for greet in ["hi", "hello", "hey", "greetings"]):
        return random.choice(greetings)

    # Sustainable development responses
    sustainability_responses = {
        "sustainability": "Sustainability keeps our planet thriving. Cut plastic use—like ditching straws—or grow your own herbs. What’s your sustainability goal?",
        "eco-friendly": "Eco-friendly living rocks! Try reusable bags or bamboo toothbrushes. What’s your green swap idea?",
        "green living": "Green living is the vibe! Composting slashes landfill waste by 30%, and biking cuts emissions. What’s your eco-routine?",
        "recycling": "Recycling saves the day—cans can be reused forever! Sort paper, plastic, glass—need local recycling tips?",
        "energy": "Energy saving is clutch! LEDs use 75% less juice than old bulbs. Unplug stuff or go solar—what’s your energy trick?",
        "water": "Water’s precious—short showers save 10 gallons a pop! Catch rainwater or fix leaks—got a water hack?",
        "climate": "Climate action’s on us! Trees soak up CO2, and less meat means fewer emissions. How do you tackle climate change?",
        "waste": "Less waste, more planet! Reuse jars or upcycle clothes—Americans toss 292 million tons yearly. What’s your waste plan?",
        "aqi": None,  # Handled separately
        "air quality": None
    }

    # Check for sustainability keywords
    for keyword, response in sustainability_responses.items():
        if keyword in message_lower:
            if keyword in ["aqi", "air quality"]:
                city = None
                if "in" in message_lower:
                    city = message_lower.split("in")[-1].strip()
                if not city:
                    city = get_city_from_location()
                aqi_data = get_aqi_data(city) if city else {"error": "No city specified."}
                if "error" not in aqi_data:
                    return f"The AQI in {aqi_data['City']} is {aqi_data['AQI']} ({aqi_data['CO AQI Category']} for CO). Poor air? Add plants or wear a mask—want more air tips?"
                return f"Can’t find AQI for {city or 'your spot'}. Try another city or ask me something else!"
            return response

    # Fallback
    return f"{greeting_prefix} I’m here for all things green—air quality, recycling, you name it! What’s on your mind?"

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
            users[username]['streak'] = users[username].get('streak', 0) + 1  # Increment streak
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
        users[username] = {'password': password, 'streak': 0}  # Initialize streak
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
            "username": session.get('username', 'Anonymous'),  # Include username if logged in
            "feedback": feedback_text,
            "timestamp": "2025-03-18"  # Hardcoded for now; use datetime for real apps
        })
        save_feedbacks(feedbacks)
    return render_template('feedback_submitted.html')  # Show message for 3 seconds before redirect

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
    response = get_chatbot_response(message, username)
    return jsonify({"response": response})

# User-specific home route with streak and leaderboard
@app.route('/home/<user>')
def user_home(user):
    if 'username' not in session or session['username'] != user:
        return redirect(url_for('login'))
    user_initial = user[0].upper()
    users = load_users()  # Load users from users.json
    streak = users.get(user, {}).get('streak', 0)  # Get current user's streak
    leaderboard = sorted(users.items(), key=lambda x: x[1].get('streak', 0), reverse=True)  # Sort by streak
    return render_template('afterlogin.html', user_initial=user_initial, username=user, streak=streak, leaderboard=leaderboard)

if __name__ == '__main__':
    app.run(debug=True)