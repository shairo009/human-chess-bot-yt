import os
import asyncio
import edge_tts

def generate_voice(text: str, output_path: str, voice_id: str = None, api_key: str = None) -> str:
    # We switch to edge-tts because ElevenLabs has limits. 
    # This is free and high quality.
    
    # Common good voices: en-US-GuyNeural, en-IN-PrabhatNeural, hi-IN-MadhurNeural
    # Since the bot uses Hinglish, we use a clear Indian English voice.
    voice = "en-IN-PrabhatNeural" 
    
    print(f"Generating voice (Edge-TTS): {text[:60]}...")
    
    async def _amain():
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)
        
    asyncio.run(_amain())
    
    print(f"Voice saved: {output_path}")
    
    # Adjustment for speed if needed (Edge-TTS is already quite natural)
    # If output_path is being used by FFmpeg later, it's already there.
    return output_path
