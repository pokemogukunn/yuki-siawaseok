# main.py

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# ホームページ
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# /home に対応するページ
@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# 検索機能 (例: /search?q=キーワード)
@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, q: str):
    # Invidious API を利用して検索
    response = requests.get(f"https://inv.nadeko.net/api/v1/search?q={q}")
    results = response.json()
    return templates.TemplateResponse("search.html", {"request": request, "results": results})

# 動画ページ (例: /watch?v=VIDEO_ID)
@app.get("/watch", response_class=HTMLResponse)
async def watch(request: Request, v: str):
    # Invidious API を利用して動画情報を取得
    response = requests.get(f"https://inv.nadeko.net/api/v1/videos/{v}")
    video_data = response.json()
    return templates.TemplateResponse("video.html", {"request": request, "video_data": video_data})

# チャンネルページ (例: /channel/CHANNEL_ID)
@app.get("/channel/{channel_id}", response_class=HTMLResponse)
async def channel(request: Request, channel_id: str):
    # Invidious API を利用してチャンネル情報を取得
    response = requests.get(f"https://inv.nadeko.net/api/v1/channels/{channel_id}")
    channel_data = response.json()
    return templates.TemplateResponse("channel.html", {"request": request, "channel_data": channel_data})

