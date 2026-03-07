from fastapi import FastAPI

from fast_notes.api import notes
from fast_notes.config import settings
from fast_notes.logger import setup_logging
from fast_notes.db.schema import Base, engine

setup_logging()
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

app.include_router(notes.router, prefix="/api/v1")
