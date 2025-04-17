import datetime
from zoneinfo import ZoneInfo
from agent.shared_libraries import get_logger

# Initialize logger for this module
logger = get_logger(__name__)

def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """
    logger.info(f"--- Tool: get_current_time called for city: {city} ---")
    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    logger.info(f"--- Tool: get_current_time returned: {report} ---")
    return {"status": "success", "report": report}

logger.info(f"Current Time tools defined")