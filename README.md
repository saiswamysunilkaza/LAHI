# LAHI Vertex Agent: Error Orchestrator

This project demonstrates a stateful multi-agent system built using the Agent Development Kit (ADK) and Vertex AI. It functions as an **Error Orchestrator**, designed to intake technical error messages and delegate them to specialized sub-agents for diagnosis and resolution.

## What is a Stateful Multi-Agent System?

A Stateful Multi-Agent System combines two powerful patterns:

1. **State Management**: Persisting information about users and conversations across interactions
2. **Multi-Agent Architecture**: Distributing tasks among specialized agents based on their expertise

The result is a sophisticated agent ecosystem that can:
- Remember user information and interaction history
- Route queries to the most appropriate specialized agent
- Provide personalized responses based on past interactions
- Maintain context across multiple agent delegates

This system implements a technical support orchestrator where a root agent analyzes incoming errors (like database failures or connectivity issues) and routes them to specialist agents.

## Project Structure

```
7-stateful-multi-agent/
│
├── orchestrator_agent/         # Main agent package
│   ├── __init__.py                 # Required for ADK discovery
│   ├── agent.py                    # Root agent definition
│   └── sub_agents/                 # Specialized agents
│       ├── unix_agent/             # Handles unix issues
│       ├── mq_agent/               # Handles unix issues
│       ├── db_agent/               # Handles unix issues
│       
│
├── main.py                         # Application entry point with session setup
├── utils.py                        # Helper functions for state management
├── .env                            # Environment variables
└── README.md                       # This documentation
```

## Key Components

### 1. Session Management

The example uses `InMemorySessionService` to store session state:

```python
session_service = InMemorySessionService()

def initialize_state():
    {
    }

# Create a new session with initial state
session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initialize_state(),
)
```

### 2. State Sharing Across Agents

All agents in the system can access the same session state, enabling:
- Root agent with be Orchestrator agent himself calling the sub agents
- All agents to personalize responses based on user information

### 3. Multi-Agent Delegation

The customer service agent routes queries to specialized sub-agents:

```python
Orchestartor_agent = Agent(
    name="Orchestartor_agent",
    model="gemini-2.0-flash",
    description="Orchestartor_agent  for AI Developer Accelerator community",
    instruction="""
    You are the Orchestartor_agent for the AI Developer Accelerator community.
    Your role is to help users with their questions and direct them to the appropriate specialized agent.
    
    # ... detailed instructions ...
    
    """,
    sub_agents=[unix_agent, mq_agent, db_agent],
    tools=[],
)
```

## How It Works

1. **Initial Session Creation**:
   - A new session is created with user information and empty interaction history
   - Session state is initialized with default values

2. **Conversation Tracking**:
   - Each user message is added to `interaction_history` in the state
   - Agents can review past interactions to maintain context

3. **Query Routing**:
   - The root agent analyzes the user query and decides which specialist should handle it
   - Specialized agents receive the full state context when delegated to

4. **State Updates**:
   - When a user purchases a course, the sales agent updates `purchased_courses`
   - These updates are available to all agents for future interactions

5. **Personalized Responses**:
   - Agents tailor responses based on purchase history and previous interactions
   - Different paths are taken based on what the user has already purchased

## Getting Started


### Setup

1. Activate the virtual environment from the root directory:
```bash
# macOS/Linux:
source ../.venv/bin/activate
# Windows CMD:
..\.venv\Scripts\activate.bat
# Windows PowerShell:
..\.venv\Scripts\Activate.ps1
```

2. Make sure your Google API key is set in the `.env` file:
```
GOOGLE_API_KEY=your_api_key_here
```

### Running the Example

To run the stateful multi-agent example:

```bash
python main.py
```

This will:
1. Initialize a new session with default state
2. Start an interactive conversation with the orchestrator service agent
3. Track all interactions in the session state
4. Allow specialized agents to handle specific queries


Notice how the system remembers your purchase across different specialized agents!

## Advanced Features

### 1. Interaction History Tracking

The system maintains a history of interactions to provide context:

```python
# Update interaction history with the user's query
add_user_query_to_history(
    session_service, APP_NAME, USER_ID, SESSION_ID, user_input
)
```

### 2. Dynamic Access Control

The system implements conditional access to certain agents:

```
3. Course Support Agent
   - For questions about course content
   - Only available for courses the user has purchased
   - Check if "ai_marketing_platform" is in the purchased courses before directing here
```

### 3. State-Based Personalization

All agents tailor responses based on session state:

```
Tailor your responses based on the user's purchase history and previous interactions.
When the user hasn't purchased any courses yet, encourage them to explore the AI Marketing Platform.
When the user has purchased courses, offer support for those specific courses.
```

## Production Considerations

For a production implementation, consider:

1. **Persistent Storage**: Replace `InMemorySessionService` with `DatabaseSessionService` to persist state across application restarts
2. **User Authentication**: Implement proper user authentication to securely identify users
3. **Error Handling**: Add robust error handling for agent failures and state corruption
4. **Monitoring**: Implement logging and monitoring to track system performance

## Additional Resources

- [ADK Sessions Documentation](https://google.github.io/adk-docs/sessions/session/)
- [ADK Multi-Agent Systems Documentation](https://google.github.io/adk-docs/agents/multi-agent-systems/)
- [State Management in ADK](https://google.github.io/adk-docs/sessions/state/)
