from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.analytics import router as analytics_router

app = FastAPI(title="AI Commerce Analytics Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analytics_router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
