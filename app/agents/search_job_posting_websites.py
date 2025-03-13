from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel
import os

anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
if not anthropic_api_key:
    raise ValueError("ANTHROPIC_API_KEY not found in environment variables")


model = AnthropicModel("claude-3-5-sonnet-latest", api_key=anthropic_api_key)
agent = Agent(
    model,
    system_prompt="You are a helpful assistant that can provide the best website for a user to find job postings of a specific domain.",
)
