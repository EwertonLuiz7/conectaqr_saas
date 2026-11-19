from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from ..models import User, QRCode, ScanEvent
from ..dependencies import get_current_user

router = APIRouter(prefix="/api/analytics", tags=["Estatísticas"])

@router.get("/summary")
def summary(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    qrs = db.query(QRCode).filter(QRCode.user_id == user.id).all()
    qr_ids = [q.id for q in qrs]
    total_scans = db.query(ScanEvent).filter(ScanEvent.qr_code_id.in_(qr_ids)).count() if qr_ids else 0
    since = datetime.now(timezone.utc) - timedelta(days=30)
    recent = db.query(ScanEvent).filter(ScanEvent.qr_code_id.in_(qr_ids), ScanEvent.scanned_at >= since).count() if qr_ids else 0
    per_qr = []
    for qr in qrs:
        count = db.query(ScanEvent).filter(ScanEvent.qr_code_id == qr.id).count()
        per_qr.append({"title": qr.title, "scans": count})
    return {"total_qrs": len(qrs), "total_scans": total_scans, "scans_last_30_days": recent, "by_qr": per_qr}
