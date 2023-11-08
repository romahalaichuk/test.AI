const speakButton = document.getElementById("speakButton");
const output = document.querySelector(".output");
let recognition = null; // Zmienna, aby śledzić stan rozpoznawania mowy.
speakButton.addEventListener("click", () => {
	if (recognition && recognition.state === "recording") {
		recognition.stop();
	} else {
		output.innerText = "Słucham...";
		recognition = new webkitSpeechRecognition();
		recognition.onresult = (event) => {
			const transcript = event.results[0][0].transcript;
			output.innerText = transcript;

			fetch("/recognize", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({ question: transcript }), // Przekazuj pytanie
			})
				.then((response) => response.json())
				.then((data) => {
					const responseText = data.response;
					output.innerText = responseText;
					const synth = window.speechSynthesis;
					const utterance = new SpeechSynthesisUtterance(responseText);
					synth.speak(utterance);
				});
		};

		recognition.start();
	}
});
