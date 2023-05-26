import { useState, useEffect } from "react";

export const DriverFlow = () => {
	const [step, setStep] = useState<"rideDetails" | "passengers" | "ride" | "final">("rideDetails")

	useEffect(() => {
		if (step !== "ride") return
		const timer = setTimeout(() => {
			setStep(() => "final")
		}, 10000) // map animation time
		return () => clearTimeout(timer);
	}, [step])

	return (
		<div>
			{step === "rideDetails" && (
				<button onClick={() => setStep("passengers")}>Enter destination and how long you ready to wait</button>
			)}
			{step === "passengers" && (
				<button onClick={() => setStep("ride")}>Approve passenger request</button>
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
