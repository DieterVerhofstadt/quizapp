import io
from gtts import gTTS
#from elevenlabs import generate, play, save, set_api_key
#set_api_key(st.secrets["elevenlabs"]["api_key"])

def create_tts_mp3(text):
    try:
    	mp3_fp = io.BytesIO()
    	tts = gTTS(text=text, lang='nl', slow=True)
    	tts.write_to_fp(mp3_fp)
    	return mp3_fp.getvalue()
     except Exception as e:
        st.error(f"Er ging iets mis: {e}")
        return None
def pauze(number):
    mp3_fp = io.BytesIO()
    tts = gTTS("¤", lang='fr') 
    tts.write_to_fp(mp3_fp)
    return number*mp3_fp.getvalue()

def create_eleven_mp3(text, voice, model):
	try: 	
    audio = generate(
        text=text,
        voice=voice,
	model=model
        stream=False  # stream=True geeft een generator, stream=False geeft bytes
    )
    mp3_fp = io.BytesIO(audio)  # audio is al mp3-bytestream
    return mp3_fp
  except Exception as e:
        st.error(f"Er ging iets mis met ElevenLabs: {e}")
        return None
