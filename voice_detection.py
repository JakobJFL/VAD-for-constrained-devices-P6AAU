import numpy as np
import matplotlib.pyplot as plt
from pyannote.audio import Model
from pyannote.audio.pipelines import VoiceActivityDetection
import torch

MODEL_PATH = "models/pytorch_model.bin"

OFFLINE_MODEL = Model.from_pretrained(MODEL_PATH)

PIPELINE = VoiceActivityDetection(segmentation=OFFLINE_MODEL)
HYPER_PARAMETERS = {
  # onset/offset activation thresholds
  "onset": 0.5, "offset": 0.5,
  # remove speech regions shorter than that many seconds.
  "min_duration_on": 0.3,
  # fill non-speech regions shorter than that many seconds.
  "min_duration_off": 0.3
}
PIPELINE.instantiate(HYPER_PARAMETERS)

def voice_activation_detection(waveform, frame_rate):
    #plot_wavefrom_graph(waveform)
    sig_mic = torch.Tensor([np.frombuffer(waveform, dtype=np.int16)])
    audio_in_memory = {"waveform": sig_mic, "sample_rate": frame_rate}
    output = PIPELINE(audio_in_memory)
    for speech in output.get_timeline().support():
        print(speech)

def plot_wavefrom_graph(waveform):
    amplitude = np.frombuffer(waveform, np.int16)
    plt.plot(amplitude)
    plt.show()
