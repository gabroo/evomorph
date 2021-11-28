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
            <SimulationParamContainer simulationTitle={incoming.target[0].value} numACells={incoming.target[1].value} numBCells={incoming.target[2].value} gammaA={incoming.target[3].value} gammaB={incoming.target[4].value} xValue={incoming.target[5].value} yValue={incoming.target[6].value} zValue={incoming.target[7].value} stopTime={incoming.target[8].value} desc={incoming.target[9].value} key={simList.length}/>]);
            //console.log(incoming)
            //console.log(simList)
            }}/>
      </ul>
    )
  }
  
  //onClick={() => setSimList(simList => [...simList, <SimulationParamContainer />])}