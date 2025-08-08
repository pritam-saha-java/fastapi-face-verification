from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import face_recognition
import cv2
import tempfile
import os
from typing import List

app = FastAPI()

@app.post("/verify-face")
async def verify_face(profile_image: UploadFile = File(...), video: UploadFile = File(...)):
    try:
        # Save profile image
        profile_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        profile_path = profile_temp.name
        with open(profile_path, "wb") as f:
            f.write(await profile_image.read())

        # Save video
        video_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        video_path = video_temp.name
        with open(video_path, "wb") as f:
            f.write(await video.read())

        # Load profile face encoding
        profile_img = face_recognition.load_image_file(profile_path)
        profile_encodings = face_recognition.face_encodings(profile_img)
        if not profile_encodings:
            raise HTTPException(status_code=400, detail="No face found in profile image.")
        profile_encoding = profile_encodings[0]

        # Extract frames from video and compare
        video_cap = cv2.VideoCapture(video_path)
        total_frames = 0
        matched_frames = 0

        while True:
            ret, frame = video_cap.read()
            if not ret:
                break
            total_frames += 1
            if total_frames % 10 != 0:
                continue  # check every 10th frame

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            encodings_in_frame = face_recognition.face_encodings(rgb_frame)

            for enc in encodings_in_frame:
                result = face_recognition.compare_faces([profile_encoding], enc, tolerance=0.6)
                if result[0]:
                    matched_frames += 1
                    break  # match found in this frame

        video_cap.release()
        os.remove(profile_path)
        os.remove(video_path)

        is_verified = matched_frames >= 3
        return JSONResponse(content={"verified": is_verified})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})