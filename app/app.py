from models import Actor, OpenAIClient, Orchestrator, Play
from flask import Flask, request, jsonify
import uuid

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

sessions = {}

actor = Actor("")
play = Play("")
llm_client = OpenAIClient()
orchestrator = Orchestrator(llm_client=llm_client, play=play, actor=actor)


@app.route("/set_play", methods=["POST"])
def set_play():
    try:
        data = request.json
        session_id = str(uuid.uuid4())
        user_char = data["user_character"]
        play_name = data["play_name"]
        orchestrator.set_play_and_actor(play_title=play_name, user_actor=user_char)
        return jsonify({"status": "ok", "session_id": session_id})

    except Exception as e:
        print("error: ", e)
        return jsonify({"error": str(e)}), 500


@app.route("/line", methods=["POST"])
def line():
    try:
        if not request.is_json:
            return jsonify({"error": "expected JSON body"}), 400

        data = request.get_json()
        # session_id = data.get("session_id")
        user_line = data.get("line")
        if not user_line:
            return jsonify({"error": "missing user line"}), 400

        is_valid_line = orchestrator.check_user_line_is_valid(user_line=user_line)
        print("is line valid: ", is_valid_line)
        if not is_valid_line:
            return jsonify({"error": str("incorrect line")}), 500

        prompt = orchestrator.get_next_line_prompt(last_user_line=user_line)
        next_line = llm_client.get_next_line(prompt=prompt)

        print("ai line: ", next_line)
        # remember both lines

        return jsonify({"line": next_line})

    except Exception as e:
        print("error: ", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # debug mode auto-reloads on code changes
    app.run(host="0.0.0.0", port=5000, debug=True)
