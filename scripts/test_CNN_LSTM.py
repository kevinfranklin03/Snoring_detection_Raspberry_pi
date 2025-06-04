import numpy as np
import librosa
import sounddevice as sd
import tensorflow as tf
from helper import extract_features  # Make sure to import the correct feature extraction function

# Constants
SR = 22050  # Sampling rate
DURATION = 2 # Record 1-second chunks
FRAME_LENGTH = SR * DURATION

# Load trained model
model = tf.keras.models.load_model("../models/snoring_detection_model.h5")
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

def process_audio(indata, frames, time, status):
    """Process live audio from the microphone in real-time."""
    if status:
        print(status)

    audio_data = np.squeeze(indata)  # Convert stereo to mono if needed

    # Extract MFCC features
    mfcc_features = extract_features(audio_data, sr=SR, max_pad_len=50, n_mfcc=20)  # Use 20 MFCCs
    mfcc_features = np.expand_dims(mfcc_features, axis=[0, -1])  # Reshape for CNN input

    # Make prediction
    prediction = model.predict(mfcc_features)
    snoring_prob = prediction[0][1]  # Snoring probability (second class)

    # Print classification result
    if snoring_prob > 0.8:  # Confidence threshold
        print(f"🔥 Snoring 💤 (Probability: {round(snoring_prob, 2)})")
    else:
        print(f"✅ Non-Snoring 🚫 (Probability: {round(1 - snoring_prob, 2)})")

# Start real-time microphone streaming
print("🎙️ Real-Time Snoring Detection Started... Speak into the mic!")

with sd.InputStream(callback=process_audio, channels=1, samplerate=SR, blocksize=FRAME_LENGTH):
    input()  # Keep the script running
