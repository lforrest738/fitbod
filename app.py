import streamlit as st
import pandas as pd
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

# --- EXPANDED EXERCISE LIBRARY (VARIED ROUTINES) ---
EXERCISE_LIBRARY = [
  # --- SEATED STRENGTH ---
  {
    "id": "seated_shoulder_press",
    "title": "Seated Shoulder Press",
    "category": "Seated Strength",
    "tags": ["Wheelchair User", "Limited Lower-Body Mobility", "Upper Body", "Strength", "Resistance Bands", "Light Weights"],
    "intensity": "Moderate",
    "instructions": ["Sit upright.", "Push hands to ceiling.", "Lower slowly."],
    "safety_note": "Engage core.",
    "calories": 40, "duration_minutes": 5
  },
  {
    "id": "seated_bicep_curls",
    "title": "Seated Bicep Curls",
    "category": "Seated Strength",
    "tags": ["Wheelchair User", "Upper Body", "Strength", "Light Weights"],
    "intensity": "Low",
    "instructions": ["Hold weights at sides.", "Curl upwards.", "Lower with control."],
    "safety_note": "Keep elbows tucked.",
    "calories": 30, "duration_minutes": 5
  },
  {
    "id": "seated_row",
    "title": "Seated Band Row",
    "category": "Seated Strength",
    "tags": ["Wheelchair User", "Upper Body", "Strength", "Resistance Bands"],
    "intensity": "Moderate",
    "instructions": ["Wrap band around feet/door.", "Pull elbows back.", "Squeeze shoulder blades."],
    "safety_note": "Don't lean back too far.",
    "calories": 45, "duration_minutes": 5
  },
  
  # --- WHEELCHAIR CARDIO ---
  {
    "id": "seated_march",
    "title": "Seated High Knees",
    "category": "Cardio",
    "tags": ["Wheelchair User", "Cardio", "Endurance"],
    "intensity": "Energetic",
    "instructions": ["Lift knees rhythmically.", "Pump arms."],
    "safety_note": "Ensure stable chair.",
    "calories": 60, "duration_minutes": 10
  },
  {
    "id": "arm_circles",
    "title": "Rapid Arm Circles",
    "category": "Cardio",
    "tags": ["Wheelchair User", "Cardio", "Upper Body"],
    "intensity": "Moderate",
    "instructions": ["Extend arms out.", "Circle forward fast for 30s.", "Reverse."],
    "safety_note": "Stop if shoulders click.",
    "calories": 50, "duration_minutes": 5
  },
  {
    "id": "shadow_boxing",
    "title": "Seated Shadow Boxing",
    "category": "Cardio",
    "tags": ["Wheelchair User", "Cardio", "Upper Body", "Stress Relief"],
    "intensity": "Energetic",
    "instructions": ["Punch forward (Jab/Cross).", "Keep tempo high.", "Breathe out on punch."],
    "safety_note": "Don't overextend elbows.",
    "calories": 80, "duration_minutes": 10
  },

  # --- MOBILITY & SENSORY ---
  {
    "id": "neck_stretches",
    "title": "Gentle Neck Release",
    "category": "Mobility",
    "tags": ["Visual Impairment", "Neurodivergent Support", "Mobility", "Gentle"],
    "intensity": "Gentle",
    "instructions": ["Tilt ear to shoulder.", "Hold 10s.", "Switch."],
    "safety_note": "Move slowly.",
    "calories": 10, "duration_minutes": 3
  },
  {
    "id": "wrist_rolls",
    "title": "Wrist & Ankle Rolls",
    "category": "Mobility",
    "tags": ["Mobility", "Gentle", "Desk Work"],
    "intensity": "Gentle",
    "instructions": ["Rotate wrists clockwise.", "Rotate anti-clockwise.", "Repeat with ankles if able."],
    "safety_note": "Gentle movement only.",
    "calories": 15, "duration_minutes": 3
  },
  {
    "id": "cat_cow_seated",
    "title": "Seated Cat-Cow",
    "category": "Mobility",
    "tags": ["Mobility", "Back Pain", "Wheelchair User"],
    "intensity": "Low",
    "instructions": ["Hands on knees.", "Arch back look up (Cow).", "Round spine look down (Cat)."],
    "safety_note": "Listen to your spine.",
    "calories": 20, "duration_minutes": 5
  },

  # --- STANDING / LOWER BODY SUPPORTED ---
  {
    "id": "wall_pushup",
    "title": "Wall Push-Ups",
    "category": "Strength",
    "tags": ["Limited Lower-Body Mobility", "Strength", "Balance"],
    "intensity": "Moderate",
    "instructions": ["Face wall.", "Push chest to wall.", "Push back."],
    "safety_note": "Non-slip shoes needed.",
    "calories": 50, "duration_minutes": 5
  },
  {
    "id": "chair_squats",
    "title": "Sit-to-Stand",
    "category": "Strength",
    "tags": ["Limited Upper-Body Mobility", "Strength", "Balance", "Chair"],
    "intensity": "Energetic",
    "instructions": ["Sit on edge of chair.", "Stand up.", "Sit down slowly."],
    "safety_note": "Chair against wall.",
    "calories": 70, "duration_minutes": 8
  },
  {
    "id": "kitchen_counter_calf",
    "title": "Supported Calf Raises",
    "category": "Strength",
    "tags": ["Balance", "Strength", "Limited Lower-Body Mobility"],
    "intensity": "Low",
    "instructions": ["Hold counter.", "Lift heels.", "Lower."],
    "safety_note": "Hold tight for balance.",
    "calories": 30, "duration_minutes": 5
  }
]

# --- RECIPE DATA ---
RECIPES = [
    {
        "id": "r1", 
        "title": "Power Protein Oats", 
        "price": 0.99,
        "image": "https://images.unsplash.com/photo-1517673132405-a56a62b18caf?w=400",
        "desc": "High energy breakfast.",
        "ingredients": ["Oats", "Protein Powder", "Chia Seeds", "Almond Milk", "Blueberries"]
    },
    {
        "id": "r2", 
        "title": "Green Recovery Smoothie", 
        "price": 0.99,
        "image": "https://images.unsplash.com/photo-1610970881699-44a5587cabec?w=400",
        "desc": "Perfect post-workout.",
        "ingredients": ["Spinach", "Banana", "Protein Powder", "Coconut Water"]
    },
    {
        "id": "r3", 
        "title": "Quinoa Energy Bowl", 
        "price": 0.99,
        "image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400",
        "desc": "Lunch for stamina.",
        "ingredients": ["Quinoa", "Chickpeas", "Avocado", "Lemon", "Olive Oil"]
    },
    {
        "id": "r4", 
        "title": "Lentil Stew", 
        "price": 0.99,
        "image": "https://images.unsplash.com/photo-1547592166-23acbe346499?w=400",
        "desc": "Warm comfort food.",
        "ingredients": ["Lentils", "Carrots", "Vegetable Stock", "Turmeric"]
    }
]

# --- SPONSOR MAPPING ---
# If user buys a recipe with these ingredients, show a voucher
SPONSOR_DEALS = {
    "Protein Powder": {"sponsor": "ProteinPlus", "code": "PRO20 (20% Off)", "color": "#fff3e0"},
    "Oats": {"sponsor": "WholeGrainz", "code": "OAT5 (5% Off)", "color": "#f1f8e9"},
    "Almond Milk": {"sponsor": "NutriMilk", "code": "MILK10 (10% Off)", "color": "#e0f7fa"},
    "Resistance Bands": {"sponsor": "FlexMat", "code": "FLEX15 (15% Off)", "color": "#f3e5f5"} # Cross-sell example
}

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
    Standard Mode: Modern Gradient Theme (Teal/Emerald/Slate).
    Accessibility Mode: High Contrast, Large Text.
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
        # --- MODERN UX MODE ---
        st.markdown(
            """
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Poppins:wght@500;700&display=swap');
            
            /* Global Reset & Font */
            html, body, [class*="css"] {
                font-family: 'Inter', sans-serif;
                color: #1e293b; /* Slate 800 */
            }
            
            /* Background */
            .stApp {
                background: linear-gradient(135deg, #f0fdfa 0%, #e0f2fe 100%); /* Teal to Sky light gradient */
            }
            
            /* Headers */
            h1, h2, h3 {
                font-family: 'Poppins', sans-serif;
                color: #0f766e; /* Teal 700 */
                font-weight: 700;
            }
            
            h1 {
                background: linear-gradient(120deg, #0d9488, #0f766e);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            
            /* Modern Cards (Glassmorphism-lite) */
            div[data-testid="stContainer"], div[data-testid="stMetric"], div[data-testid="stExpander"] {
                background: #ffffff;
                border-radius: 16px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.5);
                padding: 1.5rem;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }
            
            div[data-testid="stContainer"]:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
            }
            
            /* Metrics */
            div[data-testid="stMetric"] label {
                color: #64748b; /* Slate 500 */
                font-size: 0.9rem;
            }
            div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
                color: #0f766e;
                font-weight: 800;
            }
            
            /* Primary Buttons */
            .stButton > button {
                background: linear-gradient(to right, #0d9488, #0f766e);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 0.6rem 1.2rem;
                font-weight: 600;
                letter-spacing: 0.5px;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                box-shadow: 0 4px 6px rgba(13, 148, 136, 0.2);
                width: 100%;
            }
            
            .stButton > button:hover {
                background: linear-gradient(to right, #14b8a6, #0d9488);
                transform: translateY(-2px);
                box-shadow: 0 10px 15px rgba(13, 148, 136, 0.3);
                color: white !important;
            }
            
            .stButton > button:active {
                transform: translateY(0);
            }
            
            /* Premium/Purchase Button Style (Gold) */
            button[kind="secondary"] {
                background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
                color: white !important;
                border: none;
            }

            /* Inputs */
            .stTextInput input, .stSelectbox div[data-baseweb="select"], .stMultiSelect div[data-baseweb="select"] {
                background-color: #ffffff;
                border: 1px solid #cbd5e1;
                border-radius: 10px;
                color: #334155;
            }
            
            /* Navigation Bar Simulation */
            div[data-testid="column"] button {
                background: transparent;
                color: #475569;
                box-shadow: none;
                border: 1px solid transparent;
            }
            
            div[data-testid="column"] button:hover {
                background: #e0f2fe;
                color: #0f766e;
                box-shadow: none;
                transform: none;
                border: 1px solid #ccfbf1;
            }

            /* Expander Header */
            .streamlit-expanderHeader {
                font-family: 'Poppins', sans-serif;
                color: #334155;
                font-weight: 600;
            }
            
            /* Success/Info Messages */
            .stSuccess, .stInfo, .stWarning {
                border-radius: 12px;
                border: none;
                color: #334155;
            }
            .stSuccess {
                background-color: #d1fae5;
                border-left: 5px solid #10b981;
            }
            .stInfo {
                background-color: #e0f2fe;
                border-left: 5px solid #0ea5e9;
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
    """
    Robust generator that uses the expanded library.
    It tries to find unique routines suitable for the user's needs.
    """
    disability = user_profile.get('disability', [])
    equipment = user_profile.get('equipment', [])
    goal = user_profile.get('goal', 'Mobility')
    
    suitable = []
    
    # 1. Scoring System
    for ex in EXERCISE_LIBRARY:
        score = 0
        # Positive filtering: Does this exercise match their needs?
        if any(tag in ex['tags'] for tag in disability): score += 3
        if "Wheelchair User" in disability and "Wheelchair User" in ex['tags']: score += 5
        
        # Equipment filtering: Must have required equipment
        required_eq = [t for t in ex['tags'] if t in ["Resistance Bands", "Light Weights", "Chair"]]
        has_eq = all(eq in equipment for eq in required_eq)
        
        if has_eq or "None" in ex['tags']: 
            score += 1
        else: 
            score = -999 # Impossible to do
            
        # Goal Boost
        if goal in ex['tags'] or goal in ex['category']: score += 2
        
        if score > 0: suitable.append(ex)
    
    # 2. Random Selection ensuring variety
    # If we have enough, pick 3 random ones
    if len(suitable) >= 3: 
        return random.sample(suitable, 3)
    # If limited options, return what we have
    return suitable

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
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        if st.button("🏠 Home", use_container_width=True): navigate_to("Dashboard")
    with col2:
        if st.button("💪 Library", use_container_width=True): navigate_to("Library")
    with col3:
        if st.button("📈 Progress", use_container_width=True): navigate_to("Progress")
    with col4:
        if st.button("🥦 Nutrition", use_container_width=True): navigate_to("Nutrition")
    with col5:
        if st.button("🤝 Sponsors", use_container_width=True): navigate_to("Sponsors")
    with col6:
        if st.button("⚙️ Settings", use_container_width=True): navigate_to("Settings")
    st.markdown("---")

# --- 5. COMPONENTS ---

def render_onboarding(is_edit=False):
    profile = st.session_state.user_profile if is_edit else {}
    
    if is_edit:
        st.header("✏️ Edit Your Profile")
        btn_label = "Update Profile"
        container = st.container(border=True)
    else:
        st.markdown(
            """
            <div style="text-align: center; padding: 40px 0; background: linear-gradient(180deg, rgba(220,252,231,0) 0%, rgba(220,252,231,0.5) 100%); border-radius: 20px; margin-bottom: 30px;">
                <h1 style="font-size: 4rem; margin-bottom: 0; background: -webkit-linear-gradient(45deg, #166534, #15803d); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">FitBod 🥑</h1>
                <h3 style="font-weight: 300; font-style: italic; color: #374151; margin-top: 10px;">Empowering Movement. No Limits.</h3>
                <p style="font-size: 1.2rem; color: #4b5563; max-width: 600px; margin: 20px auto;">
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

            st.subheader("2. Access & Mobility Needs")
            access_options = [
                "Wheelchair User (Manual)", "Wheelchair User (Power)",
                "Limited Upper-Body Mobility", "Limited Lower-Body Mobility",
                "Limited Grip Strength", "Balance Issues / Vertigo",
                "Chronic Pain / Fatigue", "Visual Impairment (Low Vision)",
                "Visual Impairment (Blind)", "Neurodivergent (Autism/ADHD)",
                "Sensory Sensitivity (Low Noise)", "Post-Injury Recovery",
                "None / General Fitness"
            ]
            disability_default = profile.get("disability", [])
            safe_default = [x for x in disability_default if x in access_options]
            disability = st.multiselect("Select all that apply:", access_options, default=safe_default)

            col_a, col_b = st.columns(2)
            with col_a:
                st.subheader("3. Fitness Goal")
                goal_opts = ["Strength", "Mobility & Flexibility", "Balance & Stability", "Cardiovascular Health", "Weight Management", "Mental Wellbeing", "Confidence Building"]
                try: idx = goal_opts.index(profile.get("goal", "Mobility & Flexibility"))
                except: idx = 1
                goal = st.selectbox("Main Focus", goal_opts, index=idx)
            
            with col_b:
                st.subheader("4. Available Equipment")
                eq_opts = ["Resistance Bands", "Light Weights (Dumbbells)", "Heavy Weights", "Chair (Sturdy)", "Yoga Mat", "None (Bodyweight Only)"]
                def_eq = profile.get("equipment", [])
                safe_eq = [x for x in def_eq if x in eq_opts]
                equipment = st.multiselect("Select what you have:", eq_opts, default=safe_eq)

            st.subheader("5. Lifestyle & Preferences")
            col_l1, col_l2 = st.columns(2)
            with col_l1:
                style_idx = ["Gentle", "Direct", "Energetic"].index(profile.get("style", "Gentle")) if "style" in profile else 0
                style = st.select_slider("Coaching Style", ["Gentle", "Direct", "Energetic"], value=["Gentle", "Direct", "Energetic"][style_idx])
            with col_l2:
                diet_opts = ["No Preference", "Vegetarian", "Vegan", "Gluten-Free", "Keto", "High Protein"]
                diet_def = profile.get("diet", "No Preference")
                diet = st.selectbox("Dietary Preference", diet_opts, index=diet_opts.index(diet_def) if diet_def in diet_opts else 0)

            submitted = st.form_submit_button(btn_label, use_container_width=True)
            
            if submitted:
                if not name:
                    st.error("Please enter your name!")
                else:
                    st.session_state.user_profile = {
                        "name": name, "age_group": age_group, "disability": disability,
                        "goal": goal, "equipment": equipment, "style": style, "diet": diet
                    }
                    st.session_state.current_page = "Dashboard"
                    if 'current_plan' in st.session_state: del st.session_state.current_plan
                    st.rerun()

def render_workout_card(exercise):
    with st.container():
        c1, c2 = st.columns([3, 1])
        with c1:
            st.markdown(f"### {exercise['title']}")
            st.markdown(f"**{exercise['category']}** • *{exercise['intensity'].title()} Intensity*")
        with c2:
            st.markdown(f"## ⏱️ {exercise['duration_minutes']}m")
        st.divider()
        ic1, ic2 = st.columns([2, 1])
        with ic1:
            st.markdown("#### Instructions")
            for i, step in enumerate(exercise['instructions']):
                st.write(f"**{i+1}.** {step}")
        with ic2:
            st.markdown("#### Safety First 🛡️")
            st.info(exercise['safety_note'])
            st.markdown(f"🔥 **{exercise['calories']} kcal**")
        if st.session_state.accessibility_mode:
            text = f"{exercise['title']}. {'. '.join(exercise['instructions'])}."
            st.markdown(get_audio_html(text), unsafe_allow_html=True)

# --- 6. PAGE RENDERERS ---

def render_dashboard():
    profile = st.session_state.user_profile
    greeting = get_greeting(profile.get('name', 'Friend'))
    
    col_head, col_img = st.columns([3, 1])
    with col_head:
        st.title(greeting)
        quote = random.choice(QUOTES)
        st.markdown(
            f"""
            <div style="background-color: #0f766e; padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
                <h3 style="color: #fbbf24; margin:0; font-family: 'Poppins', sans-serif;">✨ Daily Motivation</h3>
                <p style="font-size: 1.3em; font-style: italic; margin-top: 10px; color: #f0fdfa;">"{quote}"</p>
            </div>
            """, unsafe_allow_html=True
        )
        st.markdown(f"**Current Focus:** `{profile.get('goal', 'General Fitness')}`")
    with col_img:
        st.metric("Current Streak", f"🔥 {st.session_state.streak}")

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
                st.session_state.workout_completed = False
                st.rerun()

    st.markdown("---")

    if st.session_state.workout_completed:
        st.balloons()
        st.markdown("## 🎉 Amazing Job, " + profile.get('name', 'Friend') + "!")
        st.success("You've completed your daily routine. Take a moment to rest and reflect.")
        c1, c2 = st.columns(2)
        with c1:
            st.info("💡 **Tip:** Tracking how you feel helps us adjust future intensity.")
            feeling = st.text_area("How are you feeling?", key="journal_input", placeholder="I feel energized...")
            col_save, col_view = st.columns([1, 1])
            with col_save:
                if st.button("💾 Save to Journal"):
                    if feeling:
                        entry = {"date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "note": feeling}
                        st.session_state.journal_entries.append(entry)
                        st.session_state.last_saved_feeling = True
                        st.toast("Journal Entry Saved!")
                    else: st.error("Please write something to save!")
            if st.session_state.get('last_saved_feeling', False):
                with col_view: st.success("Saved!")
                if st.button("📖 View in Progress Tab"):
                    st.session_state.last_saved_feeling = False
                    navigate_to("Progress")
        with c2:
            st.markdown("### What's Next?")
            if st.button("📈 View Progress Stats", use_container_width=True): navigate_to("Progress")
            st.write("")
            if st.button("🔄 Generate Another Workout", use_container_width=True):
                st.session_state.workout_completed = False
                st.session_state.current_plan = generate_workout_plan(profile)
                st.rerun()
    else:
        st.markdown("### Today's Personalized Plan")
        if 'current_plan' not in st.session_state:
            st.session_state.current_plan = generate_workout_plan(profile)
        plan = st.session_state.current_plan
        if not plan:
            st.warning("We're adjusting parameters to find the best fit. Here is a mobility starter.")
            plan = [ex for ex in EXERCISE_LIBRARY if "Mobility" in ex['tags']][:2]
        for ex in plan:
            render_workout_card(ex)
            st.write("")
        if st.button("✅ Complete Workout", type="primary", use_container_width=True):
            st.session_state.streak += 1
            st.session_state.workout_completed = True
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
    if cat_filter != "All": filtered = [e for e in filtered if e['category'] == cat_filter]
    if search_term: filtered = [e for e in filtered if search_term.lower() in e['title'].lower()]
    for ex in filtered: render_workout_card(ex)

def render_progress():
    st.title("📈 Your Progress")
    data = {"Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "Workouts": [1, 0, 1, 1, 0, 1, 0]}
    df = pd.DataFrame(data)
    col1, col2 = st.columns(2)
    with col1: st.metric("Total Active Minutes", f"{st.session_state.streak * 15} mins")
    with col2: st.metric("Total Calories Burned", f"{st.session_state.streak * 120} kcal")
    st.subheader("Weekly Activity")
    st.bar_chart(df.set_index("Day"))
    st.subheader("📝 Journal History")
    if st.session_state.journal_entries:
        for entry in reversed(st.session_state.journal_entries):
            with st.container(border=True):
                st.caption(f"📅 {entry['date']}")
                st.write(entry['note'])
    else:
        st.info("No journal entries yet. Complete a workout to add one!")

def render_nutrition_marketplace():
    """UPDATED: Recipe Marketplace Logic"""
    st.title("🥦 Nutrition Marketplace")
    st.write("Unlock healthy, adaptive recipes for just **£0.99**. Ingredients are automatically added to your shopping list!")
    
    # 1. RECIPE GRID
    for recipe in RECIPES:
        is_owned = recipe['id'] in st.session_state.purchased_recipes
        
        with st.container():
            c1, c2 = st.columns([1, 3])
            with c1:
                st.image(recipe['image'], use_container_width=True)
            with c2:
                st.subheader(recipe['title'])
                st.write(recipe['desc'])
                
                if is_owned:
                    st.success("✅ Purchased")
                    with st.expander("View Recipe & Ingredients"):
                        st.write("**Ingredients:**")
                        for ing in recipe['ingredients']:
                            st.write(f"- {ing}")
                else:
                    if st.button(f"🛒 Buy Recipe (£{recipe['price']})", key=f"buy_{recipe['id']}"):
                        # SIMULATE PURCHASE
                        st.session_state.purchased_recipes.add(recipe['id'])
                        # Add ingredients to list (deduplicated)
                        for ing in recipe['ingredients']:
                            if ing not in st.session_state.shopping_list:
                                st.session_state.shopping_list.append(ing)
                        st.toast(f"Bought {recipe['title']}!")
                        st.rerun()

    st.markdown("---")
    
    # 2. SMART SHOPPING LIST
    st.header("📝 Smart Shopping List")
    
    if not st.session_state.shopping_list:
        st.info("Your list is empty. Buy a recipe above to populate it!")
    else:
        st.write("Tick off items as you shop. Look out for Sponsor Deals! 🎁")
        
        for item in st.session_state.shopping_list:
            col_check, col_deal = st.columns([2, 3])
            
            with col_check:
                st.checkbox(item, key=f"shop_{item}")
                
            with col_deal:
                # SPONSOR LOGIC
                if item in SPONSOR_DEALS:
                    deal = SPONSOR_DEALS[item]
                    st.markdown(
                        f"""
                        <div style="background-color: {deal['color']}; padding: 5px 10px; border-radius: 5px; border: 1px solid #ddd; font-size: 0.9em;">
                            <strong>🎁 {deal['sponsor']} Deal:</strong> Use code <code>{deal['code']}</code>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

def render_sponsors():
    st.title("🤝 Our Sponsors & Partners")
    st.write("We are proud to be supported by these accessible fitness brands.")
    
    sponsors = [
        {"name": "ProteinPlus", "offer": "20% OFF Shakes", "desc": "Plant-based nutrition with easy-open caps.", "color": "#fff3e0"},
        {"name": "WholeGrainz", "offer": "5% OFF Oats", "desc": "Organic oats for sustained energy.", "color": "#f1f8e9"},
        {"name": "FlexMat", "offer": "Buy 1 Get 1 Free", "desc": "Extra thick mats for chair stability.", "color": "#f3e5f5"},
    ]
    
    for s in sponsors:
        st.markdown(
            f"""
            <div style="background-color: {s['color']}; padding: 20px; border-radius: 15px; margin-bottom: 15px; border-left: 5px solid #333;">
                <h3 style="margin:0; color: #333;">{s['name']}</h3>
                <h4 style="color: #d81b60; margin: 5px 0;">{s['offer']}</h4>
                <p style="color: #555;">{s['desc']}</p>
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
    render_onboarding(is_edit=True)

# --- 7. MAIN EXECUTION FLOW ---

if 'user_profile' not in st.session_state: st.session_state.user_profile = None
if 'current_page' not in st.session_state: st.session_state.current_page = "Dashboard"
if 'streak' not in st.session_state: st.session_state.streak = 0
if 'hydration' not in st.session_state: st.session_state.hydration = 0
if 'accessibility_mode' not in st.session_state: st.session_state.accessibility_mode = False
if 'workout_completed' not in st.session_state: st.session_state.workout_completed = False
if 'journal_entries' not in st.session_state: st.session_state.journal_entries = []
if 'last_saved_feeling' not in st.session_state: st.session_state.last_saved_feeling = False

# NEW STATES FOR RECIPES
if 'purchased_recipes' not in st.session_state: st.session_state.purchased_recipes = set()
if 'shopping_list' not in st.session_state: st.session_state.shopping_list = []

inject_custom_css(st.session_state.accessibility_mode)

if not st.session_state.user_profile:
    render_onboarding()
else:
    render_navbar()
    page = st.session_state.current_page
    
    if page == "Dashboard": render_dashboard()
    elif page == "Library": render_library()
    elif page == "Progress": render_progress()
    elif page == "Nutrition": render_nutrition_marketplace() # Updated function
    elif page == "Sponsors": render_sponsors()
    elif page == "Settings": render_settings()
