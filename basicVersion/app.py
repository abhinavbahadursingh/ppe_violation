import streamlit as st
import cv2
import numpy as np
import tempfile
import smtplib
from email.mime.text import MIMEText


# ---------------- FIXED EMAIL CREDS (PUT YOURS HERE) ----------------
# --- EMAIL CONFIGURATION ---
SENDER_EMAIL = "itsshreyasingh00@gmail.com"
SENDER_PASSWORD = "iiplkmtrdusnpqvz"
RECEIVER_EMAIL = "abhinavbahadursingh69@gmail.com"
APP_PASSWORD = "rksp tjvl ovpz rxcz"


# ---------------- EMAIL FUNCTION ----------------
def send_alert_email():
    msg = MIMEText("PPE Violation Detected in Video! Please check the system.")
    msg["Subject"] = "PPE Violation Alert"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    try:
        st.write("Connecting to Gmail SMTP…")  # Debug
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        st.error(f"Email Error: {e}")  # Show exact reason
        return False


# ---------------- STREAMLIT UI ----------------
st.set_page_config(page_title="PPE Violation Detection (Video)", layout="wide")

st.title("PPE Violation Detection System (Video Upload)")
st.write("Upload a video file. The system will detect violations and send an email alert automatically.")


video_file = st.file_uploader("Upload Video", type=["mp4", "avi", "mov"])


# ---------------- SIMPLE PPE DETECTION (DUMMY LOGIC) ----------------
def detect_ppe_violation(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(gray)
    return brightness < 100  # Mark as violation if too dark


# ---------------- MAIN VIDEO PROCESSING ----------------
if video_file:
    # Save uploaded video to temp file
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(video_file.read())

    cap = cv2.VideoCapture(tfile.name)

    stframe = st.empty()
    violation_found = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (640, 380))

        # Check violation
        if detect_ppe_violation(frame):
            violation_found = True
            txt = "VIOLATION"
            clr = (0, 0, 255)
        else:
            txt = "OK"
            clr = (0, 255, 0)

        cv2.putText(frame, txt, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, clr, 2)

        stframe.image(frame, channels="BGR")

    cap.release()

    # ---------------- SEND EMAIL IF VIOLATION FOUND ----------------
    if violation_found:
        st.error("❌ PPE Violation Detected!")

        st.info("Attempting to send email alert...")
        if send_alert_email():
            st.success("📧 Email Alert Sent Successfully!")
        else:
            st.warning("Email sending failed. Check SMTP/App Password.")
    else:
        st.success("✅ No PPE Violations Detected")
