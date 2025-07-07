import io
from gtts import gTTS


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

