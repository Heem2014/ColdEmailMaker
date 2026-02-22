from crewai import Agent, Task, Crew, LLM

import os

llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)
game_designer_agent=Agent(
    role="Game Designer",
    goal="Design a fun game for kids",  
    backstory="You are a creative game designer who loves making games for kids",
    llm=llm
)

game_designer_task=Task(
    description="Design a simple and fun game for kids that can be played indoors",
    expected_output="A simple and fun game design with rules and objectives",
    agent=game_designer_agent
)
game_reviewer_agent=Agent(
    role="Game Reviewer",
    goal="Review the game design, and rate it out of 100",
    backstory="You are a critical game reviewer who loves to review games for kids",
    llm=llm
)
game_reviewer_task=Task(
    description="Review the game design and rate it out of 100",
    expected_output="A review of the game design with a rating out of 100",
    agent=game_reviewer_agent
)
game_improver_agent=Agent(
    role="Game Improver",
    goal="Improve the game design based on the review",
    backstory="You are a creative game designer who loves to improve games for kids",
    llm=llm
)

game_improver_task=Task(
    description="Improve the game design based on the review",
    expected_output="An improved game design with better rules and objectives",
    agent=game_improver_agent
)

crew = Crew(
    agents=[game_designer_agent, game_reviewer_agent, game_improver_agent],
    tasks=[game_designer_task, game_reviewer_task, game_improver_task],
    verbose=True
)
result = crew.kickoff()
print(result)