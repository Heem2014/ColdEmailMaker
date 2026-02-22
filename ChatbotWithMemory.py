from crewai import Agent, Task, Crew, LLM
from dotenv import load_dotenv
import os

load_dotenv()

# Use a confirmed model version
llm = LLM(
    model="gemini/gemini-2.5-flash", 
    api_key=os.getenv("GEMINI_API_KEY")
)

# --- 1. Get info ONCE at the start ---
name = input("What's your name?: ")
food = input("What's your favorite food?: ")
hobby = input("What's your favorite hobby?: ")

print(f"\n[System] Setup complete. Type 'exit' to stop chatting.\n")

while True:
    user_input = input(f"{name}: ")
    
    if user_input.lower() in ["exit", "quit"]:
        print("AI: Goodbye! It was great talking to you.")
        break

    # --- 2. Define the Agent ---
    friend = Agent(
        role="AI Friend",
        goal="Engage in friendly conversation and provide companionship",
        backstory=f"You are a friendly AI. You know the user is {name}, likes {food}, and enjoys {hobby}.",
        llm=llm
    )

    
    chat_task = Task(
        description=f"The user said: '{user_input}'. Respond as a friend. Mention their interest in {hobby} or {food} only if it feels natural.",
        expected_output="A friendly, conversational response.",
        agent=friend
    )

    # --- 4. Define the Crew ---
    crew = Crew(
        agents=[friend],
        tasks=[chat_task],
        verbose=False,
        memory=True,
        embedder={
            "provider": "sentence-transformer",
            "config": {
                "model": "sentence-transformers/all-MiniLM-L6-v2"
            }
        }
    )

    # --- 5. Kickoff ---
    result = crew.kickoff()
    print(f"\nAI: {result}\n")