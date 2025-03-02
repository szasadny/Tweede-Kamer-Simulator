from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db

# Add dependencies here that can be reused across the application
