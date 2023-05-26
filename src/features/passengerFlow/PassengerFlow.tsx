import { useState, useEffect } from "react";
import { Map } from "../map/map"

export const PassengerFlow = () => {
	const [step, setStep] = useState<"rideDetails" | "drivers" | "ride" | "final">("rideDetails")

	useEffect(() => {
		if (step !== "ride") return
		const timer = setTimeout(() => {
			setStep(() => "final")
		}, 10000) // map animation time
		return () => clearTimeout(timer);
	}, [step])

	return (
		<div>
			<Map />
		</div>
	)
}
