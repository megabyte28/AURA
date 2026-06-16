# app.py jjjjj
from flask import Flask, jsonify
import speech_recognition as sr
from deep_translator import GoogleTranslator
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin requests for frontend access

# -------------------------------
# Translate Hinglish to English
# -------------------------------
def translate_text(text: str) -> str:
    try:
        translation = GoogleTranslator(source='auto', target='en').translate(text)
        return translation[0].upper() + translation[1:] if translation else translation
    except Exception as e:
        print("Translation error:", str(e))
        return text

# -------------------------------
# Speech recognition (Hinglish)
# -------------------------------
def listen_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source, phrase_time_limit=7)

    try:
        text = recognizer.recognize_google(audio, language='hi-IN')
        print("Recognized:", text)
        return text
    except Exception as e:
        print("Speech recognition error:", str(e))
        return ""

# -------------------------------
# Route to handle speech input
@app.route('/listen', methods=['GET'])
def handle_listen():
    try:
        spoken_text = listen_speech()
        if spoken_text:
            translated = translate_text(spoken_text)
            return jsonify({
                'success': True,
                'spoken_text': spoken_text,
                'translated_text': translated
            })
        else:
            return jsonify({'success': False, 'error': 'Could not recognize speech'})
    except Exception as e:
        print("Error in /listen route:", str(e))
        return jsonify({'success': False, 'error': 'Server error occurred'})

# -------------------------------
# Run server
# -------------------------------
if __name__ == '__main__':
    app.run(debug=True)
