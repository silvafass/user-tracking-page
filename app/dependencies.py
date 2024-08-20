import logging
from typing import Annotated, Any, Generator

import httpx
from fastapi import Depends, Request
from sqlalchemy import Engine
from sqlmodel import Session, create_engine

from app import user_crud
from app.models import User
from app.settings import settings

logger = logging.getLogger(__name__)

engine = create_engine(
    str(settings.postgress_db_connection_uri), echo=settings.db_echo
)


def db_engine() -> Engine:
    return engine


EngineDB = Annotated[Engine, Depends(db_engine)]


def db_session(engine: EngineDB) -> Generator[Session, Any, Any]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(db_session)]


def get_session_userid(request: Request, session: SessionDep) -> str:
    session_userid = request.session.get("userid")
    valid_user_stored_session = (
        "userid" in request.session
        and user_crud.user_exists(session_userid, session=session)
    )
    if not valid_user_stored_session:
        random_user_data = (
            httpx.get("https://random-data-api.com/api/v2/users")
            .raise_for_status()
            .json()
        )
        randon_userid = random_user_data.get("id")
        if randon_userid:
            request.session["userid"] = randon_userid
            user_crud.save(
                {
                    **random_user_data,
                    "employment_title": random_user_data.get(
                        "employment", {}
                    ).get("title"),
                    "employment_key_skill": random_user_data.get(
                        "employment", {}
                    ).get("key_skill"),
                },
                session=session,
            )

    return request.session.get("userid")


SessionUserIdDep = Annotated[str, Depends(get_session_userid)]


def get_session_user(userid: SessionUserIdDep, session: SessionDep) -> User:
    return user_crud.get(userid, session=session)


SessionUserDep = Annotated[User, Depends(get_session_user)]
