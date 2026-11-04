from fastapi import FastAPI

app = FastAPI()

@app.get("/api/circles")
def hello():
    return [
        {"id": 1, "name": "ロンロック","category": "音楽"},
        {"id": 2, "name": "クラッシックギター部","gategory": "音楽"},
        {"id": 3, "name": "サッカー部","gategory": "スポーツ"}
    ]
