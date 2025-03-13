from pydantic import BaseModel, Field
from typing import Optional, List


class SearchJobPostingWebsitesRequest(BaseModel):
    query: str = Field(..., description="Search query for job postings")
    location: Optional[str] = Field(None, description="Job location")


class JobPostingWebsite(BaseModel):
    url: str = Field(..., description="URL of the job posting website")
    name: str = Field(..., description="Name of the website")


class SearchJobPostingWebsitesResponse(BaseModel):
    results: List[JobPostingWebsite] = Field(
        ..., description="List of job posting websites found"
    )
    total_found: int = Field(..., description="Total number of job postings found")
