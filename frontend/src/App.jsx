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
      <CircleCard name="ロンロック" category="音楽" />
      <CircleCard name="クラッシックギター部" category="音楽" />
    </div>
  )
}

export default App
