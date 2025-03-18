import random
import csv
import json
import os

# Paths to data files (duplicated from app.py for independence)
data_path = "./static/aqi_data.csv"
location_path = "./static/location_details.json"

# Function to fetch AQI data from local CSV (copied from app.py)
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

# Function to get the city name from location_details.json (copied from app.py)
def get_city_from_location():
    try:
        with open(location_path, 'r') as file:
            location_data = json.load(file)
            return location_data.get("city", "")
    except Exception as e:
        return ""

# Chatbot response logic
def get_chatbot_response(message, username=None):
    message_lower = message.lower().strip()
    greeting_prefix = f"Hi {username}!" if username else "Hi there!"

    # Greetings
    greetings = [
        f"{greeting_prefix} I’m Eco Buddy, your green guide. What’s sparking your eco-curiosity today?",
        f"{greeting_prefix} Welcome to the sustainability crew! How can I make your day greener?",
        f"{greeting_prefix} Hey, eco-warrior! Ready to chat about saving the planet?"
    ]
    if any(greet in message_lower for greet in ["hi", "hello", "hey", "greetings"]):
        return random.choice(greetings)

    # Daily Conversation Responses
    daily_responses = {
        "how are you": f"I’m doing great, thanks! How about you, {username or 'friend'}? Feeling green today?",
        "weather": "I don’t have live weather data, but I’d say plant some trees for better air no matter the forecast! How’s the weather where you are?",
        "what’s up": f"Not much, just here to help you save the planet! What’s up with you, {username or 'eco-pal'}?",
        "plans": "My plan’s to keep the Earth thriving—how about you? Got any eco-friendly plans today?",
        "good morning": f"Good morning, {username or 'sunshine'}! Ready to kick off the day with some sustainable vibes?",
        "good night": f"Good night, {username or 'star'}! Dream of a greener world—I’ll be here tomorrow!",
        "mood": f"My mood’s always green! How’s yours? Need an eco-pick-me-up?",
        "joke": "Why don’t skeletons fight for the planet? They don’t have the guts! Want another?"
    }
    for key, response in daily_responses.items():
        if key in message_lower:
            return response

    # Sustainability Responses
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

    # Project-Specific Responses
    project_responses = {
        "project": f"This is the Eco-Friendly Sustainability Platform! It’s all about AQI tracking, eco-tips, and streaks to keep you green. What feature do you like most?",
        "leaderboard": "The leaderboard ranks users by their daily login streaks—top eco-warriors shine! Want to climb the ranks?",
        "streak": f"Your streak goes up every day you log in—it’s your eco-commitment score! What’s your current streak, {username or 'eco-friend'}?",
        "feedback": "Feedback helps us grow greener! Submit yours at /feedback—it’s stored safely. Got a suggestion now?",
        "eco-tips": "Eco-tips are at /eco-tips—daily ideas to live sustainably. Want a quick tip? Try reusable bottles!",
        "polluted areas": "Check /pollutedareas for AQI in your city—know what you’re breathing! Curious about your local air?",
        "stores": "The /stores page links to eco-friendly shops via AQI insights. Need sustainable shopping ideas?",
        "chatbot": "That’s me! I’m Eco Buddy, here for daily chats and project help. What’s on your mind?",
        "about us": "Visit /about-us to learn our mission—sustainability for all! What’s your take on our goal?"
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

    # Check for project-specific keywords
    for keyword, response in project_responses.items():
        if keyword in message_lower:
            return response

    # Fallback
    return f"{greeting_prefix} I’m here for daily chats or eco-questions—air quality, recycling, project stuff, you name it! What’s on your mind?"