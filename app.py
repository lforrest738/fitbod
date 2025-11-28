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
    Standard Mode: Expert UI, Avocado/Slate Palette, Glassmorphism.
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
        # --- EXPERT UX MODE (Avocado & Slate) ---
        st.markdown(
            """
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
            
            /* Global Font & Background */
            html, body, [class*="css"] {
                font-family: 'Poppins', sans-serif;
                color: #1e293b; /* Slate 800 */
            }
            .stApp {
                background-color: #f0fdf4; /* Very light green bg */
                background-image: radial-gradient(#dcfce7 1px, transparent 1px);
                background-size: 20px 20px;
            }
            
            /* Typography */
            h1 {
                color: #166534; /* Green 700 */
                font-weight: 700;
                letter-spacing: -0.5px;
            }
            h2, h3 {
                color: #334155; /* Slate 700 */
                font-weight: 600;
            }
            
            /* Glassmorphism Containers */
            div[data-testid="stContainer"], div[data-testid="stMetric"], div[data-testid="stExpander"] {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 20px;
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.025);
                border: 1px solid rgba(255, 255, 255, 0.5);
                padding: 1.5rem;
                backdrop-filter: blur(10px);
            }
            
            /* Primary Buttons */
            .stButton > button {
                background: linear-gradient(135deg, #16a34a 0%, #15803d 100%); /* Green Gradient */
                color: white;
                border: none;
                border-radius: 12px;
                padding: 0.6rem 1.2rem;
                font-weight: 600;
                letter-spacing: 0.5px;
                transition: all 0.3s ease;
                box-shadow: 0 4px 6px rgba(22, 163, 74, 0.2);
            }
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 12px rgba(22, 163, 74, 0.3);
            }
            
            /* Premium Button Style (Gold) */
            button[kind="secondary"] {
                background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
                color: white !important;
                border: none;
            }
            
            /* Form Elements */
            .stTextInput input, .stSelectbox, .stMultiSelect {
                border-radius: 12px;
                border: 1px solid #cbd5e1;
                padding: 0.5rem;
            }
            
            /* Navbar Simulation */
            div[data-testid="column"] {
                text-align: center;
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
        if st.button("🔗 Links", use_container_width=True): 
            navigate_to("Resources")
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
    else:
        st.title("Welcome to FitBod 🥑")
        st.markdown("### Let's design your accessible fitness journey.")
        btn_label = "Start My Journey"

    with st.container(border=True):
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
    
    # 1. Hero Section
    col_head, col_img = st.columns([3, 1])
    with col_head:
        st.title(greeting)
        quote = random.choice(QUOTES)
        st.caption(f"✨ \"{quote}\"")
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
                st.rerun()

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
        st.balloons()
        st.success("Workout Complete! Streak updated.")
        time.sleep(2)
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

def render_nutrition_premium():
    """NEW PREMIUM FEATURE PAGE"""
    st.title("🥦 Nutrition & Meal Plans")
    st.write("Fuel your body with adaptive meal plans suited to your lifestyle.")
    
    profile = st.session_state.user_profile
    user_diet = profile.get("diet", "No Preference")
    
    # Teaser Content
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
            <div style="background: linear-gradient(135deg, #16a34a 0%, #064e3b 100%); padding: 30px; border-radius: 20px; text-align: center; color: white;">
                <h1>🔒 Unlock FitBod Premium</h1>
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
                st.balloons()
                st.success("Thank you for your interest! Payment gateway would open here.")

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
    elif page == "Nutrition":
        render_nutrition_premium()
    elif page == "Resources":
        render_resources()
    elif page == "Settings":
        render_settings()
