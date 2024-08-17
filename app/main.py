import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel
from starlette.middleware.sessions import SessionMiddleware

from app.dependencies import SessionUserDep, engine
from app.settings import settings

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def user_profile(user: SessionUserDep, request: Request):
    return templates.TemplateResponse(
        request=request, name="user_profile.html", context={"user": user}
    )


@app.get("/tracking_report", response_class=HTMLResponse)
async def tracking_report(request: Request):
    return templates.TemplateResponse(
        request=request, name="tracking_report.html"
    )
