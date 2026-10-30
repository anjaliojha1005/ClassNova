# ClassPulse — Multimodal Attendance & Classroom Activity Insights

A complete Python/Streamlit application for classroom session management, student rosters, human-verified attendance, and basic video/audio activity analysis. Data is stored locally in SQLite.

## Features
- Create, view and delete class sessions.
- Add students or import a CSV roster (`student_id`, `name`, optional `email`).
- Mark Present, Absent, Late and Excused attendance.
- Sample uploaded video frames and detect visible faces with OpenCV Haar cascades.
- Analyze PCM WAV sound activity using RMS amplitude windows.
- Save analysis summaries per session.
- Export attendance CSV and session PDF reports.
- Uploaded media is processed temporarily and is not retained by the application.

## Important limitations
Video detects visible faces; it does not recognize named students. Audio analysis estimates signal activity; it does not transcribe speech or identify speakers. The app does not infer emotions, comprehension, or an individual's attention. Activity metrics are not validated engagement measures. Attendance must be verified by an instructor.

## Requirements
Python 3.10 or 3.11 recommended. For video, use a codec OpenCV can decode (H.264 MP4 recommended). For audio, use uncompressed PCM WAV.

## Run on Windows
```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

## Run on macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```
Open the local URL shown by Streamlit (usually http://localhost:8501).

## Roster CSV example
```csv
student_id,name,email
LNCT-AI-001,Aarav Sharma,aarav@example.com
LNCT-AI-002,Diya Verma,diya@example.com
```

## Streamlit Community Cloud
Push this folder to GitHub, create an app in Streamlit Community Cloud, and set the main file path to `app.py`. Dependencies install from `requirements.txt`. Community Cloud local storage is ephemeral: SQLite records may be lost after restarts/redeployments. For persistent multi-user use, connect a managed database and add authentication.

## Privacy
Obtain informed consent and institutional authorization before recording/analyzing classroom media. Minimize retention and restrict report access. Never use automated activity metrics as the sole basis for grading, discipline, or attendance penalties.

## License
MIT.
