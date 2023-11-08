from flask import Flask, request, jsonify, render_template
import subprocess
import speech_recognition as sr  # Importuj bibliotekę SpeechRecognition

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recognize', methods=['POST'])
def recognize_speech():
    data = request.get_json()
    question = data.get("question")

    # Tutaj dodaj kod do rozpoznawania pytania
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)  # Dostosuj mikrofon do poziomu szumu
        audio = r.listen(source)

    try:
        recognized_question = r.recognize_google(audio, language="pl-PL")  # Rozpoznaj pytanie w języku polskim
        # Tutaj dodaj kod do wygenerowania odpowiedzi na podstawie pytania
        response_text = "Odpowiedź na pytanie: " + recognized_question
    except sr.UnknownValueError:
        response_text = "Nie rozpoznano pytania"
    except sr.RequestError:
        response_text = "Błąd w trakcie rozpoznawania"

    # Tutaj dodaj kod do wygenerowania odpowiedzi w mowie
    subprocess.call(["C:\\testAinarzendzia3\\eSpeak\\command_line\\espeak.exe", response_text])

    return jsonify({"response": response_text})

if __name__ == '__main__':
    app.run()
