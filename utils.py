import io
from gtts import gTTS
from elevenlabs import generate, play, save, set_api_key
# Zet je eigen API key hier
set_api_key(sk_7e7ca833c6de08494dcfce96f283a92fe3c0bb33c4813fb7)

def create_tts_mp3(text):
    mp3_fp = io.BytesIO()
    tts = gTTS(text=text, lang='nl', slow=True)
    tts.write_to_fp(mp3_fp)
    return mp3_fp.getvalue()

def pauze(number):
    mp3_fp = io.BytesIO()
    tts = gTTS("¤", lang='fr') 
    tts.write_to_fp(mp3_fp)
    return number*mp3_fp.getvalue()

def create_eleven_mp3(text, voice="Tijs", model="eleven_monolingual_v1"):
    """
    Genereert een mp3-bestand met TTS via ElevenLabs.
    Geeft een BytesIO stream terug die je direct in Streamlit kan gebruiken.
    """
    audio = generate(
        text=text,
        voice=voice,
	model=model
        stream=False  # stream=True geeft een generator, stream=False geeft bytes
    )
    mp3_fp = io.BytesIO(audio)  # audio is al mp3-bytestream
    return mp3_fp



