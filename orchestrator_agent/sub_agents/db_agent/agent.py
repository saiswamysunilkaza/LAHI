from google.adk.agents import Agent, ParallelAgent
from .db_sub_agents.db_conf_agent import db_conf_agent
# Assuming db_jira_agent is defined similarly in the sibling directory
from .db_sub_agents.db_jira_agent import db_jira_agent

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
    Your role is to coordinate troubleshooting by gathering data from multiple sources.

    Workflow:
    1. When a database issue or request is received, immediately call the 'db_info_gathering' agent.
    2. This will trigger searches in both Confluence and Jira at the same time.
    3. Once you receive the results from both sub-agents, synthesize the information.
    4. Look for correlations between Jira tickets (recent changes/bugs) and Confluence documentation (known solutions).
    5. if no solutions are provided as per point#4 .Provide a comprehensive summary to the user including the root cause, suggested fix, and relevant links in three different ways.
    

    Always be direct and technical in your synthesis.
    """,
    sub_agents=[db_info_gathering]
)