import re
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Profile
from ..schemas import RegisterIn, LoginIn, TokenOut, UserOut
from ..security import hash_password, verify_password, create_access_token
from ..dependencies import get_current_user

router = APIRouter(prefix="/api/auth", tags=["Autenticação"])

def make_slug(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:50] or "perfil"
    return slug

@router.post("/register", response_model=TokenOut, status_code=201)
def register(data: RegisterIn, db: Session = Depends(get_db)):
    email = data.email.strip().lower()
    if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
        raise HTTPException(422, "Informe um e-mail válido")
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(409, "Este e-mail já está cadastrado")
    user = User(name=data.name.strip(), email=email, password_hash=hash_password(data.password))
    db.add(user)
    db.flush()
    base = make_slug(data.name)
    slug = base
    n = 2
    while db.query(Profile).filter(Profile.slug == slug).first():
        slug = f"{base}-{n}"
        n += 1
    profile = Profile(user_id=user.id, slug=slug, display_name=data.name.strip())
    db.add(profile)
    db.commit()
    return {"access_token": create_access_token(user.id)}

@router.post("/login", response_model=TokenOut)
def login(data: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email.strip().lower()).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, "E-mail ou senha incorretos")
    if not user.is_active:
        raise HTTPException(403, "Conta desativada")
    return {"access_token": create_access_token(user.id)}

@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user
