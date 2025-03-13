from pydantic import BaseModel, Field
from typing import List, Optional


class BrowseJobPostingsRequest(BaseModel):
    query: str = Field(..., description="Search query for job postings")
    location: Optional[str] = Field(None, description="Job location")
    experience_level: Optional[str] = Field(None, description="Experience level")
    remote_only: bool = Field(False, description="Filter for remote jobs only")


class JobPosting(BaseModel):
    title: str
    company: str
    location: str
    description: str
    url: str
    posted_date: Optional[str] = None
    salary_range: Optional[str] = None


class BrowseJobPostingsResponse(BaseModel):
    results: List[JobPosting]
    total_found: int
