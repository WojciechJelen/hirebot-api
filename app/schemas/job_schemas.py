from pydantic import BaseModel, Field
from typing import List, Optional


class JobPostingWebsite(BaseModel):
    url: str = Field(..., description="URL of the job posting website")
    has_job_postings: bool = Field(
        ..., description="Whether the website has job postings"
    )
    name: str = Field(..., description="Name of the website")
    description: str = Field(..., description="Description of the website")


class BrowseJobPostingsRequest(BaseModel):
    query: str = Field(..., description="Search query for job postings")
    location: Optional[str] = Field(None, description="Job location")


class BrowseJobPostingsResponse(BaseModel):
    results: List[JobPostingWebsite] = Field(
        ..., description="List of job posting websites found"
    )
    total_found: int = Field(..., description="Total number of job postings found")
