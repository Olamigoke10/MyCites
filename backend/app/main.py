from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.citations import router as citations_router

app = FastAPI(title="MyCites API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(citations_router, prefix="/citations", tags=["citations"])
