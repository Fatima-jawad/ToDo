from app.db import SessionLocal
from app import models


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
