from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    """
    Health check endpoint to verify the API is running.
    """
    return {"message": "OK"}


@router.get("/")
def read_root():
    """
    Root endpoint that returns a welcome message.
    """
    return {"message": "Hello World"}
