# ClassNova --- Multimodal Attendance & Classroom Activity Insights

## Live Application

**Deployment:** https://classnova-hc734ecwvcxzuf46ppewcp.streamlit.app/

**Source code:** https://github.com/anjaliojha1005/ClassNova

The live application is deployed using **Streamlit Community Cloud**.
Open the deployment link above to access the application.

## Project Overview

ClassNova is a classroom support application for organizing class
sessions, maintaining a student roster, recording attendance, analyzing
basic classroom media signals, and generating reports.

The application combines a Streamlit interface with a local SQLite
database. It provides video-based visible-face counting using OpenCV and
audio signal activity estimation using RMS amplitude analysis.

## Features

-   **Dashboard:** View the number of sessions, roster size, attendance
    marks, and recent sessions.
-   **Session management:** Create, view, and delete classroom sessions.
-   **Student roster:** Add students individually or import a CSV
    roster.
-   **Attendance register:** Record Present, Absent, Late, and Excused
    statuses.
-   **Video analysis:** Sample frames from an uploaded video and count
    visible faces using OpenCV.
-   **Audio analysis:** Analyze PCM WAV audio and estimate periods of
    sound activity using RMS energy.
-   **Reports:** Export attendance as CSV and generate a session PDF
    report.
-   **Local-first data:** Store roster, sessions, attendance, and
    analysis summaries in SQLite.

## Technology Stack

  Layer                  Technology
  ---------------------- ---------------------------
  User interface         Streamlit
  Programming language   Python
  Database               SQLite
  Data handling          Pandas, NumPy
  Video processing       OpenCV
  Audio processing       Python `wave`, NumPy
  PDF generation         ReportLab
  Deployment             Streamlit Community Cloud
  Version control        Git and GitHub

## Application Workflow

1.  Add students to the roster or import a CSV file.
2.  Create a classroom session.
3.  Record each student's attendance status.
4.  Optionally upload a consented video or WAV audio recording for
    analysis.
5.  Review the saved results.
6.  Export attendance data and the session PDF report.

## Repository Structure

``` text
ClassNova/
├── app.py
├── requirements.txt
├── runtime.txt
├── README.md
├── LICENSE
├── src/
│   ├── __init__.py
│   ├── database.py
│   ├── analyzers.py
│   └── reporting.py
├── tests/
│   └── test_database.py
└── data/
```

The SQLite database is created automatically in the `data/` directory
when the application initializes.

## Run the Project Locally

### Prerequisites

-   Python 3.10 or 3.11 recommended.
-   Git (optional, for cloning the repository).
-   Windows, macOS, or Linux.

### 1. Clone the repository

``` bash
git clone https://github.com/anjaliojha1005/ClassNova.git
cd ClassNova
```

Alternatively, download the repository as a ZIP from GitHub and extract
it.

### 2. Create a virtual environment

**Windows PowerShell:**

``` powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

``` bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Start the application

``` bash
streamlit run app.py
```

Open the local address printed in the terminal. It is usually:

``` text
http://localhost:8501
```

## Student Roster CSV Format

To import students, prepare a UTF-8 CSV file with the following columns:

``` csv
student_id,name,email
LNCT-AI-001,Aarav Sharma,aarav@example.com
LNCT-AI-002,Diya Verma,diya@example.com
LNCT-AI-003,Rohan Patel,rohan@example.com
```

The `student_id` and `name` columns are required. The `email` column is
optional.

## Media Input Guidance

### Video

-   Supported upload extensions in the interface: MP4, MOV, AVI, MKV.
-   H.264-encoded MP4 is a good starting point if other files fail to
    decode.
-   The analyzer samples frames at a configurable interval and detects
    visible faces.

### Audio

-   Upload uncompressed PCM WAV audio.
-   The included sample audio dataset can be used to test the audio
    analysis workflow.
-   The analyzer estimates sound activity from signal amplitude.

## Sample Dataset

A sample dataset is available separately:

**[Download ClassNova Sample
Dataset](https://github.com/anjaliojha1005/ClassNova)**

The sample package includes: - `sample_roster.csv` --- fictional student
roster for CSV import. - `sample_attendance_reference.csv` --- example
attendance statuses for manual testing. - `sample_classroom_audio.wav`
--- synthetic test signal, not real classroom speech. - `README.txt` ---
sample dataset instructions.

If the sample dataset is not committed to the repository, download it
from the project handoff provided with this application.

## Deployment on Streamlit Community Cloud

This project is configured to run on Streamlit Community Cloud.

1.  Push the project files to a GitHub repository.
2.  Sign in to [Streamlit Community Cloud](https://share.streamlit.io/)
    using GitHub.
3.  Choose **Create app**.
4.  Select the `ClassNova` repository and the `main` branch.
5.  Set **Main file path** to `app.py`.
6.  Deploy the application.
7.  After deployment, use the app URL shown by Streamlit.

**Current live deployment:**\
https://classnova-hc734ecwvcxzuf46ppewcp.streamlit.app/

### Deployment and database persistence

The application currently uses a local SQLite database. Streamlit
Community Cloud's local filesystem is not guaranteed to persist across
restarts, rebuilds, or redeployments. Do not rely on the current
deployment for permanent attendance records. For long-term or multi-user
use, connect a managed persistent database and implement appropriate
authentication, authorization, backups, and access controls.

## Testing

The repository includes a database test. To run the test suite locally,
install dependencies and execute:

``` bash
python -m pytest tests/ -v
```

## Important Limitations

-   **No identity recognition:** The video module counts visible faces.
    It does not match a face to a named student.
-   **No emotion or attention detection:** Face counts and audio
    activity are not measurements of an individual's attention,
    understanding, emotion, or learning.
-   **Audio is not transcription:** RMS analysis does not transcribe
    speech or identify speakers.
-   **Human verification is required:** Attendance must be checked and
    confirmed by an authorized instructor.
-   **Media compatibility varies:** Results depend on camera angle,
    lighting, occlusion, video codec, audio quality, and file format.
-   **Not a production biometric system:** This project should not be
    used for automated disciplinary, grading, or high-stakes attendance
    decisions.

## Privacy and Responsible Use

-   Obtain informed consent and institutional authorization before
    recording or analyzing classroom media.
-   Use only recordings you are authorized to process.
-   Minimize collection and retention of student data.
-   Restrict access to attendance reports and exported files.
-   Avoid uploading sensitive classroom recordings to public
    repositories.
-   Do not commit real student information, credentials, database files,
    or private media to GitHub.
-   Use synthetic or anonymized records for demonstrations.

## Future Improvements

-   Persistent managed database integration.
-   Authentication and role-based access for administrators and
    instructors.
-   Improved attendance workflows and audit history.
-   Configurable report templates and analytics.
-   More extensive automated tests and deployment monitoring.

## License

This project is distributed under the MIT License. See
[LICENSE](LICENSE).

## Project Links

-   **Live application:**
    https://classnova-hc734ecwvcxzuf46ppewcp.streamlit.app/
-   **GitHub repository:** https://github.com/anjaliojha1005/ClassNova
-   **Streamlit Community Cloud:** https://share.streamlit.io/
