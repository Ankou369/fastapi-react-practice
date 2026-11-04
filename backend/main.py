from fastapi import FastAPI, HTTPException

app = FastAPI()

circles = [
    {"id": 1, "name": "ロンロック","category": "音楽"},
    {"id": 2, "name": "クラッシックギター部","category": "音楽"},
    {"id": 3, "name": "サッカー部","category": "スポーツ"}
]

@app.get("/api/circles")
def get_circles():
    return circles

@app.get("/api/circles/{circle_id}")
def get_circle(circle_id: int):
    for circle in circles:
        if circle["id"] == circle_id:
            return circle

    raise HTTPException(status_code=404, detail="サークルが見つかりません")
