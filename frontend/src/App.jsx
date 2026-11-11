import { useState } from "react"

const circles = [
  { id: 1, name: "ロンロック", category: "音楽"},
  { id: 2, name: "クラッシックギター部", category: "音楽"},
  { id: 3, name: "バスケ部", category: "スポーツ"},
]

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
  const [keyword, setKeyword] = useState("")
  const filtered = circles.filter((circle) => circle.name.includes(keyword))
  return (
    <div>

      <input
      value = {keyword}
      onChange={(e) => setKeyword(e.target.value)}
      placeholder="サークル名で検索"
      />

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
