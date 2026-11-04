from fastapi import FastAPI

app = FastAPI()

@app.get("/api/circles")
def get_circles():
    return [
        {"id": 1, "name": "ロンロック","category": "音楽"},
        {"id": 2, "name": "クラッシックギター部","category": "音楽"},
        {"id": 3, "name": "サッカー部","category": "スポーツ"}
    ]
