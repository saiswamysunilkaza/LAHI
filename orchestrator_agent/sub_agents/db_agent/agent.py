from google.adk.agents import Agent, ParallelAgent
from .db_sub_agents.db_conf_agent import db_conf_agent
# Assuming db_jira_agent is defined similarly in the sibling directory
from .db_sub_agents.db_jira_agent import db_jira_agent

def task_complete() -> str:
    """Signals that the current task is successfully completed and control can return to the orchestrator agent."""
    return "Task completed successfully."

def task_incomplete() -> str:
    """Signals that the current task could not be completed (e.g., not a database issue) and control should return to the orchestrator agent."""
    return "Task incomplete: issue is outside the scope of the database agent."



# Define a ParallelAgent to execute both research tasks concurrently
db_info_gathering = ParallelAgent(
    name="db_info_gathering",
    description="Gathers documentation from Confluence and issue details from Jira in parallel.",
    sub_agents=[db_conf_agent, db_jira_agent],
)

# Define the main DB Agent that orchestrates the overall workflow
db_agent = Agent(
    name="db_agent",
    model="gemini-2.0-flash",
    description="Main Database Agent for the Galileo Team",
    instruction="""
    You are the primary Database Agent for project Galileo. 
    Your role is to provide solutions for database queue issues.

    Workflow:
    1. Verify if the issue is a database error. If not, call task_incomplete immediately.
    2. For database errors, you MUST first consult your sub-agent 'db_info_gathering'.
       This will trigger parallel searches in 'db_conf_agent' and 'db_jira_agent'.
       (Note: 'db_jira_agent' is expected to search 'JIRA_solutions.csv' for relevant tickets.)
    3. If 'db_info_gathering' provides historical JIRA data or Confluence links, summarize and relay that information.
    4. If 'db_info_gathering' reports that no matching records were found (e.g., "Unfortunately, no jira..." or "Unfortunately, no confluence data..."), you MUST NOT stop; instead, provide at least 3 contextually relevant Oracle expert solutions, explaining the root cause and preventive actions.
    5. Call task_complete ONLY after you have provided a meaningful response (either historical data or your own expertise) to ensure the orchestrator agent receives the solution.

    Always be direct and technical in your synthesis.
    """,
    sub_agents=[db_info_gathering],
    tools=[task_complete, task_incomplete],
)