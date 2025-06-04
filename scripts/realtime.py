import numpy as np
import librosa
import sounddevice as sd
import tensorflow as tf
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
from helper import extract_features  # Make sure to import the correct feature extraction function

# Firebase Admin Setup
cred = credentials.Certificate('../../auth/firebase-adminsdk.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://snoring-detectionv1-default-rtdb.europe-west1.firebasedatabase.app'
})

# Constants
SR = 22050  # Sampling rate
DURATION = 2  # Record 1-second chunks
FRAME_LENGTH = SR * DURATION

# Load trained model
model = tf.keras.models.load_model("../../models/snoring_detection_model.h5")
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Firebase Reference Path (Set user ID dynamically or statically)
user_id = "user123"
path = f'users/{user_id}/snoring_data/'

def sanitize_timestamp(timestamp):
    """Sanitize the timestamp to make it compatible wth Firebase paths."""
    # Replace colons and dots with underscores or another allowed character
    return timestamp.replace(":", "_").replace(".", "_")


def upload_to_firebase(timestamp, snoring_prob, detected_snoring):
    """Uploads snoring prediction data to Firebase."""
    sanitized_timestamp = sanitize_timestamp(timestamp)

    # Convert snoring_prob (float32) to Python float
    snoring_prob = float(snoring_prob)

    # Convert detected_snoring (bool) to JSON compatible (bool in Python is already fine for Firebase)
    detected_snoring = bool(detected_snoring)

    snoring_data = {
        'timestamp': timestamp,
        'snoring_prob': snoring_prob,
        'detected_snoring': detected_snoring
    }

    # Reference to a specific path in Firebase using the sanitized timestamp
    ref = db.reference(path + sanitized_timestamp)
    ref.set(snoring_data)

    print(f"Data uploaded to Firebase: {timestamp}, Snoring Probability: {snoring_prob}, Detected: {detected_snoring}")


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

    # Determine snoring detection result
    detected_snoring = snoring_prob > 0.8  # Confidence threshold

    # Print classification result
    if detected_snoring:
        print(f"🔥 Snoring 💤 (Probability: {round(snoring_prob, 2)})")
    else:
        print(f"✅ Non-Snoring 🚫 (Probability: {round(1 - snoring_prob, 2)})")

    # Upload to Firebase with timestamp
    timestamp = datetime.now().isoformat()
    upload_to_firebase(timestamp, snoring_prob, detected_snoring)

# Start real-time microphone streaming
print("🎙️ Real-Time Snoring Detection Started... Speak into the mic!")

with sd.InputStream(callback=process_audio, channels=1, samplerate=SR, blocksize=FRAME_LENGTH):
    input()  # Keep the script running