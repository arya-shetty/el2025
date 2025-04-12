
import cv2
import os

def extract_frames(video_path, frames_folder, fps_rate=1):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Get video information
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"FPS: {fps}")
    print(f"Total frames: {frame_count}")

    # Extract frames at the given fps_rate
    frame_number = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Only save frames based on the desired fps_rate
        if frame_number % int(fps / fps_rate) == 0:
            frame_filename = os.path.join(frames_folder, f"frame_{frame_number + 1}.jpg")
            cv2.imwrite(frame_filename, frame)

        frame_number += 1

    cap.release()
    print("Frame extraction completed.")

if __name__ == "__main__":
    # Example usage: You can run this script directly by passing the video path and FPS rate
    video_path = 'your_video.mp4'  # Replace with your video file path
    frames_folder = 'frames'       # Folder to save extracted frames
    os.makedirs(frames_folder, exist_ok=True)  # Create the frames folder if it doesn't exist

    extract_frames(video_path, frames_folder, fps_rate=1)
