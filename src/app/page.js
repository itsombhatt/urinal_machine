'use client'

import { useEffect, useState } from 'react';

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
  const [urinalState, setUrinalState] = useState([])

  //console.log(urinalState)
  console.log("HELP")

  useEffect(() => {
    console.log("LOADING")
    setUrinalState(generateUrinals())
  }, [])


  return (
    <div className="App">
      <h1 className='text-9xl font-bold text-center'>
        Urinal Machine
      </h1>
      <p className='py-8 text-center'>
        Somebody gonna match my freak??
      </p>
      <div className="grid grid-cols-5 gap-4">
        {urinalState.map((urinal, index) => {
          let state = "empty"
          if (urinal === 0) {
            state = "empty"
          } else if (urinal === 1) {
            state = "piss"
          } else {
            state = "person"
          }
          return (<div key = {index}>
            {state}
            <div key = {index}>
              {urinal===2 ? false : (<button className='py-2 bg-yellow-300 rounded px-2'  key = {index} onClick={() => setUrinalState(generateUrinals)}>Selection</button>)}

            </div>
          </div>
          )
        })}
      </div>
    </div>
  );
}

export default App;
