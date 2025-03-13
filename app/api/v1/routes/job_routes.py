from fastapi import APIRouter
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
)
async def search_job_posting_websites(
    request: SearchJobPostingWebsitesRequest,
):
    """
    Search job posting websites based on search criteria.
    This endpoint triggers the browse_job_postings_agent.
    """
    return await search_job_posting_websites_service(request)
