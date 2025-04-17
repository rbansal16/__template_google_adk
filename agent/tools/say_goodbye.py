from agent.shared_libraries import get_logger

# Initialize logger for this module
logger = get_logger(__name__)

# @title Define Tools for Greeting and Farewell Agents

def say_goodbye() -> str:
    """Provides a simple farewell message to conclude the conversation."""
    logger.info(f"--- Tool: say_goodbye called ---")
    return "Goodbye! Have a great day."

logger.info("Farewell tools defined.")

# Optional self-test
logger.debug(f"Farewell tool: {say_goodbye()}")