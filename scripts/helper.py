import numpy as np
import librosa
import random


def extract_features(audio_data, sr=16000, max_pad_len=50, n_mfcc=20):  # Increased MFCCs
    """Extracts and normalizes MFCC features."""
    mfcc = librosa.feature.mfcc(y=audio_data, sr=sr, n_mfcc=n_mfcc)

    # Normalize MFCCs
    mfcc = (mfcc - np.mean(mfcc)) / (np.std(mfcc) + 1e-6)

    # Padding or truncation
    if mfcc.shape[1] < max_pad_len:
        pad_width = max_pad_len - mfcc.shape[1]
        mfcc = np.pad(mfcc, ((0, 0), (0, pad_width)), mode='constant')
    else:
        mfcc = mfcc[:, :max_pad_len]

    return mfcc.T  # Transpose for CNN-LSTM compatibility


def augment_audio(audio_data, sr=16000):
    """Applies random pitch shifting, noise addition, and time stretching."""
    n_steps = random.uniform(-4, 4)  # Increased pitch shift range
    audio_data = librosa.effects.pitch_shift(y=audio_data, sr=sr, n_steps=n_steps)

    noise = np.random.normal(0, 0.01, audio_data.shape)  # Increased noise level
    audio_data = audio_data + noise

    rate = random.uniform(0.7, 1.3)  # Increased time-stretch range
    audio_data = librosa.effects.time_stretch(y=audio_data, rate=rate)

    return audio_data
