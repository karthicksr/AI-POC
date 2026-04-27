import requests
from crewai import Agent, Task, Crew

# ---------------------------
# CONFIG
# ---------------------------
API_KEY = "52b102ff8460eb8ada004558fa84dae8"
MODEL = "ollama/tinyllama"

# ---------------------------
# STEP 1: Get Weather (Python handles API)
# ---------------------------
def get_weather(city: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
    except Exception as e:
        return f"ERROR: API call failed: {e}"

    if data.get("cod") != 200:
        return "ERROR: City not found"

    return {
        "city": city,
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"]
    }

# ---------------------------
# STEP 2: Input
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

weather_data = get_weather(city)

# ---------------------------
# STEP 3: Agent (NO TOOLS)
# ---------------------------
agent = Agent(
    role="Weather Formatter",
    goal="Format weather data clearly and concisely",
    backstory="Expert in presenting weather information",
    llm=MODEL,
    verbose=False
)

# ---------------------------
# STEP 4: Task
# ---------------------------
task = Task(
    description=f"""
Format the following weather data into clean output:

Weather Data:
{weather_data}

Return format:
City: <name>
Temperature: <value> °C
Description: <text>
""",
    expected_output="""
City: 
Temperature: 
Description:
""",
    agent=agent
)

# ---------------------------
# STEP 5: Run
# ---------------------------
crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=False
)

result = crew.kickoff()

print("\n===== WEATHER OUTPUT =====\n")
print(result)