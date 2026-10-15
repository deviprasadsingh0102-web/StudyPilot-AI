# StudyPilot AI

A Streamlit-based student learning support MVP.

## Features
- Dashboard for quiz and study-time summaries
- Subjects: Python, Machine Learning, Data Science, Artificial Intelligence
- 10-question Python quiz with score and explanations
- Rule-based FAQ mentor (not a live generative AI model)
- Progress charts and quiz history
- Study planner and student profile
- SQLite local storage

## Run locally on Windows
1. Install Python 3.10+.
2. Extract this folder.
3. Open Command Prompt inside this folder.
4. Run:
   ```bat
   python -m venv venv
   venv\Scripts\activate
   python -m pip install -r requirements.txt
   python -m streamlit run app.py
   ```

Or double-click `RUN_STUDYPILOT.bat`.

## Deploy free using Streamlit Community Cloud
1. Sign in at https://share.streamlit.io/ using your GitHub account.
2. Create a GitHub repository named `StudyPilot-AI`.
3. Upload `app.py`, `requirements.txt`, `README.md`, `.gitignore`, and the `.streamlit` folder.
4. In Streamlit Community Cloud choose **Create app**.
5. Select your repository, branch `main`, and main file path `app.py`.
6. Click **Deploy** and wait for the build to finish.

## Important deployment note
This project uses SQLite. On hosted platforms, local files may be reset when the app restarts or redeploys, depending on the platform. This starter project does not include a hosted persistent database. For durable multi-user production data, connect a hosted database such as PostgreSQL.

## AI Mentor note
The AI Mentor uses built-in topic responses. It is not connected to a live AI API. Do not add API keys directly to source code; use the hosting platform's secrets manager if you later integrate an AI provider.

## GitHub safety
Do not upload `venv/`, `.env`, API keys, private student data, or `studypilot.db`.
