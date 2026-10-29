import asyncio
import urllib.parse
import aiohttp

async def test_trans():
    text = "Hello, welcome to this video about space exploration."
    # 1. Test MyMemory
    encoded = urllib.parse.quote(text)
    url_mm = f"https://api.mymemory.translated.net/get?q={encoded}&langpair=en|uz"
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(url_mm, timeout=5) as r:
                data = await r.json()
                print("MyMemory:", data.get("responseData", {}).get("translatedText"))
    except Exception as e:
        print("MyMemory error:", e)

if __name__ == "__main__":
    asyncio.run(test_trans())
