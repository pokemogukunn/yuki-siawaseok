from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# InvidiousインスタンスのURL
BASE_URL = "https://inv.nadeko.net/api/v1"

# ホームページのルート
@app.route("/")
def index():
    return render_template("index.html")

# ホームのルート
@app.route("/home")
def home():
    return render_template("home.html")
    
# 動画ページのルート
@app.route("/watch")
def watch():
    video_id = request.args.get("v")
    if not video_id:
        return "動画IDが指定されていません", 400

    response = requests.get(f"{BASE_URL}/videos/{video_id}")
    if response.status_code == 200:
        video_data = response.json()
        
        # ストリームURLの取得
        stream_url = None
        for stream in video_data.get("adaptiveFormats", []):
            if "url" in stream:
                stream_url = stream["url"]
                break
        
        if not stream_url:
            return "ストリームURLが見つかりません", 404

        return render_template("video.html", video=video_data, stream_url=stream_url)
    else:
        return "動画が見つかりません", 404

# チャンネルページのルート
@app.route("/channel/<channel_id>")
def channel(channel_id):
    response = requests.get(f"{BASE_URL}/channels/{channel_id}")
    if response.status_code == 200:
        channel_data = response.json()
        return render_template("channel.html", channel=channel_data)
    else:
        return "チャンネルが見つかりません", 404

# 検索ページのルート
@app.route("/search")
def search():
    query = request.args.get("q")
    if not query:
        return "検索ワードが指定されていません", 400

    response = requests.get(f"{BASE_URL}/search", params={"q": query})
    if response.status_code == 200:
        search_results = response.json()
        return render_template("search.html", results=search_results, query=query)
    else:
        return "検索に失敗しました", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
