#!/usr/bin/env python

from app.agents.search_job_posting_websites import (
    search_job_posting_websites_agent,
    SearchJobPostingWebsitesDeps,
)
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def test_job_search_agent():
    """
    Test the search_job_posting_websites_agent with different domains
    """
    # Test domains
    domains = ["software developer", "IT", "data science", "healthcare", "finance"]

    for domain in domains:
        print(f"\n=== Testing job search for domain: {domain} ===\n")

        # Run the agent
        result = search_job_posting_websites_agent.run_sync(
            "Find me the best job websites for my industry",
            deps=SearchJobPostingWebsitesDeps(domain=domain),
        )

        # Print results
        print(f"Found {len(result.data)} job websites:")
        for i, job_site in enumerate(result.data, 1):
            print(f"{i}. {job_site.name} - {job_site.url}")


if __name__ == "__main__":
    test_job_search_agent()
