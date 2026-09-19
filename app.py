# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re
import sys

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
# pyrefly: ignore [missing-import]
from predict import predict_placement, get_recommendations, load_metrics
# pyrefly: ignore [missing-import]
from chatbots import (
    generate_aptitude_mcq,
    get_tech_question,
    next_difficulty,
    get_coding_challenge,
    run_coding_tests,
    generate_project_ideas,
    STATIC_PROJECT_STARTERS,
    GD_TOPICS,
    COMM_PROMPTS,
    score_communication,
    TECH_TOPICS,
    friendly_correct,
    friendly_wrong,
    HR_WARM_OPENERS,
)
# pyrefly: ignore [missing-import]
from voice_ui import bot_speak, voice_mic_panel, voice_answer_box

# --- App Config ---
st.set_page_config(
    page_title="Placement Atelier",
    page_icon="❀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Darker floral night-garden theme ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Outfit:wght@300;400;500;600&display=swap');

    :root {
        --night: #07040a;
        --garden: #0c0710;
        --petal: #160e18;
        --rose: #a84868;
        --rose-deep: #6e1f38;
        --plum: #4a284e;
        --lilac: #9a7aad;
        --sage: #4f6a52;
        --gold: #c4925c;
        --ink: #efe4eb;
        --mute: #9e8a98;
        --glass: rgba(14, 8, 16, 0.88);
        --pin-shadow: 0 22px 50px rgba(0, 0, 0, 0.65);
    }

    html, body, [class*="css"]  {
        font-family: 'Outfit', sans-serif !important;
        color: var(--ink);
    }

    .stApp {
        background-color: #050308;
        background-image:
            radial-gradient(ellipse 85% 50% at 5% -8%, rgba(110, 31, 56, 0.72), transparent 50%),
            radial-gradient(ellipse 65% 45% at 100% 0%, rgba(74, 40, 78, 0.55), transparent 48%),
            radial-gradient(ellipse 50% 35% at 48% 108%, rgba(79, 106, 82, 0.18), transparent 50%),
            radial-gradient(circle at 78% 38%, rgba(168, 72, 104, 0.14), transparent 32%),
            radial-gradient(circle at 18% 62%, rgba(154, 122, 173, 0.1), transparent 28%),
            linear-gradient(168deg, #050308 0%, #0a0610 38%, #08050c 100%);
        background-attachment: fixed;
        color: var(--ink);
    }

    /* floral silhouette + grain */
    .stApp::before {
        content: "";
        pointer-events: none;
        position: fixed;
        inset: 0;
        z-index: 0;
        opacity: 0.09;
        background-image:
            url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 800'%3E%3Cg fill='none' stroke='%23a84868' stroke-width='1.2' opacity='0.35'%3E%3Cpath d='M120 680c40-120 80-160 140-180-60-20-90-70-100-140 50 40 110 50 160 30-30-50-30-110 0-160 20 60 70 100 140 110-40-60-40-130-10-190 40 70 120 110 200 100-50-70-50-150 10-210'/%3E%3Ccircle cx='620' cy='160' r='18'/%3E%3Ccircle cx='580' cy='200' r='10'/%3E%3Ccircle cx='200' cy='520' r='14'/%3E%3C/g%3E%3C/svg%3E"),
            url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
        background-size: min(92vw, 900px) auto, 200px 200px;
        background-position: right -40px bottom -60px, 0 0;
        background-repeat: no-repeat, repeat;
    }

    [data-testid="stHeader"] {
        background: rgba(5, 3, 8, 0.82);
        backdrop-filter: blur(18px);
        border-bottom: 1px solid rgba(168, 72, 104, 0.22);
    }

    [data-testid="stSidebar"] {
        background:
            linear-gradient(175deg, #08050c 0%, #100814 45%, #07040a 100%) !important;
        border-right: 1px solid rgba(154, 122, 173, 0.18);
        box-shadow: 12px 0 48px rgba(0,0,0,0.55);
    }
    [data-testid="stSidebar"] * { color: var(--ink) !important; }
    [data-testid="stSidebar"] .stRadio label {
        font-weight: 500;
        letter-spacing: 0.02em;
        padding: 0.4rem 0.65rem;
        border-radius: 999px;
        transition: background 0.25s ease, color 0.25s ease;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(168, 72, 104, 0.28);
    }

    .block-container {
        padding-top: 1.4rem !important;
        padding-bottom: 3rem !important;
        max-width: 1180px;
    }

    .brand-hero {
        text-align: center;
        padding: 2.5rem 1.5rem 2rem;
        margin: 0 auto 1.8rem;
        position: relative;
        animation: softRise 0.85s ease both;
    }
    .brand-mark {
        display: inline-block;
        font-family: 'Cormorant Garamond', serif;
        font-size: 0.82rem;
        letter-spacing: 0.34em;
        text-transform: uppercase;
        color: var(--gold);
        margin-bottom: 0.75rem;
    }
    .main-header {
        font-family: 'Cormorant Garamond', serif !important;
        font-size: clamp(2.4rem, 5vw, 3.6rem);
        font-weight: 600;
        color: #f6e6ee;
        line-height: 1.1;
        margin: 0 auto 0.65rem;
        letter-spacing: -0.015em;
        max-width: 13ch;
        text-shadow: 0 0 48px rgba(168, 72, 104, 0.35);
    }
    .brand-sub {
        font-family: 'Outfit', sans-serif;
        font-weight: 300;
        font-size: 1.05rem;
        color: var(--mute);
        max-width: 36rem;
        margin: 0 auto;
        line-height: 1.65;
    }
    .brand-divider {
        width: 72px;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--rose-deep), var(--rose), var(--gold), transparent);
        margin: 1.25rem auto 0;
        border-radius: 2px;
    }

    .sub-header {
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 1.95rem;
        color: #f0dde6;
        font-weight: 600;
        margin: 0.4rem 0 1rem;
        padding-bottom: 0.7rem;
        border-bottom: none;
        position: relative;
        display: inline-block;
        animation: softRise 0.7s ease 0.1s both;
    }
    .sub-header::after {
        content: "";
        position: absolute;
        left: 0; bottom: 0;
        width: 48%;
        height: 3px;
        border-radius: 3px;
        background: linear-gradient(90deg, var(--rose-deep), var(--rose), var(--gold));
    }

    .voice-banner {
        background: var(--glass);
        border: 1px solid rgba(168, 72, 104, 0.32);
        border-radius: 22px;
        padding: 1rem 1.25rem;
        margin-bottom: 1.15rem;
        color: var(--mute);
        font-size: 0.95rem;
        box-shadow: var(--pin-shadow);
        backdrop-filter: blur(14px);
        animation: softRise 0.75s ease 0.15s both;
    }

    .metric-card {
        background: linear-gradient(165deg, #140c18 0%, #0a0610 100%);
        border: 1px solid rgba(154, 122, 173, 0.22);
        padding: 1.55rem 1.1rem 1.4rem;
        border-radius: 22px;
        box-shadow: var(--pin-shadow);
        text-align: center;
        transition: transform 0.35s cubic-bezier(.2,.8,.2,1), box-shadow 0.35s ease, border-color 0.35s ease;
        position: relative;
        overflow: hidden;
        animation: softRise 0.7s ease both;
    }
    .metric-card::before {
        content: "";
        position: absolute;
        inset: 0 0 auto 0;
        height: 3px;
        background: linear-gradient(90deg, #4a1528, var(--rose), var(--gold), #4a284e);
    }
    .metric-card:hover {
        transform: translateY(-8px) scale(1.015);
        border-color: rgba(168, 72, 104, 0.5);
        box-shadow: 0 30px 60px rgba(80, 16, 36, 0.45);
    }
    .metric-card h3 {
        color: var(--mute);
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.14em;
        font-weight: 600;
        margin-bottom: 0.55rem;
    }
    .metric-card h2 {
        color: #e8b8c8;
        font-family: 'Cormorant Garamond', serif;
        font-size: 2.55rem;
        font-weight: 600;
        margin: 0;
        letter-spacing: -0.02em;
    }

    .pred-placed, .pred-not-placed {
        background: linear-gradient(165deg, #140c18, #0a0610);
        color: var(--ink);
        padding: 1.4rem 1.35rem;
        border-radius: 22px;
        box-shadow: var(--pin-shadow);
        border: 1px solid rgba(154, 122, 173, 0.22);
    }
    .pred-placed { border-top: 5px solid var(--sage); }
    .pred-not-placed { border-top: 5px solid var(--rose); }

    .recommendation-box {
        background: rgba(12, 7, 16, 0.92);
        padding: 1rem 1.15rem;
        border-radius: 18px;
        margin-top: 0.65rem;
        color: var(--ink);
        border: 1px solid rgba(168, 72, 104, 0.28);
        box-shadow: 0 14px 34px rgba(0,0,0,0.4);
        transition: transform 0.25s ease;
    }
    .recommendation-box:hover { transform: translateX(4px); }

    div[data-testid="stChatMessage"] {
        background: rgba(12, 7, 16, 0.94) !important;
        border: 1px solid rgba(154, 122, 173, 0.22);
        border-radius: 22px !important;
        padding: 0.35rem 0.65rem;
        box-shadow: 0 16px 36px rgba(0,0,0,0.45);
        margin-bottom: 0.55rem;
        color: var(--ink) !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #4a1528 0%, #a84868 50%, #4a284e 100%) !important;
        color: #fff5f8 !important;
        border: 1px solid rgba(196, 146, 92, 0.28) !important;
        border-radius: 999px !important;
        font-weight: 600 !important;
        letter-spacing: 0.03em;
        padding: 0.55rem 1.35rem !important;
        box-shadow: 0 14px 30px rgba(74, 21, 40, 0.55);
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 18px 36px rgba(168, 72, 104, 0.5) !important;
        color: #fff !important;
    }

    textarea, .stTextInput input, [data-baseweb="select"] > div,
    [data-baseweb="input"], .stNumberInput input {
        border-radius: 16px !important;
        border-color: rgba(154, 122, 173, 0.32) !important;
        background: rgba(8, 5, 12, 0.95) !important;
        color: #efe4eb !important;
    }

    [data-testid="stExpander"] {
        background: rgba(10, 6, 14, 0.9);
        border: 1px solid rgba(154, 122, 173, 0.2);
        border-radius: 18px;
        box-shadow: 0 14px 32px rgba(0,0,0,0.4);
        overflow: hidden;
    }

    h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    p, label, .stMarkdown, .stCaption {
        color: var(--ink) !important;
    }
    h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        font-family: 'Cormorant Garamond', serif !important;
        font-weight: 600 !important;
    }

    .stAlert {
        border-radius: 18px !important;
        border: 1px solid rgba(168, 72, 104, 0.32) !important;
        background: rgba(10, 6, 14, 0.94) !important;
        color: var(--ink) !important;
    }

    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(110,31,56,0.7), rgba(196,146,92,0.35), transparent);
        margin: 1.6rem 0;
    }

    [data-testid="stImage"], .stPlotlyChart, [data-testid="stPyplot"] {
        background: #0a0610;
        padding: 0.85rem;
        border-radius: 20px;
        box-shadow: var(--pin-shadow);
        border: 1px solid rgba(154, 122, 173, 0.18);
    }

    @keyframes softRise {
        from { opacity: 0; transform: translateY(14px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .brand-mark span.dot {
        display: inline-block;
        animation: pulseDot 2.6s ease-in-out infinite;
        color: var(--rose);
    }
    @keyframes pulseDot {
        0%, 100% { opacity: 0.5; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.22); }
    }

    div[role="radiogroup"] label {
        background: rgba(10, 6, 14, 0.85);
        border-radius: 999px !important;
        padding-right: 0.6rem;
        border: 1px solid rgba(154, 122, 173, 0.2);
        margin-bottom: 0.25rem;
        color: var(--ink) !important;
    }

    [data-testid="stWidgetLabel"] p { color: var(--mute) !important; }
    .stSlider label, .stSelectbox label { color: var(--mute) !important; }
</style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <div class="brand-hero">
      <div class="brand-mark"><span class="dot">❀</span> Placement Atelier · Midnight Bloom</div>
      <div class="main-header">Dark petals. Bright future.</div>
      <p class="brand-sub">Predict · practice · speak · rise — a deep floral night garden for placement skills.</p>
      <div class="brand-divider"></div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Load Data ---
@st.cache_data
def load_data():
    path = 'data/student_placement.csv'
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

df = load_data()

# --- Sidebar Navigation ---
st.sidebar.markdown(
    """
    <div style="text-align:center;padding:0.6rem 0 1rem;">
      <div style="font-family:Cormorant Garamond,serif;font-size:1.55rem;color:#efe4eb;font-weight:600;">❀ atelier</div>
      <div style="font-size:0.7rem;letter-spacing:0.22em;text-transform:uppercase;color:#c4925c;margin-top:0.25rem;">midnight bloom</div>
    </div>
    """,
    unsafe_allow_html=True,
)
page = st.sidebar.radio(
    "Go to:",
    ["Dashboard (EDA)", "Prediction Form", "Company Directory", "HR Interview Practice", "Aptitude Chatbot"],
)
st.sidebar.markdown("---")
st.sidebar.markdown("### ✦ Voice")
auto_speak = st.sidebar.toggle("Bot auto-speaks replies", value=True, key="auto_speak")
st.sidebar.caption("Chrome / Edge · allow mic when asked")

if page == "Dashboard (EDA)":
    st.markdown("<div class='sub-header'>Mood board · insights</div>", unsafe_allow_html=True)
    
    if df is not None:
        metrics = load_metrics()
        
        # Key Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"<div class='metric-card'><h3>Total Students</h3><h2>{len(df)}</h2></div>", unsafe_allow_html=True)
        with col2:
            placement_rate = (df['placement_status'] == 'Placed').mean() * 100
            st.markdown(f"<div class='metric-card'><h3>Placement Rate</h3><h2>{placement_rate:.1f}%</h2></div>", unsafe_allow_html=True)
        with col3:
            acc = metrics['accuracy'] * 100 if metrics else 0
            st.markdown(f"<div class='metric-card'><h3>Model Accuracy</h3><h2>{acc:.1f}%</h2></div>", unsafe_allow_html=True)
        with col4:
            f1 = metrics['f1_score'] * 100 if metrics else 0
            st.markdown(f"<div class='metric-card'><h3>Model F1-Score</h3><h2>{f1:.1f}%</h2></div>", unsafe_allow_html=True)
            
        st.markdown("---")
        
        # Visualizations
        st.markdown("### Soft data pins")
        
        def _style_ax(ax, fig):
            fig.patch.set_facecolor("#0a0610")
            ax.set_facecolor("#0a0610")
            for spine in ax.spines.values():
                spine.set_color("#4a284e")
            ax.tick_params(colors="#9e8a98")
            ax.title.set_color("#efe4eb")
            ax.xaxis.label.set_color("#9e8a98")
            ax.yaxis.label.set_color("#9e8a98")

        col_viz1, col_viz2 = st.columns(2)
        
        with col_viz1:
            st.subheader("Placement Distribution")
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.countplot(data=df, x='placement_status', color='#c45c7a', ax=ax)
            _style_ax(ax, fig)
            st.pyplot(fig)
            
            st.subheader("Coding Score vs Placement")
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.boxplot(data=df, x='placement_status', y='coding_score', color='#b895c9', ax=ax)
            _style_ax(ax, fig)
            st.pyplot(fig)
            
            st.subheader("Internship vs Placement")
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.countplot(data=df, x='internship', hue='placement_status', palette=['#8b2e4a', '#6e8b6e'], ax=ax)
            _style_ax(ax, fig)
            st.pyplot(fig)
            
        with col_viz2:
            st.subheader("CGPA vs Placement")
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.boxplot(data=df, x='placement_status', y='cgpa', color='#d4a574', ax=ax)
            _style_ax(ax, fig)
            st.pyplot(fig)
            
            st.subheader("Technical Score vs Placement")
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.boxplot(data=df, x='placement_status', y='technical_score', color='#6b3a6e', ax=ax)
            _style_ax(ax, fig)
            st.pyplot(fig)
            
            st.subheader("Projects vs Placement")
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.countplot(data=df, x='number_of_projects', hue='placement_status', palette=['#c45c7a', '#6e8b6e'], ax=ax)
            _style_ax(ax, fig)
            st.pyplot(fig)

        st.markdown("---")
        st.subheader("Feature Correlation Heatmap")
        fig, ax = plt.subplots(figsize=(12, 8))
        numeric_df = df.select_dtypes(include=[np.number])
        sns.heatmap(numeric_df.corr(), annot=True, cmap='magma', fmt=".2f", ax=ax, linewidths=0.5,
                    cbar_kws={"shrink": 0.7})
        _style_ax(ax, fig)
        st.pyplot(fig)
            
    else:
        st.warning("Dataset not found. Please run the data generation and training pipeline first.")

elif page == "Prediction Form":
    st.markdown("<div class='sub-header'>Predict your bloom</div>", unsafe_allow_html=True)
    st.write("Enter your details — a calm estimate of placement readiness, plus gentle skill tips.")
    
    with st.form("prediction_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            cgpa = st.number_input("CGPA", min_value=0.0, max_value=10.0, value=7.5, step=0.1)
            tenth_percentage = st.number_input("10th Percentage", min_value=0.0, max_value=100.0, value=80.0, step=1.0)
            twelfth_percentage = st.number_input("12th Percentage", min_value=0.0, max_value=100.0, value=80.0, step=1.0)
            aptitude_score = st.number_input("Aptitude Score (0-100)", min_value=0, max_value=100, value=70)
            coding_score = st.number_input("Coding Score (0-100)", min_value=0, max_value=100, value=75)
            
        with col2:
            technical_score = st.number_input("Technical Score (0-100)", min_value=0, max_value=100, value=70)
            communication_score = st.number_input("Communication Score (0-100)", min_value=0, max_value=100, value=75)
            number_of_projects = st.number_input("Number of Projects", min_value=0, max_value=10, value=2)
            internship = st.selectbox("Completed Internship?", ["Yes", "No"])
            internship_months = st.number_input("Internship Duration (Months)", min_value=0, max_value=24, value=2 if internship=="Yes" else 0)
            
        with col3:
            certifications = st.number_input("Number of Certifications", min_value=0, max_value=10, value=1)
            attendance_percentage = st.number_input("Attendance Percentage", min_value=0.0, max_value=100.0, value=85.0, step=1.0)
            backlogs = st.number_input("Number of Active Backlogs", min_value=0, max_value=10, value=0)
            extracurricular = st.selectbox("Extracurricular Activities?", ["Yes", "No"])
            
        submit_button = st.form_submit_button(label="Predict Placement")
        
    if submit_button:
        input_data = {
            'cgpa': cgpa,
            'tenth_percentage': tenth_percentage,
            'twelfth_percentage': twelfth_percentage,
            'aptitude_score': aptitude_score,
            'coding_score': coding_score,
            'technical_score': technical_score,
            'communication_score': communication_score,
            'number_of_projects': number_of_projects,
            'internship': internship,
            'internship_months': internship_months,
            'certifications': certifications,
            'attendance_percentage': attendance_percentage,
            'backlogs': backlogs,
            'extracurricular_activities': extracurricular
        }
        
        try:
            result = predict_placement(input_data)
            recommendations = get_recommendations(input_data)
            
            st.markdown("---")
            st.markdown("### Prediction Results")
            
            pred_class = result['prediction_class']
            prob = result['probability']
            prob_percent = result['probability_percent']
            
            res_col1, res_col2 = st.columns(2)
            
            with res_col1:
                if pred_class == 'Placed':
                    st.markdown(f"""
                    <div class='pred-placed'>
                        <h2>🎉 Predicted: {pred_class}</h2>
                        <p>Placement Probability: <strong>{prob_percent}</strong></p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class='pred-not-placed'>
                        <h2>⚠️ Predicted: {pred_class}</h2>
                        <p>Placement Probability: <strong>{prob_percent}</strong></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
            with res_col2:
                # Risk level
                if prob >= 0.7:
                    risk = "Low Risk"
                    risk_color = "#7B6BA8"
                elif prob >= 0.4:
                    risk = "Medium Risk"
                    risk_color = "#9B8EC4"
                else:
                    risk = "High Risk"
                    risk_color = "#C97B8A"
                    
                st.markdown(f"#### Risk Level: <span style='color:{risk_color}; font-weight:600;'>{risk}</span>", unsafe_allow_html=True)
                st.info("Disclaimer: This prediction is based on historical data and does not guarantee actual employment.")
                
            st.markdown("### Areas for Improvement")
            for rec in recommendations:
                st.markdown(f"<div class='recommendation-box'>💡 {rec}</div>", unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Error during prediction: {e}")
            st.info("Ensure the model has been trained by running 'python src/train.py'")

elif page == "Company Directory":
    st.markdown("<div class='sub-header'>Company mood board · 2026</div>", unsafe_allow_html=True)
    st.write("Explore soft pins of top tech hubs — Chennai, Bangalore, Dubai, Coimbatore.")
    
    comp_path = 'data/companies_2026.csv'
    if os.path.exists(comp_path):
        cdf = pd.read_csv(comp_path)
        
        col1, col2 = st.columns([1, 2])
        with col1:
            cities = ["All"] + list(cdf['City'].unique())
            selected_city = st.selectbox("Filter by City", cities)
            
        if selected_city != "All":
            cdf = cdf[cdf['City'] == selected_city]
            
        st.markdown("### Company Locations")
        map_data = cdf[['Latitude', 'Longitude']].rename(columns={'Latitude': 'lat', 'Longitude': 'lon'})
        st.map(map_data, color="#9B8EC4")
        
        st.markdown("### Company Profiles & Vacancies")
        for idx, row in cdf.iterrows():
            with st.expander(f"🏢 {row['Company']} ({row['City']}) — {row['Vacancies']} Vacancies"):
                st.markdown(f"**Overview:** {row['Profile']}")
                st.markdown(f"**History:** {row['History']}")
                st.markdown(f"**Skills to Improve for this Company:** <span style='color:#7B6BA8; font-weight:600;'>{row['Required_Skills']}</span>", unsafe_allow_html=True)
    else:
        st.error("Company dataset not found. Please ensure 'data/companies_2026.csv' exists.")

elif page == "HR Interview Practice":
    import random

    st.markdown("<div class='sub-header'>HR atelier · practice room</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='voice-banner'>🎙️ <b>Voice studio:</b> speak your answers, and the coach can read aloud. "
        "Toggle auto-speak in the sidebar — soft, calm, judgment-free.</div>",
        unsafe_allow_html=True,
    )
    st.write(
        "Pick a mode below. Tell me what you know (e.g. only Python) — I'll stick to that and raise the level "
        "from easy → medium → hard. Wrong answers always come with the correct explanation."
    )

    hr_mode = st.radio(
        "Practice mode",
        [
            "HR Soft Skills",
            "Group Discussion",
            "Technical Q&A",
            "Coding Test",
            "Project Ideas",
            "Communication Skills",
        ],
        horizontal=True,
        key="hr_mode_select",
    )

    if st.button("🔄 Reset this mode", key="hr_reset"):
        for k in list(st.session_state.keys()):
            if str(k).startswith("hr_"):
                del st.session_state[k]
        st.rerun()

    # ----- HR Soft Skills -----
    if hr_mode == "HR Soft Skills":
        soft_qs = [
            "Tell me a little about yourself.",
            "What is your greatest technical strength?",
            "What's one area you're actively improving?",
            "Why do you want to join our company?",
            "Where do you see yourself in 5 years?",
            "Tell me about a time you worked in a team.",
            "How do you handle pressure or tight deadlines?",
        ]
        if "hr_soft_idx" not in st.session_state:
            st.session_state.hr_soft_idx = 0
            opener = f"{random.choice(HR_WARM_OPENERS)}\n\n**Q1:** {soft_qs[0]}"
            st.session_state.hr_soft_msgs = [{"role": "assistant", "content": opener}]
            st.session_state.hr_soft_speak = opener

        for m in st.session_state.hr_soft_msgs:
            with st.chat_message(m["role"]):
                st.markdown(m["content"])

        # Always offer voice for the latest coach message (auto only once per new reply)
        last_coach = next(
            (m["content"] for m in reversed(st.session_state.hr_soft_msgs) if m["role"] == "assistant"),
            None,
        )
        if last_coach:
            do_auto = bool(st.session_state.get("hr_soft_speak")) and auto_speak
            bot_speak(last_coach, auto=do_auto, label="Coach speaking")
            st.session_state.hr_soft_speak = None

        voice_mic_panel("hr_soft")
        spoken = st.session_state.get("hr_soft_transcript", "")
        prompt = voice_answer_box("hr_soft", "Type here or record your voice above…")
        if st.button("Send answer", key="hr_soft_send") and (prompt or spoken).strip():
            text = (prompt or spoken).strip()
            st.session_state.hr_soft_msgs.append({"role": "user", "content": text})
            _, tip = score_communication(text)
            idx = st.session_state.hr_soft_idx + 1
            st.session_state.hr_soft_idx = idx
            if idx < len(soft_qs):
                reply = f"Thanks for sharing — that helps a lot!\n\n{tip}\n\n**Q{idx+1}:** {soft_qs[idx]}"
            else:
                reply = (
                    f"You wrapped the soft-skills round — proud of you!\n\n{tip}\n\n"
                    "Tip: try **Group Discussion** or **Technical Q&A** next. Use Reset to restart."
                )
            st.session_state.hr_soft_msgs.append({"role": "assistant", "content": reply})
            st.session_state.hr_soft_speak = reply
            st.session_state.pop("hr_soft_transcript", None)
            st.rerun()

    # ----- Group Discussion -----
    elif hr_mode == "Group Discussion":
        if "hr_gd" not in st.session_state:
            st.session_state.hr_gd = random.choice(GD_TOPICS)
            st.session_state.hr_gd_msgs = []
            st.session_state.hr_gd_speak = f"Group discussion topic: {st.session_state.hr_gd['topic']}"
        gd = st.session_state.hr_gd
        st.info(f"**GD Topic:** {gd['topic']}")
        st.markdown(
            f"**Points you can use (For):** {', '.join(gd['points_for'])}  \n"
            f"**Points you can use (Against):** {', '.join(gd['points_against'])}"
        )
        if st.session_state.get("hr_gd_speak"):
            do_auto = auto_speak
            bot_speak(st.session_state.hr_gd_speak, auto=do_auto, label="Moderator")
            st.session_state.hr_gd_speak = None
        elif st.session_state.hr_gd_msgs:
            last = next(
                (m["content"] for m in reversed(st.session_state.hr_gd_msgs) if m["role"] == "assistant"),
                None,
            )
            if last:
                bot_speak(last, auto=False, label="Moderator")
        else:
            bot_speak(f"Group discussion topic: {gd['topic']}", auto=False, label="Moderator")
        if st.button("Show a sample opening statement"):
            st.success(gd["sample_opening"])
            bot_speak(gd["sample_opening"], auto=True, label="Sample opening")
        if st.button("New GD topic"):
            st.session_state.hr_gd = random.choice(GD_TOPICS)
            st.session_state.hr_gd_msgs = []
            st.session_state.hr_gd_speak = f"New topic: {st.session_state.hr_gd['topic']}"
            st.rerun()

        for m in st.session_state.hr_gd_msgs:
            with st.chat_message(m["role"]):
                st.markdown(m["content"])

        voice_mic_panel("hr_gd")
        prompt = voice_answer_box("hr_gd", "Speak or type your GD point…")
        if st.button("Share my point", key="hr_gd_send") and prompt.strip():
            st.session_state.hr_gd_msgs.append({"role": "user", "content": prompt.strip()})
            score, tip = score_communication(prompt)
            peer = random.choice(
                [
                    "Interesting angle! Can you add one real-life example?",
                    "Clear point. Now try a polite counter to the opposite view.",
                    "Good structure. Conclude with a one-line summary for the group.",
                    "Nice. Invite others in: I'd love to hear other views on this.",
                ]
            )
            reply = f"{tip}\n\n**Moderator tip:** {peer}"
            st.session_state.hr_gd_msgs.append({"role": "assistant", "content": reply})
            st.session_state.hr_gd_speak = reply
            st.session_state.pop("hr_gd_transcript", None)
            st.rerun()

    # ----- Technical Q&A -----
    elif hr_mode == "Technical Q&A":
        st.caption(
            "Select only the topics you know. If you know only Python, tick Python — "
            "I'll ask easy → medium → hard questions just on that."
        )
        selected = st.multiselect(
            "Topics I know",
            TECH_TOPICS,
            default=st.session_state.get("hr_tech_topics", ["Python"]),
            key="hr_tech_topics_widget",
        )
        if not selected:
            st.warning("Pick at least one topic so I can quiz you kindly.")
        else:
            if (
                "hr_tech_q" not in st.session_state
                or st.session_state.get("hr_tech_topics") != selected
            ):
                st.session_state.hr_tech_topics = selected
                st.session_state.hr_tech_diff = "easy"
                st.session_state.hr_tech_score = 0
                st.session_state.hr_tech_total = 0
                st.session_state.hr_tech_q = get_tech_question(selected, "easy")
                st.session_state.hr_tech_feedback = None
                st.session_state.hr_tech_speak = True

            q = st.session_state.hr_tech_q
            st.markdown(
                f"**Score:** {st.session_state.hr_tech_score}/{st.session_state.hr_tech_total}  ·  "
                f"**Level:** {q['difficulty'].title()}  ·  **Topic:** {q['topic']}"
            )
            if st.session_state.get("hr_tech_feedback"):
                st.markdown(st.session_state.hr_tech_feedback)
            st.markdown(f"### {q['question']}")
            opts_read = ". ".join(f"Option {i+1}: {o}" for i, o in enumerate(q["options"]))
            if st.session_state.get("hr_tech_speak"):
                bot_speak(
                    f"{q['topic']} question, {q['difficulty']} level. {q['question']}. {opts_read}",
                    auto=auto_speak,
                    label="Technical coach",
                )
                st.session_state.hr_tech_speak = False
            else:
                if st.button("🔊 Read question aloud", key="tech_read"):
                    bot_speak(
                        f"{q['question']}. {opts_read}",
                        auto=True,
                        label="Technical coach",
                    )

            choice = st.radio("Choose one:", q["options"], key=f"tech_opt_{st.session_state.hr_tech_total}")
            if st.button("Submit answer", key="tech_submit"):
                st.session_state.hr_tech_total += 1
                correct = choice == q["answer"]
                if correct:
                    st.session_state.hr_tech_score += 1
                    fb = f"✅ {friendly_correct()} **{q['answer']}**\n\n_{q['explanation']}_"
                else:
                    fb = f"❌ {friendly_wrong()} **{q['answer']}**\n\n_{q['explanation']}_"
                st.session_state.hr_tech_feedback = fb
                st.session_state.hr_tech_last_fb = fb
                new_diff = next_difficulty(st.session_state.hr_tech_diff, correct)
                st.session_state.hr_tech_diff = new_diff
                st.session_state.hr_tech_q = get_tech_question(selected, new_diff)
                st.session_state.hr_tech_speak = True
                st.rerun()
            if st.session_state.get("hr_tech_last_fb"):
                bot_speak(st.session_state.hr_tech_last_fb, auto=auto_speak, label="Feedback")
                st.session_state.hr_tech_last_fb = None

    # ----- Coding Test -----
    elif hr_mode == "Coding Test":
        level = st.select_slider("Difficulty", options=["easy", "medium", "hard"], value="easy")
        if "hr_code_chal" not in st.session_state or st.session_state.get("hr_code_level") != level:
            st.session_state.hr_code_level = level
            st.session_state.hr_code_chal = get_coding_challenge(level)
            st.session_state.hr_code_speak = True

        chal = st.session_state.hr_code_chal
        st.markdown(f"### {chal['title']} ({level})")
        st.markdown(chal["prompt"])
        if st.session_state.get("hr_code_speak"):
            bot_speak(f"Coding challenge. {chal['title']}. {chal['prompt']}", auto=auto_speak, label="Coding coach")
            st.session_state.hr_code_speak = False
        with st.expander("Need a hint?"):
            st.write(chal["hint"])
        if st.button("New coding problem"):
            st.session_state.hr_code_chal = get_coding_challenge(level)
            st.session_state.hr_code_speak = True
            st.rerun()

        code = st.text_area(
            "Write your Python solution here",
            value=f"def {chal['check_fn']}(...):\n    # your code\n    pass\n",
            height=220,
            key="hr_code_editor",
        )
        if st.button("Run tests"):
            ok, feedback = run_coding_tests(code, chal)
            if ok:
                st.success(f"{friendly_correct()} {feedback}")
                bot_speak(feedback, auto=auto_speak, label="Result")
                if level != "hard":
                    st.info("Great — try sliding difficulty up when you're ready!")
            else:
                st.error(f"{friendly_wrong()}")
                st.markdown(feedback)
                bot_speak("Some tests failed. Check the sample solution on screen.", auto=auto_speak, label="Result")

    # ----- Project Ideas -----
    elif hr_mode == "Project Ideas":
        skills = st.multiselect(
            "Skills to tailor ideas",
            TECH_TOPICS,
            default=["Python", "ML"],
            key="hr_proj_skills",
        )
        n = st.slider("How many fresh ideas?", 5, 30, 10)
        if st.button("Generate project ideas") or "hr_proj_ideas" not in st.session_state:
            ideas = STATIC_PROJECT_STARTERS[:] + generate_project_ideas(n=n, skills=skills or ["Python"])
            random.shuffle(ideas)
            st.session_state.hr_proj_ideas = ideas[:n]
        st.markdown("### Real-time / portfolio project ideas")
        for i, idea in enumerate(st.session_state.hr_proj_ideas, 1):
            st.markdown(f"{i}. {idea}")
        if st.button("🔊 Read ideas aloud"):
            bot_speak(
                "Here are some project ideas. " + " ".join(
                    f"Idea {i}: {re.sub(r'[*_]', '', idea)}"
                    for i, idea in enumerate(st.session_state.hr_proj_ideas[:5], 1)
                ),
                auto=True,
                label="Projects",
            )
        st.caption(
            "Click **Generate project ideas** anytime for a new batch — combinations are effectively endless."
        )

    # ----- Communication Skills -----
    else:
        if "hr_comm" not in st.session_state:
            st.session_state.hr_comm = random.choice(COMM_PROMPTS)
            st.session_state.hr_comm_speak = True
        task = st.session_state.hr_comm
        st.markdown(f"### Practice prompt\n{task['prompt']}")
        st.info(f"**Coach tip:** {task['tips']}")
        if st.session_state.get("hr_comm_speak"):
            bot_speak(f"Communication practice. {task['prompt']}. Tip: {task['tips']}", auto=auto_speak, label="Comm coach")
            st.session_state.hr_comm_speak = False
        if st.button("New communication prompt"):
            st.session_state.hr_comm = random.choice(COMM_PROMPTS)
            st.session_state.hr_comm_speak = True
            st.rerun()
        voice_mic_panel("hr_comm")
        ans = voice_answer_box("hr_comm", "Speak or type your answer…", height=150)
        if st.button("Get friendly feedback"):
            if not ans.strip():
                st.warning("Write or record something first — even a rough draft helps!")
            else:
                score, tip = score_communication(ans)
                st.success(tip)
                bot_speak(tip, auto=auto_speak, label="Feedback")
                with st.expander("See a sample strong answer"):
                    st.write(task["sample"])

elif page == "Aptitude Chatbot":
    st.markdown("<div class='sub-header'>Aptitude · poll pins</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='voice-banner'>🔊 The coach can <b>read each question aloud</b>. "
        "Four soft options — wrong answers come with the key + a kind explanation.</div>",
        unsafe_allow_html=True,
    )
    st.write(
        "Every question is a **4-option poll**. Pick an answer — if you're wrong, I'll gently show the correct one and the logic."
    )

    if "apt_poll_q" not in st.session_state:
        st.session_state.apt_poll_q = generate_aptitude_mcq()
        st.session_state.apt_score = 0
        st.session_state.apt_total = 0
        st.session_state.apt_feedback = None
        st.session_state.apt_speak = True

    if st.button("🔄 New question / reset score"):
        st.session_state.apt_poll_q = generate_aptitude_mcq()
        st.session_state.apt_score = 0
        st.session_state.apt_total = 0
        st.session_state.apt_feedback = None
        st.session_state.apt_speak = True
        st.rerun()

    q = st.session_state.apt_poll_q
    st.markdown(f"**Score:** {st.session_state.apt_score} / {st.session_state.apt_total}")
    st.caption(f"Category: {q.get('category', 'Aptitude')}")
    st.markdown(f"### {q['question']}")

    opts_line = ". ".join(f"Option {chr(65+i)}: {o}" for i, o in enumerate(q["options"]))
    speak_text = f"{q['question']}. {opts_line}"
    if st.session_state.get("apt_speak"):
        bot_speak(speak_text, auto=auto_speak, label="Aptitude coach")
        st.session_state.apt_speak = False
    elif st.button("🔊 Read question again"):
        bot_speak(speak_text, auto=True, label="Aptitude coach")

    if st.session_state.apt_feedback:
        st.markdown(st.session_state.apt_feedback)

    choice = st.radio(
        "Choose one of the 4 options:",
        q["options"],
        key=f"apt_choice_{st.session_state.apt_total}_{q['question'][:24]}",
    )
    col_a, col_b = st.columns(2)
    with col_a:
        submit = st.button("✅ Submit answer", use_container_width=True)
    with col_b:
        skip = st.button("⏭ Skip to next", use_container_width=True)

    if submit:
        st.session_state.apt_total += 1
        if choice == q["answer"]:
            st.session_state.apt_score += 1
            st.session_state.apt_feedback = (
                f"✅ {friendly_correct()} **{q['answer']}**\n\n*Logic:* {q['explanation']}"
            )
        else:
            st.session_state.apt_feedback = (
                f"❌ {friendly_wrong()} **{q['answer']}**\n\n*Logic:* {q['explanation']}"
            )
        st.session_state.apt_speak_fb = st.session_state.apt_feedback
        st.session_state.apt_poll_q = generate_aptitude_mcq()
        st.session_state.apt_speak = True
        st.rerun()

    if skip:
        st.session_state.apt_feedback = (
            f"Skipped — the answer was **{q['answer']}**. _{q['explanation']}_"
        )
        st.session_state.apt_speak_fb = st.session_state.apt_feedback
        st.session_state.apt_poll_q = generate_aptitude_mcq()
        st.session_state.apt_speak = True
        st.rerun()

    if st.session_state.get("apt_speak_fb"):
        bot_speak(st.session_state.apt_speak_fb, auto=auto_speak, label="Feedback")
        st.session_state.apt_speak_fb = None

