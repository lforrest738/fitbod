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
    page_title="FitBod",
    page_icon="🥑",
    layout="centered",  # Centered layout mimics a mobile app screen on desktop
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
    "duration_minutes": 5,
    "image": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=800&auto=format&fit=crop"
  },
  {
    "id": "seated_march",
    "title": "Seated High Knees",
    "category": "Cardio",
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
    "duration_minutes": 10,
    "image": "https://images.unsplash.com/photo-1518611012118-696072aa579a?w=800&auto=format&fit=crop"
  },
  {
    "id": "wall_pushup",
    "title": "Wall Push-Ups",
    "category": "Upper Body",
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
    "duration_minutes": 5,
    "image": "https://images.unsplash.com/photo-1599058945522-28d584b6f0ff?w=800&auto=format&fit=crop"
  },
  {
    "id": "neck_stretches",
    "title": "Gentle Neck Release",
    "category": "Mobility",
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
    "duration_minutes": 3,
    "image": "https://images.unsplash.com/photo-1544367563-12123d8965cd?w=800&auto=format&fit=crop"
  },
  {
    "id": "band_pull_apart",
    "title": "Resistance Band Pulls",
    "category": "Upper Body",
    "tags": ["Wheelchair User", "Strength", "Resistance Bands"],
    "intensity": "Moderate",
    "instructions": [
      "Hold a resistance band with both hands in front of you at shoulder height.",
      "Keep arms straight and pull the band apart by squeezing your shoulder blades together.",
      "Return to center with control."
    ],
    "safety_note": "Don't shrug your shoulders. Keep neck relaxed.",
    "calories": 45,
    "duration_minutes": 5,
    "image": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=800&auto=format&fit=crop"
  },
  {
    "id": "chair_squats",
    "title": "Sit-to-Stand",
    "category": "Lower Body",
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
    "duration_minutes": 8,
    "image": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?w=800&auto=format&fit=crop"
  }
]

QUOTES = [
    "Small steps, big changes.",
    "Listen to your body.",
    "Your pace is the best pace.",
    "Fitness is for every body.",
    "You showed up, that's a win.",
    "Focus on what you CAN do."
]

# --- 2. STYLE & THEME ENGINE ---

def inject_custom_css(mode_active):
    """
    Injects CSS. 
    Standard Mode: Modern 'Social App' Aesthetic (Clean, White, Rounded, Shadows).
    Accessibility Mode: High Contrast, Large Text.
    """
    if mode_active:
        # --- ACCESSIBILITY MODE (High Contrast) ---
        st.markdown(
            """
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&display=swap');
            
            html, body, [class*="css"], p, div, h1, h2, h3 { 
                font-size: 22px !important; 
                font-family: 'Atkinson Hyperlegible', sans-serif !important; 
                line-height: 1.6 !important;
                color: #FFFFFF !important;
                background-color: #000000 !important;
            }
            .stApp { background-color: #000000 !important; }
            
            /* High Contrast Elements */
            .stButton > button { 
                background-color: #FFFF00 !important; 
                color: #000000 !important; 
                border: 4px solid #FFFFFF !important; 
                font-weight: bold !important; 
                padding: 15px !important; 
                border-radius: 0px !important;
                margin-bottom: 10px !important;
            }
            
            /* Containers */
            div[data-testid="stContainer"] {
                border: 2px solid #FFFF00 !important;
                margin-bottom: 20px !important;
                background-color: #000000 !important;
            }
            
            h1, h2, h3 { 
                color: #FFFF00 !important; 
                text-decoration: underline; 
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        # --- MODERN SOCIAL APP MODE ---
        st.markdown(
            """
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
            
            /* GLOBAL RESET */
            html, body, [class*="css"] {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                color: #111827;
                background-color: #fafafa;
            }
            
            .stApp {
                background-color: #fafafa; /* Light Grey Background */
            }
            
            /* HEADER STYLING */
            h1 {
                font-weight: 800;
                font-size: 2rem;
                letter-spacing: -0.025em;
                color: #111827;
                margin-bottom: 0.5rem;
            }
            
            h3 {
                font-weight: 600;
                font-size: 1.1rem;
                color: #374151;
            }
            
            /* STORIES / QUICK ACTIONS */
            /* We simulate stories with circular buttons if possible, but standard buttons work too */
            
            /* CARD DESIGN (FEED STYLE) */
            div[data-testid="stContainer"] {
                background: #ffffff;
                border-radius: 20px;
                border: 1px solid #f3f4f6;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
                padding: 20px;
                margin-bottom: 24px;
            }
            
            /* BUTTONS - PILL SHAPE & GRADIENT */
            .stButton > button {
                border-radius: 9999px; /* Pill shape */
                background: #111827; /* Dark elegant black/blue */
                color: white;
                font-weight: 600;
                border: none;
                padding: 10px 24px;
                transition: transform 0.1s ease;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }
            
            .stButton > button:hover {
                background: #374151;
                transform: scale(1.02);
                color: white !important;
            }
            
            /* Secondary Buttons (Outlined) */
            button[kind="secondary"] {
                background: white;
                color: #111827 !important;
                border: 2px solid #e5e7eb;
                box-shadow: none;
            }
            
            /* NAVIGATION BAR SIMULATION */
            /* We style the top columns to look like tabs */
            div[data-testid="column"] button {
                background: transparent;
                color: #9ca3af; /* Inactive Grey */
                box-shadow: none;
                padding: 0px;
                font-size: 0.9rem;
            }
            div[data-testid="column"] button:hover {
                background: transparent;
                color: #111827; /* Active Black */
                transform: none;
            }
            div[data-testid="column"] button:focus {
                color: #10b981; /* Active Green */
            }

            /* INPUTS - MINIMALIST */
            .stTextInput input, .stSelectbox div[data-baseweb="select"] {
                border-radius: 12px;
                border: 1px solid #e5e7eb;
                background-color: #f9fafb;
                padding: 10px;
            }
            
            /* SUCCESS MESSAGES */
            .stSuccess {
                background-color: #ecfdf5;
                color: #065f46;
                border: none;
                border-radius: 12px;
            }
            
            /* HIDE DEFAULT STREAMLIT ELEMENTS */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            
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
        return "<small>Audio unavailable.</small>"

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
    if hour < 12: msg = "Good morning"
    elif hour < 18: msg = "Good afternoon"
    else: msg = "Good evening"
    return f"{msg}, {name}" if name else msg

# --- 4. NAVIGATION ---

def navigate_to(page):
    st.session_state.current_page = page
    st.rerun()

def render_tab_nav():
    """Simulates a mobile app Tab Bar at the top."""
    st.markdown("---")
    # Using columns for the nav icons
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Simple Text Icons for Clean Look
    with col1:
        if st.button("🏠\nHome", key="nav_home", use_container_width=True): navigate_to("Dashboard")
    with col2:
        if st.button("💪\nLibrary", key="nav_lib", use_container_width=True): navigate_to("Library")
    with col3:
        if st.button("📊\nStats", key="nav_prog", use_container_width=True): navigate_to("Progress")
    with col4:
        if st.button("🥗\nFood", key="nav_food", use_container_width=True): navigate_to("Nutrition")
    with col5:
        if st.button("👤\nProfile", key="nav_set", use_container_width=True): navigate_to("Settings")
    st.markdown("---")

# --- 5. COMPONENT RENDERERS ---

def render_story_bubble(emoji, label, action_key):
    """Renders a 'Story' style action bubble."""
    if st.button(f"{emoji}\n{label}", key=action_key, use_container_width=True):
        return True
    return False

def render_workout_post(exercise, index):
    """Renders an exercise like a social media post card."""
    with st.container():
        # User Header (Simulated)
        c1, c2 = st.columns([1, 5])
        with c1:
            st.markdown("🥑") # Avatar placeholder
        with c2:
            st.markdown(f"**FitBod Coach** • {exercise['category']}")
            st.caption(f"{exercise['intensity']} Intensity • {exercise['duration_minutes']} min")
        
        # Image / Visual
        if 'image' in exercise:
            st.image(exercise['image'], use_container_width=True)
        else:
            st.markdown(f"### {exercise['title']}")

        # Content
        st.markdown(f"**{exercise['title']}**")
        with st.expander("Read Instructions"):
            for i, step in enumerate(exercise['instructions']):
                st.write(f"{i+1}. {step}")
            st.info(f"🛡️ Safety: {exercise['safety_note']}")
            
        # Actions
        ac1, ac2 = st.columns([4, 1])
        with ac1:
            # Audio in 'Social' mode might be an icon
            if st.session_state.accessibility_mode:
                 text = f"{exercise['title']}. {'. '.join(exercise['instructions'])}."
                 st.markdown(get_audio_html(text), unsafe_allow_html=True)
        with ac2:
            st.button("❤️", key=f"like_{exercise['id']}_{index}", help="Mark as favorite")

# --- 6. PAGE VIEWS ---

def render_dashboard():
    profile = st.session_state.user_profile
    
    # 1. Header (Instagram Style)
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown(f"### {get_greeting(profile.get('name', 'Friend'))}")
    with c2:
        st.caption(f"🔥 {st.session_state.streak} Day Streak")
    
    # 2. Stories / Quick Actions Row
    st.markdown("#### Daily Habits")
    sc1, sc2, sc3, sc4 = st.columns(4)
    with sc1:
        if render_story_bubble("💧", "Hydrate", "act_water"):
            st.session_state.hydration += 1
            st.toast("Water logged! 💧")
    with sc2:
        if render_story_bubble("📓", "Journal", "act_journal"):
            # Minimal inline journal
            st.session_state.show_journal_modal = True
    with sc3:
         if render_story_bubble("🔄", "Refresh", "act_refresh"):
             st.session_state.current_plan = generate_workout_plan(profile)
             st.session_state.workout_completed = False
             st.rerun()
    with sc4:
        st.markdown(f"<div style='text-align:center; font-size:0.8rem; color:grey; margin-top:10px;'>{st.session_state.hydration}/8<br>Cups</div>", unsafe_allow_html=True)

    # 3. Journal Modal (Simulated)
    if st.session_state.get('show_journal_modal', False):
        with st.container():
            st.info("✍️ Quick Journal")
            note = st.text_input("How do you feel?", placeholder="Type here...")
            if st.button("Post Entry"):
                if note:
                    st.session_state.journal_entries.append({"date": datetime.datetime.now().strftime("%d %b"), "note": note})
                    st.toast("Posted to Journal!")
                    st.session_state.show_journal_modal = False
                    st.rerun()
                if st.button("Cancel"):
                    st.session_state.show_journal_modal = False
                    st.rerun()

    st.write("") # Spacer

    # 4. Main Feed (Workout Plan)
    st.markdown("#### Your Feed")
    
    if st.session_state.workout_completed:
        with st.container():
            st.markdown("### 🎉 You're all caught up!")
            st.image("https://images.unsplash.com/photo-1499540633137-7d63ae0e8f16?w=800&auto=format&fit=crop", use_container_width=True)
            st.success("Daily workout completed.")
            if st.button("Start Bonus Round"):
                st.session_state.workout_completed = False
                st.session_state.current_plan = generate_workout_plan(profile)
                st.rerun()
    else:
        if 'current_plan' not in st.session_state:
            st.session_state.current_plan = generate_workout_plan(profile)
        
        plan = st.session_state.current_plan
        
        for idx, ex in enumerate(plan):
            render_workout_post(ex, idx)
        
        # Complete Button fixed at bottom of feed
        if st.button("✅ Mark Workout Complete", type="primary", use_container_width=True):
            st.session_state.streak += 1
            st.session_state.workout_completed = True
            st.balloons()
            st.rerun()

def render_library():
    st.markdown("### 📚 Explore")
    search = st.text_input("Search", placeholder="Find exercises...")
    
    # Categories as horizontal pills (simulated)
    cols = st.columns(4)
    cats = ["All", "Cardio", "Strength", "Mobility"]
    selected_cat = "All"
    # Basic implementation of filters
    
    filtered = EXERCISE_LIBRARY
    if search:
        filtered = [e for e in filtered if search.lower() in e['title'].lower()]
        
    # Grid Layout for Library
    for i in range(0, len(filtered), 2):
        c1, c2 = st.columns(2)
        if i < len(filtered):
            with c1:
                with st.container():
                    st.image(filtered[i].get('image', 'https://via.placeholder.com/150'), use_container_width=True)
                    st.caption(filtered[i]['title'])
        if i+1 < len(filtered):
            with c2:
                with st.container():
                    st.image(filtered[i+1].get('image', 'https://via.placeholder.com/150'), use_container_width=True)
                    st.caption(filtered[i+1]['title'])

def render_progress():
    st.markdown("### 📊 Activity Stats")
    
    # Modern Stats Grid
    c1, c2 = st.columns(2)
    with c1:
        with st.container():
            st.metric("Streak", f"{st.session_state.streak}", delta="Days")
    with c2:
        with st.container():
            st.metric("Workouts", f"{st.session_state.streak}", delta="+1")
            
    st.markdown("#### History")
    if st.session_state.journal_entries:
        for entry in reversed(st.session_state.journal_entries):
            with st.container():
                st.markdown(f"**{entry['date']}**")
                st.write(entry['note'])
                st.markdown("---")
    else:
        st.caption("No entries yet.")

def render_nutrition():
    st.markdown("### 🥗 Nutrition Plans")
    
    if st.session_state.premium_unlocked:
        st.success("Premium Active")
        st.markdown("**Your Meal Plan**")
        st.image("https://images.unsplash.com/photo-1543339308-43e59d6b73a6?w=800&auto=format&fit=crop", use_container_width=True)
        st.info("Today: Quinoa Salad Bowl & Green Smoothie")
    else:
        st.markdown("**Upgrade to FitBod+**")
        st.image("https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=800&auto=format&fit=crop", use_container_width=True)
        st.write("Get personalized meal plans tailored to your needs.")
        if st.button("Unlock for $4.99/mo", type="primary"):
            with st.spinner("Processing..."):
                time.sleep(1)
                st.session_state.premium_unlocked = True
                st.rerun()

def render_onboarding():
    st.markdown(
        """
        <div style='text-align: center; margin-bottom: 30px;'>
            <h1 style='font-size: 3rem;'>FitBod 🥑</h1>
            <p style='color: #6b7280;'>Your personal fitness companion.</p>
        </div>
        """, unsafe_allow_html=True
    )
    
    with st.container():
        with st.form("onboard"):
            name = st.text_input("First Name")
            
            st.markdown("### I want to focus on...")
            goal = st.selectbox("", ["Mobility", "Strength", "Balance", "Cardio"])
            
            st.markdown("### I identify as...")
            disability = st.multiselect("", ["Wheelchair User", "Limited Mobility", "Visual Impairment", "Neurodivergent", "General Fitness"])
            
            if st.form_submit_button("Get Started", use_container_width=True):
                if name:
                    st.session_state.user_profile = {"name": name, "goal": goal, "disability": disability, "equipment": []}
                    st.rerun()

# --- 7. MAIN EXECUTION ---

if 'user_profile' not in st.session_state: st.session_state.user_profile = None
if 'current_page' not in st.session_state: st.session_state.current_page = "Dashboard"
if 'streak' not in st.session_state: st.session_state.streak = 0
if 'hydration' not in st.session_state: st.session_state.hydration = 0
if 'accessibility_mode' not in st.session_state: st.session_state.accessibility_mode = False
if 'premium_unlocked' not in st.session_state: st.session_state.premium_unlocked = False
if 'workout_completed' not in st.session_state: st.session_state.workout_completed = False
if 'journal_entries' not in st.session_state: st.session_state.journal_entries = []

# Styling
inject_custom_css(st.session_state.accessibility_mode)

# App Flow
if not st.session_state.user_profile:
    render_onboarding()
else:
    # Top Tab Navigation (Simulating App Bar)
    render_tab_nav()
    
    # Router
    page = st.session_state.current_page
    if page == "Dashboard": render_dashboard()
    elif page == "Library": render_library()
    elif page == "Progress": render_progress()
    elif page == "Nutrition": render_nutrition()
    elif page == "Settings":
        st.markdown("### Settings")
        access = st.toggle("Accessibility Mode", value=st.session_state.accessibility_mode)
        if access != st.session_state.accessibility_mode:
            st.session_state.accessibility_mode = access
            st.rerun()
