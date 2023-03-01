from threading import Thread
from queue import Queue # allows to pass messages between threads
import pyaudio

CHANNELS = 1
AUDIO_FORMAT = pyaudio.paInt16
SAMPLE_SIZE = 2
CHUNK = 1024

messages = Queue()
recordings = Queue()

def start_recording(process_func, record_seconds, rate):
    messages.put(True)
    print("Starting...")
    record = Thread(target=record_mic, args=(record_seconds, rate,))
    record.start()
    vad = Thread(target=run_thread_process, args=(process_func, rate,))
    vad.start()

def stop_recording():
    messages.get()
    print("Stopped.")

def record_mic(record_seconds, rate):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=AUDIO_FORMAT, channels=CHANNELS,
                    rate=rate, input=True,
                    frames_per_buffer=CHUNK)
    frames = []
    while not messages.empty():
        data = stream.read(CHUNK)
        frames.append(data)
        if len(frames) >= (rate / CHUNK * record_seconds): # recorded more than 10 sec
            print ("finished recording")
            recordings.put(frames.copy())
            frames = []
    stream.stop_stream()
    stream.close()
    audio.terminate()

def run_thread_process(process_func, rate):
    while not messages.empty():
        frames = recordings.get()
        process_func(b''.join(frames), rate)
