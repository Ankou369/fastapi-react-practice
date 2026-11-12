import { useState, useEffect } from "react"

function CircleCard(props) {
  const [likes, setLikes] = useState(0)

  return (
    <div>
      <h2>{props.name}</h2>
      <p>{props.category}</p>
      <button onClick={() => setLikes(likes + 1)}>いいね </button>
      <p>いいね数: {likes}</p>
    </div>
  )
}

function App() {
  const [circles, setCircles] = useState([])
  const [keyword, setKeyword] = useState("")

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  const [newName, setNewName] = useState("")
  const [newCategory, setNewCategory] = useState("")
  const [newDescription, setNewDescription] = useState("")


  const filtered = circles.filter((circle) => circle.name.includes(keyword))
  
  useEffect(() => {
    async function load() {
      try{
        const res = await fetch("http://127.0.0.1:8000/api/circles")
        const data = await res.json()
        setCircles(data)
      } catch(e) {
        setError("データの読み込みに失敗しました")
      }
      setLoading(false)
    }
    load()
  }, [])

  if (loading) return <p>読み込み中...</p>
  if (error) return <p>{error}</p>

  async function handleSubmit(e) {
    e.preventDefault()
    const res = await fetch("http://127.0.0.1:8000/api/circles", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: newName, category: newCategory, description: newDescription }),
    })
    const created = await res.json()
    setCircles([...circles, created])
    setNewName("")
    setNewCategory("")
    setNewDescription("")
  }

  
  return (
    <div>

      <input
      value = {keyword}
      onChange={(e) => setKeyword(e.target.value)}
      placeholder="サークル名で検索"
      />

      <form onSubmit={handleSubmit}>
        <input value={newName} onChange={(e) => setNewName(e.target.value)} placeholder="名前" />
        <input value={newCategory} onChange={(e) => setNewCategory(e.target.value)} placeholder="カテゴリ" />
        <input value={newDescription} onChange={(e) => setNewDescription(e.target.value)} placeholder="説明" />
        <button type="submit">登録</button>
      </form>

      {filtered.map((circle) => (
        <CircleCard
        key={circle.id}
        name={circle.name}
        category={circle.category}
        />
    ))}
    </div>
  )
}

export default App
