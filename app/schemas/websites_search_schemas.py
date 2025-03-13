from pydantic import BaseModel, Field, field_validator
from typing import Optional, List


class SearchJobPostingWebsitesRequest(BaseModel):
    query: str = Field(
        ...,
        description="Search query for job postings",
        min_length=1,
        max_length=200,
        examples=["Software Engineer", "Data Scientist", "Product Manager"],
    )
    location: Optional[str] = Field(
        None,
        description="Job location (city, state, country or 'Remote')",
        max_length=100,
        examples=["San Francisco, CA", "Remote", "New York", "London, UK"],
    )

    @field_validator("query")
    def query_not_empty(cls, v):
        if not v.strip():
            raise ValueError("query cannot be empty")
        return v.strip()

    @field_validator("location")
    def clean_location(cls, v):
        if v is None:
            return v
        return v.strip()

    class Config:
        schema_extra = {
            "example": {"query": "Software Engineer", "location": "San Francisco, CA"}
        }


class JobPostingWebsite(BaseModel):
    url: str = Field(
        ...,
        description="URL of the job posting website",
        examples=["https://www.linkedin.com", "https://www.indeed.com"],
    )
    name: str = Field(
        ...,
        description="Name of the website",
        examples=["LinkedIn", "Indeed", "Glassdoor"],
    )

    class Config:
        schema_extra = {
            "example": {"url": "https://www.linkedin.com", "name": "LinkedIn"}
        }


class SearchJobPostingWebsitesResponse(BaseModel):
    results: List[JobPostingWebsite] = Field(
        ..., description="List of job posting websites found"
    )
    total_found: int = Field(
        ..., description="Total number of job postings found", ge=0
    )

    class Config:
        schema_extra = {
            "example": {
                "results": [
                    {"url": "https://www.linkedin.com", "name": "LinkedIn"},
                    {"url": "https://www.indeed.com", "name": "Indeed"},
                ],
                "total_found": 2,
            }
        }
