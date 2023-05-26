import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { DriverFlow } from "../driverFlow/DriverFlow";
import { PassengerFlow } from "../passengerFlow/PassengerFlow";

export const FlowManager = () => {
	const [mode, setMode] = useState<string | null>(null);
	const navigate = useNavigate();

	useEffect(() => {
		const mode$ = localStorage.getItem('mode')
		if (!mode$) {
			navigate('/welcome');
		}
		setMode(mode$);
	}, [])

	return (
		<>
			{mode === 'driver' && <DriverFlow />}
			{mode === 'passenger' && <PassengerFlow />}
		</>
	)
}
