import React, { Component } from "react";

export function SimulationParamContainer(props) {
  return (
    <Container>
      <InfoContainer>
        <SimulationTitle>{props.simulationTitle}</SimulationTitle>
        <SimulationDescription numACells={props.numACells} numBCells={props.numBCells} desc={props.desc} >
        </SimulationDescription>
      </InfoContainer>
      <RunEditContainer>
        <RunButton properties={props}>Run</RunButton>
        <EditButton>Edit</EditButton>
        <Result properties={props}></Result>
      </RunEditContainer>
    </Container>
  );
  }

function Container(props) {
  return (
    <div className="flex bg-white border-8 rounded-sm border-pink-500 text-black justify-center p-1 m-1 w-full">
      {props.children}
    </div>
  )
}

function buttonClick(props){
  var url = "http://localhost:5000";

  var xhr = new XMLHttpRequest();
  xhr.open("POST", url, false);

  xhr.setRequestHeader("Accept", "application/json");
  xhr.setRequestHeader("Content-Type", "application/json");

  //console.log(props.properties)
  var data = JSON.stringify(props.properties);
  //console.log(data)

  xhr.send(data);

  //console.log(props.properties['simulationTitle'])
  var elem = document.getElementById(props.properties['simulationTitle']);
  //console.log(elem)
  elem.innerHTML = xhr.responseText;
}

function RunButton(props) {
  console.log(props)
  return (
    <button className="w-full text-lg text-white bg-green-500 rounded-md self-end my-1" onClick={() => buttonClick(props)}>Run</button>
  )
}

function EditButton(props) {
  return (
    <button className="w-full text-lg text-white bg-yellow-400 rounded-md self-end my-1">Edit</button>
  )
}

function Result(props) {
  console.log(props.properties.simulationTitle)
  return (
    <p id={props.properties.simulationTitle}>Result</p>
  )
}

function RunEditContainer(props) {
  return (
    <div className="flex justify-end w-1/4 flex-col py-4">
      {props.children}
    </div>
  )
}

function InfoContainer(props) {
  return (
    <div className="flex flex-col w-3/4 items-start">
      {props.children}
    </div>
  )
}

function SimulationTitle(props) {
  return (
    <div className="text-4xl font-extralight">
      {props.children}
    </div>
  )
}

function SimulationDescription(props) {
  return (
    <div className="font-lg font-medium text-left">
      Number of A Cells: {props.numACells} <br/>
      Number of B Cells: {props.numBCells} <br/>
      Description: {props.desc}
    </div>
  )
}
