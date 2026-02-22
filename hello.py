from crewai import Agent, Task, Crew, LLM 
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import os

load_dotenv()

user_input = input("Enter your research topic: ")

llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)
search_tool = SerperDevTool()

researcher_agent = Agent(
    role="Researcher Assistant",
    goal= f"tell me 5 interesting facts about {user_input} with sources and references",
    backstory=f"you are a research assistant who loves to find interesting facts about {user_input}",
    llm=llm,
    tools=[search_tool]
)

researcher_task = Task(
    description=f"find 3 interesting facts about the {user_input} with references",
    expected_output=f"3 interesting facts about the {user_input} with references",
    agent=researcher_agent
)

crew = Crew(
    
    agents=[researcher_agent],
    tasks=[researcher_task],
    verbose = True
)

result = crew.kickoff(inputs={"given topic": user_input})
print(result)
    
