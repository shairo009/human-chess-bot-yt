import os
import requests
import json

def generate_voice(text: str, output_path: str, voice_id: str, api_key: str) -> str:
    print(f"Generating voice (ElevenLabs): {text[:60]}...")
    
    if not api_key or not voice_id:
        print("WARNING: Missing ElevenLabs API Key or Voice ID. Falling back to gTTS.")
        from gtts import gTTS
        tts = gTTS(text=text, lang='en', tld='co.in') 
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        tts.save(output_path)
        print(f"Voice saved (gTTS fallback): {output_path}")
        return output_path

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }
    
    with open("config.json") as f:
        config = json.load(f)
        
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": config.get("elevenlabs_settings", {
            "stability": 0.50,
            "similarity_boost": 0.75,
            "style": 0.0,
            "use_speaker_boost": True
        })
    }
    
    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        raise Exception(f"ElevenLabs Error: {response.status_code} - {response.text}")
        
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(response.content)
        
    print(f"Voice saved (ElevenLabs): {output_path}")
    return output_path
