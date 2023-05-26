import { useState, useEffect } from "react";
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import { useQuery } from "react-query";
import axios from "axios";

import { Welcome } from "./features/welcome";
import { FlowManager } from "./features/flowManager";

import './App.css'
import {Map} from "./features/map/Map";

const router = createBrowserRouter([
  {
    path: "/",
    element: <FlowManager />,
  },
  {
    path: "/welcome",
    element: <Welcome />,
  },
]);

function App() {
  const [modal, setModal] = useState(false);

  const data = useQuery('hubs', () => axios('http://localhost:80/get_hubs/'))
  console.log(data)

  useEffect(() => {
    if (!localStorage.getItem('mode')) {
      router.navigate('/welcome')
    }
  }, [])

  const setMode = (mode: 'driver' | 'passenger') => {
    localStorage.setItem('mode', mode)
    router.navigate(0)
  }

  return (
    <div>
      <button className='hamburger' onClick={() => setModal(m => !m)}>[]</button>
      {modal && (
        <div className='modal'>
          <button onClick={() => setMode('driver')}>Driver</button>
          <button onClick={() => setMode('passenger')}>Passenger</button>
        </div>
      )}
      <Map hubs={} />
      {/*<RouterProvider router={router} />*/}
    </div>
  )
}

export default App
