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

