from flask import Flask, render_template, request, jsonify
import csv
import json

app = Flask(__name__)

data_path = "./static/aqi_data.csv"  # Path to the AQI data file
location_path = "./static/location_details.json"  # Path to the location details file

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

if __name__ == '__main__':
    app.run(debug=True)
