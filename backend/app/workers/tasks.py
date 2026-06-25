from app.workers.celery_app import celery
from app.core.database import SessionLocal
from app.db.models import Request
from app.services.orchestrator import run_pipeline
from app.api.metrics import counter


@celery.task
def process_request(
    request_id
):

    db = SessionLocal()

    req = (
        db.query(Request)
        .filter(
            Request.id == request_id
        )
        .first()
    )

    req.status = "PROCESSING"
    req.current_agent = "router"
    db.commit()

    result = run_pipeline(
        req
    )

    req.output = result

    req.route = (
        result[
            "route"
        ]
    )

    counter[req.route] += 1

    req.status = (
        "COMPLETED"
    )

    db.commit()

    db.close()