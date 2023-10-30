function sendMessage() {
	const userInput = document.getElementById("user-input").value;
	const chatHistory = document.getElementById("chat-history");

	chatHistory.innerHTML += `<div><strong>Użytkownik:</strong> ${userInput}</div>`;

	// Wysyłanie komunikatu do serwera Flask
	fetch("/ask", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({ message: userInput }),
	})
		.then((response) => response.json())
		.then((data) => {
			const response = data.response;
			chatHistory.innerHTML += `<div><strong>Wirtualny Przyjaciel:</strong> ${response}</div>`;
		});

	document.getElementById("user-input").value = "";
}
