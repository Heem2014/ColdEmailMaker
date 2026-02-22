from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool
import os
search = SerperDevTool()


llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)


name = input("What's your name? ")
subject = input("What subject? (math/science/history): ")
question = input("What's your homework question? ")


researcher = Agent(
    role="Research Expert",
    goal="Find accurate information for homework",
    backstory="You find facts to help kids learn",
    tools=[search],
    llm=llm
)


teacher = Agent(
    role="Teacher",
    goal="Explain things simply for kids",
    backstory="You make learning fun and easy to understand",
    llm=llm
)


research_task = Task(
    description=f"Research the topic '{question}' for {subject}.",
    expected_output="Clear facts and key points.",
    agent=researcher
)


teach_task = Task(
    description=f"Explain the answer to {name} in a simple, kid-friendly way.",
    expected_output="Easy explanation a kid can understand.",
    agent=teacher
)


crew = Crew(
    agents=[researcher, teacher],
    tasks=[research_task, teach_task],
    verbose=True
)


result = crew.kickoff(inputs={"student_name": name, "subject": subject, "homework_question": question})
print(result)
