from google.adk.agents import LlmAgent
from agent.shared_libraries import MODEL_GPT_4O_MINI, get_logger
from agent.tools import say_goodbye

# Initialize logger for this module
logger = get_logger(__name__)

# --- Farewell Agent ---
farewell_agent = None
try:
    farewell_agent = LlmAgent(
        # Can use the same or a different model
        model=MODEL_GPT_4O_MINI, # Sticking with GPT for this example
        name="farewell_agent",
        instruction="You are the Farewell Agent. Your ONLY task is to provide a polite goodbye message. "
                    "Use the 'say_goodbye' tool when the user indicates they are leaving or ending the conversation "
                    "(e.g., using words like 'bye', 'goodbye', 'thanks bye', 'see you'). "
                    "Do not perform any other actions.",
        description="Handles simple farewells and goodbyes using the 'say_goodbye' tool.", # Crucial for delegation
        tools=[say_goodbye],
    )
    logger.info(f"Agent '{farewell_agent.name}' created using model '{MODEL_GPT_4O_MINI}'.")
except Exception as e:
    logger.error(f"Could not create Farewell agent. Check API Key ({MODEL_GPT_4O_MINI}). Error: {e}", exc_info=True)