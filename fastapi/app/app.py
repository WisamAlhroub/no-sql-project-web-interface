from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .routers import search

# creates a fastapi application
app = FastAPI()

# mounting 'fastapi/app/static' folder to be easily accessed with jinja2
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# defining the template object which holdes the templates directory used by jinja2
templates = Jinja2Templates(directory="app/templates")

app.include_router(search.router)


@app.get("/", tags=['main-route'], response_class=HTMLResponse)  
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
