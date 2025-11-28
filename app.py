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

# --- EXPANDED EXERCISE LIBRARY ---
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
SPONSOR_DEALS = {
    "Protein Powder": {"sponsor": "ProteinPlus", "code": "PRO20 (20% Off)", "color": "#FFF3E0"},
    "Oats": {"sponsor": "WholeGrainz", "code": "OAT5 (5% Off)", "color": "#F1F8E9"},
    "Almond Milk": {"sponsor": "NutriMilk", "code": "MILK10 (10% Off)", "color": "#E0F7FA"},
    "Resistance Bands": {"sponsor": "FlexMat", "code": "FLEX15 (15% Off)", "color": "#F3E5F5"} 
}

QUOTES = [
    "Small steps lead to big changes.",
    "Your pace is the best pace.",
    "Fitness is for everybody.",
    "You showed up today, and that is a victory.",
    "Focus on what you CAN do.",
    "Believe in yourself."
]

# --- 2. STYLE & THEME ENGINE ---

def inject_custom_css(mode_active):
    """
    Injects CSS. 
    Standard Mode: 'Apple Aesthetic' (Clean, Minimal, San Francisco font, Soft Shadows).
    Accessibility Mode: STRICT High Contrast (Black/Yellow).
    """
    if mode_active:
        # --- STRICT ACCESSIBILITY MODE ---
        st.markdown(
            """
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Verdana&display=swap');
            
            /* FORCE OVERRIDES FOR EVERYTHING */
            html, body, .stApp {
                background-color: #000000 !important;
                font-family: 'Verdana', sans-serif !important;
            }
            
            /* TEXT */
            h1, h2, h3, h4, h5, h6, p, div, span, label, li {
                color: #FFFF00 !important;
                text-shadow: none !important;
            }
            
            /* BUTTONS */
            .stButton > button {
                background-color: #000000 !important;
                color: #FFFF00 !important;
                border: 4px solid #FFFF00 !important;
                font-weight: bold !important;
                font-size: 20px !important;
                border-radius: 0px !important;
                box-shadow: none !important;
                padding: 15px !important;
            }
            .stButton > button:hover {
                background-color: #FFFF00 !important;
                color: #000000 !important;
            }
            
            /* CONTAINERS & CARDS */
            div[data-testid="stContainer"], div[data-testid="stExpander"] {
                background-color: #000000 !important;
                border: 4px solid #FFFF00 !important;
                border-radius: 0px !important;
                box-shadow: none !important;
            }
            
            /* INPUTS */
            input, select, textarea, div[data-baseweb="select"] {
                background-color: #000000 !important;
                color: #FFFF00 !important;
                border: 2px solid #FFFF00 !important;
            }
            
            /* MESSAGES */
            .stSuccess, .stInfo, .stWarning, .stError {
                background-color: #000000 !important;
                color: #FFFF00 !important;
                border: 2px solid #FFFF00 !important;
            }
            
            /* HIDE DECORATIVE ELEMENTS */
            .decoration, .gradient { display: none !important; }
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        # --- APPLE / CUPERTINO MODE ---
        st.markdown(
            """
            <style>
            /* Apple-like System Font Stack */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
            
            /* Global Reset & Font */
            html, body, [class*="css"] {
                font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                color: #1D1D1F; /* Apple Dark Grey */
                letter-spacing: -0.015em;
            }
            
            /* Background - Soft Off-White Wash */
            .stApp {
                background-color: #F5F5F7; 
            }
            
            /* Headers */
            h1, h2, h3 {
                color: #1D1D1F;
                font-weight: 600; /* Semibold */
                letter-spacing: -0.025em;
            }
            
            h1 { font-size: 3rem; margin-bottom: 0.2em; }
            
            /* Modern Cards (Apple Card Style) */
            div[data-testid="stContainer"], div[data-testid="stExpander"] {
                background: #FFFFFF;
                border-radius: 18px; /* Classic Apple curvature */
                border: 1px solid rgba(0,0,0,0.02);
                box-shadow: 0 4px 24px rgba(0,0,0,0.04); /* Soft, diffuse shadow */
                padding: 24px;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }
            
            div[data-testid="stContainer"]:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 32px rgba(0,0,0,0.06);
            }
            
            /* Buttons - Pill Shape & Apple Blue */
            .stButton > button {
                background-color: #0071E3; /* Apple Blue */
                color: white;
                border: none;
                border-radius: 980px; /* Fully rounded pill */
                padding: 10px 22px;
                font-weight: 500;
                font-size: 16px;
                box-shadow: none;
                transition: all 0.2s ease;
            }
            
            .stButton > button:hover {
                background-color: #0077ED; /* Slightly lighter on hover */
                transform: scale(1.02);
                color: white !important;
            }
            
            .stButton > button:active {
                transform: scale(0.98);
                background-color: #006EDB;
            }
            
            /* Secondary Action Buttons (Purchase/Action) */
            button[kind="secondary"] {
                background-color: #F5F5F7;
                color: #0071E3 !important;
                border: none;
            }
            button[kind="secondary"]:hover {
                background-color: #E8E8ED;
            }

            /* Inputs - Clean & Minimal */
            .stTextInput input, .stSelectbox div[data-baseweb="select"], .stMultiSelect div[data-baseweb="select"] {
                background-color: #FFFFFF;
                border: 1px solid #D2D2D7; /* Apple border grey */
                border-radius: 12px;
                padding: 10px;
                color: #1D1D1F;
            }
            .stTextInput input:focus {
                border-color: #0071E3;
                box-shadow: 0 0 0 3px rgba(0,113,227,0.15);
            }

            /* Navigation Bar Simulation - Tab Bar Style */
            div[data-testid="column"] button {
                background: transparent;
                color: #86868B; /* Inactive grey */
                box-shadow: none;
                border: none;
                font-weight: 500;
            }
            div[data-testid="column"] button:hover {
                background: rgba(0,0,0,0.03);
                color: #1D1D1F;
                border-radius: 12px;
            }
            div[data-testid="column"] button:focus {
                color: #0071E3;
            }

            /* Success/Info Messages */
            .stSuccess {
                background-color: #E4F9E8; /* Light Green Wash */
                color: #1F6F36;
                border-radius: 14px;
                border: none;
            }
            .stInfo {
                background-color: #E7F3FF; /* Light Blue Wash */
                color: #0059B3;
                border-radius: 14px;
                border: none;
            }
            
            /* Metrics */
            div[data-testid="stMetricValue"] {
                color: #1D1D1F;
                font-weight: 700;
                font-family: -apple-system, sans-serif;
            }
            div[data-testid="stMetricLabel"] {
                color: #86868B;
            }
            
            /* Slider Customization */
            div[data-baseweb="slider"] {
                accent-color: #0071E3;
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
    Robust generator ensuring diverse routines.
    """
    disability = user_profile.get('disability', [])
    equipment = user_profile.get('equipment', [])
    goal = user_profile.get('goal', 'Mobility')
    
    suitable = []
    
    for ex in EXERCISE_LIBRARY:
        score = 0
        # Filter Logic
        if any(tag in ex['tags'] for tag in disability): score += 3
        if "Wheelchair User" in disability and "Wheelchair User" in ex['tags']: score += 5
        
        required_eq = [t for t in ex['tags'] if t in ["Resistance Bands", "Light Weights", "Chair"]]
        has_eq = all(eq in equipment for eq in required_eq)
        
        if has_eq or "None" in ex['tags']: 
            score += 1
        else: 
            score = -999
            
        if goal in ex['tags'] or goal in ex['category']: score += 2
        
        if score > 0: suitable.append(ex)
    
    # Ensure unique selection
    if len(suitable) >= 3: 
        return random.sample(suitable, 3)
    return suitable

def get_greeting(name):
    hour = datetime.datetime.now().hour
    if hour < 12: msg = "Good Morning"
    elif hour < 18: msg = "Good Afternoon"
    else: msg = "Good Evening"
    return f"{msg}, {name}" if name else msg

# --- 4. NAVIGATION HANDLER ---

def navigate_to(page):
    st.session_state.current_page = page
    st.rerun()

def render_navbar():
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
        # Apple-Style Hero Section (Clean)
        st.markdown(
            """
            <div style="text-align: center; padding: 60px 20px; background: white; border-radius: 24px; margin-bottom: 30px; box-shadow: 0 10px 40px rgba(0,0,0,0.06);">
                <h1 style="color: #1D1D1F; font-size: 3.5rem; margin-bottom: 10px; font-weight: 700; letter-spacing: -0.03em;">FitBod 🥑</h1>
                <h3 style="color: #86868B; font-weight: 500; font-size: 1.5rem; margin-top: 0;">Designed for Every Body.</h3>
                <p style="font-size: 1.1rem; color: #1D1D1F; max-width: 500px; margin: 20px auto; line-height: 1.6;">
                    A personalized, adaptive fitness companion that puts you first.
                </p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        st.markdown("### Let's get started")
        btn_label = "Start My Journey"
        container = st.container(border=True)

    with container:
        with st.form("profile_form"):
            st.subheader("1. The Basics")
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("First Name", value=profile.get("name", ""))
            with col2:
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
            st.caption(f"{exercise['category']} • {exercise['intensity']} Intensity")
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
        # Apple-Style Info Card (Subtle gradient or clean white)
        st.markdown(
            f"""
            <div style="background-color: #FFFFFF; padding: 24px; border-radius: 18px; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.04); box-shadow: 0 4px 12px rgba(0,0,0,0.03);">
                <h4 style="color: #0071E3; margin:0; text-transform: uppercase; font-size: 0.8rem; letter-spacing: 1px;">Daily Wisdom</h4>
                <p style="font-size: 1.4rem; font-weight: 600; font-style: italic; margin-top: 8px; color: #1D1D1F;">"{quote}"</p>
            </div>
            """, unsafe_allow_html=True
        )
        st.markdown(f"**Focus:** `{profile.get('goal', 'General Fitness')}`")
    with col_img:
        st.metric("Streak 🔥", f"{st.session_state.streak}")

    # Quick Actions
    with st.container():
        hc1, hc2, hc3 = st.columns(3)
        with hc1:
            st.metric("Hydration 💧", f"{st.session_state.hydration} / 8")
        with hc2:
            if st.button("➕ Drink", use_container_width=True):
                st.session_state.hydration += 1
                st.rerun()
        with hc3:
            if st.button("🔄 New Mix", use_container_width=True):
                st.session_state.current_plan = generate_workout_plan(profile)
                st.session_state.workout_completed = False
                st.rerun()

    st.markdown("---")

    if st.session_state.workout_completed:
        st.balloons()
        st.markdown(f"## 🎉 Woohoo, {profile.get('name', 'Friend')}!")
        st.success("You crushed it! Time to relax.")
        c1, c2 = st.columns(2)
        with c1:
            st.info("💡 **Check-in:** How do you feel?")
            feeling = st.text_area("Write it down...", key="journal_input")
            col_save, col_view = st.columns([1, 1])
            with col_save:
                if st.button("💾 Save"):
                    if feeling:
                        entry = {"date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "note": feeling}
                        st.session_state.journal_entries.append(entry)
                        st.session_state.last_saved_feeling = True
                        st.toast("Saved!")
                    else: st.error("Empty note!")
            if st.session_state.get('last_saved_feeling', False):
                with col_view: st.success("Done!")
                if st.button("📖 Go to Journal"):
                    st.session_state.last_saved_feeling = False
                    navigate_to("Progress")
        with c2:
            st.markdown("### Next Steps")
            if st.button("📈 See Stats", use_container_width=True): navigate_to("Progress")
            st.write("")
            if st.button("🔄 Another Round?", use_container_width=True):
                st.session_state.workout_completed = False
                st.session_state.current_plan = generate_workout_plan(profile)
                st.rerun()
    else:
        st.markdown("### ⚡ Today's Mix")
        if 'current_plan' not in st.session_state:
            st.session_state.current_plan = generate_workout_plan(profile)
        plan = st.session_state.current_plan
        if not plan:
            st.warning("Adjusting based on your gear... Here's a mobility starter!")
            plan = [ex for ex in EXERCISE_LIBRARY if "Mobility" in ex['tags']][:2]
        for ex in plan:
            render_workout_card(ex)
            st.write("")
        if st.button("✅ I Did It!", type="primary", use_container_width=True):
            st.session_state.streak += 1
            st.session_state.workout_completed = True
            st.rerun()

def render_library():
    st.title("📚 Exercise Library")
    col_search, col_filter = st.columns([2, 1])
    with col_search:
        search_term = st.text_input("Find an exercise...", placeholder="e.g. 'Push'")
    with col_filter:
        cat_filter = st.selectbox("Filter", ["All"] + list(set(e['category'] for e in EXERCISE_LIBRARY)))
    filtered = EXERCISE_LIBRARY
    if cat_filter != "All": filtered = [e for e in filtered if e['category'] == cat_filter]
    if search_term: filtered = [e for e in filtered if search_term.lower() in e['title'].lower()]
    for ex in filtered: render_workout_card(ex)

def render_progress():
    st.title("📈 Progress Party")
    data = {"Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "Workouts": [1, 0, 1, 1, 0, 1, 0]}
    df = pd.DataFrame(data)
    col1, col2 = st.columns(2)
    with col1: st.metric("Active Mins", f"{st.session_state.streak * 15}")
    with col2: st.metric("Total Burn", f"{st.session_state.streak * 120} kcal")
    st.subheader("Weekly Activity")
    st.bar_chart(df.set_index("Day"))
    st.subheader("📝 My Journal")
    if st.session_state.journal_entries:
        for entry in reversed(st.session_state.journal_entries):
            with st.container(border=True):
                st.caption(f"📅 {entry['date']}")
                st.write(entry['note'])
    else:
        st.info("No entries yet. Go work out!")

def render_nutrition_marketplace():
    st.title("🥦 Recipe Market")
    st.write("Delicious, healthy recipes for just **£0.99**! Populates your list automatically.")
    
    # Grid Layout
    c1, c2 = st.columns(2)
    
    for i, recipe in enumerate(RECIPES):
        # Alternate columns
        col = c1 if i % 2 == 0 else c2
        is_owned = recipe['id'] in st.session_state.purchased_recipes
        
        with col:
            with st.container():
                st.image(recipe['image'], use_container_width=True)
                st.subheader(recipe['title'])
                st.write(recipe['desc'])
                
                if is_owned:
                    st.success("✅ Owned")
                    with st.expander("Ingredients"):
                        for ing in recipe['ingredients']: st.write(f"• {ing}")
                else:
                    if st.button(f"🛒 Buy (£{recipe['price']})", key=f"buy_{recipe['id']}", use_container_width=True):
                        st.session_state.purchased_recipes.add(recipe['id'])
                        for ing in recipe['ingredients']:
                            if ing not in st.session_state.shopping_list:
                                st.session_state.shopping_list.append(ing)
                        st.toast(f"Bought {recipe['title']}!")
                        st.rerun()

    st.markdown("---")
    st.header("📝 Smart Shopping List")
    
    if not st.session_state.shopping_list:
        st.info("List empty! Buy some recipes above.")
    else:
        st.write("Check for **Sponsor Deals** below! 🎁")
        for item in st.session_state.shopping_list:
            col_check, col_deal = st.columns([2, 3])
            with col_check:
                st.checkbox(item, key=f"shop_{item}")
            with col_deal:
                if item in SPONSOR_DEALS:
                    deal = SPONSOR_DEALS[item]
                    st.markdown(f"<span style='background-color:{deal['color']}; padding: 4px 8px; border-radius: 5px; border: 1px solid #ddd; font-size: 0.8rem; color: #1d1d1f;'>🎁 <b>{deal['sponsor']}</b>: {deal['code']}</span>", unsafe_allow_html=True)

def render_sponsors():
    st.title("🤝 Partners")
    st.write("Brands that support accessible fitness.")
    
    sponsors = [
        {"name": "ProteinPlus", "offer": "20% OFF Shakes", "desc": "Easy-open caps.", "color": "#FFF3E0"},
        {"name": "WholeGrainz", "offer": "5% OFF Oats", "desc": "Organic energy.", "color": "#F1F8E9"},
        {"name": "FlexMat", "offer": "BOGO Mats", "desc": "Extra thick & stable.", "color": "#F3E5F5"},
    ]
    
    for s in sponsors:
        st.markdown(
            f"""
            <div style="background-color: #FFFFFF; padding: 24px; border-radius: 18px; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.04); box-shadow: 0 4px 12px rgba(0,0,0,0.03);">
                <h3 style="margin:0; color: #1D1D1F; font-size: 1.2rem;">{s['name']}</h3>
                <h4 style="color: #0071E3; margin: 5px 0;">{s['offer']}</h4>
                <p style="color: #86868B;">{s['desc']}</p>
                <button style="background: #F5F5F7; color: #0071E3; border:none; padding: 8px 16px; border-radius: 980px; cursor: pointer; font-weight: 500;">Shop Now</button>
            </div>
            """,
            unsafe_allow_html=True
        )

def render_settings():
    st.title("⚙️ Settings")
    st.subheader("Visuals")
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
    elif page == "Nutrition": render_nutrition_marketplace()
    elif page == "Sponsors": render_sponsors()
    elif page == "Settings": render_settings()
