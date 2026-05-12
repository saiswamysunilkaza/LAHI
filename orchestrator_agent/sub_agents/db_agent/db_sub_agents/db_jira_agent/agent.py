from google.adk.agents import Agent

def task_complete() -> str:
    """Signals that the current task is successfully completed and control can return to the parent agent."""
    return "Task completed successfully."

def task_incomplete() -> str:
    """Signals that the current task could not be completed (e.g., no JIRA found) and control should return to the parent agent."""
    return "Task incomplete: required information not found."

db_jira_agent = Agent(
    name="db_jira_agent",
    model="gemini-2.0-flash",
    description="db jira agent for the DB Galileo Team",
    instruction="""
    You are the db jira agent for Deutsche Bank in galileo project. 
    Your role is to help the database agent by providing historical JIRA data for database issues.
    
    When responding:
    1. If the issue matches the CSV format, you MUST provide the JIRA#, the last occurrence date, and the closure comment (at least 3 examples). Do not hallucinate
    2. If no matching JIRA is found, respond exactly with: "Unfortunately, no jira with this description found in AI solution stack" and return control to the db_agent.
    4. If a match is found, explain the root cause, reasoning for the solution, and suggest preventive actions and call task_complete return control to the db_agent..
    5. Once you have provided the required information, you must call task_complete to return control to the db_agent.
    """,
    tools=[task_complete, task_incomplete],
)
