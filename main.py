import asyncio

# The Runner expects the module path of the root agent.
# The orchestrator_agent package's __init__.py should expose 'root_agent'.
from dotenv import load_dotenv
from utils import call_agent_async
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
# ===== PART 1: Initialize In-Memory Session Service =====
# Using in-memory storage for this example (non-persistent)
session_service = InMemorySessionService()

# Import pandas for CSV processing
import pandas as pd
from google.adk import Agent

async def process_jira_csv_workflow_async(csv_file_path: str, runner: Runner, user_id: str, session_id: str):
    """
    Reads a CSV file, processes its data, and orchestrates sub-agents
    to handle Jira and Confluence tasks based on the CSV content.
    """
    print(f"\n--- Starting CSV processing for {csv_file_path} ---")

    # 1. Read the CSV using Pandas
    try:
        df = pd.read_csv(csv_file_path)
        
        # Validation: check if required columns exist
        required_cols = ['JIRA', 'Description', 'Solution', 'Date Solved']
        if not all(col in df.columns for col in required_cols):
            print(f"Error: CSV is missing one of the required columns: {required_cols}")
            return
            
    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_file_path}")
        return
    except Exception as e:
        print(f"Failed to read CSV: {e}")
        return

    # 2. Convert to a structured string format (JSON is very reliable for LLMs)
    data_context = df.to_json(orient='records', indent=2)

    # 3. Define the Sub-Agents (these are already defined in orchestrator_agent/sub_agents/mq_agent/agent.py
    #    but we define them here to show the context of what the manager is delegating to.)
    #    In a real scenario, the manager agent would already have access to these.
    #    For this example, we'll assume the 'orchestrator_agent' is smart enough to delegate
    #    to its children based on the prompt.
    #    The actual agent definitions are in orchestrator_agent/sub_agents/mq_agent/agent.py
    #    and its sub-folders.

    # 4. Build the prompt with the data embedded
    task_prompt = f"""
    Here is the data from the CSV file JIRA_solution:

    {data_context}

    Please process these entries. For each entry, identify the Jira ticket number ('JIRA') and its closing date ('Date Solved'),
    and instruct the db_jira_agent to mark it as closed.
    Also, extract the 'Description' and 'Solution', and instruct the db_confluence_agent to create
    or update a knowledge base article for each entry.
    """

    # 5. Execute the workflow through the main runner
    print("Delegating CSV data processing to orchestrator agent...")
    await call_agent_async(runner, user_id, session_id, task_prompt)


# ===== PART 2: Define Initial State =====

    # ===== PART 5: Interactive Conversation Loop =====
    # --- New: Call the CSV processing workflow before the interactive loop ---
    # For demonstration, we'll hardcode the CSV path. In a real app, this might come from user input or config.
    await process_jira_csv_workflow_async('/home/saiswamysunil_kaza/lahi-vertex-agent/JIRA_solution.csv', runner, USER_ID, SESSION_ID)
    # --- End New ---
    print("\nWelcome to the Error Orchestrator Demo!")
    print("Enter an error message (e.g., 'DB connection failed', 'MQ queue full', 'SSH permission denied')")
    print("The orchestrator agent will attempt to handle it by calling appropriate sub-agents.")
