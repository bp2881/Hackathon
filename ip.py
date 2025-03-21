import requests
import json
import os

def get_location(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        if data.get("city") != "Hyderabad":
            details = {
                "city": "Hyderabad",
                "region": "Abdullapurmet",
                "country": "India",
                "lat": 17.334680,
                "lon": 78.696969,
                "ip": ip
            }
        else:
            details = {
                "city": data.get("city", "Hyderabad"),
                "region": data.get("regionName", "Abdullapurmet"),
                "country": data.get("country", "India"),
                "lat": data.get("lat", 17.334680), 
                "lon": data.get("lon", 78.696969),
                "ip": ip
            }
        return details
    except Exception as e:
        return {"error": str(e)}

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        if response.status_code == 200:
            data = response.json()
            return data.get('ip')
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def save_to_json(data, filename="location_details.json"):
    try:
        if os.path.exists(filename):
            os.remove(filename)
            print(f"Deleted existing file: {filename}")
        with open(filename, "w") as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving to JSON file: {e}")

# Get public IP
public_ip = get_public_ip()
if public_ip:
    print(f"Your public IP address is: {public_ip}")
    # Get location details
    location_details = get_location(public_ip)
    if "error" not in location_details:
        # Save location details to JSON file
        save_to_json(location_details)
    else:
        print(f"Error fetching location: {location_details['error']}")
else:
    print("Failed to retrieve public IP.")