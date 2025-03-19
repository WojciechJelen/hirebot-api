#!/usr/bin/env python

from app.agents.utils.firecrawl import app as firecrawl_app
import json
from dotenv import load_dotenv
import re

# Load environment variables from .env file
load_dotenv()


def search_it_job_websites():
    """
    Search for IT job websites using Firecrawl and print the results.
    """
    # Construct search query for IT jobs
    search_query = "best job websites for IT professionals"

    print(f"Searching for: {search_query}")

    try:
        # Use Firecrawl's search method to find job posting websites
        search_results = firecrawl_app.search(
            query=search_query,
            params={
                "limit": 5  # Limit to top 5 results
            },
        )

        # Print raw results type for debugging
        print("\n--- Raw Firecrawl Search Results ---\n")
        print(f"Response type: {type(search_results)}")

        # Handle list response
        if isinstance(search_results, list):
            results_list = search_results
            success = len(results_list) > 0
            print(f"Got a list response with {len(results_list)} items")
        # Handle dictionary response
        elif isinstance(search_results, dict):
            success = search_results.get("success", False)
            results_list = search_results.get("data", []) if success else []
            print(
                f"Got a dict response with success={success} and {len(results_list)} items"
            )
        else:
            print(f"Unexpected response type: {type(search_results)}")
            success = False
            results_list = []

        # Print results if we have any
        if success and len(results_list) > 0:
            print(f"\n--- Found {len(results_list)} Job Websites ---\n")

            # List to collect all job sites mentioned
            all_job_sites = set()

            # Common job sites to look for
            common_job_sites = [
                "Dice",
                "Indeed",
                "LinkedIn",
                "Monster",
                "CareerBuilder",
                "Glassdoor",
                "ZipRecruiter",
                "Stack Overflow",
                "GitHub Jobs",
                "AngelList",
                "Hired",
                "We Work Remotely",
                "Authentic Jobs",
                "SimplyHired",
                "Robert Half",
                "TechCareers",
                "ComputerJobs",
                "ITJobPro",
                "CyberCoders",
                "Ladders",
            ]

            # Extract and print useful information from search results
            for i, result in enumerate(results_list, 1):
                title = "No title"
                url = "No URL"
                description = "No description"

                # Try to extract title and URL from metadata
                if "metadata" in result and isinstance(result["metadata"], dict):
                    meta = result["metadata"]
                    if "title" in meta:
                        title = meta["title"]
                    if "sourceURL" in meta:
                        url = meta["sourceURL"]
                    if "description" in meta:
                        description = meta["description"]

                # Also check if there's a direct url field
                if "url" in result:
                    url = result["url"]

                print(f"#{i} - {title}")
                print(f"URL: {url}")
                print(f"Description: {description}")

                # Try to extract job sites mentioned in the content
                content = ""
                if "content" in result:
                    content = result["content"]
                elif "markdown" in result:
                    content = result["markdown"]

                # Find job sites mentioned in the content
                job_sites = []
                for site in common_job_sites:
                    if site in content:
                        job_sites.append(site)
                        all_job_sites.add(site)

                if job_sites:
                    print(f"Mentioned job sites: {', '.join(job_sites)}")

                print("-" * 60)

            # Print summary of all job sites found
            if all_job_sites:
                print("\n--- Summary of IT Job Websites Mentioned ---")
                print(", ".join(all_job_sites))

        else:
            print("No results found or search was unsuccessful.")

    except Exception as e:
        print(f"Error using Firecrawl search: {str(e)}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    search_it_job_websites()
