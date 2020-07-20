from tortoise.contrib.fastapi import register_tortoise
from models.models import Links, Link
from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from datetime import datetime, timedelta
from utils.db_utils import get_random_string
from utils.text_utils import is_url


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/stat")
async def get_stats(request: Request):
    links = await Links.all().limit(100).order_by("-visits")
    return templates.TemplateResponse("stats.html", {"request": request,
                                                     "links": links})


@app.get("/{key}")
async def get_key(request: Request, key):
    link = await Links.get_or_none(id=key)
    if link and (not link.lifetime or link.lifetime > datetime.now()):
        link.visits += 1
        await link.save()
        return RedirectResponse(link.url)
    else:
        return templates.TemplateResponse("expired.html", {"request": request})


@app.post("/create")
async def create(request: Request, url: str = Form(...), lifetime: str = Form(...)):
    #  Validation
    if not is_url(url):
        return {"error": "Invalid url!"}

    #  Generate ID
    code_length = 5
    code = get_random_string(code_length)
    while await Links.get_or_none(id=code):
        code = get_random_string(code_length)
        code_length += 1
        if code_length > 20:
            return {"error": "Can't generate code"}

    #  Set lifetime variable
    db_lifetime = None
    if lifetime.isdigit() and int(lifetime) > 0:
        db_lifetime = datetime.now() + timedelta(minutes=int(lifetime))

    link = Links(id=code, url=url, lifetime=db_lifetime)
    await link.save()
    return await Link.from_tortoise_orm(link)


register_tortoise(
    app,
    db_url="postgres://evo_user:evo_password@db/urlshortener",
    modules={"models": ["models.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)