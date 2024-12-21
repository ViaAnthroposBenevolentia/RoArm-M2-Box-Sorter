from flask import Flask, render_template, jsonify, Response
import cv2
import threading
from datetime import datetime
import time

app = Flask(__name__)

# Global variables to store system state
system_state = {
    "last_detected_color": None,
    "arm_position": "default",
    "last_action_time": None,
    "system_status": "idle",
    "total_boxes_processed": 0,
    "color_counts": {"Red": 0, "Green": 0, "Yellow": 0}
}

camera_lock = threading.Lock()  # Add at top with other globals

@app.route('/')
def index():
    return render_template('index.html', state=system_state)

@app.route('/api/state')
def get_state():
    return jsonify(system_state)

# Helper function to update system state
def update_system_state(color=None, position=None, status=None):
    if color:
        system_state["last_detected_color"] = color
        system_state["color_counts"][color] = system_state["color_counts"].get(color, 0) + 1
        system_state["total_boxes_processed"] += 1
    if position:
        system_state["arm_position"] = position
    if status:
        system_state["system_status"] = status
    system_state["last_action_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def gen_frames():
    while True:
        with camera_lock:
            cap = cv2.VideoCapture(0)
            success, frame = cap.read()
            cap.release()  # Important: release immediately
            
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.5)  # Add small delay to prevent excessive CPU usage

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 