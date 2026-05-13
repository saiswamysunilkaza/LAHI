from google.adk.agents import Agent, ParallelAgent
from .db_sub_agents.db_conf_agent import db_conf_agent as db_confluence_agent
from .db_sub_agents.db_jira_agent import db_jira_agent

# Define the main Unix Agent that orchestrates the overall workflow
unix_agent = Agent(
    name="unix_agent",
    model="gemini-2.0-flash",
    description="Main Unix Agent for the Galileo Team",
    instruction="""
    You are the primary Unix Agent for project Galileo. 
    Your role is to coordinate troubleshooting and manage Unix-related information across Jira and Confluence.

    Workflow:
    1. For Unix troubleshooting or information gathering, consult both 'db_jira_agent' and 'db_confluence_agent' to gather full context.
    2. For requests involving ticket updates or documentation creation (e.g., from CSV data), delegate directly to 'db_jira_agent' or 'db_confluence_agent' as appropriate.
    3. Synthesize information from sub-agents to provide clear, technical summaries and identify correlations between tickets and documentation.
    4. Provide comprehensive summaries including root cause analysis and suggested fixes.

    Always be direct and technical in your synthesis.
    """,
    sub_agents=[db_jira_agent, db_confluence_agent]
)