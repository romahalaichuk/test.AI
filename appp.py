import speech_recognition as sr
import pyttsx3

# Inicjalizacja obiektu rozpoznawania mowy
recognizer = sr.Recognizer()

# Inicjalizacja obiektu generującego mowę
engine = pyttsx3.init()

# Słownik z pytaniami i odpowiedziami
qa_dict = {
    "Jaka jest dzisiejsza pogoda?": "Dzisiaj jest słonecznie i ciepło.",
    "Co dzisiaj zjesz na obiad?": "Na obiad zamierzam zjeść sałatkę.",
    "Która godzina?": "Jest godzina 14:30.",
}

# Rozpoznawanie mowy z mikrofonu
with sr.Microphone() as source:
    print("Mów teraz...")
    audio = recognizer.listen(source)

try:
    # Rozpoznawanie mowy przy użyciu rozpoznawacza Google
    recognized_text = recognizer.recognize_google(audio, language="pl-PL")
    print(f"Rozpoznany tekst: {recognized_text}")

    # Szukanie odpowiedzi w słowniku
    response = qa_dict.get(recognized_text, "Nie mam odpowiedzi na to pytanie.")

    # Generuj odpowiedź głosową
    engine.say(response)
    engine.runAndWait()
except sr.UnknownValueError:
    print("Nie udało się rozpoznać mowy.")
except sr.RequestError as e:
    print(f"Błąd w trakcie rozpoznawania mowy: {e}")
