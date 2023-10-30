from flask import Flask, request, jsonify
import spacy
import sqlite3

app = Flask(__name)
nlp = spacy.load("en_core_web_sm")

# Prosta baza danych SQLite z przykładowymi odpowiedziami
conn = sqlite3.connect("responses.db")
cursor = conn.cursor()

# Utwórz tabelę, jeśli nie istnieje
cursor.execute('''
    CREATE TABLE IF NOT EXISTS responses (
        id INTEGER PRIMARY KEY,
        question TEXT,
        response TEXT
    )
''')
conn.commit()

# Dodaj przykładowe odpowiedzi
cursor.executemany("INSERT INTO responses (question, response) VALUES (?, ?)", [
    ("Cześć", "Cześć! Jak mogę Ci pomóc?"),
    ("Jak się masz?", "Dziękuję, że pytasz! Jestem w formie."),
    ("Co słychać?", "Wszystko w porządku, a u Ciebie?"),
])
conn.commit()

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_message = data["message"]
    response = generate_response(user_message)
    return jsonify({"response": response})

def generate_response(user_message):
    # Sprawdź bazę danych w poszukiwaniu odpowiedzi
    cursor.execute("SELECT response FROM responses WHERE question=?", (user_message,))
    row = cursor.fetchone()
    if row:
        return row[0]

    # Jeśli nie znaleziono odpowiedzi w bazie danych, przeprocesuj pytanie za pomocą spaCy
    doc = nlp(user_message)
    # Tutaj można dodać bardziej zaawansowaną logikę, np. uczenie maszynowe, aby generować odpowiedzi.

    return "Przepraszam, nie jestem pewien, jak na to odpowiedzieć."

if __name__ == "__main__":
    app.run(debug=True)
