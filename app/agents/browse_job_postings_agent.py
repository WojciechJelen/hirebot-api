from pydantic_ai import Agent
from pydantic import BaseModel, Field
from firecrawl import FirecrawlApp
from dataclasses import dataclass
from urllib.parse import urlparse
import re


@dataclass
class BrowseJobPostingsWebstitesDeps:
    query: str
    location: str


@dataclass
class JobPostingWebsite:
    url: str
    has_job_postings: bool
    name: str
    description: str


app = FirecrawlApp(api_key="your_api_key")


class BrowseJobPostingsResponse(BaseModel):
    results: list[JobPostingWebsite] = Field(
        description="List of job posting websites found"
    )


job_postings_agent = Agent(
    "anthropic:claude-3-5-haiku-latest",
    deps_type=BrowseJobPostingsWebstitesDeps,
    result_type=BrowseJobPostingsResponse,
    system_prompt="Find job posting websites for the given domain.",
)


@job_postings_agent.tool
def find_websites_posting_jobs(specific_domain):
    query = f"{specific_domain} jobs"
    base_search_url = f"https://www.google.com/search?q={query}&start="
    num_pages = 5
    all_website_domains = set()

    for start in range(0, num_pages * 10, 10):
        search_url = base_search_url + str(start)
        app = FirecrawlApp()
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
            job_posting_websites.append(website_domain)

    return job_posting_websites


def browse_job_postings_agent() -> BrowseJobPostingsResponse:
    """
    Agent that searches for job postings based on given criteria.
    Currently returns dummy data for testing purposes.

    Args:
        request: The job search request parameters

    Returns:
        A BrowseJobPostingsResponse with dummy job postings
    """
    deps = BrowseJobPostingsWebstitesDeps(
        query="Python developer",
        location="San Francisco, CA",
    )
    result = job_postings_agent.run(deps)

    return BrowseJobPostingsResponse(
        results=result.results, total_found=result.total_found
    )
