import os
from dotenv import load_dotenv
from ollama import chat
from destination_profiles import get_destination_profile

load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")


def create_packing_rules(daily_weather, destination_profile):
    """
    Rule-based packing recommendations from weather data.
    """
    items = set()
    clothing = set()

    has_rain = any(day["rain_slots"] > 0 for day in daily_weather)
    has_snow = any(day["snow_slots"] > 0 for day in daily_weather)
    cold_days = any(day["min_temp"] <= 12 for day in daily_weather)
    hot_days = any(day["max_temp"] >= 28 for day in daily_weather)
    windy_days = any(day["avg_wind_speed"] >= 6 for day in daily_weather)

    if has_rain:
        items.add("umbrella")
        items.add("raincoat or windcheater")
        items.add("waterproof shoes")

    if has_snow:
        items.add("thermal wear")
        items.add("gloves")
        items.add("woolen socks")
        items.add("snow shoes if available")

    if cold_days:
        clothing.add("warm jacket")
        clothing.add("hoodie or sweater")
        clothing.add("full-sleeve t-shirts")
        clothing.add("warm socks")

    if hot_days:
        clothing.add("light breathable cotton clothes")
        clothing.add("t-shirts")
        clothing.add("shorts or light trousers")
        items.add("sunscreen")
        items.add("sunglasses")
        items.add("water bottle")

    if windy_days:
        items.add("windcheater")

    items.add("basic medicines")
    items.add("phone charger and power bank")
    items.add("comfortable walking shoes")

    clothing.update(destination_profile["men_clothing"])
    clothing.update(destination_profile["women_clothing"])
    items.update(destination_profile["packing_extras"])

    clothing.add("sleepwear")
    clothing.add("extra innerwear")

    return {
        "clothing": sorted(clothing),
        "items": sorted(items),
    }


def format_weather_for_prompt(weather_data):
    """
    Convert weather JSON into readable text for the LLM.
    """
    location = weather_data["location"]
    days = weather_data["daily_weather"]

    text = f"""
Destination: {location['name']}, {location.get('country', '')}
Forecast Window: next {len(days)} day(s) available from OpenWeather

Available Weather Forecast:
"""

    for i, day in enumerate(days, start=1):
        text += f"""
Day {i} - {day['date']}
Weather: {day['weather']}
Type: {day['day_type']}
Temperature: {day['min_temp']}°C to {day['max_temp']}°C
Humidity: {day['avg_humidity']}%
Wind Speed: {day['avg_wind_speed']} m/s
Rain Slots: {day['rain_slots']}
Snow Slots: {day['snow_slots']}
"""

    return text


def bullet_list(items):
    return "\n".join(f"- {item}" for item in items)


def format_destination_profile_for_prompt(destination_profile):
    return f"""
Destination Type: {destination_profile['destination_type']}
Known Outdoor Options:
{bullet_list(destination_profile['outdoor_activities'])}
Known Indoor / Rain Plan Options:
{bullet_list(destination_profile['indoor_activities'])}
Food Suggestions:
{bullet_list(destination_profile['food_suggestions'])}
Avoid:
{bullet_list(destination_profile['avoid'])}
Dress Style: {destination_profile['dress_style']}
Men Clothing:
{bullet_list(destination_profile['men_clothing'])}
Women Clothing:
{bullet_list(destination_profile['women_clothing'])}
"""


def generate_itinerary(weather_data, budget_type="medium"):
    """
    Generate travel itinerary using Ollama.
    """
    destination_name = weather_data["location"]["name"]
    destination_profile = get_destination_profile(destination_name)
    packing = create_packing_rules(weather_data["daily_weather"], destination_profile)
    weather_text = format_weather_for_prompt(weather_data)
    profile_text = format_destination_profile_for_prompt(destination_profile)

    system_prompt = """
You are an AI Travel Planner Agent.

Your job:
- Create a practical travel itinerary using the weather forecast.
- Put outdoor activities on pleasant/sunny/cold clear days.
- Put indoor activities, food breaks, markets, rest, or short travel on rainy/snowy/very hot days.
- Give dress recommendations for men and women.
- Give estimated daily budget in Indian Rupees only.
- Print the packing list clearly. Never say "refer to packing rules".
- Do not claim weather data beyond the forecast provided.
- Use only the destination profile below for named attractions.
- If the profile is generic, do not invent specific attraction names. Use categories like "local market" or "popular landmark".
- Follow the Avoid list strictly.
- Do not print the Avoid list in the final answer unless warning the user about a real safety issue.
- On hot days, schedule outdoor visits early morning or evening and rest indoors during peak afternoon heat.
- Treat light rain as a reason to carry rain protection, not automatically as a full-day cancellation.
- Use the exact rain intensity from the forecast. Do not call light rain "heavy rain".
- Keep the answer simple and student-project friendly.
"""

    user_prompt = f"""
Create a travel itinerary using this weather forecast:

{weather_text}

Destination guidance:
{profile_text}

Budget type: {budget_type}

Packing rules already generated:
Clothing: {", ".join(packing["clothing"])}
Items: {", ".join(packing["items"])}

Required output format:

1. Trip Summary
2. Weather Summary
3. Day-wise Itinerary
4. What to Pack
5. Men Clothing Suggestions
6. Women Clothing Suggestions
7. Important Tips

For each day include:
- Date
- Weather
- Temperature
- Recommended plan
- Food suggestion
- Indoor/outdoor decision
- Estimated budget in INR only
- Dress recommendation

Important:
- Make exactly one itinerary day for each forecast day.
- Use the exact dates shown in the weather forecast.
- Do not add extra dates.
- In "What to Pack", list the generated Clothing and Items directly.
- Do not convert INR to USD.
"""

    response = chat(
        model=OLLAMA_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response["message"]["content"]
