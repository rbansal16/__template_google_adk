from google.adk.tools.tool_context import ToolContext
from agent.shared_libraries import get_logger

# Initialize logger for this module
logger = get_logger(__name__)


def get_weather(city: str, tool_context: ToolContext) -> dict:
    """Retrieves weather, converts temp unit based on session state."""
    logger.info(f"--- Tool: get_weather called for {city} ---")

    # --- Read preference from state ---
    preferred_unit = tool_context.state.get("user_preference_temperature_unit", "Celsius") # Default to Celsius
    logger.info(f"--- Tool: Reading state 'user_preference_temperature_unit': {preferred_unit} ---")

    city_normalized = city.lower().replace(" ", "")

    # Mock weather data (always stored in Celsius internally)
    mock_weather_db = {
        "newyork": {"temp_c": 25, "condition": "sunny"},
        "london": {"temp_c": 15, "condition": "cloudy"},
        "tokyo": {"temp_c": 18, "condition": "light rain"},
    }

    if city_normalized in mock_weather_db:
        data = mock_weather_db[city_normalized]
        temp_c = data["temp_c"]
        condition = data["condition"]

        # Format temperature based on state preference
        if preferred_unit == "Fahrenheit":
            temp_value = (temp_c * 9/5) + 32 # Calculate Fahrenheit
            temp_unit = "°F"
        else: # Default to Celsius
            temp_value = temp_c
            temp_unit = "°C"

        report = f"The weather in {city.capitalize()} is {condition} with a temperature of {temp_value:.0f}{temp_unit}."
        result = {"status": "success", "report": report}
        logger.info(f"--- Tool: Generated report in {preferred_unit}. Result: {result} ---")

        # Example of writing back to state (optional for this tool)
        tool_context.state["last_city_checked_stateful"] = city
        logger.info(f"--- Tool: Updated state 'last_city_checked_stateful': {city} ---")

        return result
    else:
        # Handle city not found
        error_msg = f"Sorry, I don't have weather information for '{city}'."
        logger.info(f"--- Tool: City '{city}' not found. ---")
        return {"status": "error", "error_message": error_msg}

logger.info("✅ State-aware 'get_weather' tool defined.")

# # @title Define the get_weather Tool
# def get_weather(city: str) -> dict:
#     """Retrieves the current weather report for a specified city.

#     Args:
#         city (str): The name of the city (e.g., "New York", "London", "Tokyo").

#     Returns:
#         dict: A dictionary containing the weather information.
#               Includes a 'status' key ('success' or 'error').
#               If 'success', includes a 'report' key with weather details.
#               If 'error', includes an 'error_message' key.
#     """
#     # Best Practice: Log tool execution for easier debugging
#     logger.info(f"--- Tool: get_weather called for city: {city} ---")
#     city_normalized = city.lower().replace(" ", "") # Basic input normalization

#     # Mock weather data for simplicity
#     mock_weather_db = {
#         "newyork": {"status": "success", "report": "The weather in New York is sunny with a temperature of 25°C."},
#         "london": {"status": "success", "report": "It's cloudy in London with a temperature of 15°C."},
#         "tokyo": {"status": "success", "report": "Tokyo is experiencing light rain and a temperature of 18°C."},
#         "raleigh": {"status": "success", "report": "Raleigh is experiencing light rain and a temperature of 18°C."},
#     }

#     # Best Practice: Handle potential errors gracefully within the tool
#     if city_normalized in mock_weather_db:
#         return mock_weather_db[city_normalized]
#     else:
#         return {"status": "error", "error_message": f"Sorry, I don't have weather information for '{city}'."}

# logger.info("Weather tools defined.")

# Example tool usage (optional self-test)
# logger.debug(f"Weather Root Agent tool: {get_weather("New York")}")
# logger.debug(f"Weather Root Agent tool: {get_weather("Paris")}")