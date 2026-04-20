import os
import json
import requests
import subprocess

with open("config.json") as f:
    config = json.load(f)

SETTINGS = config["elevenlabs_settings"]


def generate_voice(text: str, output_path: str, voice_id: str = None, api_key: str = None) -> str:
    voice_id = voice_id or os.environ.get("ELEVENLABS_VOICE_ID", config.get("elevenlabs_voice_id", ""))
    api_key  = api_key  or os.environ.get("ELEVENLABS_API_KEY", "")

    if not voice_id:
        raise Exception("ELEVENLABS_VOICE_ID not set!")
    if not api_key:
        raise Exception("ELEVENLABS_API_KEY not set!")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability":        SETTINGS["stability"],
            "similarity_boost": SETTINGS["similarity_boost"],
            "style":            SETTINGS["style"],
            "use_speaker_boost": SETTINGS["use_speaker_boost"]
        }
    }

    print(f"Generating voice: {text[:60]}...")
    r = requests.post(url, headers=headers, json=payload)

    if r.status_code != 200:
        raise Exception(f"ElevenLabs error {r.status_code}: {r.text}")

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(r.content)
    print(f"Voice saved: {output_path}")

    speed = SETTINGS.get("speed", 1.10)
    if speed != 1.0:
        fast_path = output_path.replace(".mp3", "_fast.mp3")
        subprocess.run(
            ["ffmpeg", "-y", "-i", output_path, "-filter:a", f"atempo={speed}", fast_path],
            check=True, capture_output=True
        )
        print(f"Speed adjusted ({speed}x): {fast_path}")
        return fast_path

    return output_path
