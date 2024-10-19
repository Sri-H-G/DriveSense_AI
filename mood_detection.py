import os
import asyncio
from pydub import AudioSegment
from dotenv import load_dotenv
from hume.client import AsyncHumeClient
from hume.empathic_voice.chat.socket_client import ChatConnectOptions
from hume import Stream

load_dotenv()

HUME_API_KEY = os.getenv("HUME_API_KEY")
HUME_SECRET_KEY= os.getenv("HUME_SECRET_KEY")
HUME_CONFIG_ID= os.getenv("HUME_CONFIG_ID")

print(f"HUME_API_KEY: {HUME_API_KEY}")
print(f"HUME_SECRET_KEY: {HUME_SECRET_KEY}")
print(f"HUME_CONFIG_ID: {HUME_CONFIG_ID}")

async def on_message(message):
    print ("MESSAGE:", message)

    if 'prosody' in message['models']:
        emotions = message['model']['prosody']['scores']
        print ("Detected EMOTIONS:", emotions)

        if emotions.get("stress") > 0.5:
            print ("STRESS")
        elif emotions.get("calm") > 0.5:
            print ("CALM")

async def stream_audio_to_hume(audio_file):
    audio = AudioSegment.from_file(audio_file, format="wav")

    audio_bytes = audio.raw_data
    byte_stream = Stream.new()

    await byte_stream.put(audio_bytes)

    return byte_stream

async def connect_to_hume():
    client = AsyncHumeClient(api_key=HUME_API_KEY)

    options = ChatConnectOptions(config_id=HUME_CONFIG_ID, secret_key=HUME_SECRET_KEY)

    async with client.empathic_voice.chat.connect_with_callbacks(
        options=options, 
        on_message=on_message
    ) as socket: 
        print ("Connected to Hume")

        byte_stream = await stream_audio_to_hume(audio_file)

        await asyncio.sleep(5)

if __name__== "__main__":
    audio_file = "Test.wav"
    asyncio.run(connect_to_hume())
    