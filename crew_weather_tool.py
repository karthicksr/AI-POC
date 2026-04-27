import requests
from crewai import Agent, Task, Crew
from crewai.tools import tool

# ---------------------------
# CONFIG
# ---------------------------
API_KEY = "52b102ff8460eb8ada004558fa84dae8"
MODEL = "ollama/llama3"

# ---------------------------
# TOOL DEFINITION
# ---------------------------
@tool("get_weather")
def get_weather(city: str) -> str:
    """
    Fetch current weather for a given city using OpenWeather API
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()
    except Exception as e:
        return f"ERROR: API failed: {e}"

    if data.get("cod") != 200:
        return f"ERROR: City '{city}' not found"

    return f"""
City: {city}
Temperature: {data['main']['temp']} °C
Description: {data['weather'][0]['description']}
"""

# ---------------------------
# AGENT
# ---------------------------
weather_agent = Agent(
    role="Weather Assistant",
    goal="Provide accurate weather using tools",
    backstory="You ALWAYS use the get_weather tool to fetch real weather data",
    tools=[get_weather],
    llm=MODEL,
    verbose=True
)

# ---------------------------
# INPUT
# ---------------------------
def get_current_city():
    try:
        res = requests.get("http://ip-api.com/json", timeout=5)
        return res.json().get("city")
    except:
        return "Chennai"

city = input("Enter city (or press Enter for auto): ").strip()
if not city:
    city = get_current_city()

# ---------------------------
# TASK
# ---------------------------
task = Task(
    description=f"""
You MUST use the get_weather tool. Do not guess.

Get current weather for {city}.

Return:
- City
- Temperature
- Description
""",
    expected_output="""
City:
Temperature:
Description:
""",
    agent=weather_agent
)

# ---------------------------
# RUN CREW
# ---------------------------
crew = Crew(
    agents=[weather_agent],
    tasks=[task],
    verbose=True
)

result = crew.kickoff()

print("\n===== WEATHER OUTPUT =====\n")
print(result)