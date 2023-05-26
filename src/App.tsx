import { useState, useEffect } from "react";
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

import { Welcome } from "./features/welcome";

import './App.css'
import {FlowManager} from "./features/flowManager/FlowManager";

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
      <RouterProvider router={router} />
    </div>
  )
}

export default App
