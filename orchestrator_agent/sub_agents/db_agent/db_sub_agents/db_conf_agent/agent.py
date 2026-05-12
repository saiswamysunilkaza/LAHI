from google.adk.agents import Agent

def task_complete() -> str:
    """Signals that the current task is successfully completed and control can return to the db_agent."""
    return "Task completed successfully."

def task_incomplete() -> str:
    """Signals that the current task could not be completed (e.g., no Jconfluence links found) and control should return to the db_agent."""
    return "Task incomplete: required information not found."

# Create the course support agent
db_conf_agent = Agent(
    name="db_conf_agent",
    model="gemini-2.0-flash",
    description="db confluence agent for the DB Galileo Team",
    instruction="""
    You are the db confluence agent for Deutsche Bank in the Galileo project. 
    Your role is to help the database agent with documentation and solutions found in Confluence.

    When responding:
    1. If a relevant document is found, provide the Confluence links (at least 3) and summarize the relevant solution data.
    2. If no matching documentation is found, respond exactly with: "Unfortunately, no confluence data with this description found in AI solution stack" and return control to the db_agent.
    3. If data is found, be clear and direct, explaining the root cause, reasoning behind the solution, and preventive actions and call task_complete to return control to the db_agent.
    4. Do not overstep on other agents.
    5. Once you have provided the solutions and recommendations, call task_complete to return control to the db_agent.
    """,
    tools=[task_complete, task_incomplete],
    output_key="confluence_data",
)
