from flask import Flask, render_template, request, jsonify
import csv
import json
import os

app = Flask(__name__)

# Paths to data files
data_path = "aqi_data.csv"  # Path to the AQI data file
location_path = "static/location_details.json"  # Path to the location details file

# Function to fetch AQI data for a specific city
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

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# About Us route
@app.route('/about-us')
def about():
    return render_template('aboutus.html')

# Signup route
@app.route('/signup')
def signup():
    return render_template('signup.html')

# Contact Us route
@app.route('/contactus')
def contact():
    return render_template('contactus.html')

# Feedback route
@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

# Login route
@app.route('/login')
def login():
    return render_template('login.html')

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
    return render_template('polluted_areas.html')

# Stores route
@app.route('/stores')
def stores():
    return render_template('stores.html')

# Chatbot route
@app.route('/chatbot')
def chatbot():
    return render_template("chatbot.html")

# AQI API route
@app.route('/aqi', methods=['GET'])
def aqi():
    city = get_city_from_location()
    if not city:
        return jsonify({"error": "Could not determine city from location."})
    return jsonify(get_aqi_data(city))

if __name__ == '__main__':
    app.run(debug=True)