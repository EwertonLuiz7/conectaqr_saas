from datetime import datetime, timezone
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

def utcnow():
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    plan: Mapped[str] = mapped_column(String(30), default="free")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    qr_codes = relationship("QRCode", back_populates="user", cascade="all, delete-orphan")

class Profile(Base):
    __tablename__ = "profiles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, index=True)
    slug: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(120), default="")
    profession: Mapped[str] = mapped_column(String(160), default="")
    bio: Mapped[str] = mapped_column(Text, default="")
    whatsapp: Mapped[str] = mapped_column(String(30), default="")
    email_public: Mapped[str] = mapped_column(String(255), default="")
    website: Mapped[str] = mapped_column(String(500), default="")
    instagram: Mapped[str] = mapped_column(String(500), default="")
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)
    user = relationship("User", back_populates="profile")

class QRCode(Base):
    __tablename__ = "qr_codes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    code: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(120))
    destination_type: Mapped[str] = mapped_column(String(30), default="profile")
    destination_value: Mapped[str] = mapped_column(String(1000), default="")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    user = relationship("User", back_populates="qr_codes")
    scans = relationship("ScanEvent", back_populates="qr_code", cascade="all, delete-orphan")

class ScanEvent(Base):
    __tablename__ = "scan_events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    qr_code_id: Mapped[int] = mapped_column(ForeignKey("qr_codes.id"), index=True)
    scanned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    user_agent: Mapped[str] = mapped_column(String(500), default="")
    qr_code = relationship("QRCode", back_populates="scans")
