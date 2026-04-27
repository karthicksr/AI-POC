from crewai import Agent, Task, Crew

# Fast local model
llm = "ollama/tinyllama"

# -----------------------
# 1. Single Agent
# -----------------------

log_analyzer = Agent(
    role="Log Analyzer",
    goal="Analyze logs and identify errors quickly",
    backstory="Expert in debugging application logs and identifying root causes",
    verbose=False,   # faster
    llm=llm
)

# -----------------------
# 2. Sample Log Input
# -----------------------

logs = """
2026-04-25 10:21:20 INFO Starting application
2026-04-25 10:21:21 ERROR Database connection failed
2026-04-25 10:21:22 WARN Retrying connection
2026-04-25 10:21:23 ERROR Database connection failed
2026-04-25 10:21:25 INFO Application stopped
"""

# -----------------------
# 3. Task (Structured Prompt)
# -----------------------

task = Task(
    description=f"""
Analyze the following logs and provide output in this format:

1. Errors found
2. Possible root cause
3. Suggested fix

Logs:
{logs}
""",
    expected_output="""
Errors:
Root Cause:
Fix:
""",
    agent=log_analyzer
)

# -----------------------
# 4. Run
# -----------------------

crew = Crew(
    agents=[log_analyzer],
    tasks=[task],
    verbose=False
)

result = crew.kickoff()

print("\n===== LOG ANALYSIS =====\n")
print(result)

# Crew pipeline execution flow when calling kickoff method
#crew.kickoff()
#      ↓
#  Crew reads the task list
#      ↓
#  Assigns each task to the appropriate agent
#      ↓
#  Agent uses its LLM + role/goal/backstory context
#      ↓
#  Executes the task (calls tools, reasons, generates output)
#      ↓
#  Returns the final result