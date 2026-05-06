import asyncio

# The Runner expects the module path of the root agent.
# The orchestrator_agent package's __init__.py should expose 'root_agent'.
from dotenv import load_dotenv
from google.adk.runners import Runner 
from google.adk.sessions import InMemorySessionService
from utils import call_agent_async, display_state # Added display_state for formatted output

load_dotenv()

# ===== PART 1: Initialize In-Memory Session Service =====
# Using in-memory storage for this example (non-persistent)
session_service = InMemorySessionService()


# ===== PART 2: Define Initial State =====
# This will be used when creating a new session
initial_state = {
    # For an error orchestrator, user-specific details like name or purchased courses might be unnecessary.
}


async def main_async():
    # Setup constants
    APP_NAME = "ErrorOrchestrator" # Renamed app for clarity in this demo
    USER_ID = "error_tester" # Renamed user ID for this specific demo

    # ===== PART 3: Session Creation =====
    # Create a new session with initial state
    new_session = session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state=initial_state,
    )
    SESSION_ID = new_session.id
    print(f"Created new session: {SESSION_ID}")

    # ===== PART 4: Agent Runner Setup =====
    # Create a runner with the main customer service agent
    # The orchestrator_agent is now the primary agent.
    runner = Runner( # Pass the module path string for the root agent
        agent='orchestrator_agent',
        app_name=APP_NAME,
        session_service=session_service,
    )

    # ===== PART 5: Interactive Conversation Loop =====
    print("\nWelcome to the Error Orchestrator Demo!")
    print("Enter an error message (e.g., 'DB connection failed', 'MQ queue full', 'SSH permission denied')")
    print("The orchestrator agent will attempt to handle it by calling appropriate sub-agents.")
    print("Type 'exit' or 'quit' to end the demo.\n")

    while True:
        # Get user input
        user_input = input("Enter error message: ") # Changed prompt to reflect expected input

        # Check if user wants to exit
        if user_input.lower() in ["exit", "quit"]:
            print("Ending conversation. Goodbye!")
            break

        # Process the user query through the agent
        # The orchestrator_agent will process this input.
        await call_agent_async(runner, USER_ID, SESSION_ID, user_input)

    # ===== PART 6: State Examination =====
    # Display the final session state using the utility function for formatted output.
    display_state(session_service, APP_NAME, USER_ID, SESSION_ID, "Final Session State")


def main():
    """Entry point for the application."""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
