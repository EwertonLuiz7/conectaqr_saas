from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Profile, User
from ..schemas import ProfileIn, ProfileOut
from ..dependencies import get_current_user

router = APIRouter(tags=["Perfis"])

@router.get("/api/profile/me", response_model=ProfileOut)
def get_my_profile(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.user_id == user.id).first()
    if not profile:
        raise HTTPException(404, "Perfil não encontrado")
    return profile

@router.put("/api/profile/me", response_model=ProfileOut)
def update_my_profile(data: ProfileIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.user_id == user.id).first()
    if not profile:
        raise HTTPException(404, "Perfil não encontrado")
    values = data.model_dump()
    values["whatsapp"] = "".join(ch for ch in values["whatsapp"] if ch.isdigit())
    for key, value in values.items():
        setattr(profile, key, value)
    db.commit()
    db.refresh(profile)
    return profile

@router.get("/api/public/profile/{slug}")
def public_profile(slug: str, db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.slug == slug, Profile.is_published == True).first()
    if not profile:
        raise HTTPException(404, "Perfil não encontrado")
    return {
        "display_name": profile.display_name, "profession": profile.profession,
        "bio": profile.bio, "whatsapp": profile.whatsapp,
        "email_public": profile.email_public, "website": profile.website,
        "instagram": profile.instagram, "slug": profile.slug
    }
