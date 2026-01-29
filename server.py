from flask import Flask, request, Response
import threading

app = Flask(__name__)

latest_frame = None
lock = threading.Lock()

@app.route("/upload", methods=["POST"])
def upload():
    global latest_frame
    file = request.files.get("frame")
    if file:
        with lock:
            latest_frame = file.read()
    return "OK"

@app.route("/stream")
def stream():
    def generate():
        global latest_frame
        while True:
            with lock:
                frame = latest_frame
            if frame:
                yield (b"--frame\r\n"
                       b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/")
def home():
    return "Relay server running"
