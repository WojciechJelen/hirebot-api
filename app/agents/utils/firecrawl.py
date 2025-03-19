import os
from firecrawl import FirecrawlApp
from dotenv import load_dotenv

load_dotenv()


firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")
if not firecrawl_api_key:
    raise ValueError("FIRECRAWL_API_KEY not found in environment variables")

app = FirecrawlApp(api_key=firecrawl_api_key)
