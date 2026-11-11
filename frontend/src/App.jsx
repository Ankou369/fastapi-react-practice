const circles = [
  { id: 1, name: "ロンロック", category: "音楽"},
  { id: 2, name: "クラッシックギター部", category: "音楽"},
  { id: 3, name: "バスケ部", category: "スポーツ"},
]

function CircleCard(props) {
  return (
    <div>
      <h2>{props.name}</h2>
      <p>{props.category}</p>
    </div>
  )
}

function App() {
  return (
    <div>
      {circles.map((circle) => (
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
