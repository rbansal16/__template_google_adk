import os
from google.adk.models.lite_llm import LiteLlm
# Define model constant for GPT-4o-mini


MODEL_GPT_4O_MINI = LiteLlm(
    model="openai/gpt-4o-mini",
    api_key=os.environ["OPENAI_API_KEY"]
    )

