from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import buildings, activities, organizations
from app import models  # noqa

app = FastAPI(
    title="Organizations directory API",
    version="1.0.0",
    description="REST API для справочника организаций, зданий и деятельностей",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(buildings.router)
app.include_router(activities.router)
app.include_router(organizations.router)


@app.get("/health", tags=["meta"])
def health() -> dict[str, str]:
    return {"status": "ok"}
