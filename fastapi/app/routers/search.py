from fastapi import APIRouter, status
from fastapi.params import Form
import requests
from starlette.requests import Request
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from requests import auth
from xml.etree import ElementTree as ET
import math


user = auth.HTTPDigestAuth("admin", "admin")
request_headers = {"Content-type": "application/xml"}


router = APIRouter(
    prefix="/search",
    tags=["search"]
)


def clean(element: str):
  """Custom Jinja2 filter"""
  xml_el = ET.fromstring(element.encode('utf-8'))
  return xml_el.text


def contains(element: str, substr):
  """Custom Jinja2 filter"""
  return element.__contains__(substr)


templates = Jinja2Templates(directory="app/templates")
templates.env.filters['clean'] = clean
templates.env.filters['contains'] = contains


@router.post("/send", tags=['search-post-route'])
async def accept(request: Request, query: str = Form(...)):
  return RedirectResponse(f"http://localhost:4000/search/{query}", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/{query}", tags=['search-get-route'])
async def search(request: Request, query: str, start: int = 1):
  global user
  global request_headers

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
        "show_document": False,
        "results": doc,
        "pages_section": pages_section
      }
    )
