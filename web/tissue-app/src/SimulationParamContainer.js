import React, { Component } from "react";

export function SimulationParamContainer(props) {
  return (
    <Container>
      <InfoContainer>
        <SimulationTitle>{props.simulationTitle}</SimulationTitle>
        <SimulationDescription simType={props.simType} numCells={props.numCells} desc={props.desc} >
        </SimulationDescription>
      </InfoContainer>
      <RunEditContainer>
        <RunButton>Run</RunButton>
        <EditButton>Edit</EditButton>
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

function RunButton(props) {
  return (
    <button className="w-full text-lg text-white bg-green-500 rounded-md self-end my-1">Run</button>
  )
}

function EditButton(props) {
  return (
    <button className="w-full text-lg text-white bg-yellow-400 rounded-md self-end my-1">Edit</button>
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
      Type: {props.simType} <br/>
      Number of Cells: {props.numCells} <br/>
      Description: {props.desc}
    </div>
  )
}
