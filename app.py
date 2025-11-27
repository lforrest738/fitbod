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

# --- EXERCISE LIBRARY ---
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
    "Focus on what you CAN do.",
    "Believe in yourself and all that you are."
]

# --- 2. STYLE & THEME ENGINE ---

def inject_custom_css(mode_active):
    """
    Injects CSS. 
    Standard Mode: Modern, Clean, 'Glassy' feel.
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
                line-height: 1.5 !important;
            }
            .stApp { background-color: #000000 !important; color: #FFFFFF !important; }
            
            /* Buttons */
            .stButton > button { 
                background-color: #FFFF00 !important; 
                color: #000000 !important; 
                border: 4px solid #FFFFFF !important; 
                font-weight: bold !important; 
                font-size: 26px !important; 
                padding: 20px !important; 
                border-radius: 0px !important;
                box-shadow: none !important;
            }
            .stButton > button:hover {
                background-color: #FFFFFF !important;
            }

            /* Nav Buttons specifically */
            div[data-testid="column"] button {
                width: 100%;
                margin-bottom: 10px;
            }
            
            /* Containers */
            div[data-testid="stMetric"], div[data-testid="stExpander"], div[data-testid="stContainer"] {
                background-color: #222222 !important; 
                border: 3px solid #FFFF00 !important; 
                color: #FFFFFF !important;
            }
            
            h1, h2, h3, h4 { 
                color: #FFFF00 !important; 
                text-decoration: underline; 
                text-transform: uppercase;
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
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
            
            /* Global Font & Background */
            html, body, [class*="css"] {
                font-family: 'Inter', sans-serif;
            }
            .stApp {
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            }
            
            /* Header Styling */
            h1 {
                color: #111827;
                font-weight: 800;
                letter-spacing: -1px;
            }
            h2, h3 {
                color: #374151;
                font-weight: 600;
            }
            
            /* Card Containers */
            div[data-testid="stContainer"], div[data-testid="stMetric"], div[data-testid="stExpander"] {
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 16px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                border: none;
                padding: 1rem;
            }
            
            /* Buttons */
            .stButton > button {
                background: linear-gradient(to right, #10B981, #34D399); /* Emerald Gradient */
                color: white;
                border: none;
                border-radius: 12px;
                padding: 0.5rem 1rem;
                font-weight: 600;
                transition: all 0.2s;
                box-shadow: 0 4px 6px rgba(16, 185, 129, 0.3);
            }
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 8px rgba(16, 185, 129, 0.4);
            }
            .stButton > button:active {
                transform: translateY(0px);
            }
            
            /* Secondary Buttons (Gray) - We can't target specifically easily, but we can override generally */
            
            /* Navigation Bar Simulation */
            div[data-testid="column"] {
                text-align: center;
            }

            /* Input Fields */
            .stTextInput input, .stSelectbox, .stMultiSelect {
                border-radius: 10px;
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
    goal = user_profile.get('goal', 'mobility')
    
    suitable = []
    for ex in EXERCISE_LIBRARY:
        score = 0
        if any(tag in ex['tags'] for tag in disability): score += 2
        
        required_eq = [t for t in ex['tags'] if t in ["resistance bands", "light weights", "chair"]]
        has_eq = all(eq in equipment for eq in required_eq)
        
        if has_eq or "none" in ex['tags']: score += 1
        else: score = -10
            
        if goal in ex['tags'] or goal in ex['category'].lower(): score += 1
        
        if score > 0: suitable.append(ex)
    
    if len(suitable) >= 3: return random.sample(suitable, 3)
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
    # Use different emoji icons for active vs inactive state if desired, 
    # here we stick to clean labels.
    
    st.markdown("---")
    col1, col2, col3, col4, col5 = st.columns(5)
    
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
        if st.button("🔗 Links", use_container_width=True): # New Resources Tab
            navigate_to("Resources")
    with col5:
        if st.button("⚙️ Settings", use_container_width=True):
            navigate_to("Settings")
    st.markdown("---")

# --- 5. COMPONENTS ---

def render_onboarding(is_edit=False):
    profile = st.session_state.user_profile if is_edit else {}
    
    if is_edit:
        st.header("✏️ Edit Your Profile")
        btn_label = "Update Profile"
    else:
        st.title("Welcome to FitBod 🥑")
        st.write("Let's build a fitness journey that fits **you**.")
        btn_label = "Start My Journey"

    with st.container(border=True):
        with st.form("profile_form"):
            # Personalization
            st.subheader("1. The Basics")
            name = st.text_input("What should we call you?", value=profile.get("name", ""))
            
            # Disability / Needs
            st.subheader("2. Access Needs")
            disability_default = profile.get("disability", [])
            disability = st.multiselect(
                "I identify with / require support for:",
                ["wheelchair user", "limited upper-body mobility", "limited lower-body mobility", "visual impairment", "neurodivergent support"],
                default=disability_default
            )

            col_a, col_b = st.columns(2)
            with col_a:
                st.subheader("3. Goal")
                goal_opts = ["strength", "mobility", "balance", "endurance", "confidence building"]
                try:
                    idx = goal_opts.index(profile.get("goal", "mobility"))
                except:
                    idx = 1
                goal = st.selectbox("Main Focus", goal_opts, index=idx)
            
            with col_b:
                st.subheader("4. Equipment")
                eq_opts = ["resistance bands", "light weights", "chair"]
                equipment = st.multiselect("Available Items", eq_opts, default=profile.get("equipment", []))

            st.subheader("5. Motivation Style")
            style_idx = ["gentle", "direct", "energetic"].index(profile.get("style", "gentle")) if "style" in profile else 0
            style = st.select_slider("How should we coach you?", ["gentle", "direct", "energetic"], value=["gentle", "direct", "energetic"][style_idx])

            submitted = st.form_submit_button(btn_label, use_container_width=True)
            
            if submitted:
                if not name:
                    st.error("Please enter your name!")
                else:
                    st.session_state.user_profile = {
                        "name": name,
                        "disability": disability,
                        "goal": goal,
                        "equipment": equipment,
                        "style": style
                    }
                    st.session_state.current_page = "Dashboard"
                    # Reset plan to force regeneration
                    if 'current_plan' in st.session_state: del st.session_state.current_plan
                    st.rerun()

def render_workout_card(exercise):
    """Modern Card Design for exercises"""
    with st.container():
        # Using columns to create a header layout within the card
        c1, c2 = st.columns([3, 1])
        with c1:
            st.markdown(f"### {exercise['title']}")
            st.markdown(f"**{exercise['category']}** • *{exercise['intensity'].title()} Intensity*")
        with c2:
            st.markdown(f"## ⏱️ {exercise['duration_minutes']}m")
        
        st.divider()
        
        # Split instructions and safety for better readability
        ic1, ic2 = st.columns([2, 1])
        with ic1:
            st.markdown("#### Instructions")
            for i, step in enumerate(exercise['instructions']):
                st.write(f"**{i+1}.** {step}")
        
        with ic2:
            st.markdown("#### Safety First 🛡️")
            st.info(exercise['safety_note'])
            st.markdown(f"🔥 **{exercise['calories']} kcal**")
        
        # Audio Player (Access Mode Only or Toggle)
        if st.session_state.accessibility_mode:
            text = f"{exercise['title']}. {'. '.join(exercise['instructions'])}."
            st.markdown(get_audio_html(text), unsafe_allow_html=True)

# --- 6. PAGE RENDERERS ---

def render_dashboard():
    profile = st.session_state.user_profile
    greeting = get_greeting(profile.get('name', 'Friend'))
    
    # 1. Header Section
    col_head, col_img = st.columns([3, 1])
    with col_head:
        st.title(greeting)
        quote = random.choice(QUOTES)
        st.caption(f"✨ \"{quote}\"")
    with col_img:
        # Just a visual placeholder or streak display
        st.metric("Current Streak", f"🔥 {st.session_state.streak}")

    # 2. Quick Actions / Hydration
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
                st.rerun()

    st.markdown("### Today's Personalized Plan")
    
    if 'current_plan' not in st.session_state:
        st.session_state.current_plan = generate_workout_plan(profile)
        
    plan = st.session_state.current_plan
    
    if not plan:
        st.warning("We're adjusting parameters to find the best fit. Here is a mobility starter.")
        plan = [ex for ex in EXERCISE_LIBRARY if "mobility" in ex['tags']][:2]

    # Render Cards
    for ex in plan:
        render_workout_card(ex)
        st.write("") # spacer

    if st.button("✅ Complete Workout", type="primary", use_container_width=True):
        st.session_state.streak += 1
        st.balloons()
        st.success("Workout Complete! Streak updated.")
        time.sleep(2)
        st.rerun()

def render_library():
    st.title("📚 Exercise Library")
    st.write("Browse all accessible exercises.")
    
    # Search/Filter Bar
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
    
    # Mock Data for Chart
    data = {
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "Workouts": [1, 0, 1, 1, 0, 1, 0] # Mock data
    }
    df = pd.DataFrame(data)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Active Minutes", f"{st.session_state.streak * 15} mins")
    with col2:
        st.metric("Total Calories Burned", f"{st.session_state.streak * 120} kcal")
        
    st.subheader("Weekly Activity")
    st.bar_chart(df.set_index("Day"))
    
    with st.expander("Journal History"):
        st.write("No journal entries yet. Complete a workout to add one!")

def render_resources():
    st.title("🔗 Resources & Equipment")
    st.write("Curated links for adaptive fitness equipment.")
    
    links = [
        {"name": "Theraband Resistance Bands", "url": "#", "desc": "Latex-free bands suitable for seated exercises."},
        {"name": "Active Hands Gripping Aids", "url": "#", "desc": " Essential for users with limited hand function."},
        {"name": "Wheelchair Yoga Mat", "url": "#", "desc": "Non-slip mats designed for chair stability."},
    ]
    
    for link in links:
        with st.container():
            st.markdown(f"**[{link['name']}]({link['url']})**")
            st.caption(link['desc'])

def render_settings():
    st.title("⚙️ Settings")
    
    # Accessibility Toggle
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
    elif page == "Resources":
        render_resources()
    elif page == "Settings":
        render_settings()import streamlit as st
import pandas as pd
import random
import datetime
import base64
import io
from gtts import gTTS

# --- 1. DATA: EXERCISE LIBRARY ---
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
    # Ensure profile is safe to use
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

def render_profile_form(existing_profile=None):
    """Renders the onboarding form, pre-filled if editing."""
    
    # Determine Header and Defaults
    if existing_profile:
        st.header("Edit Profile")
        btn_text = "Update Profile"
        # Extract defaults
        def_disability = existing_profile.get("disability", [])
        def_goal_val = existing_profile.get("goal", "mobility")
        def_equip = existing_profile.get("equipment", [])
        def_style = existing_profile.get("style", "gentle")
    else:
        st.header("Welcome to FitBod 👋")
        st.write("Let's build a plan that works for *you*.")
        btn_text = "Create My Plan"
        def_disability = []
        def_goal_val = "mobility"
        def_equip = []
        def_style = "gentle"

    # Define Options
    goal_options = ["strength", "mobility", "balance", "endurance", "confidence building"]
    
    # Handle Selectbox Index safely
    try:
        goal_index = goal_options.index(def_goal_val)
    except ValueError:
        goal_index = 0

    with st.form("profile_form"):
        st.subheader("1. About You")
        disability = st.multiselect(
            "I identify with / require support for:",
            ["wheelchair user", "limited upper-body mobility", "limited lower-body mobility", "visual impairment", "neurodivergent support"],
            default=def_disability
        )
        
        st.subheader("2. Your Goal")
        goal = st.selectbox("Main focus?", goal_options, index=goal_index)
        
        st.subheader("3. Equipment")
        equipment = st.multiselect(
            "What do you have available?", 
            ["resistance bands", "light weights", "chair"],
            default=def_equip
        )
        
        st.subheader("4. Motivation Style")
        style = st.select_slider("Coaching style?", ["gentle", "direct", "energetic"], value=def_style)
        
        submitted = st.form_submit_button(btn_text)
        
        if submitted:
            st.session_state.user_profile = {
                "disability": disability, "goal": goal, 
                "equipment": equipment, "style": style, "onboarded": True
            }
            # Clear edit mode
            st.session_state.editing_profile = False
            # Clear current plan to force regeneration with new settings
            if 'current_plan' in st.session_state:
                del st.session_state.current_plan
                
            st.success("Profile Saved!")
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
if 'editing_profile' not in st.session_state: st.session_state.editing_profile = False

# Sidebar: Settings & Edit Profile
with st.sidebar:
    st.title("Settings")
    
    # Accessibility Toggle
    mode = st.toggle("♿ Accessibility Mode", value=st.session_state.accessibility_mode)
    if mode != st.session_state.accessibility_mode:
        st.session_state.accessibility_mode = mode
        st.rerun()
    
    st.write("---")
    
    # Edit Profile Button
    if st.session_state.user_profile:
        if st.button("✏️ Edit Profile"):
            st.session_state.editing_profile = True
            st.rerun()

apply_accessibility_styles(st.session_state.accessibility_mode)

# Main Title
st.title("FitBod 🥑")

# App Routing Logic
# 1. If in Edit Mode OR No Profile -> Show Form
if st.session_state.editing_profile or not st.session_state.user_profile:
    render_profile_form(st.session_state.user_profile)

# 2. Main App (Profile exists and not editing)
else:
    # Navigation
    if not st.session_state.accessibility_mode:
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Go to", ["Daily Dashboard", "Exercise Library", "My Progress"])
    else:
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

        # Plan Logic: Create or Retrieve
        if 'current_plan' not in st.session_state:
            st.session_state.current_plan = generate_workout_plan(user_profile)
        
        # Generate New Button
        col_act1, col_act2 = st.columns([1,3])
        with col_act1:
            if st.button("🔄 New Routine"):
                st.session_state.current_plan = generate_workout_plan(user_profile)
                st.rerun()

        todays_plan = st.session_state.current_plan
        
        if not todays_plan:
            st.warning("No perfect matches found for your equipment, showing general mobility.")
            todays_plan = [ex for ex in EXERCISE_LIBRARY if "mobility" in ex['tags']][:2]

        st.subheader("Your Routine")
        for ex in todays_plan:
            render_workout_card(ex, show_audio=st.session_state.accessibility_mode)
            
        st.write("---")
        if st.button("✅ I Completed This Workout", use_container_width=True):
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
