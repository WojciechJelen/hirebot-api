from pydantic_ai import Agent, RunContext
from pydantic_ai.models.anthropic import AnthropicModel
from dataclasses import dataclass
from typing import List, Optional
from app.agents.utils.firecrawl import app as firecrawl_app
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
    job_sites = []
    location = ctx.deps.location or "anywhere"

    # Construct search query
    search_query = f"best job websites for {domain} jobs {location}"

    print(f"Searching for: {search_query}")

    # Common job sites to look for as fallback
    common_job_sites = [
        ("Dice", "https://www.dice.com"),
        ("Indeed", "https://www.indeed.com"),
        ("LinkedIn", "https://www.linkedin.com/jobs"),
        ("Monster", "https://www.monster.com"),
        ("CareerBuilder", "https://www.careerbuilder.com"),
        ("Glassdoor", "https://www.glassdoor.com"),
        ("ZipRecruiter", "https://www.ziprecruiter.com"),
        ("Stack Overflow", "https://stackoverflow.com/jobs"),
        ("GitHub Jobs", "https://jobs.github.com"),
        ("AngelList", "https://angel.co/jobs"),
        ("Hired", "https://hired.com"),
        ("We Work Remotely", "https://weworkremotely.com"),
        ("Authentic Jobs", "https://authenticjobs.com"),
        ("SimplyHired", "https://www.simplyhired.com"),
        ("Robert Half", "https://www.roberthalf.com"),
    ]

    try:
        # Use Firecrawl to search for job posting websites
        search_results = firecrawl_app.search(
            query=search_query,
            params={
                "limit": 5  # Limit to top 5 results
            },
        )

        # Convert to list if we received a dict response
        if isinstance(search_results, dict):
            if search_results.get("success", False) and "data" in search_results:
                results_list = search_results["data"]
            else:
                results_list = []
        elif isinstance(search_results, list):
            results_list = search_results
        else:
            # Unexpected response type
            results_list = []

        # Process search results
        if results_list:
            # Keep track of URLs we've already added
            added_urls = set()

            # Process each search result
            for result in results_list:
                # Extract name and URL from result
                site_name = None
                site_url = None

                # Try to get title from metadata
                if "metadata" in result and isinstance(result["metadata"], dict):
                    meta = result["metadata"]
                    if "title" in meta:
                        site_name = meta["title"]
                    if "sourceURL" in meta:
                        site_url = meta["sourceURL"]

                # Also check if there's a direct url field
                if "url" in result:
                    site_url = result["url"]

                # Add to job_sites if we have both name and URL
                if site_name and site_url and site_url not in added_urls:
                    job_sites.append(JobPostingWebsite(url=site_url, name=site_name))
                    added_urls.add(site_url)

                # Look for job websites mentioned in the content
                content = ""
                if "content" in result:
                    content = result["content"]
                elif "markdown" in result:
                    content = result["markdown"]

                # Look for common job sites in the content
                for site_name, site_url in common_job_sites:
                    if site_name in content and site_url not in added_urls:
                        job_sites.append(
                            JobPostingWebsite(url=site_url, name=site_name)
                        )
                        added_urls.add(site_url)

    except Exception as e:
        print(f"Error using Firecrawl search: {str(e)}")

    # If no results found through Firecrawl, return some common job sites as fallback
    if not job_sites:
        # Customize the fallback list based on domain
        if domain.lower() in ["tech", "it", "software", "developer", "programming"]:
            fallback_sites = [
                ("Dice", "https://www.dice.com"),
                ("Stack Overflow", "https://stackoverflow.com/jobs"),
                ("GitHub Jobs", "https://jobs.github.com"),
                ("LinkedIn", "https://www.linkedin.com/jobs"),
                ("Indeed", "https://www.indeed.com"),
            ]
        elif domain.lower() in ["finance", "banking", "accounting"]:
            fallback_sites = [
                ("eFinancialCareers", "https://www.efinancialcareers.com"),
                ("LinkedIn", "https://www.linkedin.com/jobs"),
                ("Indeed", "https://www.indeed.com"),
                ("Robert Half", "https://www.roberthalf.com"),
                ("Glassdoor", "https://www.glassdoor.com"),
            ]
        elif domain.lower() in ["healthcare", "medical", "nursing"]:
            fallback_sites = [
                ("Health eCareers", "https://www.healthecareers.com"),
                ("LinkedIn", "https://www.linkedin.com/jobs"),
                ("Indeed", "https://www.indeed.com"),
                ("Hospital Careers", "https://www.hospitalcareers.com"),
                ("MedicalJobs", "https://www.medicaljobs.org"),
            ]
        else:
            # Generic fallback
            fallback_sites = [
                ("LinkedIn", "https://www.linkedin.com/jobs"),
                ("Indeed", "https://www.indeed.com"),
                ("Glassdoor", "https://www.glassdoor.com"),
                ("ZipRecruiter", "https://www.ziprecruiter.com"),
                ("Monster", "https://www.monster.com"),
            ]

        for site_name, site_url in fallback_sites:
            job_sites.append(JobPostingWebsite(url=site_url, name=site_name))

    return job_sites
