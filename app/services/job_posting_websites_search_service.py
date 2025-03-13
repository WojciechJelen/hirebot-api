# from app.agents.browse_job_postings_agent import browse_job_postings_agent
import logging
from fastapi import HTTPException
from app.schemas.websites_search_schemas import (
    SearchJobPostingWebsitesRequest,
    SearchJobPostingWebsitesResponse,
    JobPostingWebsite,
)
from app.agents.search_job_posting_websites import (
    search_job_posting_websites_agent,
    SearchJobPostingWebsitesDeps,
)

# Set up logger
logger = logging.getLogger(__name__)


async def search_job_posting_websites_service(
    request: SearchJobPostingWebsitesRequest,
) -> SearchJobPostingWebsitesResponse:
    """
    Service that handles searching job posting websites based on search criteria.

    Args:
        request: The SearchJobPostingWebsitesRequest containing search parameters

    Returns:
        SearchJobPostingWebsitesResponse containing the search results

    Raises:
        HTTPException: If an error occurs during the search process
    """
    try:
        logger.info(
            f"Processing job posting websites search request: query={request.query}, location={request.location}"
        )

        # Input validation (beyond what Pydantic already does)
        if not request.query.strip():
            logger.error("Empty search query provided")
            raise ValueError("Search query cannot be empty")

        # Create dependencies for the agent
        deps = SearchJobPostingWebsitesDeps(
            domain=request.query, location=request.location
        )

        # Run the agent
        agent_result = await search_job_posting_websites_agent.run(
            "Suggest job posting websites for the given domain", deps=deps
        )

        # Log the result to understand its structure
        logger.info(f"Agent result type: {type(agent_result)}")
        logger.info(f"Agent result content: {agent_result.data}")

        # Get websites list directly from the agent result
        websites_list = agent_result.data
        logger.info(f"Found {len(websites_list)} websites")

        # Convert to appropriate response format
        response = SearchJobPostingWebsitesResponse(
            results=websites_list,
            total_found=len(websites_list),
        )

        logger.info(
            f"Completed job posting websites search with {response.total_found} results"
        )
        return response

    except ValueError as e:
        # Handle validation errors
        logger.error(f"Validation error in job posting websites search: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except ConnectionError as e:
        # Handle connection errors (for when we implement external service calls)
        logger.error(f"Connection error in job posting websites search: {str(e)}")
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")
    except Exception as e:
        # Handle unexpected errors
        logger.exception(f"Unexpected error in job posting websites search: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
