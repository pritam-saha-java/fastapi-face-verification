# 🧠 Face Verification API

A FastAPI-based service to verify if the person in a **profile image** appears in a given **video**. This system uses `face_recognition` and `OpenCV` to detect and match faces frame-by-frame from a video.

---

## 📁 Project Structure

```
.
├── main.py              # FastAPI application code
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker setup
└── README.md            # Project documentation
```

---

## 🚀 Features

- Upload a **profile image** and a **video**
- Face is detected in the profile image
- Every 10th frame of the video is checked for a face
- At least 3 matching frames → Verified ✅

---

## 📦 Requirements

- Python 3.10+
- FastAPI
- face_recognition
- OpenCV
- ffmpeg (for video decoding)

---

## 📥 Installation (Locally)

### 1. Clone the Repository
```bash
git clone https://github.com/pritam-saha-java/fastapi-face-verification.git
cd fastapi-face-verification
```

### 2. Install Python Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Run the App
```bash
uvicorn main:app --host 0.0.0.0 --port 5000
```

---

## 🐳 Docker Setup

### 1. Build the Docker Image
```bash
docker build -t face-verification-api .
```

### 2. Run the Container
```bash
docker run -p 5000:5000 face-verification-api
```

---

## ✅ API Endpoint

### `POST /verify-face`

**Description**: Verifies if the person in the profile image appears in the uploaded video.

#### Request:
- `multipart/form-data`
  - `profile_image`: JPG/PNG image of a face.
  - `video`: MP4 video file.

#### Curl Example:
```bash
curl -X POST http://localhost:5000/verify-face \
  -F "profile_image=@profile.jpg" \
  -F "video=@video.mp4"
```

#### Response:
```json
{
  "verified": true
}
```

- `verified = true` → Face detected in ≥ 3 frames
- `verified = false` → Face detected in < 3 frames

---

## ⚠️ Error Responses

- `400 Bad Request`: No face found in profile image
- `500 Internal Server Error`: General failure

---

## 📝 Dependencies (`requirements.txt`)

```txt
fastapi
uvicorn
face_recognition
opencv-python
python-multipart
```

---

## 🐧 Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
```

---

## 📌 Notes

- The app checks **every 10th frame** of the video to improve performance.
- Face match is considered valid if **at least 3 frames** match.
- `face_recognition` uses deep learning via dlib, so installation can take time in Docker.

---

## 🛡️ Security Considerations

- Limit upload file size (can be enforced via FastAPI configuration)
- Add authentication/token protection for production use
- Ensure file types are validated before processing

---

## 📃 License

This project is licensed under the MIT License.