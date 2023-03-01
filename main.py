from record_audio import start_recording
from voice_detection import voice_activation_detection

FRAME_RATE = 16000
RECORD_SECONDS = 2

def main():
    start_recording(voice_activation_detection, RECORD_SECONDS, FRAME_RATE)

main()
