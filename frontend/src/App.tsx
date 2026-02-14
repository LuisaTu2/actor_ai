import "./App.css";
import SelectPlay from "./components/SelectPlay";

function App() {
  return (
    <>
      <div className="app">
        <div className="title">Shakespeare AI</div>
        <div className="content">
          <SelectPlay />
        </div>
      </div>
    </>
  );
}

export default App;
