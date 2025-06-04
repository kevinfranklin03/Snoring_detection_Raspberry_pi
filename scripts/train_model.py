import os
import numpy as np
import librosa
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report, roc_curve, auc, precision_score
from helper import extract_features, augment_audio
from tensorflow.keras import layers, models, regularizers, callbacks

# === Dataset Paths ===
SNORING_PATH = "../../dataset/1/"
NON_SNORING_PATH = "../../dataset/0/"

# === Load Dataset ===
X, y = [], []

for file in os.listdir(SNORING_PATH):
    if file.endswith(".wav"):
        audio, _ = librosa.load(os.path.join(SNORING_PATH, file), sr=16000)
        audio = augment_audio(audio, sr=16000)
        X.append(extract_features(audio, n_mfcc=20))
        y.append(1)  # Snoring

for file in os.listdir(NON_SNORING_PATH):
    if file.endswith(".wav"):
        audio, _ = librosa.load(os.path.join(NON_SNORING_PATH, file), sr=16000)
        X.append(extract_features(audio, n_mfcc=20))
        y.append(0)  # Non-snoring

X = np.array(X)[..., np.newaxis]  # (samples, 50, 20, 1)
y = np.array(y)

# === Train-Test Split ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)

# === CNN Model (Baseline) ===
def build_cnn_model(input_shape):
    inputs = tf.keras.Input(shape=input_shape)
    x = layers.Conv1D(64, 3, activation='relu', padding='same')(inputs)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling1D(2)(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Conv1D(128, 3, activation='relu', padding='same')(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling1D(2)(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Flatten()(x)
    x = layers.Dense(64, activation='relu')(x)
    x = layers.Dropout(0.4)(x)
    outputs = layers.Dense(2, activation='softmax')(x)
    model = models.Model(inputs, outputs)
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

# === Improved CNN-LSTM Model ===
def build_cnn_lstm_model(input_shape):
    inputs = tf.keras.Input(shape=input_shape)
    x = layers.Conv1D(64, 3, activation='relu', padding='same')(inputs)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling1D(2)(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Conv1D(128, 3, activation='relu', padding='same')(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling1D(2)(x)
    x = layers.Dropout(0.3)(x)
    x = layers.LSTM(64)(x)
    x = layers.Dense(32, activation='relu', kernel_regularizer=regularizers.l2(0.001))(x)
    x = layers.Dropout(0.5)(x)
    outputs = layers.Dense(2, activation='softmax')(x)
    model = models.Model(inputs, outputs)
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

# === Train CNN Model ===
cnn_model = build_cnn_model((50, 20))
cnn_history = cnn_model.fit(X_train, y_train, epochs=15, batch_size=16, validation_data=(X_test, y_test))

# === Evaluate CNN ===
cnn_preds = cnn_model.predict(X_test).argmax(axis=1)
print("\n📋 CNN Classification Report:\n")
print(classification_report(y_test, cnn_preds, target_names=["Non-Snoring", "Snoring"]))
ConfusionMatrixDisplay.from_predictions(y_test, cnn_preds, display_labels=["Non-Snoring", "Snoring"], cmap=plt.cm.Greens)
plt.title("CNN Confusion Matrix")
plt.grid(False)
plt.show()

# === CNN Accuracy/Loss Plots ===
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(cnn_history.history['accuracy'], label='Train Acc')
plt.plot(cnn_history.history['val_accuracy'], label='Val Acc')
plt.title('CNN Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(cnn_history.history['loss'], label='Train Loss')
plt.plot(cnn_history.history['val_loss'], label='Val Loss')
plt.title('CNN Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


# Get prediction probabilities for class 1 (snoring)
cnn_probs = cnn_model.predict(X_test)[:, 1]  # softmax probabilities for class 1
fpr_cnn, tpr_cnn, _ = roc_curve(y_test, cnn_probs)
auc_cnn = auc(fpr_cnn, tpr_cnn)

# Calculate precision
cnn_precision = precision_score(y_test, cnn_preds)

# Plot ROC Curve
plt.figure()
plt.plot(fpr_cnn, tpr_cnn, label=f'CNN ROC Curve (AUC = {auc_cnn:.2f})', color='green')
plt.plot([0, 1], [0, 1], 'k--', label='Random Guess')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('CNN ROC Curve')
plt.legend()
plt.grid(True)
plt.show()

print(f"✅ CNN AUC Score: {auc_cnn:.4f}")
print(f"✅ CNN Precision: {cnn_precision:.4f}")


# === Train Improved CNN-LSTM Model ===
early_stop = callbacks.EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
lr_schedule = callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=2)

cnn_lstm_model = build_cnn_lstm_model((50, 20))
history = cnn_lstm_model.fit(
    X_train, y_train,
    epochs=30,
    batch_size=16,
    validation_data=(X_test, y_test),
    callbacks=[early_stop, lr_schedule]
)

# === Evaluate CNN-LSTM ===
lstm_preds = cnn_lstm_model.predict(X_test).argmax(axis=1)
print("\n📋 CNN-LSTM Classification Report:\n")
print(classification_report(y_test, lstm_preds, target_names=["Non-Snoring", "Snoring"]))
ConfusionMatrixDisplay.from_predictions(y_test, lstm_preds, display_labels=["Non-Snoring", "Snoring"], cmap=plt.cm.Blues)
plt.title("CNN-LSTM Confusion Matrix")
plt.grid(False)
plt.show()

# === CNN-LSTM Accuracy/Loss Plots ===
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Train Acc')
plt.plot(history.history['val_accuracy'], label='Val Acc')
plt.title('CNN-LSTM Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Val Loss')
plt.title('CNN-LSTM Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Get prediction probabilities for class 1 (snoring)
lstm_probs = cnn_lstm_model.predict(X_test)[:, 1]
fpr_lstm, tpr_lstm, _ = roc_curve(y_test, lstm_probs)
auc_lstm = auc(fpr_lstm, tpr_lstm)

# Calculate precision
lstm_precision = precision_score(y_test, lstm_preds)

# Plot ROC Curve
plt.figure()
plt.plot(fpr_lstm, tpr_lstm, label=f'CNN-LSTM ROC Curve (AUC = {auc_lstm:.2f})', color='blue')
plt.plot([0, 1], [0, 1], 'k--', label='Random Guess')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('CNN-LSTM ROC Curve')
plt.legend()
plt.grid(True)
plt.show()

print(f"✅ CNN-LSTM AUC Score: {auc_lstm:.4f}")
print(f"✅ CNN-LSTM Precision: {lstm_precision:.4f}")

