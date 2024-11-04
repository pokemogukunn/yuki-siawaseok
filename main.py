from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 複数の Invidious インスタンスをリスト化
API_INSTANCES = [
    "https://invidious.instance1.com/api/v1",
    "https://invidious.instance2.com/api/v1",
    "https://invidious.instance3.com/api/v1"
]

def fetch_data_from_invidious(endpoint: str):
    """Invidiousインスタンスのリストから順に試してデータを取得"""
    for api_base in API_INSTANCES:
        try:
            response = requests.get(f"{api_base}/{endpoint}", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            print(f"Failed to connect to {api_base}, trying next instance...")
    raise ConnectionError("すべてのInvidiousインスタンスで接続に失敗しました")

# チャンネル情報のエンドポイント
@app.get("/channel/{channel_id}", response_class=HTMLResponse)
async def channel(request: Request, channel_id: str):
    try:
        channel_data = fetch_data_from_invidious(f"channels/{channel_id}")
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=str(e))
    return templates.TemplateResponse("channel.html", {"request": request, "channel_data": channel_data})

# 動画情報のエンドポイント
@app.get("/watch", response_class=HTMLResponse)
async def watch(request: Request, v: str):
    try:
        video_data = fetch_data_from_invidious(f"videos/{v}")
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=str(e))
    return templates.TemplateResponse("video.html", {"request": request, "video_data": video_data})
