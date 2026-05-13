from google.adk.agents import Agent
import csv
import os

def task_complete() -> str:
    """Signals that the current task is successfully completed and control can return to the parent agent."""
    return "Task completed successfully."

def task_incomplete() -> str:
    """Signals that the current task could not be completed (e.g., no JIRA found) and control should return to the parent agent."""
    return "Task incomplete: required information not found."

def search_jira_solutions_csv(issue_description: str) -> str:
    """
    Reads the JIRA_solutions.csv file and searches for historical JIRA tickets and solutions 
    matching the provided issue description.
    """
    csv_path = "JIRA_solutions.csv"
    if not os.path.exists(csv_path):
        return f"Error: {csv_path} not found. Ensure the file is in the project root."

    matches = []
    try:
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            search_query = issue_description.lower()
            for row in reader:
                # Check if any value in the row contains the search query
                row_str = " ".join(str(v) for v in row.values()).lower() # Convert each value to string before joining
                if search_query in row_str:
                    matches.append(row)
        
        if not matches:
            return "Unfortunately, no jira with this description found in AI solution stack."
        
        return str(matches)
    except Exception as e:
        return f"Error reading JIRA CSV: {str(e)}"

db_jira_agent = Agent(
    name="db_jira_agent",
    model="gemini-2.0-flash",
    description="db jira agent for the DB Galileo Team",
    instruction="""
    You are the db jira agent for Deutsche Bank in galileo project. 
    Your role is to provide historical JIRA data from the 'JIRA_solutions.csv' file.
    
    Workflow:
    1. Use the 'search_jira_solutions_csv' tool to find relevant tickets based on the user's issue.
    2. If the tool returns tickets, summarize them clearly for the parent agent.
    3. If the tool returns "Unfortunately, no jira...", report exactly that message so the parent agent knows to provide an LLM-based solution.
    4. Call task_complete after reporting the findings.

    Always be direct and technical in your synthesis.
    """,
    tools=[task_complete, task_incomplete, search_jira_solutions_csv],
)
