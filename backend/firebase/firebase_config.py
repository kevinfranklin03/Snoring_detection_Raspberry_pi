import firebase_admin
from firebase_admin import credentials, db
import time
import os

# Get the absolute path to firebase-adminsdk.json file
cert_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'firebase-adminsdk.json')

cred = credentials.Certificate(cert_path)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://snoring-detectionv1-default-rtdb.europe-west1.firebasedatabase.app'  # Replace with your URL
})

def upload_snoring_data(snoring_prob, detected_snoring):
    current_date = time.strftime("%Y-%m-%d")
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")

    ref = db.reference(f'users/user123/snoring_data/{current_date}')

    data = {
        'timestamp': timestamp,
        'snoring_prob': float(snoring_prob),
        'detected_snoring': bool(detected_snoring)
    }

    ref.child(timestamp).set(data)
    print(f"✅ Uploaded under date {current_date}: {data}")

def upload_session_summary(start_time, end_time, total_minutes, snoring_minutes, snoring_events, avg_snoring_prob, sleep_quality):
    ref = db.reference('users/user123/session_summaries')
    session_id = start_time.replace(":", "-")

    summary = {
        'start_time': start_time,
        'end_time': end_time,
        'total_sleep_minutes': total_minutes,
        'snoring_minutes': snoring_minutes,
        'snoring_events': snoring_events,
        'avg_snoring_probability': round(avg_snoring_prob, 2),
        'snoring_percent': round((snoring_minutes / total_minutes) * 100, 1) if total_minutes > 0 else 0.0,
        'sleep_quality': sleep_quality
    }

    ref.child(session_id).set(summary)
    print(f"📊 Session summary uploaded: {summary}")

