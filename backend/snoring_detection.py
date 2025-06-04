import numpy as np
import librosa
import tensorflow as tf
import time
import sounddevice as sd
import os
from firebase.firebase_config import upload_snoring_data  # Make sure this import is valid

# Constants
SR = 22050
DURATION = 1  # seconds
N_MFCC = 20
MAX_PAD_LEN = 50

# Load trained model
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../models/snoring_detection_model.h5')
model = tf.keras.models.load_model(model_path)

def extract_features(audio):
    """Extract MFCC features from audio."""
    mfcc = librosa.feature.mfcc(y=audio, sr=SR, n_mfcc=N_MFCC)
    mfcc = (mfcc - np.mean(mfcc)) / (np.std(mfcc) + 1e-6)  # Normalize

    if mfcc.shape[1] < MAX_PAD_LEN:
        pad_width = MAX_PAD_LEN - mfcc.shape[1]
        mfcc = np.pad(mfcc, ((0, 0), (0, pad_width)), mode='constant')
    else:
        mfcc = mfcc[:, :MAX_PAD_LEN]

    mfcc = mfcc.T  # Shape: (50, 20)
    return mfcc[np.newaxis, ...]

def detect_snoring():
    """Record audio using system mic, detect snoring, upload to Firebase."""
    try:
        print("🎙️ Recording...")
        audio = sd.rec(int(SR * DURATION), samplerate=SR, channels=1, dtype='float32')
        sd.wait()

        audio = audio.flatten()
        mfcc_features = extract_features(audio)

        prediction = model.predict(mfcc_features)
        snoring_prob = float(prediction[0][0])
        detected_snoring = snoring_prob > 0.5

        print(f"{'🔥 Snoring 💤' if detected_snoring else '✅ Non-Snoring 🚫'} (Probability: {snoring_prob:.2f})")

        # Upload to Firebase
        upload_snoring_data(snoring_prob, detected_snoring)

    except Exception as e:
        print(f"⚠️ Detection error: {str(e)}")
