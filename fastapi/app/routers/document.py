from fastapi import APIRouter
import requests, xmljson
from starlette.responses import JSONResponse
from starlette.requests import Request
from fastapi.templating import Jinja2Templates
import xml.etree.ElementTree as ET
from requests import auth


user = auth.HTTPDigestAuth("admin", "admin")
request_headers = {"Content-type": "application/xml"}


router = APIRouter(
    prefix="/document",
    tags=["document"]
)


templates = Jinja2Templates(directory="app/templates")


@router.get("/show", tags=['document-get-route'])
async def document(request: Request, href: str):
  global user
  global request_headers
  
  resp = requests.get(
    f"http://localhost:8040{href}",
    auth=user, 
    headers=request_headers
  )

  doc = xmljson.parker.data(ET.fromstring(resp.text))
  
  return templates.TemplateResponse(
    "document.html", 
    {
      "request": request,
      "show_document": True,
      "show_facets": False,
      "doc": doc
    }
  )


@router.get("/got", tags=['document-get-route'])
async def document(request: Request, href: str):
  global user
  global request_headers
  
  resp = requests.get(
    f"http://localhost:8040{href}",
    auth=user, 
    headers=request_headers
  )

  doc = xmljson.parker.data(ET.fromstring(resp.text))
  
  return JSONResponse(doc)