from pydantic_ai import Agent, RunContext
from firecrawl import FirecrawlApp
from pydantic_ai.models.anthropic import AnthropicModel
from dataclasses import dataclass
from urllib.parse import urlparse
import re
import os
from dotenv import load_dotenv
from typing import List
from app.schemas.job_schemas import (
    JobPostingWebsite,
    BrowseJobPostingsResponse,
    BrowseJobPostingsRequest,
)

# Load environment variables from .env file
load_dotenv()


@dataclass
class BrowseJobPostingsWebstitesDeps:
    query: str
    location: str
    firecrawl_app: FirecrawlApp


# Get API key from environment variables
firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")
if not firecrawl_api_key:
    raise ValueError("FIRECRAWL_API_KEY not found in environment variables")

firecrawl_app = FirecrawlApp(api_key=firecrawl_api_key)


# Get Anthropic API key from environment variables
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
if not anthropic_api_key:
    raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

# Get number of search pages from environment variables (with default)
num_search_pages = int(os.getenv("NUM_SEARCH_PAGES", "5"))

model = AnthropicModel("claude-3-5-sonnet-latest", api_key=anthropic_api_key)
job_postings_agent = Agent(
    model,
    deps_type=BrowseJobPostingsWebstitesDeps,
    result_type=List[JobPostingWebsite],
    system_prompt="Find job posting websites for the given domain.",
)


@job_postings_agent.tool
def find_websites_posting_jobs(
    ctx: RunContext[BrowseJobPostingsWebstitesDeps],
) -> List[JobPostingWebsite]:
    """
    Tool that finds websites posting jobs for a specific domain.

    Args:
        ctx: The run context containing the dependencies (query and location)

    Returns:
        A list of JobPostingWebsite objects
    """
    specific_domain = ctx.deps.query
    query = f"{specific_domain} jobs {ctx.deps.location}"
    base_search_url = f"https://www.google.com/search?q={query}&start="
    all_website_domains = set()

    # Use the firecrawl app from dependencies
    app = ctx.deps.firecrawl_app

    for start in range(0, num_search_pages * 10, 10):
        search_url = base_search_url + str(start)
        scrape_result = app.scrape(search_url, formats=["markdown"])
        markdown_content = scrape_result["markdown"]
        url_pattern = r"\[[^\]]*\]\(([^)]*)\)"
        urls = re.findall(url_pattern, markdown_content)
        for url in urls:
            if url.startswith("http"):
                parsed_url = urlparse(url)
                website_domain = parsed_url.netloc
                all_website_domains.add(website_domain)

    job_posting_websites = []
    for website_domain in all_website_domains:
        homepage_url = f"https://{website_domain}"
        prompt = f"Does this website have job postings related to {specific_domain}? Answer yes or no."
        scrape_result_with_prompt = app.scrape(
            homepage_url, formats=["json"], jsonOptions={"prompt": prompt}
        )
        response = scrape_result_with_prompt["data"].get("answer", "")
        if response.lower() == "yes":
            # Create a JobPostingWebsite object instead of just returning the domain
            website = JobPostingWebsite(
                url=homepage_url,
                has_job_postings=True,
                name=website_domain,  # Using domain as name for simplicity
                description=f"Job posting website for {specific_domain}",
            )
            job_posting_websites.append(website)

    return job_posting_websites


async def browse_job_postings_agent(
    request: BrowseJobPostingsRequest,
) -> BrowseJobPostingsResponse:
    """
    Agent that searches for job postings based on given criteria.

    Args:
        request: The BrowseJobPostingsRequest object

    Returns:
        A BrowseJobPostingsResponse with job postings
    """
    deps = BrowseJobPostingsWebstitesDeps(
        query=request.query,
        location=request.location or "",
        firecrawl_app=firecrawl_app,
    )

    # Run the agent to find websites
    result = await job_postings_agent.run("Find job posting websites", deps=deps)

    return BrowseJobPostingsResponse(results=result, total_found=len(result))
