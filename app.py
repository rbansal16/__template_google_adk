import asyncio

from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner


from agent.shared_libraries import get_logger
from agent import agent
from call_agent_async import call_agent_async
# Initialize logger for this module
logger = get_logger(__name__)

# @title Setup Session Service and Runner

# --- Session Management ---
# Key Concept: SessionService stores conversation history & state.
# InMemorySessionService is simple, non-persistent storage for this tutorial.
session_service_stateful = InMemorySessionService()

# Define constants for identifying the interaction context
SESSION_ID_STATEFUL = "session_state_demo_001"
USER_ID_STATEFUL = "user_state_demo"
APP_NAME = "weather_tutorial_app"

# Define initial state data - user prefers Celsius initially
initial_state = {
    "user_preference_temperature_unit": "Celsius"
}

# Create the specific session where the conversation will happen
session_stateful = session_service_stateful.create_session(
    app_name=APP_NAME, # Use the consistent app name
    user_id=USER_ID_STATEFUL,
    session_id=SESSION_ID_STATEFUL,
    state=initial_state # <<< Initialize state during creation
)
logger.info(f"Session created: App='{APP_NAME}', User='{USER_ID_STATEFUL}', Session='{SESSION_ID_STATEFUL}'")

# Verify the initial state was set correctly
retrieved_session = session_service_stateful.get_session(app_name=APP_NAME,
                                                         user_id=USER_ID_STATEFUL,
                                                         session_id = SESSION_ID_STATEFUL)
logger.info("\n--- Initial Session State ---")
if retrieved_session:
    logger.info(retrieved_session.state)
else:
    logger.error("Error: Could not retrieve session.")

# --- Runner ---
# Key Concept: Runner orchestrates the agent execution loop.
runner = Runner(
    agent=agent.root_agent, # The agent we want to run
    app_name=APP_NAME,   # Associates runs with our app
    session_service=session_service_stateful # Uses our session service (not the session itself)
)
logger.info(f"Runner created for agent '{runner.agent.name}' using stateful session service.")


async def run_stateful_conversation():
      logger.info("\n--- Testing State: Temp Unit Conversion & output_key ---")

      # 1. Check weather (Uses initial state: Celsius)
      logger.info("--- Turn 1: Requesting weather in London (expect Celsius) ---")
      await call_agent_async("What's the weather in London?", runner, USER_ID_STATEFUL, SESSION_ID_STATEFUL)

      # 2. Manually update state preference to Fahrenheit - DIRECTLY MODIFY STORAGE
      logger.info("\n--- Manually Updating State: Setting unit to Fahrenheit ---")
      try:
          # Access the internal storage directly - THIS IS SPECIFIC TO InMemorySessionService for testing
          stored_session = session_service_stateful.sessions[APP_NAME][USER_ID_STATEFUL][SESSION_ID_STATEFUL]
          stored_session.state["user_preference_temperature_unit"] = "Fahrenheit"
          # Optional: You might want to update the timestamp as well if any logic depends on it
          # import time
          # stored_session.last_update_time = time.time()
          logger.info(f"--- Stored session state updated. Current 'user_preference_temperature_unit': {stored_session.state['user_preference_temperature_unit']} ---")
      except KeyError:
          logger.error(f"--- Error: Could not retrieve session '{SESSION_ID_STATEFUL}' from internal storage for user '{USER_ID_STATEFUL}' in app '{APP_NAME}' to update state. Check IDs and if session was created. ---")
      except Exception as e:
          logger.error(f"--- Error updating internal session state: {e} ---")

      # 3. Check weather again (Tool should now use Fahrenheit)
      logger.info("\n--- Turn 2: Requesting weather in New York (expect Fahrenheit) ---")
      await call_agent_async("Tell me the weather in New York.", runner, USER_ID_STATEFUL, SESSION_ID_STATEFUL)

      # 4. Test basic delegation (should still work)
      logger.info("\n--- Turn 3: Sending a greeting ---")
      await call_agent_async("Hi!", runner, USER_ID_STATEFUL, SESSION_ID_STATEFUL)


if __name__ == "__main__":
    asyncio.run(run_stateful_conversation())