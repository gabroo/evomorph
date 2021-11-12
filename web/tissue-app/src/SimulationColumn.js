import { useState } from "react"
import { CreateSimulationModal } from "./createSimulationModal";
import { Title } from "./title";
import { SimulationParamContainer } from "./SimulationParamContainer";

export function SimulationColumn(props) {

    const [simList, setSimList] = useState([]);

    return (
      <ul className="w-3/5 px-2 py-8 flex flex-col items-center justify-center">
        <Title>Simulations</Title>
        {simList}
        <CreateSimulationModal handleSubmit={(incoming) => { incoming.preventDefault(); setSimList(simList => [...simList, 
            <SimulationParamContainer simulationTitle={incoming.target[0].value} numCells={incoming.target[1].value} simType={incoming.target[2].value} desc={incoming.target[3].value} key={simList.length}/>]);
            console.log(incoming)}}/>
      </ul>
    )
  }
  
  //onClick={() => setSimList(simList => [...simList, <SimulationParamContainer />])}