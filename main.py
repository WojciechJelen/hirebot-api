from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health():
    return {"message": "OK"}


@app.get("/")
def read_root():
    return {"message": "Hello World"}
