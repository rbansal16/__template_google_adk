# Google ADK Multi-Agent Service

A multi-agent service using Google ADK with MCP client integration for tool interactions.

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in your API keys and config values
4. Run the project: `python -m agent.agent`

## Centralized Logging

This project uses a centralized logging system that can be configured through environment variables.

### Configuration

In your `.env` file, you can set:

```
# Logging Configuration
LOG_LEVEL=INFO  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_PATH=logs   # Directory to store log files
```

### Usage

In any module where you need logging:

```python
from shared_libraries import get_logger

# Initialize logger with the current module name
logger = get_logger(__name__)

# Use standard logging methods
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")

# With exceptions
try:
    # Some code that might raise an exception
    result = 1 / 0
except Exception as e:
    logger.exception(f"An error occurred: {e}")  # Includes stacktrace
```

### Features

The logging system provides:
- Console and file logging simultaneously
- Daily log files with timestamps
- Automatic log rotation (10MB max size, 5 backup files)
- Consistent formatting across the application
- Configurability through environment variables

## Project Structure

```
/
├── agent/
│   ├── agent.py          # Main agent implementation
│   ├── prompt.py         # Agent prompts
│   ├── tools/            # Tool implementations
│   └── shared_libraries/ # Shared code and utilities
│       ├── __init__.py
│       ├── constants.py  # Shared constants
│       └── logging_config.py  # Centralized logging
├── .env                  # Environment variables
├── .env.example          # Example environment config
└── requirements.txt      # Dependencies
``` 