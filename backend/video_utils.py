import cv2

def analyze_video(video_path):
    cap = cv2.VideoCapture(video_path)
    total, face_frames = 0, 0

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        total += 1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        if len(faces) > 0:
            face_frames += 1

    cap.release()
    return {"face_presence": face_frames / total if total else 0}
