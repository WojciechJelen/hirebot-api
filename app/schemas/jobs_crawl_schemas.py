from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
import re


class JobCrawlRequest(BaseModel):
    website_url: str = Field(
        ...,
        description="URL of the job posting website to crawl",
        min_length=1,
        max_length=500,
        examples=["https://www.linkedin.com/jobs/search?keywords=software+engineer"],
    )

    @field_validator("website_url")
    def validate_website_url(cls, v):
        if not v.strip():
            raise ValueError("website_url cannot be empty")
        
        # Simple URL validation
        url_pattern = re.compile(
            r'^(https?://)?(www\.)?'  # http:// or https:// + www. (optional)
            r'[a-zA-Z0-9][\w\-\.]+\.[a-zA-Z]{2,}'  # domain
            r'(/[a-zA-Z0-9\-\._~:/?#[\]@!$&\'\(\)*+,;=]*)?$'  # path, query, etc.
        )
        
        if not url_pattern.match(v):
            raise ValueError("Invalid URL format")
        
        # Ensure URL has http:// or https:// prefix
        if not v.startswith(('http://', 'https://')):
            v = f"https://{v}"
            
        return v

    class Config:
        schema_extra = {
            "example": {"website_url": "https://www.linkedin.com/jobs/search?keywords=software+engineer"}
        }


class JobPosting(BaseModel):
    title: str = Field(
        ...,
        description="Job title",
        examples=["Senior Software Engineer", "Data Scientist", "Product Manager"],
    )
    company: Optional[str] = Field(
        None,
        description="Company name",
        examples=["Google", "Microsoft", "Amazon"],
    )
    description: str = Field(
        ...,
        description="Job description",
        examples=["We are looking for a senior software engineer with 5+ years of experience..."],
    )
    url: str = Field(
        ...,
        description="Job posting URL",
        examples=["https://www.linkedin.com/jobs/view/12345678"],
    )
    location: Optional[str] = Field(
        None,
        description="Job location",
        examples=["San Francisco, CA", "Remote", "New York, NY"],
    )
    salary_range: Optional[str] = Field(
        None,
        description="Salary range",
        examples=["$100,000 - $150,000", "$80k - $120k per year"],
    )
    date_posted: Optional[str] = Field(
        None,
        description="Date when the job was posted",
        examples=["2023-01-15", "3 days ago", "Yesterday"],
    )

    class Config:
        schema_extra = {
            "example": {
                "title": "Senior Software Engineer",
                "company": "Google",
                "description": "We are looking for a senior software engineer with 5+ years of experience...",
                "url": "https://www.linkedin.com/jobs/view/12345678",
                "location": "San Francisco, CA",
                "salary_range": "$150,000 - $200,000",
                "date_posted": "2023-01-15",
            }
        }


class JobCrawlResponse(BaseModel):
    results: List[JobPosting] = Field(
        ..., description="List of job postings found"
    )
    total_found: int = Field(
        ..., description="Total number of job postings found", ge=0
    )
    website_url: str = Field(
        ..., description="URL of the website that was crawled"
    )

    class Config:
        schema_extra = {
            "example": {
                "results": [
                    {
                        "title": "Senior Software Engineer",
                        "company": "Google",
                        "description": "We are looking for a senior software engineer with 5+ years of experience...",
                        "url": "https://www.linkedin.com/jobs/view/12345678",
                        "location": "San Francisco, CA",
                        "salary_range": "$150,000 - $200,000",
                        "date_posted": "2023-01-15",
                    },
                    {
                        "title": "Full Stack Developer",
                        "company": "Microsoft",
                        "description": "Join our team to build cutting-edge web applications...",
                        "url": "https://www.linkedin.com/jobs/view/87654321",
                        "location": "Remote",
                        "salary_range": "$120,000 - $180,000",
                        "date_posted": "2023-01-10",
                    }
                ],
                "total_found": 2,
                "website_url": "https://www.linkedin.com/jobs/search?keywords=software+engineer",
            }
        }