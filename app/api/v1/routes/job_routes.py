from fastapi import APIRouter, HTTPException, status
from app.schemas.websites_search_schemas import (
    SearchJobPostingWebsitesRequest,
    SearchJobPostingWebsitesResponse,
)
from app.schemas.jobs_crawl_schemas import (
    JobCrawlRequest,
    JobCrawlResponse,
)
from app.services.job_posting_websites_search_service import (
    search_job_posting_websites_service,
)
from app.services.jobs_crawl_service import (
    jobs_crawl_service,
)

router = APIRouter(tags=["jobs"])


@router.post(
    "/search-job-posting-websites",
    response_model=SearchJobPostingWebsitesResponse,
    status_code=status.HTTP_200_OK,
    summary="Search job posting websites",
    response_description="A list of job posting websites matching the search criteria",
)
async def search_job_posting_websites(
    request: SearchJobPostingWebsitesRequest,
):
    """
    Search job posting websites based on search criteria.

    This endpoint allows users to search for job posting websites
    using specific search terms and optional location filters.

    Parameters:
    - **query**: Required search term (e.g., "Software Engineer", "Data Science")
    - **location**: Optional location filter (e.g., "San Francisco, CA", "Remote")

    Returns:
    - List of job posting websites matching the criteria
    - Total count of results found

    Note: Currently returns empty results as the underlying agent implementation
    is pending. Future versions will connect to a full browsing-capable AI agent.
    """
    return await search_job_posting_websites_service(request)


@router.post(
    "/crawl-job-website",
    response_model=JobCrawlResponse,
    status_code=status.HTTP_200_OK,
    summary="Crawl job postings from a website",
    response_description="A list of job postings extracted from the provided website",
)
async def crawl_job_website(
    request: JobCrawlRequest,
):
    """
    Crawl and extract job postings from a specified job posting website.
    
    This endpoint accepts a job posting website URL and uses an AI agent to crawl
    the website and extract detailed information about each job posting found.
    
    Parameters:
    - **website_url**: Required URL of the job posting website to crawl
      (e.g., "https://www.linkedin.com/jobs/search?keywords=software+engineer")
    
    Returns:
    - List of job postings found on the website, including details like:
      - Job title
      - Company name (if available)
      - Job description
      - Location (if available)
      - Salary range (if available)
      - Date posted (if available)
    - Total count of job postings found
    - The website URL that was crawled
    """
    return await jobs_crawl_service(request)
