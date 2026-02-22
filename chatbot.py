from crewai import Agent, Task, Crew, LLM
import os

llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)

story_agent = Agent(
    role="storyteller",
    goal="tell a fun story for kids",
    backstory="the stories will be fun and creative for kids about traveling",
    llm=llm
)

story_task = Task(
    description="create a 10 line story that is funny and talks about a cat",
    expected_output="a funny story about a cat",
    agent=story_agent
)

crew = Crew(
    agents=[story_agent],
    tasks=[story_task],
    verbose=True
    
)

result = crew.kickoff()
print(result)
