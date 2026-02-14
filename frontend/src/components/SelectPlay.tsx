import { useState } from "react";
import "./SelectPlay.css";
import playsData from "./plays.json";

interface PlayData {
  characters: string[];
  text: string;
}

interface Plays {
  [key: string]: PlayData; // <- allows any string key
}

const SelectPlay = () => {
  const [selectedPlay, setSelectedPlay] = useState<string>("");
  const [selectedActor, setSelectedActor] = useState<string>("");
  const [listening, setListening] = useState<boolean>(false);
  const [userLine, setUserLine] = useState("");
  const plays: Plays = playsData;

  const handlePlayChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedPlay(e.target.value);
    setSelectedActor(""); // reset actor when play changes
  };

  const handleActorChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedActor(e.target.value);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (selectedPlay && selectedActor) {
      try {
        const response = await fetch("http://localhost:5000/set_play", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            play_name: selectedPlay,
            user_character: selectedActor,
          }),
        });

        const data = await response.json();

        if (!response.ok) {
          console.error("Server error:", data);
          alert("Error setting play: " + data.error);
          return;
        }

        console.log("settings saved:", data);
      } catch (err) {
        console.error("Network error:", err);
        alert("Network error, check console.");
      }
    } else {
      alert("Please select both a play and a character.");
    }
  };

  const startListening = () => {
    const SpeechRecognition =
      (window as any).SpeechRecognition ||
      (window as any).webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert("Speech recognition not supported in this browser.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.start();
    setListening(true);

    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      console.log("User said:", transcript);
      setUserLine(transcript);
      setListening(false);

      // Optionally: submit immediately
      // submitLine(transcript);
    };

    recognition.onerror = (event: any) => {
      console.error("Speech recognition error", event.error);
      setListening(false);
    };

    recognition.onend = () => {
      setListening(false);
    };
  };

  return (
    <div>
      <form onSubmit={handleSubmit} className="select-form">
        <div className="select-form-detail">
          <label className="select-play">select a play:</label>
          <select
            value={selectedPlay}
            onChange={handlePlayChange}
            className="select-play-label"
          >
            <option value="">-- choose a play --</option>
            {Object.keys(plays).map((play) => (
              <option key={play} value={play}>
                {play}
              </option>
            ))}
          </select>
        </div>

        <div className="select-form-detail">
          <label className="block mb-1 font-semibold">
            select your character:
          </label>
          <select
            value={selectedActor}
            onChange={handleActorChange}
            className="border rounded p-2 w-full"
            disabled={!selectedPlay}
          >
            <option value="">-- choose a character --</option>
            {selectedPlay &&
              plays[selectedPlay].characters.map((actor: any) => (
                <option key={actor} value={actor}>
                  {actor}
                </option>
              ))}
          </select>
        </div>

        <button type="submit" className="submit-btn">
          save settings
        </button>
      </form>

      <div className="say-line">
        <button
          onClick={startListening}
          disabled={listening}
          className="speak-btn"
        >
          {listening ? "listening..." : "🎤 say your line"}
        </button>
      </div>
      <div className="lines">{userLine}</div>
    </div>
  );
};

export default SelectPlay;
