from fastapi import APIRouter
import requests
from starlette.requests import Request
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from requests import auth
import math


router = APIRouter(
    prefix="/search",
    tags=["search"]
)


templates = Jinja2Templates(directory="app/templates")


@router.get("/{query}", tags=['search-route'], response_class=HTMLResponse)
async def search(request: Request, query: str, start: int = 1):
  user = auth.HTTPDigestAuth("admin", "admin")
  request_headers = {"Content-type": "application/xml"}

  resp = requests.get(
    f"http://localhost:8040/v1/search?q={query}&start={start}&options=mysearch&format=json",
    auth=user, 
    headers=request_headers
  )

  if resp.status_code == 404:
    return templates.TemplateResponse("404.html", {"request": request, "not_found": True})
  elif resp.status_code == 200:
    doc = resp.json()
    if start % doc['page-length']:
      pages_section = math.floor(doc['start'] / doc['page-length']) * doc['page-length']
    else:
      pages_section = math.floor((doc['start']-1) / doc['page-length']) * doc['page-length']

    return templates.TemplateResponse(
      "index.html", 
      {
        "request": request, 
        "show_facets": True,
        "results": doc,
        "pages_section": pages_section
      }
    )