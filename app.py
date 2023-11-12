from flask import Flask, request, jsonify, render_template
import subprocess
import speech_recognition as sr

app = Flask(__name__, static_url_path='/static')
@app.route('/meta.json', methods=['GET'])
def get_meta_data():
    # Tutaj możesz umieścić dowolne dane, które chcesz udostępnić jako meta.json
    meta_data = {
        "key": "value",
        "another_key": "another_value"
    }

    return jsonify(meta_data)

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

        # Dodaj warunek na podstawie rozpoznanego języka pytania
        if "pl" in recognized_question.lower():
            # Jeśli rozpoznano język polski, generuj odpowiedź w języku polskim
            response_text = "Odpowiedź po polsku na pytanie: " + recognized_question
        else:
            # Jeśli rozpoznano inny język, generuj odpowiedź w języku angielskim
            response_text = "Odpowiedź po angielsku na pytanie: " + recognized_question
    except sr.UnknownValueError:
        response_text = "Nie rozpoznano pytania"
    except sr.RequestError:
        response_text = "Błąd w trakcie rozpoznawania"

    # Tutaj dodaj kod do wygenerowania odpowiedzi w mowie
    subprocess.call(["C:\\testAinarzendzia3\\eSpeak\\command_line\\espeak.exe", "--voice=pl", "--rate=100", "--pitch=30", response_text])


    return jsonify({"response": response_text})

if __name__ == '__main__':
    app.run()
