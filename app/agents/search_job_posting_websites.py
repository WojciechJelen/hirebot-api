from pydantic_ai import Agent, RunContext
from pydantic_ai.models.anthropic import AnthropicModel
from dataclasses import dataclass
from typing import List, Optional
import os
from dotenv import load_dotenv
from app.schemas.websites_search_schemas import (
    JobPostingWebsite,
)

# Load environment variables from .env file
load_dotenv()


@dataclass
class SearchJobPostingWebsitesDeps:
    domain: str
    location: Optional[str] = None


# Get Anthropic API key from environment variables
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
if not anthropic_api_key:
    raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

model = AnthropicModel("claude-3-5-sonnet-latest", api_key=anthropic_api_key)

# Define the agent with proper deps_type and result_type
search_job_posting_websites_agent = Agent(
    model,
    deps_type=SearchJobPostingWebsitesDeps,
    result_type=List[JobPostingWebsite],
    system_prompt="You are a helpful assistant that can provide the best websites for a user to find job postings of a specific domain.",
)


@search_job_posting_websites_agent.tool
def suggest_job_posting_websites(
    ctx: RunContext[SearchJobPostingWebsitesDeps],
) -> List[JobPostingWebsite]:
    """
    Tool that suggests the best websites for finding job postings in a specific domain.

    Args:
        ctx: The run context containing the dependencies (domain and location)

    Returns:
        A list of JobPostingWebsite objects
    """
    domain = ctx.deps.domain
    location = ctx.deps.location or "anywhere"

    # In a real implementation, this would contain logic to find actual job posting websites
    # For demonstration, we'll return a hardcoded list of common job sites
    # This should be replaced with actual logic in production

    job_sites = [
        JobPostingWebsite(
            url="https://www.linkedin.com/jobs",
            name="LinkedIn",
        ),
        JobPostingWebsite(
            url="https://www.indeed.com",
            name="Indeed",
        ),
        JobPostingWebsite(
            url=f"https://www.{domain.lower().replace(' ', '')}.com/careers",
            name=f"{domain} Official Site",
        ),
    ]

    return job_sites
