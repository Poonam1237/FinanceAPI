from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import getdb
from models.financialmodel import Records

router = APIRouter(prefix="/dashboard", tags=["Dashboard"]) 

@router.get("/summary")
def dashboard_summary(db:Session=Depends(getdb)):

    total_income = db.query(func.sum(Records.amount)).filter(Records.type == "income").scalar()
    total_expense = db.query(func.sum(Records.amount)).filter(Records.type == "expense").scalar()

    income = total_income or 0
    expense = total_expense or 0

    return {
        "total_income": income,
        "total_expense": expense,
        "balance": income - expense
    }

@router.get("/monthly-trends")
def monthly_trends(db: Session = Depends(getdb)):

    data = db.query(func.month(Records.date).label("month"),func.sum(Records.amount).label("total_amount")).group_by(func.month(Records.date)).all()

    result = []

    for row in data:
        result.append({
            "month": row.month,
            "total_amount": row.total_amount
        })

    return result
