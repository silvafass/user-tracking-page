from typing import Literal

from fastapi import APIRouter

from app import tracking_crud
from app.dependencies import SessionDep
from app.models import (
    ListTrackingReportPublic,
    TrackingPublic,
)

router = APIRouter()


@router.get("/", response_model=TrackingPublic)
async def tracking(
    id: str,
    metric_type: Literal["page_access", "visibility"],
    description: str,
    session: SessionDep,
) -> TrackingPublic:
    tracking_crud.save(
        {
            "id": id,
            "metric_type": metric_type,
            "description": description,
        },
        session,
    )
    return TrackingPublic(
        id=id, metric_type=metric_type, description=description
    )


@router.get("/report", response_model=ListTrackingReportPublic)
async def report(session: SessionDep) -> ListTrackingReportPublic:
    report = tracking_crud.report(session)
    return ListTrackingReportPublic(data=report, count=len(report))
