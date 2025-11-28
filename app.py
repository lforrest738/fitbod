import streamlit as st
import pandas as pd
import numpy as np
import random
import datetime
import base64
import io
import time
from gtts import gTTS

# --- 1. CONFIGURATION & DATA ---

st.set_page_config(
    page_title="FitBod - Accessible Fitness",
    page_icon="🥑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- EXERCISE LIBRARY ---
EXERCISE_LIBRARY = [
  {
    "id": "seated_shoulder_press",
    "title": "Seated Shoulder Press",
    "category": "Seated Strength",
    "tags": ["Wheelchair User", "Limited Lower-Body Mobility", "Upper Body", "Strength", "Resistance Bands", "Light Weights"],
    "intensity": "Moderate",
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
    "tags": ["Wheelchair User", "Limited Lower-Body Mobility", "Cardio", "Endurance", "None"],
    "intensity": "Energetic",
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
    "tags": ["Limited Lower-Body Mobility", "Strength", "Balance", "None"],
    "intensity": "Moderate",
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
    "tags": ["Visual Impairment", "Neurodivergent Support", "Mobility", "Gentle", "None", "Chair"],
    "intensity": "Gentle",
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
    "tags": ["Wheelchair User", "Strength", "Resistance Bands"],
    "intensity": "Moderate",
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
    "tags": ["Limited Upper-Body Mobility", "Strength", "Balance", "Chair"],
    "intensity": "Energetic",
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
    "Focus on what you CAN do.",
    "Believe in yourself and all that you are."
]

# --- 2. STYLE & THEME ENGINE ---

def inject_custom_css(mode_active):
    """
    Injects CSS. 
    Standard Mode: Opal-Inspired Dark Theme (Black, Dark Grey, Neon Accents).
    Accessibility Mode: High Contrast, Large Text (Yellow on Black).
    """
    if mode_active:
        # --- ACCESSIBILITY MODE (High Contrast) ---
        st.markdown(
            """
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&display=swap');
            
            html, body, [class*="css"], p, div, h1, h2, h3 { 
                font-size: 24px !important; 
                font-family: 'Atkinson Hyperlegible', sans-serif !important; 
                line-height: 1.6 !important;
                color: #FFFFFF !important;
            }
            .stApp { background-color: #000000 !important; }
            
            /* High Contrast Interactive Elements */
            .stButton > button { 
                background-color: #FFFF00 !important; 
                color: #000000 !important; 
                border: 4px solid #FFFFFF !important; 
                font-weight: bold !important; 
                font-size: 26px !important; 
                padding: 20px !important; 
                border-radius: 0px !important;
                margin-bottom: 15px !important;
            }
            .stButton > button:hover {
                background-color: #FFFFFF !important;
                border-color: #FFFF00 !important;
            }
            
            /* High Contrast Containers */
            div[data-testid="stMetric"], div[data-testid="stExpander"], div[data-testid="stContainer"] {
                background-color: #1a1a1a !important; 
                border: 3px solid #FFFF00 !important; 
                border-radius: 0px !important;
            }
            
            h1, h2, h3, h4 { 
                color: #FFFF00 !important; 
                text-decoration: underline; 
                text-transform: uppercase;
                letter-spacing: 2px;
            }
            .stSuccess, .stInfo, .stWarning { 
                background-color: #333333 !important; 
                color: #FFFF00 !important; 
                border-left: 10px solid #FFFFFF !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        # --- OPAL INSPIRED DARK MODE ---
        st.markdown(
            """
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Poppins:wght@500;700&display=swap');
            
            /* Global Reset & Font */
            html, body, [class*="css"] {
                font-family: 'Inter', sans-serif;
                color: #E2E8F0; /* Off-white text */
                background-color: #000000;
            }
            
            /* Background */
            .stApp {
                background-color: #000000;
            }
            
            /* Headers */
            h1, h2, h3 {
                font-family: 'Poppins', sans-serif;
                color: #F8FAFC;
                font-weight: 700;
            }
            
            h1 {
                background: linear-gradient(120deg, #4ade80, #38bdf8); /* Neon Green to Blue */
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            
            /* Modern Dark Cards */
            div[data-testid="stContainer"], div[data-testid="stMetric"], div[data-testid="stExpander"] {
                background: #1C1C1E; /* Dark Grey Surface */
                border-radius: 20px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
                border: 1px solid #333333;
                padding: 1.5rem;
            }
            
            div[data-testid="stContainer"]:hover {
                border: 1px solid #4ade80; /* Hover Green Border */
                transform: translateY(-2px);
                transition: all 0.2s ease;
            }
            
            /* Metrics */
            div[data-testid="stMetric"] label {
                color: #94A3B8; /* Muted text */
                font-size: 0.9rem;
            }
            div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
                color: #38bdf8; /* Light Blue */
                font-weight: 800;
            }
            
            /* Primary Buttons */
            .stButton > button {
                background: linear-gradient(to right, #4ade80, #22c55e); /* Green Gradient */
                color: #000000;
                border: none;
                border-radius: 12px;
                padding: 0.6rem 1.2rem;
                font-weight: 700;
                letter-spacing: 0.5px;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                box-shadow: 0 0 15px rgba(74, 222, 128, 0.3); /* Glow effect */
                width: 100%;
            }
            
            .stButton > button:hover {
                background: linear-gradient(to right, #22c55e, #16a34a);
                transform: scale(1.02);
                box-shadow: 0 0 20px rgba(74, 222, 128, 0.5);
                color: #000000 !important;
            }
            
            .stButton > button:active {
                transform: scale(0.98);
            }
            
            /* Premium Button Style (Gold/Orange) */
            button[kind="secondary"] {
                background: linear-gradient(135deg, #facc15 0%, #eab308 100%);
                color: black !important;
                border: none;
                font-weight: bold;
            }

            /* Inputs */
            .stTextInput input, .stSelectbox div[data-baseweb="select"], .stMultiSelect div[data-baseweb="select"] {
                background-color: #27272a;
                border: 1px solid #3f3f46;
                border-radius: 12px;
                color: #ffffff;
            }
            
            /* Navigation Bar Simulation */
            div[data-testid="column"] button {
                background: transparent;
                color: #94A3B8;
                box-shadow: none;
                border: 1px solid transparent;
            }
            
            div[data-testid="column"] button:hover {
                background: #27272a;
                color: #4ade80; /* Hover Green */
                box-shadow: none;
                transform: none;
                border: 1px solid #4ade80;
            }

            /* Expander Header */
            .streamlit-expanderHeader {
                font-family: 'Poppins', sans-serif;
                color: #E2E8F0;
                font-weight: 600;
                background-color: #1C1C1E;
            }
            
            /* Success/Info Messages */
            .stSuccess, .stInfo, .stWarning {
                border-radius: 12px;
                border: none;
                color: #ffffff;
            }
            .stSuccess {
                background-color: rgba(74, 222, 128, 0.1);
                border: 1px solid #4ade80;
                color: #4ade80;
            }
            .stInfo {
                background-color: rgba(56, 189, 248, 0.1);
                border: 1px solid #38bdf8;
                color: #38bdf8;
            }
            
            /* Charts */
            canvas {
                filter: invert(1) hue-rotate(180deg);
            }
            </style>
            """,
            unsafe_allow_html=True
        )

# --- 3. UTILITIES & LOGIC ---

def get_audio_html(text):
    try:
        tts = gTTS(text=text, lang='en')
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        audio_base64 = base64.b64encode(mp3_fp.read()).decode()
        return f'<audio controls src="data:audio/mp3;base64,{audio_base64}" style="width: 100%; margin-top: 10px;"></audio>'
    except:
        return "<small>Audio unavailable in offline mode.</small>"

def generate_workout_plan(user_profile):
    disability = user_profile.get('disability', [])
    equipment = user_profile.get('equipment', [])
    goal = user_profile.get('goal', 'Mobility')
    
    suitable = []
    for ex in EXERCISE_LIBRARY:
        score = 0
        if any(tag in ex['tags'] for tag in disability): score += 2
        
        required_eq = [t for t in ex['tags'] if t in ["Resistance Bands", "Light Weights", "Chair"]]
        has_eq = all(eq in equipment for eq in required_eq)
        
        if has_eq or "None" in ex['tags']: score += 1
        else: score = -10
            
        if goal in ex['tags'] or goal in ex['category']: score += 1
        
        if score > 0: suitable.append(ex)
    
    if len(suitable) >= 3: return random.sample(suitable, 3)
    return suitable

def generate_dummy_history():
    """Generates 30 days of dummy workout data for charts."""
    dates = pd.date_range(end=datetime.date.today(), periods=30)
    data = {
        "Date": dates,
        "Minutes": np.random.randint(15, 60, size=30),
        "Calories": np.random.randint(100, 400, size=30),
        "Mood": np.random.choice(["Energized", "Tired", "Happy", "Strong"], size=30)
    }
    # Add some zeros to simulate rest days
    mask = np.random.choice([True, False], size=30, p=[0.2, 0.8])
    data["Minutes"][mask] = 0
    data["Calories"][mask] = 0
    
    return pd.DataFrame(data)

def get_greeting(name):
    hour = datetime.datetime.now().hour
    if hour < 12: msg = "Good Morning"
    elif hour < 18: msg = "Good Afternoon"
    else: msg = "Good Evening"
    return f"{msg}, {name}!" if name else msg

# --- 4. NAVIGATION HANDLER ---

def navigate_to(page):
    st.session_state.current_page = page
    st.rerun()

def render_navbar():
    """Renders a modern top navigation bar using columns and buttons."""
    st.markdown("---")
    # 6 columns to accommodate the new Premium/Nutrition tab
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        if st.button("🏠 Home", use_container_width=True):
            navigate_to("Dashboard")
    with col2:
        if st.button("💪 Library", use_container_width=True):
            navigate_to("Library")
    with col3:
        if st.button("📈 Progress", use_container_width=True):
            navigate_to("Progress")
    with col4:
        if st.button("🥦 Nutrition", use_container_width=True): # New Premium Hook
            navigate_to("Nutrition")
    with col5:
        if st.button("🤝 Sponsors", use_container_width=True): 
            navigate_to("Sponsors")
    with col6:
        if st.button("⚙️ Settings", use_container_width=True):
            navigate_to("Settings")
    st.markdown("---")

# --- 5. COMPONENTS ---

def render_onboarding(is_edit=False):
    profile = st.session_state.user_profile if is_edit else {}
    
    if is_edit:
        st.header("✏️ Edit Your Profile")
        btn_label = "Update Profile"
        # Standard container for Edit Mode
        container = st.container(border=True)
    else:
        # --- NEW FANCIER FIRST SCREEN ---
        st.markdown(
            """
            <div style="text-align: center; padding: 40px 0; background: radial-gradient(circle, rgba(74,222,128,0.1) 0%, rgba(0,0,0,0) 70%); border-radius: 20px; margin-bottom: 30px;">
                <h1 style="font-size: 4rem; margin-bottom: 0;">FitBod 🥑</h1>
                <h3 style="font-weight: 300; font-style: italic; color: #94A3B8; margin-top: 10px;">Empowering Movement. No Limits.</h3>
                <p style="font-size: 1.2rem; color: #CBD5E1; max-width: 600px; margin: 20px auto;">
                    Your personalized, adaptive fitness companion. Designed for every body, every ability, and every goal.
                </p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        st.markdown("### Let's design your journey 👇")
        btn_label = "Start My Journey"
        container = st.container(border=True)

    with container:
        with st.form("profile_form"):
            # 1. Basics
            st.subheader("1. The Basics")
            col_basic1, col_basic2 = st.columns(2)
            with col_basic1:
                name = st.text_input("First Name", value=profile.get("name", ""))
            with col_basic2:
                age_group = st.selectbox(
                    "Age Category", 
                    ["Under 18", "18-24", "25-34", "35-44", "45-54", "55-64", "65+"],
                    index=2 if not profile else ["Under 18", "18-24", "25-34", "35-44", "45-54", "55-64", "65+"].index(profile.get("age_group", "25-34"))
                )

            # 2. Comprehensive Access Needs
            st.subheader("2. Access & Mobility Needs")
            st.caption("Select all that apply. We use this to filter unsafe exercises.")
            
            access_options = [
                "Wheelchair User (Manual)",
                "Wheelchair User (Power)",
                "Limited Upper-Body Mobility",
                "Limited Lower-Body Mobility",
                "Limited Grip Strength",
                "Balance Issues / Vertigo",
                "Chronic Pain / Fatigue",
                "Visual Impairment (Low Vision)",
                "Visual Impairment (Blind)",
                "Neurodivergent (Autism/ADHD)",
                "Sensory Sensitivity (Low Noise)",
                "Post-Injury Recovery",
                "None / General Fitness"
            ]
            
            disability_default = profile.get("disability", [])
            # Filter default to ensure they exist in new options list to avoid errors
            safe_default = [x for x in disability_default if x in access_options]
            
            disability = st.multiselect(
                "I identify with / require support for:",
                access_options,
                default=safe_default
            )

            # 3. Goals & Equipment
            col_a, col_b = st.columns(2)
            with col_a:
                st.subheader("3. Fitness Goal")
                goal_opts = ["Strength", "Mobility & Flexibility", "Balance & Stability", "Cardiovascular Health", "Weight Management", "Mental Wellbeing", "Confidence Building"]
                try:
                    idx = goal_opts.index(profile.get("goal", "Mobility & Flexibility"))
                except:
                    idx = 1
                goal = st.selectbox("Main Focus", goal_opts, index=idx)
            
            with col_b:
                st.subheader("4. Available Equipment")
                eq_opts = ["Resistance Bands", "Light Weights (Dumbbells)", "Heavy Weights", "Chair (Sturdy)", "Yoga Mat", "None (Bodyweight Only)"]
                # Sanitize defaults
                def_eq = profile.get("equipment", [])
                safe_eq = [x for x in def_eq if x in eq_opts]
                equipment = st.multiselect("Select what you have:", eq_opts, default=safe_eq)

            # 5. Lifestyle & Preferences (Premium Hook Data)
            st.subheader("5. Lifestyle & Preferences")
            col_l1, col_l2 = st.columns(2)
            with col_l1:
                style_idx = ["Gentle", "Direct", "Energetic"].index(profile.get("style", "Gentle")) if "style" in profile else 0
                style = st.select_slider("Coaching Style", ["Gentle", "Direct", "Energetic"], value=["Gentle", "Direct", "Energetic"][style_idx])
            with col_l2:
                diet_opts = ["No Preference", "Vegetarian", "Vegan", "Gluten-Free", "Keto", "High Protein"]
                diet_def = profile.get("diet", "No Preference")
                diet = st.selectbox("Dietary Preference (for Meal Plans)", diet_opts, index=diet_opts.index(diet_def) if diet_def in diet_opts else 0)

            submitted = st.form_submit_button(btn_label, use_container_width=True)
            
            if submitted:
                if not name:
                    st.error("Please enter your name!")
                else:
                    st.session_state.user_profile = {
                        "name": name,
                        "age_group": age_group,
                        "disability": disability,
                        "goal": goal,
                        "equipment": equipment,
                        "style": style,
                        "diet": diet
                    }
                    st.session_state.current_page = "Dashboard"
                    if 'current_plan' in st.session_state: del st.session_state.current_plan
                    st.rerun()

def render_workout_card(exercise):
    """Modern Card Design for exercises"""
    with st.container():
        # Header
        c1, c2 = st.columns([3, 1])
        with c1:
            st.markdown(f"### {exercise['title']}")
            st.markdown(f"**{exercise['category']}** • *{exercise['intensity'].title()} Intensity*")
        with c2:
            st.markdown(f"## ⏱️ {exercise['duration_minutes']}m")
        
        st.divider()
        
        # Content
        ic1, ic2 = st.columns([2, 1])
        with ic1:
            st.markdown("#### Instructions")
            for i, step in enumerate(exercise['instructions']):
                st.write(f"**{i+1}.** {step}")
        
        with ic2:
            st.markdown("#### Safety First 🛡️")
            st.info(exercise['safety_note'])
            st.markdown(f"🔥 **{exercise['calories']} kcal**")
        
        # Audio Player
        if st.session_state.accessibility_mode:
            text = f"{exercise['title']}. {'. '.join(exercise['instructions'])}."
            st.markdown(get_audio_html(text), unsafe_allow_html=True)

# --- 6. PAGE RENDERERS ---

def render_dashboard():
    profile = st.session_state.user_profile
    greeting = get_greeting(profile.get('name', 'Friend'))
    
    # 1. Hero Section & Motivation
    col_head, col_img = st.columns([3, 1])
    with col_head:
        st.title(greeting)
        
        # PROMINENT QUOTE DISPLAY
        quote = random.choice(QUOTES)
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #1C1C1E 0%, #27272a 100%); padding: 20px; border-radius: 10px; border: 1px solid #333; margin-bottom: 20px;">
                <h3 style="color: #4ade80; margin:0; font-family: 'Poppins', sans-serif;">✨ Daily Motivation</h3>
                <p style="font-size: 1.3em; font-style: italic; margin-top: 10px; color: #E2E8F0;">"{quote}"</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        # Display Goal Tag
        st.markdown(f"**Current Focus:** `{profile.get('goal', 'General Fitness')}`")
    with col_img:
        st.metric("Current Streak", f"🔥 {st.session_state.streak}")

    # 2. Quick Actions
    with st.container():
        hc1, hc2, hc3 = st.columns(3)
        with hc1:
            st.metric("Hydration Tracker 💧", f"{st.session_state.hydration} / 8 glasses")
        with hc2:
            if st.button("➕ Drink Water", use_container_width=True):
                st.session_state.hydration += 1
                st.rerun()
        with hc3:
            if st.button("🔄 New Routine", use_container_width=True):
                st.session_state.current_plan = generate_workout_plan(profile)
                st.session_state.workout_completed = False # Reset state
                st.rerun()

    st.markdown("---")

    # 3. Post-Workout Logic OR Workout View
    if st.session_state.workout_completed:
        # POST WORKOUT VIEW
        st.balloons()
        st.markdown("## 🎉 Amazing Job, " + profile.get('name', 'Friend') + "!")
        st.success("You've completed your daily routine. Take a moment to rest and reflect.")
        
        c1, c2 = st.columns(2)
        with c1:
            st.info("💡 **Tip:** Tracking how you feel helps us adjust future intensity.")
            feeling = st.text_area("How are you feeling?", key="journal_input", placeholder="I feel energized / tired / proud...")
            
            # Action Buttons Row
            col_save, col_view = st.columns([1, 1])
            with col_save:
                if st.button("💾 Save to Journal"):
                    if feeling:
                        entry = {
                            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "note": feeling
                        }
                        st.session_state.journal_entries.append(entry)
                        st.session_state.last_saved_feeling = True # Flag to show success
                        st.toast("Journal Entry Saved!")
                    else:
                        st.error("Please write something to save!")
            
            # Show success and offer navigation if saved
            if st.session_state.get('last_saved_feeling', False):
                with col_view:
                    st.success("Saved!")
                if st.button("📖 View in Progress Tab"):
                    st.session_state.last_saved_feeling = False # Reset
                    navigate_to("Progress")
        
        with c2:
            st.markdown("### What's Next?")
            if st.button("📈 View Progress Stats", use_container_width=True):
                navigate_to("Progress")
            
            st.write("")
            if st.button("🔄 Generate Another Workout", use_container_width=True):
                st.session_state.workout_completed = False
                st.session_state.current_plan = generate_workout_plan(profile)
                st.rerun()

    else:
        # WORKOUT CARD VIEW
        st.markdown("### Today's Personalized Plan")
        
        if 'current_plan' not in st.session_state:
            st.session_state.current_plan = generate_workout_plan(profile)
            
        plan = st.session_state.current_plan
        
        if not plan:
            st.warning("We're adjusting parameters to find the best fit. Here is a mobility starter.")
            plan = [ex for ex in EXERCISE_LIBRARY if "Mobility" in ex['tags']][:2]

        # Render Cards
        for ex in plan:
            render_workout_card(ex)
            st.write("") # spacer

        if st.button("✅ Complete Workout", type="primary", use_container_width=True):
            st.session_state.streak += 1
            st.session_state.workout_completed = True # TRIGGER POST WORKOUT VIEW
            st.rerun()

def render_library():
    st.title("📚 Exercise Library")
    st.write("Browse all accessible exercises.")
    
    col_search, col_filter = st.columns([2, 1])
    with col_search:
        search_term = st.text_input("Search exercises...", placeholder="e.g. 'shoulder'")
    with col_filter:
        cat_filter = st.selectbox("Category", ["All"] + list(set(e['category'] for e in EXERCISE_LIBRARY)))
    
    filtered = EXERCISE_LIBRARY
    if cat_filter != "All":
        filtered = [e for e in filtered if e['category'] == cat_filter]
    if search_term:
        filtered = [e for e in filtered if search_term.lower() in e['title'].lower()]
        
    for ex in filtered:
        render_workout_card(ex)

def render_progress():
    st.title("📈 Your Progress")
    
    # Generate Dummy Data
    if 'history_data' not in st.session_state:
        st.session_state.history_data = generate_dummy_history()
    
    df = st.session_state.history_data
    
    # Summary Metrics
    total_mins = df['Minutes'].sum() + (st.session_state.streak * 15)
    total_cals = df['Calories'].sum() + (st.session_state.streak * 120)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Total Active Mins", f"{total_mins}")
    with c2:
        st.metric("Calories Burned", f"{total_cals}")
    with c3:
        st.metric("Workouts Logged", f"{len(df[df['Minutes'] > 0])}")

    st.markdown("---")
    
    col_charts1, col_charts2 = st.columns(2)
    
    with col_charts1:
        st.subheader("🔥 Activity Trends (Mins)")
        st.area_chart(df.set_index("Date")["Minutes"], color="#4ade80") # Green
        
    with col_charts2:
        st.subheader("⚡ Intensity (Calories)")
        st.bar_chart(df.set_index("Date")["Calories"], color="#38bdf8") # Blue

    st.subheader("📝 Journal History")
    if st.session_state.journal_entries:
        for entry in reversed(st.session_state.journal_entries):
            with st.container(border=True):
                st.caption(f"📅 {entry['date']}")
                st.write(entry['note'])
    else:
        st.info("No journal entries yet. Complete a workout to add one!")

def render_nutrition_premium():
    """NEW PREMIUM FEATURE PAGE"""
    st.title("🥦 Nutrition & Meal Plans")
    st.write("Fuel your body with adaptive meal plans suited to your lifestyle.")
    
    profile = st.session_state.user_profile
    user_diet = profile.get("diet", "No Preference")
    
    # CHECK IF UNLOCKED
    if st.session_state.premium_unlocked:
        # UNLOCKED CONTENT
        st.success(f"🔓 Premium Unlocked! Viewing {user_diet} Plans.")
        
        tab1, tab2, tab3 = st.tabs(["Daily Meals", "Shopping List", "Chat with Coach"])
        
        with tab1:
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown("### 🥣 Breakfast")
                st.image("https://images.unsplash.com/photo-1517673132405-a56a62b18caf?w=400", use_container_width=True)
                st.info(f"**{user_diet} Power Oats**\n\n*Oats, Chia Seeds, Berries, Protein Powder*")
            with c2:
                st.markdown("### 🥗 Lunch")
                st.image("https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400", use_container_width=True)
                st.info(f"**{user_diet} Energy Bowl**\n\n*Quinoa, Avocado, Chickpeas, Tahini*")
            with c3:
                st.markdown("### 🍲 Dinner")
                st.image("https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400", use_container_width=True)
                st.info(f"**{user_diet} Recovery Stew**\n\n*Lentils, Sweet Potato, Spinach, Spices*")
                
        with tab2:
            st.checkbox("Oats (500g)")
            st.checkbox("Almond Milk")
            st.checkbox("Spinach")
            st.checkbox("Chickpeas (2 cans)")
            
        with tab3:
            st.chat_message("assistant").write("Hello! I'm your FitBod Nutrition Coach. How can I help you tweak your diet today?")
            st.chat_message("user").write("I need more iron in my diet.")
            st.chat_message("assistant").write("Great! Let's add more lentils and spinach to your dinner plan.")

    else:
        # LOCKED CONTENT (TEASER)
        st.info(f"We see you prefer a **{user_diet}** diet. We have 50+ recipes waiting for you!")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🥣 Breakfast Preview")
            st.markdown(f"**{user_diet} Power Oats**\n\n*High protein, easy prep.*")
            st.caption("Ingredients hidden...")
            
        with col2:
            st.markdown("### 🥗 Lunch Preview")
            st.markdown(f"**{user_diet} Energy Bowl**\n\n*Great for recovery.*")
            st.caption("Ingredients hidden...")
            
        st.divider()
        
        # THE UPSELL CARD
        with st.container():
            st.markdown(
                """
                <div style="background: linear-gradient(135deg, #059669 0%, #047857 100%); padding: 30px; border-radius: 20px; text-align: center; color: white;">
                    <h1 style="color: white !important;">🔒 Unlock FitBod Premium</h1>
                    <p style="font-size: 1.2rem;">Get full access to personalized Meal Plans, 1-on-1 Coaching, and Advanced Analytics.</p>
                    <ul style="list-style: none; padding: 0; font-size: 1.1rem; margin-bottom: 25px;">
                        <li>✅ 500+ Healthy Recipes</li>
                        <li>✅ Direct Chat with Physiotherapists</li>
                        <li>✅ Ad-Free Experience</li>
                    </ul>
                    <h2 style="color: #fbbf24; margin-bottom: 20px;">Only $4.99 / month</h2>
                </div>
                """,
                unsafe_allow_html=True
            )
            # We use columns to center the button visually
            b1, b2, b3 = st.columns([1, 2, 1])
            with b2:
                if st.button("⭐ Get Premium Access", use_container_width=True):
                    # SIMULATE PAYMENT
                    with st.spinner("Processing Payment..."):
                        time.sleep(1.5)
                        st.session_state.premium_unlocked = True
                        st.rerun()

def render_sponsors():
    st.title("🤝 Our Sponsors & Partners")
    st.write("We are proud to be supported by these accessible fitness brands. Their support keeps the core features of FitBod free for everyone.")
    
    sponsors = [
        {"name": "EcoHydrate", "offer": "20% OFF Smart Bottles", "desc": "Easy-grip, lightweight bottles designed for accessible hydration.", "color": "#1C1C1E"},
        {"name": "FlexMat", "offer": "Buy 1 Get 1 Free", "desc": "Extra thick, non-slip mats perfect for chair stability and joint protection.", "color": "#1C1C1E"},
        {"name": "ProteinPlus", "offer": "Free Sample Pack", "desc": "Plant-based nutrition shakes with easy-open caps.", "color": "#1C1C1E"},
    ]
    
    for s in sponsors:
        st.markdown(
            f"""
            <div style="background-color: {s['color']}; padding: 20px; border-radius: 15px; margin-bottom: 15px; border-left: 5px solid #4ade80; border: 1px solid #333;">
                <h3 style="margin:0; color: #F8FAFC;">{s['name']}</h3>
                <h4 style="color: #4ade80; margin: 5px 0;">{s['offer']}</h4>
                <p style="color: #94A3B8;">{s['desc']}</p>
                <button style="background: #333; color: white; border:none; padding: 8px 15px; border-radius: 5px; cursor: pointer;">Visit Website</button>
            </div>
            """,
            unsafe_allow_html=True
        )

def render_settings():
    st.title("⚙️ Settings")
    
    st.subheader("Appearance")
    is_access = st.toggle("Accessibility Mode (High Contrast)", value=st.session_state.accessibility_mode)
    if is_access != st.session_state.accessibility_mode:
        st.session_state.accessibility_mode = is_access
        st.rerun()
        
    st.markdown("---")
    
    # Profile Edit
    render_onboarding(is_edit=True)

# --- 7. MAIN EXECUTION FLOW ---

# Initialize Session State
if 'user_profile' not in st.session_state: st.session_state.user_profile = None
if 'current_page' not in st.session_state: st.session_state.current_page = "Dashboard"
if 'streak' not in st.session_state: st.session_state.streak = 0
if 'hydration' not in st.session_state: st.session_state.hydration = 0
if 'accessibility_mode' not in st.session_state: st.session_state.accessibility_mode = False
if 'premium_unlocked' not in st.session_state: st.session_state.premium_unlocked = False
if 'workout_completed' not in st.session_state: st.session_state.workout_completed = False
if 'journal_entries' not in st.session_state: st.session_state.journal_entries = []
if 'last_saved_feeling' not in st.session_state: st.session_state.last_saved_feeling = False

# Apply Styles
inject_custom_css(st.session_state.accessibility_mode)

# Routing Logic
if not st.session_state.user_profile:
    # Force Onboarding if no profile
    render_onboarding()
else:
    # Show Navigation Bar
    render_navbar()
    
    # Page Router
    page = st.session_state.current_page
    
    if page == "Dashboard":
        render_dashboard()
    elif page == "Library":
        render_library()
    elif page == "Progress":
        render_progress()
    elif page == "Nutrition":
        render_nutrition_premium()
    elif page == "Sponsors":
        render_sponsors()
    elif page == "Settings":
        render_settings()
