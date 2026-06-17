# AI Travel Planner Agent

AI Travel Planner Agent is a MINIPROJECT by Team Thrive. It creates a weather-aware travel itinerary and packing list using:

- OpenWeather API for the next 5 days of forecast data
- Ollama with `llama3.2:3b` for itinerary generation
- Rule-based packing suggestions from weather conditions
- Destination profiles for more practical local recommendations

## What It Does

The app asks the user:

- Where they are planning to travel
- How many days they want to plan, up to 5 days
- Budget type: `low`, `medium`, or `high`

Then it:

- Fetches weather forecast for the destination
- Groups 3-hour forecast data into day-wise weather summaries
- Plans outdoor activities on better weather days
- Plans indoor, food, market, rest, or short-travel options on rainy or very hot days
- Shows weather forecast for each day
- Gives men and women clothing suggestions
- Creates a suitcase packing list based on rain, heat, cold, wind, or snow

## Example

User input:

```text
Where are you planning to travel?: Tirupati
How many days do you want to plan? OpenWeather supports the next 5 days: 5
Budget type [low/medium/high]: medium
```

Example output sections:

```text
1. Trip Summary
2. Weather Summary
3. Day-wise Itinerary
4. What to Pack
5. Men Clothing Suggestions
6. Women Clothing Suggestions
7. Important Tips
```

## Project Files

```text
main.py                  Main CLI app
weather_tool.py          OpenWeather geocoding and forecast tool
planner_agent.py         Ollama prompt, itinerary generation, packing logic
destination_profiles.py  Curated destination guidance for better recommendations
utils.py                 Input validation helpers
.env                     Local API keys and model settings
```

## Setup

Install dependencies inside your Python environment:

```bash
pip install requests python-dotenv rich ollama
```

Install and run Ollama:

```bash
ollama pull llama3.2:3b
ollama serve
```

Create a `.env` file:

```env
OPENWEATHER_API_KEY=your_openweather_api_key_here
OLLAMA_MODEL=llama3.2:3b
```

## Run

From the project folder:

```bash
python main.py
```

If `python` is not available in your shell but the local virtual environment is available, run:

```bash
./bin/python main.py
```

## Why It Uses Only 5 Days

This project uses the free OpenWeather 5-day / 3-hour forecast API. Because of that limitation, the app asks for number of days instead of asking for start and end dates.

This avoids confusing output where the user enters future dates but the weather API only returns the next 5 forecast days.

## Current Destination Logic

The project includes simple destination profiles. For example, Tirupati is treated as a temple city / pilgrimage destination, so the app recommends temple-friendly plans and clothing instead of unrelated activities like monasteries or trekking.

For unknown destinations, the app uses safe generic categories like:

- Popular local landmarks
- Local markets
- Museums or cultural centers if available
- Cafes or restaurants
- Rest during rain or peak heat

## Limitations

- Weather forecast is limited to the next 5 days.
- Ollama does not do live web search by itself.
- Unknown destinations may get generic itinerary categories instead of exact attraction names.
- The output quality depends on the local model response.

## Future Improvements

- Add more destination profiles for popular cities.
- Add a web search tool for live attractions and restaurants.
- Export itinerary to PDF or text file.
- Add total trip budget calculation.
- Add transport suggestions between places.
