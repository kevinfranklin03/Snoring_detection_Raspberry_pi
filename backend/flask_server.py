from flask import Flask, jsonify
import threading
from snoring_detection import detect_snoring
from firebase_admin import db
import time
from firebase.firebase_config import upload_session_summary
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 
app = Flask(__name__)
is_detecting = False

session_start_time = None
session_end_time = None


def run_detection():
    global is_detecting
    is_detecting = True
    print(" Detection Started")
    while is_detecting:
        detect_snoring()

@app.route('/start', methods=['POST'])
def start_detection():
    global is_detecting, session_start_time
    if not is_detecting:
        session_start_time = time.strftime("%Y-%m-%d_%H-%M-%S")
        threading.Thread(target=run_detection).start()
        return jsonify({'status': 'Detection started'}), 200
    return jsonify({'status': 'Already running'}), 200

@app.route('/stop', methods=['POST'])
def stop_detection():
    global is_detecting, session_start_time, session_end_time
    is_detecting = False
    session_end_time = time.strftime("%Y-%m-%d_%H-%M-%S")
    print(" Detection Stopped")

    # Analyze data
    from firebase_admin import db

    date_key = session_start_time.split('_')[0]
    ref = db.reference(f'users/user123/snoring_data/{date_key}')
    all_data = ref.get()

    snoring_events = 0
    snoring_minutes = 0
    snoring_seconds = 0
    snoring_probs = []
    timestamps = []

    for ts, val in all_data.items():
        if session_start_time <= ts <= session_end_time:
            timestamps.append(ts)
            if val['detected_snoring']:
                snoring_events += 1
                snoring_seconds += 1  # 1 second per chunk
            snoring_probs.append(val['snoring_prob'])

    total_seconds = len(timestamps)
    total_minutes = round(total_seconds / 60, 2)
    snoring_minutes = round(snoring_seconds / 60, 2)

    snoring_percent = (snoring_minutes / total_minutes) * 100 if total_minutes > 0 else 0
    avg_snoring_prob = sum(snoring_probs) / len(snoring_probs) if snoring_probs else 0

    # Sleep quality logic
    sleep_quality = 'Good'

    if snoring_percent > 50:
        sleep_quality = 'Poor'
    elif snoring_percent > 20:
        sleep_quality = 'Moderate'

    # Upload summary
    upload_session_summary(
        start_time=session_start_time.replace('_', ' '),
        end_time=session_end_time.replace('_', ' '),
        total_minutes=total_minutes,
        snoring_minutes=snoring_minutes,
        snoring_events=snoring_events,
        avg_snoring_prob=avg_snoring_prob,
        sleep_quality=sleep_quality
    )

    return jsonify({'status': 'Detection stopped'}), 200

@app.route('/session_summary', methods=['GET'])
def session_summary():
    ref = db.reference('users/user123/session_summaries')
    summaries = ref.get()
    if summaries:
        last_summary = list(summaries.values())[-1]
        return jsonify(last_summary), 200
    return jsonify({'error': 'No summary found'}), 404

@app.route('/all_summaries', methods=['GET'])
def all_summaries():
    ref = db.reference('users/user123/session_summaries')
    summaries = ref.get()
    return jsonify(summaries or {}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
