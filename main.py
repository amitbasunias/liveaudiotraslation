import os
from flask import Flask, request, jsonify,send_file
import speech_recognition as sr
from gtts import gTTS
from flask_cors import CORS
from pydub import AudioSegment
from translate import Translator


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Speech recognition setup
r = sr.Recognizer()

@app.route('/translate', methods=['POST'])
def translate():
    # Check if the request contains an audio file
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file found'}), 400

    # Check if the request contains the target language
    target_language = request.form.get('language')
    print(target_language)
    if not target_language:
        return jsonify({'error': 'Target language not specified'}), 400

    audio_file = request.files['audio']

    # Save the audio file
    audio_path = 'input.wav'
    audio_file.save(audio_path)

    # Convert audio file to PCM WAV format
    converted_audio_path = 'converted_input.wav'
    convert_to_pcm_wav(audio_path, converted_audio_path)

    # Perform speech recognition
    recognized_text = recognize_speech(converted_audio_path, target_language)

    # Perform translation (not implemented in this example)

    # Perform speech synthesis
    output_path = 'output.mp3'
    language = "bn"
    synthesize_speech(recognized_text, language, output_path)

    # Return the synthesized speech file
    return send_file(output_path, mimetype='audio/mpeg')

def convert_to_pcm_wav(input_file, output_file):
    audio = AudioSegment.from_file(input_file)
    audio.export(output_file, format='wav')

def translate_text(text, target_language):
    translator = Translator(to_lang=target_language)
    translation = translator.translate(text)
    return translation
def recognize_speech(converted_audio_path,target_language):
    with sr.AudioFile(converted_audio_path) as source:
        audio = r.record(source)  # Read the audio file

    try:
        text = r.recognize_google(audio)  # Perform speech recognition using Google Speech Recognition
        translatetext = translate_text(text, target_language)

        return translatetext
    except sr.UnknownValueError:
        return "Speech recognition could not understand audio"
    except sr.RequestError as e:
        return "Could not request results from Google Speech Recognition service; {0}".format(e)

def synthesize_speech(translatetext, language, output_file):
    print(translatetext)
    tts = gTTS(text=translatetext, lang=language)  # Create a gTTS object with the translated text and target language
    tts.save(output_file)  # Save the synthesized speech to a file

if __name__ == '__main__':
    app.run()
