from constants import GPT_MODEL
from models import Rehearser
from flask import Flask, request, jsonify
import openai
import os
import uuid

from openai import OpenAI

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

sessions = {}
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.route("/set_play", methods=["POST"])
def set_play():
    try:
        data = request.json
        session_id = str(uuid.uuid4())
        user_char = data["user_character"]
        play_name = data["play_name"]
        # ai_char = data.get("ai_character", "AI")  # optional default

        sessions[session_id] = Rehearser(play_name, user_char)
        print("sessions: ", sessions)
        return jsonify({"status": "ok", "session_id": session_id})

    except Exception as e:
        print("error: ", e)


@app.route("/line", methods=["POST"])
def line():
    try:
        if not request.is_json:
            return jsonify({"error": "expected JSON body"}), 400

        data = request.get_json()
        session_id = data.get("session_id")
        user_line = data.get("line")
        if not session_id or not user_line:
            return jsonify({"error": "missing session_id or line"}), 400

        session = sessions.get(session_id)
        if not session:
            return jsonify({"error": "session not found"}), 404

        session.record_line(session.user.name, user_line)

        prompt = session.get_context_prompt()
        print("sessions: ", prompt, sessions)
        response = client.chat.completions.create(
            model=GPT_MODEL, messages=[{"role": "user", "content": prompt}]
        )
        ai_line = response.choices[0].message.content.strip()

        print("ai line: ", ai_line)
        # record AI's line
        # session.record_line(session.ai.name, ai_line)

        return jsonify({"line": ai_line})

    except Exception as e:
        print("error: ", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # debug mode auto-reloads on code changes
    app.run(host="0.0.0.0", port=5000, debug=True)
