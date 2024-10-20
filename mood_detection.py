import os
import asyncio
import pyaudio
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

#Audio Settings: 
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1 
RATE = 16000

async def on_message(message):
    print ("MESSAGE:", message)

    if 'prosody' in message['models']:
        emotions = message['model']['prosody']['scores']
        print ("Detected EMOTIONS:", emotions)

        # if emotions.get("stress") > 0.5:
        #     print ("STRESS")
        # elif emotions.get("calm") > 0.5:
        #     print ("CALM")

    
        for emotion, score in emotions.items():
            print(f"{emotion}: {score:.2f}")

async def stream_audio_to_hume(stream):

    byte_stream = Stream.new()

    while True: 
        data = stream.read(CHUNK)
        await byte_stream.put(data)
        await asyncio.sleep(0.01)


async def connect_to_hume():
    client = AsyncHumeClient(api_key=HUME_API_KEY)

    options = ChatConnectOptions(config_id=HUME_CONFIG_ID, secret_key=HUME_SECRET_KEY)

    async with client.empathic_voice.chat.connect_with_callbacks(
        options=options, 
        on_message=on_message
    ) as socket: 
        print ("Connected to Hume")

        audio = pyaudio.PyAudio()
        stream = audio.open(format = FORMAT, 
                            channels=CHANNELS, 
                            rate=RATE, 
                            input=True,
                            frames_per_buffer=CHUNK)

        await stream_audio_to_hume(stream)

        await asyncio.sleep(5)

        stream.stop_stream()
        stream.close()
        audio.terminate()

if __name__== "__main__":
    asyncio.run(connect_to_hume())
    