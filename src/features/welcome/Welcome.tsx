import { useNavigate } from "react-router-dom";


export const Welcome = () => {
	const navigate = useNavigate();

	const setMode = (mode: 'driver' | 'passenger') => {
		localStorage.setItem('mode', mode)
		navigate('/')
	}

	return (
		<div>
			<h3>How would you like to use HubHopper?</h3>
			<em>(You can switch between modes at any times)</em>
			<div>
				<button onClick={() => setMode('driver')}>Driver</button>
				<button onClick={() => setMode('passenger')}>Passenger</button>
			</div>
		</div>
	)
}
