from fastapi import APIRouter
from app.schemas.job_schemas import BrowseJobPostingsRequest, BrowseJobPostingsResponse
from app.agents.browse_job_postings_agent import browse_job_postings_agent

router = APIRouter(tags=["jobs"])


@router.post("/browse-job-postings", response_model=BrowseJobPostingsResponse)
def browse_jobs(request: BrowseJobPostingsRequest):
    """
    Browse job postings based on search criteria.
    This endpoint triggers the browse_job_postings_agent.
    """
    results = browse_job_postings_agent(request)
    return results
