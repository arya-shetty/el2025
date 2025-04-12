from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import cv2

app = Flask(__name__)

# Set the upload folder and the frames folder
UPLOAD_FOLDER = "uploads"
FRAMES_FOLDER = "frames"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["FRAMES_FOLDER"] = FRAMES_FOLDER

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(FRAMES_FOLDER, exist_ok=True)

@app.route("/")
def index():
    # This route will render the index.html page
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_video():
    # Handle the video file upload and frame extraction
    if "video" not in request.files:
        return redirect(request.url)
    
    video_file = request.files["video"]
    if video_file.filename == "":
        return redirect(request.url)

    # Save the uploaded video
    video_path = os.path.join(app.config["UPLOAD_FOLDER"], video_file.filename)
    video_file.save(video_path)

    # Process the video to extract frames
    extract_frames(video_path)

    # After extraction, redirect to the frames page to show the images
    return redirect(url_for("frames"))

def extract_frames(video_path):
    # Extract frames from the uploaded video
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    for i in range(frame_count):
        ret, frame = cap.read()
        if ret:
            frame_filename = os.path.join(FRAMES_FOLDER, f"frame_{i + 1}.jpg")
            cv2.imwrite(frame_filename, frame)
    
    cap.release()

@app.route("/frames")
def frames():
    # This route will render the frames.html page
    frames = os.listdir(FRAMES_FOLDER)
    frame_files = [f for f in frames if f.endswith(".jpg")]
    return render_template("frames.html", frame_files=frame_files)

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    # This will serve the image files
    return send_from_directory(app.config["FRAMES_FOLDER"], filename)

if __name__ == "__main__":
    app.run(debug=True)
