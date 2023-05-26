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
			{step === "rideDetails" && (
				<button onClick={() => setStep("drivers")}>Enter destination and when you ready to departure</button>
			)}
			{step === "drivers" && (
				<button onClick={() => setStep("ride")}>Request a ride</button>
			)}
			{step === "ride" && (
				<iframe src="https://giphy.com/embed/5bo92jPBIWKtHUump7" width="340" height="480" frameBorder="0"
					className="giphy-embed"
					allowFullScreen></iframe>
			)}
			{step === "final" && (
				<div>You arrived!</div>
			)}
		</div>
	)
}
