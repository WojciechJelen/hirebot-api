# from app.agents.browse_job_postings_agent import browse_job_postings_agent
from app.schemas.websites_search_schemas import (
    SearchJobPostingWebsitesRequest,
    SearchJobPostingWebsitesResponse,
)


async def search_job_posting_websites_service(
    request: SearchJobPostingWebsitesRequest,
) -> SearchJobPostingWebsitesResponse:
    # return await browse_job_postings_agent(request)

    # TODO: Implement the search job posting websites agent
    return SearchJobPostingWebsitesResponse(
        results=[],
        total_found=0,
    )
