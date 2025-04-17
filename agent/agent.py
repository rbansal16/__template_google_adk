from google.adk.agents import LlmAgent
from agent.shared_libraries import MODEL_GPT_4O_MINI, get_logger
from agent.sub_agents.greetings_agent import greeting_agent
from agent.sub_agents.farewell_agent import farewell_agent
from agent.tools import get_weather

# Initialize logger for this module
logger = get_logger(__name__)

# @title Define the Weather Agent

root_agent = None

if greeting_agent and farewell_agent and 'get_weather' in globals():
    # Let's use a capable Gemini model for the root agent to handle orchestration
    root_agent_model = MODEL_GPT_4O_MINI

    weather_agent_team = LlmAgent(
        name="weather_agent_v2", # Give it a new version name
        model=root_agent_model,
        description="Main agent: Provides weather (state-aware unit), delegates greetings/farewells, saves report to state.",
        instruction="You are the main Weather Agent. Your job is to provide weather using 'get_weather_stateful'. "
                    "The tool will format the temperature based on user preference stored in state. "
                    "Delegate simple greetings to 'greeting_agent' and farewells to 'farewell_agent'. "
                    "Handle only weather requests, greetings, and farewells.",
        tools=[get_weather], # Use the state-aware tool
        sub_agents=[greeting_agent, farewell_agent], # Include sub-agents
        output_key="last_weather_report" # <<< Auto-save agent's final weather response
    )
    logger.info(f"Root Agent '{weather_agent_team.name}' created using stateful tool and output_key.")
    root_agent = weather_agent_team
else:
    logger.error("Cannot create root agent because one or more sub-agents failed to initialize or 'get_weather' tool is missing.")
    if not greeting_agent: logger.error(" - Greeting Agent is missing.")
    if not farewell_agent: logger.error(" - Farewell Agent is missing.")
    if 'get_weather' not in globals(): logger.error(" - get_weather function is missing.")
