from pydantic_ai import Agent, RunContext
from pydantic_ai.models.anthropic import AnthropicModel
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from app.agents.utils.firecrawl import app as firecrawl_app
import os
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables from .env file
load_dotenv()


class JobPostingInfo(BaseModel):
    title: str
    company: Optional[str] = None
    description: str
    url: str
    location: Optional[str] = None
    salary_range: Optional[str] = None
    date_posted: Optional[str] = None


@dataclass
class JobsCrawlDeps:
    website_url: str


# Get Anthropic API key from environment variables
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
if not anthropic_api_key:
    raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

model = AnthropicModel("claude-3-5-sonnet-latest", api_key=anthropic_api_key)

# Define the agent with proper deps_type and result_type
jobs_crawl_agent = Agent(
    model,
    deps_type=JobsCrawlDeps,
    result_type=List[JobPostingInfo],
    system_prompt="You are a helpful assistant that can extract job postings from job websites.",
)


@jobs_crawl_agent.tool
def crawl_job_website(
    ctx: RunContext[JobsCrawlDeps],
) -> List[JobPostingInfo]:
    """
    Tool that crawls a job posting website and extracts job information.

    Args:
        ctx: The run context containing the dependencies (website_url)

    Returns:
        A list of JobPostingInfo objects
    """
    website_url = ctx.deps.website_url
    job_postings = []

    print(f"Crawling website: {website_url}")

    try:
        # Use Firecrawl to fetch website content
        crawl_result = firecrawl_app.crawl(
            url=website_url,
            params={
                "wait_for": "networkidle0",  # Wait until network is idle
                "timeout": 30000,  # 30 seconds timeout
            },
        )

        # Extract content from the crawl result
        content = ""
        if isinstance(crawl_result, dict):
            if "content" in crawl_result:
                content = crawl_result["content"]
            elif "html" in crawl_result:
                content = crawl_result["html"]
            elif "text" in crawl_result:
                content = crawl_result["text"]
            elif "markdown" in crawl_result:
                content = crawl_result["markdown"]

        if not content:
            print(f"No content found in crawl result for {website_url}")
            return []

        # Use Claude to parse job postings from content
        parse_result = model.generate(
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI expert at extracting job postings from websites. Your task is to extract job posting information from the provided website content.",
                },
                {
                    "role": "user",
                    "content": f"""
                    I need you to extract job postings from this job website content. 
                    
                    Please identify each distinct job posting and extract the following information:
                    - Job title
                    - Company name (if available)
                    - Job description (a brief summary)
                    - Location (if available)
                    - Salary information (if available)
                    - Date posted (if available)
                    
                    For each job posting, provide the information in a structured JSON format.
                    
                    Here's the website content:
                    ```
                    {content[:50000]}  # Limit content to avoid token limits
                    ```
                    
                    Format your response as a JSON array of job postings. Each job posting should include title, company, description, location, salary_range, and date_posted fields.
                    """,
                },
            ],
            max_tokens=4000,
            temperature=0,
            response_format={"type": "json_object"},
        )

        # Extract and process job postings from the model's response
        if parse_result and hasattr(parse_result, "content"):
            try:
                import json
                parsed_data = json.loads(parse_result.content)
                
                if "job_postings" in parsed_data and isinstance(parsed_data["job_postings"], list):
                    for job_data in parsed_data["job_postings"]:
                        # Create JobPostingInfo objects from the extracted data
                        job_postings.append(
                            JobPostingInfo(
                                title=job_data.get("title", "Unknown Title"),
                                company=job_data.get("company"),
                                description=job_data.get("description", "No description available"),
                                url=website_url,  # Use the main website URL since we don't have specific URLs
                                location=job_data.get("location"),
                                salary_range=job_data.get("salary_range"),
                                date_posted=job_data.get("date_posted"),
                            )
                        )
            except Exception as e:
                print(f"Error parsing job postings from model response: {str(e)}")

    except Exception as e:
        print(f"Error crawling website {website_url}: {str(e)}")

    return job_postings