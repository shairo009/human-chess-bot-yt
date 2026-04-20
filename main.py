import json
import os
import random
import time
import requests
from voice import generate_voice
from editor import create_video
from uploader import upload_to_youtube

with open("config.json") as f:
    config = json.load(f)

with open("prompt.txt") as f:
    PROMPT_TEMPLATE = f.read()

TONES = ["Shock 😱", "Funny 😂", "Savage 😈", "Smart 😎"]

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", config.get("openrouter_api_key", ""))
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", config.get("elevenlabs_api_key", ""))


def fetch_lichess_game():
    username = config["lichess_username"]
    url = f"https://lichess.org/api/games/user/{username}?max=10&analysed=true&evals=true"
    headers = {"Accept": "application/x-ndjson"}
    r = requests.get(url, headers=headers, stream=True)
    games = []
    for line in r.iter_lines():
        if line:
            games.append(json.loads(line))
    if not games:
        raise Exception("No games found on Lichess")
    return random.choice(games)


def extract_blunder(game):
    analysis = game.get("analysis", [])
    blunder_move = None
    blunder_index = -1
    for i, move_data in enumerate(analysis):
        if move_data.get("judgment", {}).get("name") in ["Blunder", "Mistake"]:
            blunder_move = move_data
            blunder_index = i
            break
    return {
        "pgn": game.get("pgn", ""),
        "blunder_move": blunder_move,
        "blunder_index": blunder_index,
        "game_id": game.get("id", "unknown")
    }


def call_openrouter_for_script(prompt, tone):
    model = config.get("openrouter_model", "mistralai/mistral-7b-instruct:free")
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/shairo009/human-chess-bot-yt",
        "X-Title": "Human Chess Bot YT"
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are a human YouTube Shorts chess creator. Respond only in the exact OUTPUT format given."
            },
            {
                "role": "user",
                "content": prompt + f"\n\nTone for this video: {tone}"
            }
        ],
        "temperature": 0.9,
        "max_tokens": 500
    }

    print(f"Calling OpenRouter model: {model}")
    r = requests.post(url, headers=headers, json=payload)

    if r.status_code != 200:
        raise Exception(f"OpenRouter error: {r.status_code} - {r.text}")

    return r.json()["choices"][0]["message"]["content"]


def parse_script(raw_output):
    result = {}
    current_key = None
    for line in raw_output.strip().split("\n"):
        matched = False
        for key in ["HOOK", "VOICE_LINES", "STYLE", "TITLE", "DESCRIPTION", "HASHTAGS", "EDIT_PLAN"]:
            if line.startswith(f"{key}:"):
                current_key = key
                result[key] = line[len(key)+1:].strip()
                matched = True
                break
        if not matched and current_key and line.strip():
            result[current_key] = result.get(current_key, "") + "\n" + line.strip()
    return result


def run_pipeline():
    videos_per_day = config.get("videos_per_day", 4)
    gap_hours = config.get("gap_hours", 3)

    for i in range(videos_per_day):
        print(f"\n=== Video {i+1}/{videos_per_day} ===")
        try:
            tone = random.choice(TONES)
            print(f"Tone: {tone}")

            game = fetch_lichess_game()
            blunder_data = extract_blunder(game)

            raw_script = call_openrouter_for_script(PROMPT_TEMPLATE, tone)
            script = parse_script(raw_script)

            print("Script generated:")
            print(json.dumps(script, indent=2, ensure_ascii=False))

            voice_file = generate_voice(
                text=script.get("HOOK", "") + " " + script.get("VOICE_LINES", ""),
                output_path=f"output/voice_{i}.mp3"
            )

            video_file = create_video(
                game_id=blunder_data["game_id"],
                blunder_index=blunder_data["blunder_index"],
                voice_file=voice_file,
                edit_plan=script.get("EDIT_PLAN", ""),
                output_path=f"output/video_{i}.mp4"
            )

            upload_to_youtube(
                video_path=video_file,
                title=script.get("TITLE", "Chess Blunder 😱"),
                description=script.get("DESCRIPTION", "") + "\n" + script.get("HASHTAGS", ""),
                tags=script.get("HASHTAGS", "").replace("#", "").split()
            )

            print(f"Video {i+1} uploaded successfully!")

        except Exception as e:
            print(f"Error on video {i+1}: {e}")

        if i < videos_per_day - 1:
            print(f"Waiting {gap_hours} hours before next video...")
            time.sleep(gap_hours * 3600)


if __name__ == "__main__":
    run_pipeline()
