from sqlmodel import Session, func, select

from app.models import Tracking, TrackingReportPublic


def save(data: dict, session: Session):
    with session, session.begin():
        model = session.get(
            Tracking, (data.get("id"), data.get("metric_type"))
        )
        if model:
            for key in Tracking.model_fields.keys():
                if data.get(key) is not None and data.get(key) != getattr(
                    model, key
                ):
                    setattr(model, key, data.get(key))
            session.add(model)
        else:
            session.add(Tracking(**data))


def get(id: int, metric_type: str, session: Session):
    with session:
        return session.get(Tracking, (id, metric_type))


def report(session: Session) -> list[TrackingReportPublic]:
    with session:
        report = []
        raw_result = session.exec(
            select(
                Tracking.metric_type, Tracking.description, func.count()
            ).group_by(Tracking.metric_type, Tracking.description)
        ).all()
        total_page_access = 0
        for metric_type, description, total in raw_result:
            if metric_type == "page_access":
                total_page_access = total_page_access + total
        for metric_type, description, total in raw_result:
            if metric_type == "visibility":
                total = f"{round((total / total_page_access) * 100, 2)}%"
            total = str(total)
            report.append(
                TrackingReportPublic(
                    metric_type=metric_type,
                    description=description,
                    total=total,
                )
            )
        return report
