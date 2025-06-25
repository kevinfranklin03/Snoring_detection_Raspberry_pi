# 💤 Snoring Detection System

This project is a full-stack **AI-powered snoring detection system** using:

- 🧠 **Backend**: Python (Flask + TensorFlow + Firebase) – on the `main` branch
- 📱 **Frontend**: React Native mobile app – on the `master` branch

An IoT-powered system that captures real-time audio via Raspberry Pi, uses an AI model to detect snoring events, logs results to Firebase, and delivers visual sleep analytics straight to your phone.


---

## 🧠 Project Branches

| Branch   | Contents                             |
|----------|--------------------------------------|
| `main`   | Python backend (Flask + Firebase)    |
| `master` | React Native mobile frontend         |

Use `git checkout <branch>` to switch between them.

---

## Screen Shots
![homepage](https://github.com/user-attachments/assets/8de975f9-1bab-4175-aa68-19bf3450950c)
![snoringDetect](https://github.com/user-attachments/assets/f94127f5-4481-4102-b372-b6a9b850f3cc)
![weekly rpeort](https://github.com/user-attachments/assets/fb8fc384-9b7c-441c-a3c4-7bb7a58d9cc2)
![session info](https://github.com/user-attachments/assets/df25bbb6-8a0b-4bd6-9fd1-c057d887d5da)
![sessionSummary](https://github.com/user-attachments/assets/eb8cdee8-b107-423a-9280-07d32cc33352)
![cnn_lstm_loss_and_accuracy](https://github.com/user-attachments/assets/4f727604-833b-4984-9c17-c139522d0b9f)
![CNN_loss_And_Accuracy](https://github.com/user-attachments/assets/d99d8ad4-74fe-4533-b2c9-d8dfcb9a84de)



## 📦 Backend (main branch)

### 🔧 Tech Stack
- Python, Flask, Flask-CORS
- TensorFlow (CNN / CNN-LSTM)
- Librosa (MFCC feature extraction)
- Firebase Realtime Database
- SoundDevice (for mic input)

### 📂 Directory Structure

snoring_detection_backend/

├── flask_server.py # Flask API server

├── snoring_detection.py # Audio snoring classification

├── firebase_config.py # Firebase integration


├── train_model.py # CNN / CNN-LSTM model training

├── models/ # Trained ML models (.h5)

├── dataset/ # Audio training samples

├── requirements.txt

└── firebase-adminsdk.json # (DO NOT commit – for Firebase auth)


---

### 🚀 API Endpoints

| Method | Route               | Description                        |
|--------|---------------------|------------------------------------|
| POST   | `/start`            | Start snoring detection session    |
| POST   | `/stop`             | Stop session & generate summary    |
| GET    | `/session_summary`  | Fetch last session summary         |
| GET    | `/all_summaries`    | Fetch all stored session summaries |

---

### 🛠️ How to Run the Backend

1. **Clone the repo and switch to backend branch**:
   ```bash
   git clone https://github.com/kevinfranklin03/Snoring_detection_Raspberry_pi.git
   cd Snoring_detection_Raspberry_pi
   git checkout main

   2. **Create and Activate Virtual Environment**:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   macOS/Linux/WSL
   
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   
4. **Configure Firebase Credentials**:
   ```bash
   Place your Firebase service account JSON file (firebase-adminsdk.json) in the backend directory
   Update firebase_config.py with:

   ```bash
   cert_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'firebase-adminsdk.json')
   
   ```bash
   firebase_admin.initialize_app(cred, {
   'databaseURL': 'https://<your-database-name>.firebaseio.com'  # Replace with your actual URL
   })

5. **Start Flask Server**:
   
   ```bash
   python flask_server.py

6. **Verify API Endpoints**:

   #### Start detection session
   curl -X POST http://localhost:5000/start

   #### Stop detection session
   curl -X POST http://localhost:5000/stop

   #### Get session summary
   curl http://localhost:5000/session_summary

