from agent.shared_libraries import get_logger

# Initialize logger for this module
logger = get_logger(__name__)

def say_hello(name: str = "there") -> str:
    """Provides a simple greeting, optionally addressing the user by name.

    Args:
        name (str, optional): The name of the person to greet. Defaults to "there".

    Returns:
        str: A friendly greeting message.
    """
    logger.info(f"--- Tool: say_hello called with name: {name} ---")
    return f"Hello, {name}!"

logger.info("Greeting tools defined.")

# Optional self-test
logger.debug(f"Greeting tool: {say_hello('Alice')}")
