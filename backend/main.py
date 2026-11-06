from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import sqlite3

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
    conn = get_db()
    if keyword is None:
        rows = conn.execute("SELECT * FROM circles").fetchall()
    else:
        rows = conn.execute("SELECT * FROM circles WHERE name LIKE ?", ("%" + keyword + "%",)).fetchall()
    conn.close()
    result = []
    for row in rows:
        result.append(dict(row))
    return result
    
# @app.get("/api/circles")
# def get_circles(keyword: str | None = None):

#     if keyword is None:
#         return circles
    
#     result = []
#     for circle in circles:
#         if keyword in circle["name"]:
#             result.append(circle)
#     return result

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

@app.delete("/api/circles/{circle_id}")
def delete_circle(circle_id: int):
    for circle in circles:
        if circle["id"] == circle_id:
            circles.remove(circle)
            return {"message": "削除しました"}

    raise HTTPException(status_code=404, detail="サークルが見つかりません")

@app.put("/api/circles/{circle_id}")
def update_circle(circle_id: int, circle: CircleCreate):
    for c in circles:
        if c["id"] == circle_id:
            c["name"] = circle.name
            c["category"] = circle.category
            c["description"] = circle.description
            return c

    raise HTTPException(status_code=404, detail="サークルが見つかりません")

def init_db():
    conn = sqlite3.connect("circles.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS circles(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT
            )
        """)

    count = conn.execute("SELECT COUNT(*) FROM circles").fetchone()[0]
    if count == 0:
        conn.execute("INSERT INTO circles (name, category) VALUES (?, ?)", ("ロンロック", "音楽"))
        conn.execute("INSERT INTO circles (name, category) VALUES (?, ?)", ("クラッシックギター部", "音楽"))
        conn.execute("INSERT INTO circles (name, category) VALUES (?, ?)", ("サッカー部", "スポーツ"))
                                                     
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect("circles.db")
    conn.row_factory = sqlite3.Row
    return conn

init_db()