from crewai import Agent, Crew, Task, Process

# ---------------------------
# MODEL
# ---------------------------
llm = "ollama/llama3.1"

# Configure local embeddings
embedder_config = {
    "provider": "ollama",
    "config": {
        "model_name": "nomic-embed-text",          # ✅ correct key name
        "url": "http://localhost:11434"
    }
}

# ---------------------------
# AGENT (memory enabled)
# ---------------------------
assistant = Agent(
    role="Personal Assistant",
    goal="Remember user details and respond correctly",
    backstory="Helpful assistant that remembers conversations",
    llm=llm,
    memory=True,
    verbose=False
)

# ---------------------------
# TASK 1
# ---------------------------
task1 = Task(
    description="User says: My name is Karthick",
    expected_output="Store the user's name",
    agent=assistant
)

# ---------------------------
# TASK 2
# ---------------------------
task2 = Task(
    description="What is my name?",
    expected_output="Return the user's name",
    agent=assistant
)

# ---------------------------
# CREW
# ---------------------------
crew = Crew(
    agents=[assistant],
    tasks=[task1, task2],
    memory=True,           # ← enable memory at crew level too
    embedder=embedder_config,  # ← use local embeddings
    verbose=False
)

# ---------------------------
# RUN
# ---------------------------
result = crew.kickoff()

print("\n===== MEMORY OUTPUT =====\n")
print(result)