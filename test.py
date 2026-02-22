from crewai import Agent, Task, Crew, LLM
from dotenv import load_dotenv
load_dotenv()
import os

llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)

game_maker = Agent(
    role="Python Game Developer",
    goal="Create a game which is Catch the apples game using the Pygame library which will be very fun to play and detailed" ,
    backstory="You are an expert Python developer who loves creating fun and interactive games using the Pygame library",
    llm=llm
)
game_task = Task(
    description="Create a simple game using the Pygame library",
    expected_output="A Python program that generates a simple game using the Pygame library",
    agent=game_maker
)
game_checker_task = Task(
    description="Check the generated Python game code for errors and ensure it runs correctly",
    expected_output="The generated Python game code runs without errors",
    agent=game_maker
)

crew = Crew(
    agents=[game_maker],
    tasks=[game_task, game_checker_task],
    verbose=False
)

result = crew.kickoff()
print(result)