from google.adk.agents import Agent, ParallelAgent
from .db_sub_agents.db_conf_agent import db_conf_agent as db_confluence_agent
from .db_sub_agents.db_jira_agent import db_jira_agent

def task_complete() -> str:
    """Signals that the current task is successfully completed and control can return to the orchestrator agent."""
    return "Task completed successfully."

def task_incomplete() -> str:
    """Signals that the current task could not be completed (e.g., not an MQ issue) and control should return to the orchestrator agent."""
    return "Task incomplete: issue is outside the scope of the MQ agent."


# Define the main MQ Agent that orchestrates the overall workflow
mq_agent = Agent(
    name="mq_agent",
    model="gemini-2.0-flash",
    description="Main MQ Agent for the Galileo Team",
    instruction="""
    You are the primary MQ Agent for project Galileo. 
    Your role is to coordinate troubleshooting and manage MQ-related information across Jira and Confluence.

    Workflow:
    1. For MQ troubleshooting or information gathering, you MUST first consult both 'db_jira_agent' and 'db_confluence_agent' to gather full context.
       (Note: 'db_jira_agent' is expected to search 'JIRA_solutions.csv' for relevant tickets.)
    2. If sub-agents provide historical JIRA data or Confluence links, summarize and relay that information.
    3. If sub-agents report that no matching records were found (e.g., "Unfortunately, no jira..." or "Unfortunately, no confluence data..."), you MUST NOT stop; instead, provide at least 3 contextually relevant MQ expert solutions, explaining the root cause and preventive actions.
    4. For requests involving ticket updates or documentation creation (e.g., from CSV data), delegate directly to 'db_jira_agent' or 'db_confluence_agent' as appropriate.
    5. Synthesize information from sub-agents to provide clear, technical summaries and identify correlations between tickets and documentation.
    6. Provide comprehensive summaries including root cause analysis and suggested fixes.
    7. Call task_complete ONLY after you have provided a meaningful response (either historical data or your own expertise) to ensure the orchestrator agent receives the solution.

    Always be direct and technical in your synthesis.
    """,
    sub_agents=[db_jira_agent, db_confluence_agent],
    tools=[task_complete, task_incomplete],
)