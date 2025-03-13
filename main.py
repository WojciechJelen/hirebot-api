from fastapi import FastAPI
from app.api.v1.routes import job_routes, health_routes

app = FastAPI(title="HireBot API", description="AI agent API for job-related tasks")

# Include routers
app.include_router(health_routes.router)
app.include_router(job_routes.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
