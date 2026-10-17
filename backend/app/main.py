from fastapi import FastAPI

app = FastAPI(title="SentinelMesh API")


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "SentinelMesh"
    }
