from __future__ import annotations
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.orm import Mapped
from .database import Base


class ScanRecord(Base):
    __tablename__ = "scan_records"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # inputs
    symbol: Mapped[str] = Column(String, index=True)
    total_value: Mapped[float] = Column(Float)
    sleep_hours: Mapped[float] = Column(Float)
    exercise_minutes: Mapped[int] = Column(Integer)

    risk_per_trade_pct: Mapped[float] = Column(Float)
    stop_loss_pct: Mapped[float] = Column(Float, nullable=True)
    price: Mapped[float] = Column(Float, nullable=True)

    # computed / policy
    bankroll_mode: Mapped[str] = Column(String, default="percent")
    bankroll_pct: Mapped[float] = Column(Float)  # computed fraction of total_value
    bankroll_amount: Mapped[float] = Column(Float)

    health_factor: Mapped[float] = Column(Float)
    health_note: Mapped[str] = Column(String)

    risk_per_trade: Mapped[float] = Column(Float)
    stop_loss_used_pct: Mapped[float] = Column(Float)
    final_position_usd: Mapped[float] = Column(Float)
    entry_price: Mapped[float] = Column(Float, nullable=True)
    est_shares: Mapped[float] = Column(Float, nullable=True)
    stop_loss_per_share: Mapped[float] = Column(Float, nullable=True)
