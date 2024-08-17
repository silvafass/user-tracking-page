from sqlmodel import Session, col, select

from app.domains.models import User


def save(data: dict, session: Session):
    with session, session.begin():
        model = session.get(User, data.get("id"))
        if model:
            for key in User.model_fields.keys():
                if data.get(key) is not None and data.get(key) != getattr(
                    model, key
                ):
                    setattr(model, key, data.get(key))
            session.add(model)
        else:
            session.add(User(**data))


def get(id: int, session: Session):
    with session:
        return session.get(User, id)


def user_exists(
    id: int,
    session: Session,
) -> bool:
    with session:
        return session.exec(
            select(col(User.id).is_not(None)).where(User.id == id)
        ).first()
