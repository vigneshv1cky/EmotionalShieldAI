from __future__ import annotations
from datetime import datetime, timezone
from typing import Optional, List
from fastapi import FastAPI, Depends, HTTPException, Query

from .database import Base, engine, get_db
from .models import ScanRecord
from .schemas import (
    ScanInput,
    ScanOutput,
    HealthBlock,
    BankrollBlock,
    RiskBlock,
    PositionBlock,
    ScanRow,
)
from .utils import health_factor, compute_dynamic_bankroll, fetch_price_and_atr
from . import crud

from .config import (
    risk_per_trade_pct,
    stop_loss_pct,
)

app = FastAPI(title="Morning TradeFit Scan API", version="4.0.0")
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {
        "name": "Morning TradeFit Scan API",
        "version": "4.0.0",
        "endpoints": [
            "GET /health",
            "POST /scan",
            "GET /scans",
            "GET /scans/{scan_id}",
        ],
        "docs": "/docs",
    }


@app.get("/health")
def liveness():
    return {"status": "ok", "time": datetime.now(timezone.utc).isoformat()}


@app.post("/scan", response_model=ScanOutput)
def scan(payload: ScanInput, db=Depends(get_db)):
    # Health adjustment
    h_factor, h_note, h_alert = health_factor(
        payload.sleep_hours, payload.exercise_minutes
    )

    # Compute bankroll automatically
    bankroll_amt, bankroll_pct = compute_dynamic_bankroll(payload.total_value, h_factor)
    if bankroll_amt <= 0:
        raise HTTPException(
            status_code=400, detail="Computed bankroll is zero. Check inputs."
        )

    # Risk per trade in $
    # risk_per_trade_pct = 0.01
    risk_per_trade = bankroll_amt * risk_per_trade_pct

    # --- Stop-loss setup ---
    # stop_loss_pct = 0.01
    if stop_loss_pct <= 0:
        raise HTTPException(status_code=400, detail="stop_loss_pct must be > 0.")

    # --- Fetch price ---
    entry_price, _atr = fetch_price_and_atr(payload.trade_symbol, lookback=14)
    if entry_price is None:
        raise HTTPException(status_code=400, detail="No price data available.")

    # --- Position sizing (capped by bankroll) ---

    # StopLoss per share
    stop_loss_at = entry_price - (entry_price * stop_loss_pct)
    risk_per_share = entry_price * stop_loss_pct

    # --- Estimated shares ---
    normal_pos_size = risk_per_trade / risk_per_share

    # Persist
    rec = ScanRecord(
        symbol=payload.trade_symbol.upper(),
        total_value=payload.total_value,
        sleep_hours=payload.sleep_hours,
        exercise_minutes=payload.exercise_minutes,
        risk_per_trade_pct=risk_per_trade_pct,
        stop_loss_pct=stop_loss_pct,
        bankroll_mode="auto",
        bankroll_pct=bankroll_pct,
        bankroll_amount=bankroll_amt,
        health_factor=h_factor,
        health_note=h_note,
        health_alert=h_alert,
        risk_per_trade=risk_per_trade,
        stop_loss_used_pct=stop_loss_pct,
        entry_price=entry_price,
        normal_pos_size=normal_pos_size,
        stop_loss_at=stop_loss_at,
        risk_per_share=risk_per_share,
    )
    rec = crud.create_scan(db, rec)

    out = ScanOutput(
        record_id=rec.id,
        symbol=rec.symbol,
        timestamp_utc=rec.created_at.isoformat(),
        health=HealthBlock(
            sleep_hours=rec.sleep_hours,
            exercise_minutes=rec.exercise_minutes,
            factor=round(rec.health_factor, 3),
            note=rec.health_note,
            alert=rec.health_alert,
        ),
        bankroll=BankrollBlock(
            mode=rec.bankroll_mode,
            amount=round(rec.bankroll_amount, 2),
            pct_of_total=round(rec.bankroll_pct, 4),
        ),
        risk=RiskBlock(
            risk_per_trade_pct=round(rec.risk_per_trade_pct, 4),
            risk_per_trade_usd=round(rec.risk_per_trade, 2),
            stop_loss_pct=round(rec.stop_loss_used_pct, 4),
        ),
        position=PositionBlock(
            entry_price=round(rec.entry_price, 4) if rec.entry_price else None,
            normal_pos_size=(
                round(rec.normal_pos_size, 4) if rec.normal_pos_size else None
            ),
            stop_loss_at=(round(rec.stop_loss_at, 4) if rec.stop_loss_at else None),
            risk_per_share=round(rec.risk_per_share, 4) if rec.risk_per_share else None,
        ),
    )
    return out


@app.get("/scans", response_model=List[ScanRow])
def list_scans(
    limit: int = 50, offset: int = 0, symbol: Optional[str] = None, db=Depends(get_db)
):
    rows = crud.list_scans(db, limit=limit, offset=offset, symbol=symbol)
    return [
        ScanRow(
            id=r.id,
            created_at=r.created_at,
            symbol=r.symbol,
            risk_per_trade=round(r.risk_per_trade, 2),
            stop_loss_used_pct=round(r.stop_loss_used_pct, 4),
        )
        for r in rows
    ]


@app.get("/scans/{scan_id}")
def get_scan(scan_id: int, db=Depends(get_db)):
    r = crud.get_scan_by_id(db, scan_id)
    if not r:
        raise HTTPException(status_code=404, detail="Scan not found")
    return {
        "id": r.id,
        "created_at": r.created_at,
        "symbol": r.symbol,
        "inputs": {
            "total_value": r.total_value,
            "sleep_hours": r.sleep_hours,
            "exercise_minutes": r.exercise_minutes,
        },
        "computed": {
            "risk_per_trade_pct": r.risk_per_trade_pct,
            "stop_loss_pct": r.stop_loss_pct,
            "bankroll_mode": r.bankroll_mode,
            "bankroll_pct": r.bankroll_pct,
            "bankroll_amount": r.bankroll_amount,
            "health_factor": r.health_factor,
            "health_note": r.health_note,
            "health_alert": r.health_alert,
            "risk_per_trade": r.risk_per_trade,
            "stop_loss_used_pct": r.stop_loss_used_pct,
            "entry_price": round(r.entry_price, 4),
            "normal_pos_size": round(r.normal_pos_size, 4),
            "stop_loss_at": round(r.stop_loss_at, 4),
            "risk_per_share": round(r.risk_per_share, 4),
        },
    }
