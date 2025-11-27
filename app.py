import streamlit as st
import pandas as pd
import random
import datetime
import base64
import io
from gtts import gTTS

# --- 1. DATA: EXERCISE LIBRARY ---
# Hardcoded data so no external JSON file is needed
EXERCISE_LIBRARY = [
  {
    "id": "seated_shoulder_press",
    "title": "Seated Shoulder Press",
    "category": "Seated Strength",
    "tags": ["wheelchair user", "limited lower-body mobility", "upper body", "strength", "resistance bands", "light weights"],
    "intensity": "moderate",
    "instructions": [
      "Sit upright with your back supported.",
      "Hold weights or resistance band handles at shoulder height, elbows bent.",
      "Push your hands up towards the ceiling until arms are fully extended.",
      "Slowly lower back to the starting position."
    ],
    "safety_note": "Keep your core engaged to protect your lower back. Stop if you feel sharp pain.",
    "calories": 40,
    "duration_minutes": 5
  },
  {
    "id": "seated_march",
    "title": "Seated High Knees",
    "category": "Cardio for Wheelchair Users",
    "tags": ["wheelchair user", "limited lower-body mobility", "cardio", "endurance", "none"],
    "intensity": "energetic",
    "instructions": [
      "Sit tall in your chair.",
      "Lift one knee as high as comfortable, then lower it.",
      "Lift the other knee.",
      "Repeat in a rhythmic marching motion. Pump your arms for extra intensity."
    ],
    "safety_note": "Ensure your chair is stable and brakes are on.",
    "calories": 60,
    "duration_minutes": 10
  },
  {
    "id": "wall_pushup",
    "title": "Wall Push-Ups",
    "category": "Upper Body Only",
    "tags": ["limited lower-body mobility", "strength", "balance", "none"],
    "intensity": "moderate",
    "instructions": [
      "Stand facing a wall, arm-length away.",
      "Place palms on the wall at shoulder height.",
      "Bend elbows to bring your chest towards the wall.",
      "Push back to the starting position."
    ],
    "safety_note": "Ensure non-slip footwear. Keep your body in a straight line.",
    "calories": 50,
    "duration_minutes": 5
  },
  {
    "id": "neck_stretches",
    "title": "Gentle Neck Release",
    "category": "Mobility & Stretch",
    "tags": ["visual impairment", "neurodivergent support", "mobility", "gentle", "none", "chair"],
    "intensity": "gentle",
    "instructions": [
      "Sit or stand comfortably.",
      "Slowly tilt your right ear towards your right shoulder.",
      "Hold for 10 seconds. Breathe deeply.",
      "Return to center and repeat on the left side."
    ],
    "safety_note": "Move slowly. Do not force your head down.",
    "calories": 10,
    "duration_minutes": 3
  },
  {
    "id": "band_pull_apart",
    "title": "Resistance Band Pull-Aparts",
    "category": "Upper Body Only",
    "tags": ["wheelchair user", "strength", "resistance bands"],
    "intensity": "moderate",
    "instructions": [
      "Hold a resistance band with both hands in front of you at shoulder height.",
      "Keep arms straight and pull the band apart by squeezing your shoulder blades together.",
      "Return to center with control."
    ],
    "safety_note": "Don't shrug your shoulders. Keep neck relaxed.",
    "calories": 45,
    "duration_minutes": 5
  },
  {
    "id": "chair_squats",
    "title": "Sit-to-Stand",
    "category": "Lower Body Only",
    "tags": ["limited upper-body mobility", "strength", "balance", "chair"],
    "intensity": "energetic",
    "instructions": [
      "Sit on the edge of a sturdy chair.",
      "Lean slightly forward and stand up using your legs.",
      "Slowly lower yourself back down to the seat.",
      "Repeat."
    ],
    "safety_note": "Ensure the chair will not slide backwards.",
    "calories": 70,
    "duration_minutes": 8
  }
]

QUOTES = [
    "Small steps every day lead to big changes.",
    "Listen to your body, it knows what it can do.",
    "Your pace is the best pace.",
    "Fitness is for everybody and every body.",
    "You showed up today, and that is a victory.",
    "Focus on what you CAN do."
]

# --- 2. UTILS: ACCESSIBILITY & LOGIC ---

def apply_accessibility_styles(mode_active):
    """Injects CSS based on whether Accessibility Mode is active."""
    if mode_active:
        st.markdown(
            """
            <style>
            html, body, [class*="css"] { font-size: 22px !important; font-family: 'Arial', sans-serif !important; }
            .stApp { background-color: #000000 !important; color: #FFFFFF !important; }
            .stButton > button { 
                background-color: #FFFF00 !important; color: #000000 !important; 
                border: 4px solid #FFFFFF !important; font-weight: bold !important; 
                font-size: 24px !important; padding: 15px !important; 
            }
            div[data-testid="stMetric"], div[data-testid="stExpander"] {
                background-color: #222222 !important; border: 2px solid #FFFF00 !important; color: #FFFFFF !important;
            }
            h1, h2, h3 { color: #FFFF00 !important; text-decoration: underline; }
            .stSuccess { background-color: #222222 !important; color: #FFFF00 !important; }
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <style>
            .stApp { background-color: #F0F8FF; }
            .stButton > button { background-color: #4CAF50; color: white; border-radius: 12px; border: none; font-weight: bold; }
            h1, h2, h3 { color: #2C3E50; }
            </style>
            """,
            unsafe_allow_html=True
        )

def get_audio_html(text):
    """Generates an HTML audio player using gTTS in memory."""
    try:
        tts = gTTS(text=text, lang='en')
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        audio_base64 = base64.b64encode(mp3_fp.read()).decode()
        return f'<audio controls src="data:audio/mp3;base64,{audio_base64}"></audio>'
    except Exception as e:
        return "Audio unavailable"

def generate_workout_plan(user_profile):
    """Simple rule-based logic to select suitable exercises."""
    plan = []
    disability = user_profile.get('disability', [])
    equipment = user_profile.get('equipment', [])
    goal = user_profile.get('goal', 'mobility')
    
    suitable_exercises = []
    
    for ex in EXERCISE_LIBRARY:
        score = 0
        # Positive Match for Disability needs
        if any(tag in ex['tags'] for tag in disability):
            score += 2
            
        # Equipment Check
        required_eq = [t for t in ex['tags'] if t in ["resistance bands", "light weights", "chair"]]
        has_eq = all(eq in equipment for eq in required_eq)
        
        if has_eq or "none" in ex['tags']:
            score += 1
        else:
            score = -10 # Strict penalty if equipment missing
            
        # Goal Match
        if goal in ex['tags'] or goal in ex['category'].lower():
            score += 1
            
        if score > 0:
            suitable_exercises.append(ex)
    
    # Return up to 3 exercises
    if len(suitable_exercises) >= 3:
        return random.sample(suitable_exercises, 3)
    return suitable_exercises

def update_streak():
    today = datetime.date.today()
    if 'last_workout_date' not in st.session_state:
        st.session_state.streak = 1
    else:
        last_date = st.session_state.last_workout_date
        delta = (today - last_date).days
        if delta == 1:
            st.session_state.streak += 1
        elif delta > 1:
            st.session_state.streak = 1 
    st.session_state.last_workout_date = today

def check_badges():
    badges = []
    s = st.session_state.get('streak', 0)
    if s >= 1: badges.append("🏅 First Step")
    if s >= 3: badges.append("🔥 3-Day Streak")
    if s >= 7: badges.append("🏆 Week Warrior")
    return badges

# --- 3. COMPONENTS ---

def render_onboarding():
    st.header("Welcome to FitBod 👋")
    st.write("Let's build a plan that works for *you*.")
    
    with st.form("onboarding_form"):
        st.subheader("1. About You")
        disability = st.multiselect(
            "I identify with / require support for:",
            ["wheelchair user", "limited upper-body mobility", "limited lower-body mobility", "visual impairment", "neurodivergent support"]
        )
        
        st.subheader("2. Your Goal")
        goal = st.selectbox("Main focus?", ["strength", "mobility", "balance", "endurance", "confidence building"])
        
        st.subheader("3. Equipment")
        equipment = st.multiselect("What do you have available?", ["resistance bands", "light weights", "chair"])
        
        st.subheader("4. Motivation Style")
        style = st.select_slider("Coaching style?", ["gentle", "direct", "energetic"])
        
        submitted = st.form_submit_button("Create My Plan")
        
        if submitted:
            st.session_state.user_profile = {
                "disability": disability, "goal": goal, 
                "equipment": equipment, "style": style, "onboarded": True
            }
            st.success("Profile Saved! Generating...")
            st.rerun()

def render_workout_card(exercise, show_audio=False):
    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(exercise['title'])
            st.caption(f"Category: {exercise['category']} | Intensity: {exercise['intensity'].title()}")
        with col2:
            st.metric("Time", f"{exercise['duration_minutes']} m")
            
        st.write("---")
        st.markdown("**Instructions:**")
        for i, step in enumerate(exercise['instructions']):
            st.write(f"{i+1}. {step}")
            
        st.info(f"🛡️ **Safety Note:** {exercise['safety_note']}")
        
        if show_audio:
            if st.button(f"🔊 Read {exercise['title']}", key=f"aud_{exercise['id']}"):
                text = f"{exercise['title']}. {'. '.join(exercise['instructions'])}. Safety note: {exercise['safety_note']}"
                st.markdown(get_audio_html(text), unsafe_allow_html=True)

# --- 4. MAIN APP EXECUTION ---

# Page Config
st.set_page_config(page_title="FitBod - Accessible Fitness", page_icon="🥑", layout="wide", initial_sidebar_state="collapsed")

# Session State Init
if 'user_profile' not in st.session_state: st.session_state.user_profile = None
if 'streak' not in st.session_state: st.session_state.streak = 0
if 'accessibility_mode' not in st.session_state: st.session_state.accessibility_mode = False

# Sidebar Toggle for Accessibility
with st.sidebar:
    st.title("Settings")
    mode = st.toggle("♿ Accessibility Mode", value=st.session_state.accessibility_mode)
    if mode != st.session_state.accessibility_mode:
        st.session_state.accessibility_mode = mode
        st.rerun()

apply_accessibility_styles(st.session_state.accessibility_mode)

# Main Title
st.title("FitBod 🥑")

# App Routing
if not st.session_state.user_profile:
    render_onboarding()
else:
    # Navigation
    if not st.session_state.accessibility_mode:
        # Standard Sidebar Nav
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Go to", ["Daily Dashboard", "Exercise Library", "My Progress"])
    else:
        # Accessible Top Nav (easier for screen readers than sidebar sometimes)
        page = st.radio("Navigation", ["Daily Dashboard", "Exercise Library", "My Progress"], horizontal=True)

    user_profile = st.session_state.user_profile

    # --- DASHBOARD ---
    if page == "Daily Dashboard":
        st.header(f"Today's Plan")
        
        # Motivation
        quote = random.choice(QUOTES)
        style = user_profile['style']
        ai_msg = "Take your time. Breathing is important." if style == "gentle" else "Let's crush it!" if style == "energetic" else "Consistency is key."
        
        with st.expander("💡 Motivation & Safety", expanded=True):
            st.markdown(f"**Quote:** *{quote}*")
            st.markdown(f"**Coach:** {ai_msg}")

        # Plan Generation
        todays_plan = generate_workout_plan(user_profile)
        
        if not todays_plan:
            st.warning("No perfect matches found for your equipment, showing general mobility.")
            todays_plan = [ex for ex in EXERCISE_LIBRARY if "mobility" in ex['tags']][:2]

        st.subheader("Your Routine")
        for ex in todays_plan:
            render_workout_card(ex, show_audio=st.session_state.accessibility_mode)
            
        st.write("---")
        if st.button("✅ I Completed Today's Workout", use_container_width=True):
            update_streak()
            st.balloons()
            st.success("Great job! Streak updated.")

    # --- LIBRARY ---
    elif page == "Exercise Library":
        st.header("Explore Exercises")
        df = pd.DataFrame(EXERCISE_LIBRARY)
        cat_filter = st.multiselect("Filter by Category", options=df['category'].unique())
        
        filtered_libs = [ex for ex in EXERCISE_LIBRARY if ex['category'] in cat_filter] if cat_filter else EXERCISE_LIBRARY
        
        for ex in filtered_libs:
            render_workout_card(ex, show_audio=st.session_state.accessibility_mode)

    # --- PROGRESS ---
    elif page == "My Progress":
        st.header("Your Journey")
        col1, col2 = st.columns(2)
        col1.metric("Current Streak", f"{st.session_state.streak} Days")
        col2.metric("Workouts Completed", st.session_state.streak)
        
        st.subheader("Badges")
        badges = check_badges()
        if badges:
            for b in badges: st.success(b)
        else:
            st.info("Complete workouts to earn badges!")
            
        st.subheader("Journal")
        st.text_area("How did you feel today?", placeholder="I felt stronger...")
        if st.button("Save Entry"):
            st.success("Entry saved!")
