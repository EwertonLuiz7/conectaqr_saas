from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import Base, engine
from . import models
from .routes import auth, profile, qrcodes, analytics

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name, version="1.0.0", description="Plataforma SaaS de QR Code e conexão digital")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"] if settings.environment == "development" else [settings.base_url],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(qrcodes.router)
app.include_router(analytics.router)

ROOT = Path(__file__).resolve().parent.parent
FRONTEND = ROOT / "frontend"
app.mount("/assets", StaticFiles(directory=FRONTEND / "assets"), name="assets")

@app.get("/", include_in_schema=False)
def home():
    return FileResponse(FRONTEND / "index.html")

@app.get("/p/{slug}", include_in_schema=False)
def public_page(slug: str):
    return FileResponse(FRONTEND / "profile.html")

@app.get("/health")
def health():
    return {"status": "ok", "app": settings.app_name}
