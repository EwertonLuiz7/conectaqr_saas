import secrets, re, io
from urllib.parse import quote
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse, StreamingResponse
from sqlalchemy.orm import Session
import qrcode
from ..database import get_db
from ..models import QRCode, ScanEvent, User, Profile
from ..schemas import QRCreateIn, QRUpdateIn
from ..dependencies import get_current_user
from ..config import settings

router = APIRouter(tags=["QR Codes"])
PLAN_LIMITS = {"free": 1, "professional": 3, "business": 10, "enterprise": 30}

def owned_qr(db, qr_id, user_id):
    qr = db.query(QRCode).filter(QRCode.id == qr_id, QRCode.user_id == user_id).first()
    if not qr:
        raise HTTPException(404, "QR Code não encontrado")
    return qr

def validate_destination(kind, value):
    if kind not in {"profile", "whatsapp", "url"}:
        raise HTTPException(422, "Tipo de destino inválido")
    if kind == "url" and value and not value.startswith(("https://", "http://")):
        raise HTTPException(422, "O endereço deve começar com http:// ou https://")
    if kind == "whatsapp" and value and not re.fullmatch(r"[0-9]{10,15}", re.sub(r"\D", "", value)):
        raise HTTPException(422, "WhatsApp deve conter DDI, DDD e número")
    return value

@router.get("/api/qrcodes")
def list_qrs(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.query(QRCode).filter(QRCode.user_id == user.id).order_by(QRCode.id.desc()).all()
    return [{"id": q.id, "code": q.code, "title": q.title, "destination_type": q.destination_type,
             "destination_value": q.destination_value, "is_active": q.is_active,
             "url": f"{settings.base_url}/q/{q.code}"} for q in rows]

@router.post("/api/qrcodes", status_code=201)
def create_qr(data: QRCreateIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    count = db.query(QRCode).filter(QRCode.user_id == user.id).count()
    limit = PLAN_LIMITS.get(user.plan, 1)
    if count >= limit:
        raise HTTPException(403, f"Limite do plano atingido ({limit} QR Code(s)).")
    value = validate_destination(data.destination_type, data.destination_value.strip())
    code = secrets.token_urlsafe(8).replace("-", "").replace("_", "")[:12]
    while db.query(QRCode).filter(QRCode.code == code).first():
        code = secrets.token_urlsafe(8)[:12]
    qr = QRCode(user_id=user.id, code=code, title=data.title.strip(),
                destination_type=data.destination_type, destination_value=value)
    db.add(qr)
    db.commit()
    db.refresh(qr)
    return {"id": qr.id, "code": qr.code, "title": qr.title, "url": f"{settings.base_url}/q/{qr.code}"}

@router.patch("/api/qrcodes/{qr_id}")
def update_qr(qr_id: int, data: QRUpdateIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    qr = owned_qr(db, qr_id, user.id)
    values = data.model_dump(exclude_unset=True)
    if "destination_type" in values or "destination_value" in values:
        kind = values.get("destination_type", qr.destination_type)
        value = values.get("destination_value", qr.destination_value)
        validate_destination(kind, value)
    for key, value in values.items():
        setattr(qr, key, value)
    db.commit()
    return {"message": "QR Code atualizado"}

@router.delete("/api/qrcodes/{qr_id}", status_code=204)
def delete_qr(qr_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    qr = owned_qr(db, qr_id, user.id)
    db.delete(qr)
    db.commit()
    return None

@router.get("/api/qrcodes/{qr_id}/image")
def qr_image(qr_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    qr = owned_qr(db, qr_id, user.id)
    img = qrcode.make(f"{settings.base_url}/q/{qr.code}")
    output = io.BytesIO()
    img.save(output, format="PNG")
    output.seek(0)
    return StreamingResponse(output, media_type="image/png")

@router.get("/q/{code}")
def redirect_qr(code: str, request: Request, db: Session = Depends(get_db)):
    qr = db.query(QRCode).filter(QRCode.code == code, QRCode.is_active == True).first()
    if not qr:
        raise HTTPException(404, "QR Code inexistente ou desativado")
    event = ScanEvent(qr_code_id=qr.id, user_agent=(request.headers.get("user-agent", "")[:500]))
    db.add(event)
    db.commit()
    if qr.destination_type == "whatsapp":
        number = re.sub(r"\D", "", qr.destination_value)
        return RedirectResponse(f"https://wa.me/{number}", status_code=302)
    if qr.destination_type == "url":
        return RedirectResponse(qr.destination_value, status_code=302)
    profile = db.query(Profile).filter(Profile.user_id == qr.user_id).first()
    if not profile or not profile.is_published:
        raise HTTPException(404, "Perfil público indisponível")
    return RedirectResponse(f"{settings.base_url}/p/{profile.slug}", status_code=302)
