# app/main.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from .scraper import scrape_articles

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    articles = scrape_articles()
    return templates.TemplateResponse("index.html", {"request": request, "articles": articles})

@app.get("/articles", response_class=JSONResponse)
async def get_articles():
    articles = scrape_articles()
    return JSONResponse(content=articles)