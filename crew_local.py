from crewai import Agent, Task, Crew

# IMPORTANT: Use model string with ollama prefix
local_model = "ollama/tinyllama"

researcher = Agent(
    role="Research Analyst",
    goal="Find key points about AI in Java microservices",
    backstory="Expert in software architecture",
    verbose=False,
    llm=local_model
)

writer = Agent(
    role="Writer",
    goal="Write a simple blog",
    backstory="Writes clear technical content",
    verbose=False,
    llm=local_model
)

reviewer = Agent(
    role="Reviewer",
    goal="Improve clarity and correctness",
    backstory="Senior editor",
    verbose=False,
    llm=local_model
)

task1 = Task(
    description="List key points about AI in Java microservices in short",
    expected_output="Bullet points",
    agent=researcher
)

task2 = Task(
    description="Write a short blog using the research (100 words)",
    expected_output="Blog content",
    agent=writer
)

task3 = Task(
    description="Review and improve the blog",
    expected_output="Final polished blog",
    agent=reviewer
)

crew = Crew(
    agents=[researcher, writer, reviewer],
    tasks=[task1, task2, task3],
    verbose=True
)

result = crew.kickoff()

print("\n===== FINAL OUTPUT =====\n")
print(result)