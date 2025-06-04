import sounddevice as sd
import librosa
import numpy as np
from tensorflow.keras.models import load_model

# Load model
model = load_model("snoring_cnn_lstm.h5")

# Settings
SAMPLE_RATE = 16000
DURATION = 3  # Seconds per chunk
CHANNELS = 1

def extract_features(audio):
    mfccs = librosa.feature.mfcc(
        y=audio,
        sr=SAMPLE_RATE,
        n_mfcc=20,
        n_fft=512,
        hop_length=160,
        n_mels=40
    )
    # Force 50 frames
    if mfccs.shape[1] > 50:
        mfccs = mfccs[:, :50]
    elif mfccs.shape[1] < 50:
        mfccs = np.pad(mfccs, ((0,0), (0,50-mfccs.shape[1])), mode='constant')
    return mfccs.T  # Shape: (50, 20)

def predict_snoring(audio):
    features = extract_features(audio)
    features = np.expand_dims(features, axis=[0, -1])  # Shape: (1, 50, 20, 1)
    prob = model.predict(features, verbose=0)[0]
    return "SNORING!" if np.argmax(prob) == 1 else "No snoring", prob

def audio_callback(indata, frames, time, status):
    audio = indata[:, 0].flatten()  # Ensure 1D array
    label, confidence = predict_snoring(audio)
    print(f"{label} (Confidence: {confidence[1]:.2f})", flush=True)

# Verify audio device
print("Available devices:", sd.query_devices(), "\n")

print("Listening for snoring... (Press Ctrl+C to stop)")
with sd.InputStream(
    samplerate=SAMPLE_RATE,
    channels=CHANNELS,
    callback=audio_callback,
    blocksize=int(SAMPLE_RATE * DURATION),
    dtype='float32'
):
    while True:
        sd.sleep(1000)  # Prevent CPU overload