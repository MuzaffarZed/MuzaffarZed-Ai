import asyncio
import edge_tts

def custom_mkssml(tc, escaped_text):
    if isinstance(escaped_text, bytes):
        escaped_text = escaped_text.decode('utf-8')
    return (
        "<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='uz-UZ'>"
        f"<voice name='{tc.voice}'>"
        f"{escaped_text}"
        "</voice>"
        "</speak>"
    )

edge_tts.communicate.mkssml = custom_mkssml

test_text = "Salom! <break time='1000ms'/> Men hozir bir soniya kutdim. <prosody pitch='+8Hz' rate='+20%'>Endi esa balandroq va tezroq gapiryapman!</prosody> <break time='500ms'/> Ajoyib!"

async def run():
    c = edge_tts.Communicate('temp', 'uz-UZ-SardorNeural')
    c.texts = [test_text]
    await c.save('test_custom_ssml.mp3')
    print('SSML audio muvaffaqiyatli saqlandi!')

asyncio.run(run())
