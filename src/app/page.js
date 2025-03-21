'use client'

import { useEffect, useState } from 'react';
//const { MongoClient, ServerApiVersion } = require('mongodb');
//const uri = "mongodb+srv://afern69:E7UowlGl45u4XRHG@cluster0.kel7s.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0";

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
  const [prediction, setPrediciton] = useState([0, 0, 0, 0, 0]);
  const [loaded, setLoaded] = useState(false)

  //console.log(urinalState)
  console.log("HELP")

  const sendEntry = async (index) =>{
    const response = await axios.post(`http://localhost:5000/data`, {
      choice: index,
      situation: urinalState
    })
    console.log(response.data);
    setPrediciton(response.data.prediction);
    
    if(loaded == false){
      setLoaded(true)
    }
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

  const makeAnotherSelection = () => {
    setUrinalState(generateUrinals)
    setLoaded(false)
  }


  return (
    <div className="App p-8 bg-white h-screen">
      <h1 className='md:text-9xl text-3xl font-bold text-center my-4'>
        Urinal Machine
      </h1>
      <div className='text-center w-full py-2 text-gray-400 text-xl'>
          Select a urinal
        </div>
      <div className="grid grid-cols-5 gap-4 text-center md:py-0 py-32 md:gap-4 gap-0">
        {urinalState.map((urinal, index) => {
          return (<div key = {index}>
            <div key = {index}>
              <button disabled={urinal===2} className='md:h-96 h-32 w-full bg-white' key = {index} onClick={() => {sendEntry(index)}}>
              <img src={images[urinal]} alt="Urinal" className='h-full w-full'/>
              </button>
              {loaded == true ? (<h2 className='font-semibold text-xl'>Probability {Number((prediction[index])*100).toFixed(2)} % </h2>) : null}

            </div>
          </div>
          )
        })}

      </div>
      <div className='text-center w-full py-8'>
        {loaded == false ? null : <button className='border-2 font-bold py-2 px-4 rounded' onClick={makeAnotherSelection}>Make Another Selection</button>}
      </div>
      <div className='text-center w-full absolute inset-x-0 bottom-0 my-4 text-gray-400'>
          {randomState ? <div>owned by Alex ({randomState + 1}%) and Om ({100 - randomState - 1}%) </div> : <div></div>}

        </div>
    </div>
  );
}

export default App;
