#The model can be used from any providers. Open AI model provide best Quality but free tier is not available. For Learning purpose, we can install models (Ollama ) locally 
#and use it at free of cost. 
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7
)

# -----------------------
# 1. Define Agents
# -----------------------

researcher = Agent(
    role="Research Analyst",
    goal="Find accurate and relevant information about the given topic",
    backstory="Expert in gathering insights from various sources",
    verbose=True,
    llm=llm
)

writer = Agent(
    role="Content Writer",
    goal="Write a well-structured blog post",
    backstory="Skilled in writing engaging and simple content",
    verbose=True,
    llm=llm
)

reviewer = Agent(
    role="Editor",
    goal="Improve the content quality and fix grammar",
    backstory="Experienced editor ensuring clarity and correctness",
    verbose=True,
    llm=llm
)

# -----------------------
# 2. Define Tasks
# -----------------------

research_task = Task(
    description="Research about 'Future of AI in Java Microservices'",
    expected_output="Bullet points with key insights",
    agent=researcher
)

writing_task = Task(
    description="Write a blog using the research insights",
    expected_output="Detailed blog article",
    agent=writer
)

review_task = Task(
    description="Review and improve the blog",
    expected_output="Final polished blog",
    agent=reviewer
)

# -----------------------
# 3. Create Crew
# -----------------------

crew = Crew(
    agents=[researcher, writer, reviewer],
    tasks=[research_task, writing_task, review_task],
    verbose=True
)

# -----------------------
# 4. Run the Crew
# -----------------------

result = crew.kickoff()

print("\n\n===== FINAL OUTPUT =====\n")
print(result)