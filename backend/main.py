from fastapi.middleware.cors import CORSMiddleware
from schemas import CircleCreate
from fastapi import FastAPI, HTTPException
from database import get_db, init_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.post("/api/circles", status_code=201)
def create_circle(circle: CircleCreate):
    conn = get_db()
    cursor = conn.execute("INSERT INTO circles (name, category, description) VALUES (?, ?, ?)", (circle.name, circle.category, circle.description))
    conn.commit()
    new_id = cursor.lastrowid
    row = conn.execute("SELECT * FROM circles WHERE id = ?", (new_id,)).fetchone()
    conn.close()
    return dict(row)

@app.get("/api/circles/{circle_id}")
def get_circle(circle_id: int):
    conn = get_db()
    row = conn.execute("SELECT * FROM circles WHERE id = ?",(circle_id,)).fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="サークルが見つかりません")
    return dict(row)

@app.delete("/api/circles/{circle_id}")
def delete_circle(circle_id: int):
    conn = get_db()
    row = conn.execute("SELECT * FROM circles WHERE id = ?", (circle_id,)).fetchone()
    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="サークルが見つかりません")
    conn.execute("DELETE FROM circles WHERE id = ?", (circle_id,))
    conn.commit()
    conn.close()
    return {"message": "削除"}

@app.put("/api/circles/{circle_id}")
def update_circle(circle_id: int, circle: CircleCreate):
    conn = get_db()
    row = conn.execute("SELECT * FROM circles WHERE id = ?",(circle_id,)).fetchone()
    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="サークルが見つかりません")
    conn.execute("UPDATE circles SET name = ?, category = ?, description = ? WHERE id = ?",
                (circle.name, circle.category, circle.description, circle_id)
    )
    conn.commit()
    row = conn.execute("SELECT * FROM circles WHERE id = ?",(circle_id,)).fetchone()
    conn.close()
    return dict(row)

init_db()