import asyncio
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.agents.jobs_crawl_agent import jobs_crawl_agent, JobsCrawlDeps


async def test_jobs_crawl_agent():
    """
    Test function for the jobs_crawl_agent.
    This function runs the agent with a test URL and prints the results.
    """
    print("Testing jobs_crawl_agent...")
    
    # Test URL - LinkedIn jobs page for software engineers
    test_url = "https://www.linkedin.com/jobs/search?keywords=software%20engineer"
    
    # Create agent dependencies
    deps = JobsCrawlDeps(website_url=test_url)
    
    try:
        # Run the agent
        print(f"Crawling: {test_url}")
        result = await jobs_crawl_agent.run(
            "Extract job postings from this website", deps=deps
        )
        
        # Print results
        print(f"\nFound {len(result.data)} job postings:")
        for i, job in enumerate(result.data, 1):
            print(f"\nJob {i}:")
            print(f"Title: {job.title}")
            print(f"Company: {job.company or 'N/A'}")
            print(f"Location: {job.location or 'N/A'}")
            print(f"Salary: {job.salary_range or 'N/A'}")
            print(f"Date Posted: {job.date_posted or 'N/A'}")
            print(f"Description: {job.description[:100]}...")
            
        print("\nTest completed successfully!")
        
    except Exception as e:
        print(f"Error testing jobs_crawl_agent: {str(e)}")


if __name__ == "__main__":
    asyncio.run(test_jobs_crawl_agent())