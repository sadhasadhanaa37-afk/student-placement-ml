# Placement Atelier · Midnight Bloom

AI-based **student placement prediction** and skill practice studio — dark floral Streamlit app with HR interview, aptitude polls, voice coaching, coding tests, and project ideas.

**Repo:** https://github.com/sadhasadhanaa37-afk/student-placement-ml

## Features
- Placement prediction + skill recommendations  
- Company directory  
- HR practice (soft skills, GD, technical Q&A, coding, projects, communication)  
- Aptitude chatbot with 4-option polls  
- Voice: bot speaks (TTS) + you can speak (mic / audio)  
- Dark floral **Midnight Bloom** theme  

## Local setup

```bash
pip install -r requirements.txt
python data/generate_data.py   # if you need to regenerate data
python src/train.py            # if you need to retrain
python -m streamlit run app.py
```

## Deploy (important)

**Vercel cannot host Streamlit** (Streamlit needs a long-running Python server; Vercel is for static / serverless Node apps).

### Option A — Streamlit Community Cloud (recommended)
1. Open: https://share.streamlit.io/  
2. Sign in with GitHub  
3. Deploy repo `sadhasadhanaa37-afk/student-placement-ml`  
4. Main file: `app.py`  

Direct deploy helper:  
https://share.streamlit.io/deploy?repository=sadhasadhanaa37-afk/student-placement-ml&branch=master&mainModule=app.py

### Option B — Render
This repo includes `render.yaml`. On [render.com](https://render.com): **New → Blueprint** → connect this GitHub repo.

## Project structure
```
student-placement-ml/
├── app.py
├── requirements.txt
├── render.yaml
├── data/
├── models/
└── src/   (predict, train, chatbots, voice_ui, …)
```
