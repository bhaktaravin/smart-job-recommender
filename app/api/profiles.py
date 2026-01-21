import os
import shutil

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.resume_parser import extract_text_from_pdf

# ✅ Define the router
router = APIRouter()


@router.post("/upload_resume/{user_id}")
def upload_resume(
    user_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)
):
    from app.models.user_profile import UserProfile

    # Save PDF temporarily
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text
    text = extract_text_from_pdf(file_path)

    # Update user profile
    user = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user:
        return {"error": "User not found"}

    user.text = text
    db.commit()
    db.refresh(user)

    return {"message": "Resume uploaded and parsed", "text_snippet": text[:200]}
