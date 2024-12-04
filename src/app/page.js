'use client'

import { useEffect, useState } from 'react';
//const { MongoClient, ServerApiVersion } = require('mongodb');
//const uri = "mongodb+srv://afern69:E7UowlGl45u4XRHG@cluster0.kel7s.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0";

import empty from "../../public/urinalEmpty.png"
import person from "../../public/urinalPerson.png"
import piss from "../../public/urinalPiss.png"

const images = ["/urinalEmpty.png", "/urinalPiss.png", "/urinalPerson.png"]

import axios from 'axios';


const generateUrinals = () => {
  const urinalState = []

  for (let j = 0; j < 2; j++) {
    let randomEmpty = Math.floor(Math.random() * 5);
    let randomEmptyState = Math.floor(Math.random() * 2);
    urinalState[randomEmpty] = randomEmptyState;
  }

  for (let i = 0; i < 5; i++) {
    let random = Math.floor(Math.random() * 3);
    if (urinalState[i] != 0)
      urinalState[i] = random;
  }

  return urinalState
}


function App() {
  const [randomState, setRandomState] = useState()
  const [urinalState, setUrinalState] = useState([])

  //console.log(urinalState)
  console.log("HELP")

  const sendEntry = async (index) =>{
    await axios.post(`http://localhost:5000/data`, {
      choice: index,
      situation: urinalState
    })
    setUrinalState(generateUrinals)
  }

  useEffect(() => {
    console.log("LOADING")
    setUrinalState(generateUrinals())

    const num = Math.random()
    if(num > 0.6){
      setRandomState(60)
    } else {
      setRandomState(40)
    }
  }, [])


  return (
    <div className="App p-8">
      <h1 className='md:text-9xl text-3xl font-bold text-center mb-8  '>
        Urinal Machine
      </h1>
      <div className="grid grid-cols-5 gap-4 text-center md:py-0 py-32">
        {urinalState.map((urinal, index) => {
          return (<div key = {index}>
            <div key = {index}>
              <img src={images[urinal]} alt="Urinal" className='md:h-96 h-32 mx-auto'/>
              {urinal===2 ? false : (<button className='md:py-2 my-4 py-1 bg-yellow-300 rounded px-2'  key = {index} onClick={() => {sendEntry(index)}}>Select</button>)}

            </div>
          </div>
          )
        })}

      </div>
      <div className='text-center w-full mt-32 text-gray-400'>
          {randomState ? <div>owned by Alex ({randomState + 1}%) and Om ({100 - randomState - 1}%) </div> : <div></div>}

        </div>
    </div>
  );
}

export default App;
