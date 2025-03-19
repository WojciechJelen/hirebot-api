import logging
from fastapi import HTTPException
from app.schemas.jobs_crawl_schemas import (
    JobCrawlRequest,
    JobCrawlResponse,
    JobPosting
)
from app.agents.jobs_crawl_agent import (
    jobs_crawl_agent,
    JobsCrawlDeps,
    JobPostingInfo
)

# Set up logger
logger = logging.getLogger(__name__)


async def jobs_crawl_service(
    request: JobCrawlRequest,
) -> JobCrawlResponse:
    """
    Service that handles crawling job postings from a specified website.

    Args:
        request: The JobCrawlRequest containing the website URL to crawl

    Returns:
        JobCrawlResponse containing the crawled job postings

    Raises:
        HTTPException: If an error occurs during the crawling process
    """
    try:
        logger.info(f"Processing job crawl request for website: {request.website_url}")

        # Create dependencies for the agent
        deps = JobsCrawlDeps(
            website_url=request.website_url
        )

        # Run the agent
        logger.info(f"Starting agent to crawl website: {request.website_url}")
        agent_result = await jobs_crawl_agent.run(
            "Crawl the provided job website and extract job postings", deps=deps
        )

        # Log the result
        logger.info(f"Agent result type: {type(agent_result)}")
        logger.info(f"Agent found {len(agent_result.data)} job postings")

        # Convert JobPostingInfo objects to JobPosting schema objects
        job_postings = []
        for job_info in agent_result.data:
            job_postings.append(
                JobPosting(
                    title=job_info.title,
                    company=job_info.company,
                    description=job_info.description,
                    url=job_info.url,
                    location=job_info.location,
                    salary_range=job_info.salary_range,
                    date_posted=job_info.date_posted
                )
            )

        # Create response
        response = JobCrawlResponse(
            results=job_postings,
            total_found=len(job_postings),
            website_url=request.website_url
        )

        logger.info(f"Completed job crawl with {response.total_found} results from {request.website_url}")
        return response

    except ValueError as e:
        # Handle validation errors
        logger.error(f"Validation error in job crawl: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except ConnectionError as e:
        # Handle connection errors
        logger.error(f"Connection error in job crawl: {str(e)}")
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")
    except Exception as e:
        # Handle unexpected errors
        logger.exception(f"Unexpected error in job crawl: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")