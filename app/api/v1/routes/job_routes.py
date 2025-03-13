from fastapi import APIRouter, HTTPException, status
from app.schemas.websites_search_schemas import (
    SearchJobPostingWebsitesRequest,
    SearchJobPostingWebsitesResponse,
)
from app.services.job_posting_websites_search_service import (
    search_job_posting_websites_service,
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
