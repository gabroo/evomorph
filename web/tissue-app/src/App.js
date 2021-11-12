import "./App.css";
import { SimulationColumn } from "./SimulationColumn";
import { Title } from "./title";

function App() {
  return (
    <div className="App">
      <link rel="stylesheet" href="https://use.typekit.net/vut8tpq.css" />
      <Title>
        Tissue Designer
      </Title>
      <SimulationColumn />
    </div>
  );
}

export default App;
