from google.adk.agents import LlmAgent
from agent.shared_libraries import MODEL_GPT_4O_MINI, get_logger
from agent.tools import say_hello

# Initialize logger for this module
logger = get_logger(__name__)

# --- Greeting Agent ---
greeting_agent = None
try:
    greeting_agent = LlmAgent(
        # Using a potentially different/cheaper model for a simple task
        model=MODEL_GPT_4O_MINI,
        name="greeting_agent",
        instruction="You are the Greeting Agent. Your ONLY task is to provide a friendly greeting to the user. "
                    "Use the 'say_hello' tool to generate the greeting. "
                    "If the user provides their name, make sure to pass it to the tool. "
                    "Do not engage in any other conversation or tasks.",
        description="Handles simple greetings and hellos using the 'say_hello' tool.", # Crucial for delegation
        tools=[say_hello],
    )
    logger.info(f"Agent '{greeting_agent.name}' created using model '{MODEL_GPT_4O_MINI}'.")
except Exception as e:
    logger.error(f"Could not create Greeting agent. Check API Key ({MODEL_GPT_4O_MINI}). Error: {e}", exc_info=True)