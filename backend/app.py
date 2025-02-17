from flask import Flask, request, jsonify
import time
from flask_cors import CORS
import os
import speech_recognition as sr
from bot.chatbot import ChatBot  # Import ChatBot class
from database import init_db, store_graphql_link_and_schema, get_stored_graphql_link_and_schema  # Import SQLite functions
from pydub import AudioSegment  # Convert audio to correct format

app = Flask(__name__)
CORS(app)

# Initialize database
init_db()

UPLOAD_FOLDER = "uploads"
CONVERTED_FOLDER = "converted_audios"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)  # Create folder to store converted files


@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message", "").strip()
        selected_model = request.json.get("model", "").strip()
        print(f"[DEBUG] User message received: {user_message}")

        print(f"[DEBUG] User model received: {selected_model}")
        if not user_message:
            print("[DEBUG] No message provided by the user.")
            return jsonify({"error": "No message provided"}), 400

        # Retrieve stored GraphQL link and schema from the database
        stored_link, stored_schema = get_stored_graphql_link_and_schema()
        print(f"[DEBUG] Current stored GraphQL link: {stored_link}")

        # Create a chatbot instance (pass stored link & schema)
        bot = ChatBot(user_message, selected_model, stored_link, stored_schema)

        # Process response
        bot_responses = bot.get_response()

        # ✅ If a new valid link & schema was found, store them in SQLite
        if bot.validated_link and bot.validated_schema:
            print(f"[DEBUG] Storing new validated GraphQL link & schema in SQLite: {bot.validated_link}")
            store_graphql_link_and_schema(bot.validated_link, bot.validated_schema)  # Save to database

        # Debugging response
        print(f"[DEBUG] Bot response: {bot_responses}")

        return jsonify(bot_responses)

    except Exception as e:
        print(f"[ERROR] Exception occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/speech-to-text", methods=["POST"])
def speech_to_text():
    if "file" not in request.files:
        return jsonify({"error": "No file received"}), 400

    file = request.files["file"]
    file_path = os.path.join(UPLOAD_FOLDER, "audio.wav")
    file.save(file_path)

    # ✅ Convert to correct WAV format and save it
    try:
        audio = AudioSegment.from_file(file_path)
        converted_file_name = "converted_audio.wav"  # You can change naming logic
        correct_wav_path = os.path.join(CONVERTED_FOLDER, converted_file_name)

        audio.export(correct_wav_path, format="wav")  # Save converted file
    except Exception as e:
        print(str(e))
        return jsonify({"error": f"Audio conversion failed: {str(e)}"}), 500

    # Process with SpeechRecognition
    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(correct_wav_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            print(text)

            # ✅ Return the converted audio file path along with text
            return jsonify({
                "text": text,
                "converted_audio_path": correct_wav_path  # Path to the saved converted file
            })
    except sr.UnknownValueError:
        print(sr)
        return jsonify({"text": "Could not understand audio"}), 400
    except sr.RequestError:
        return jsonify({"text": "Speech recognition API unavailable"}), 500


if __name__ == "__main__":
    print("[DEBUG] Flask app is starting...")
    app.run(debug=True, host="0.0.0.0", port=5005)
