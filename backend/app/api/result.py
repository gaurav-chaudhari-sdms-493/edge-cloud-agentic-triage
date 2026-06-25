from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.result_service import get_result

router = APIRouter()


@router.get("/result/{request_id}")
def result(
    request_id: int,
    db: Session = Depends(get_db)
):
    req = get_result(db, request_id)
    return {
        "route": req.route,
        "output": req.output
    }