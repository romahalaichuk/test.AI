const speakButton = document.getElementById("speakButton");
const output = document.querySelector(".output");
let recognition = null; // Zmienna, aby śledzić stan rozpoznawania mowy.

speakButton.addEventListener("click", () => {
	if (recognition && recognition.state === "recording") {
		recognition.stop(); // Jeśli rozpoznawanie mowy jest uruchomione, zatrzymaj je.
	} else {
		output.innerText = "Słucham...";
		recognition = new webkitSpeechRecognition();
		recognition.onresult = (event) => {
			const transcript = event.results[0][0].transcript;
			output.innerText = transcript;

			// Tutaj dodaj kod do wysłania nagranego tekstu na serwer Pythona
			fetch("/recognize", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({ question: transcript }), // Zmień "audio" na "question"
			})
				.then((response) => response.json())
				.then((data) => {
					// Tutaj wyświetl odpowiedź z serwera na stronie
					const responseText = data.response;
					output.innerText = responseText;
					// Tutaj dodaj kod do odtwarzania odpowiedzi w mowie
					const synth = window.speechSynthesis;
					const utterance = new SpeechSynthesisUtterance(responseText);
					synth.speak(utterance);
				})
				.catch((error) => {
					console.error("Błąd podczas wysyłania żądania:", error);
				});
		};

		recognition.start(); // Rozpocznij rozpoznawanie mowy.
	}
});
