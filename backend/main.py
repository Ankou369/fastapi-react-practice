from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

class CircleCreate(BaseModel):
    name: str
    category: str
    description: str | None = None
    
app = FastAPI()

circles = [
    {"id": 1, "name": "ロンロック","category": "音楽"},
    {"id": 2, "name": "クラッシックギター部","category": "音楽"},
    {"id": 3, "name": "サッカー部","category": "スポーツ"}
]

@app.get("/api/circles")
def get_circles(keyword: str | None = None):

    if keyword is None:
        return circles
    
    result = []
    for circle in circles:
        if keyword in circle["name"]:
            result.append(circle)
    return result

@app.post("/api/circles", status_code=201)
def create_circle(circle: CircleCreate):
    new_circle = {"id":len(circles) + 1, 
                  "name":circle.name, 
                  "category":circle.category,
                  "description":circle.description,
                  }

    circles.append(new_circle)
    return new_circle

    

@app.get("/api/circles/{circle_id}")
def get_circle(circle_id: int):
    for circle in circles:
        if circle["id"] == circle_id:
            return circle

    raise HTTPException(status_code=404, detail="サークルが見つかりません")

