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

# --- EXPANDED EXERCISE LIBRARY (TAILORED) ---
EXERCISE_LIBRARY = [
  # --- SEATED STRENGTH (Wheelchair/Office) ---
  {
    "id": "seated_shoulder_press",
    "title": "Seated Shoulder Press",
    "category": "Strength",
    "tags": ["Wheelchair User", "Limited Lower-Body Mobility", "Upper Body", "Strength"],
    "intensity": "Moderate",
    "instructions": ["Sit upright.", "Push hands/weights to ceiling.", "Lower slowly."],
    "safety_note": "Engage core to protect lower back.",
    "calories": 40, "duration_minutes": 5
  },
  {
    "id": "wheelchair_crunches",
    "title": "Seated Crunches",
    "category": "Core",
    "tags": ["Wheelchair User", "Core", "Strength"],
    "intensity": "Moderate",
    "instructions": ["Lock breaks.", "Hold chest.", "Crunch forward towards knees.", "Return upright."],
    "safety_note": "Ensure chair is stable.",
    "calories": 30, "duration_minutes": 5
  },
  {
    "id": "seated_row_band",
    "title": "Resistance Band Rows",
    "category": "Strength",
    "tags": ["Wheelchair User", "Upper Body", "Posture"],
    "intensity": "Moderate",
    "instructions": ["Secure band around sturdy object.", "Pull elbows back.", "Squeeze shoulder blades."],
    "safety_note": "Don't round shoulders.",
    "calories": 45, "duration_minutes": 5
  },

  # --- LIMITED MOBILITY / HEMIPLEGIA / STROKE RECOVERY ---
  {
    "id": "unilateral_grip",
    "title": "Unilateral Grip Strength",
    "category": "Rehab",
    "tags": ["Hemiplegia", "Limited Grip Strength", "Stroke Recovery"],
    "intensity": "Low",
    "instructions": ["Squeeze a soft ball in affected hand.", "Hold for 5s.", "Release."],
    "safety_note": "Stop if muscle spasms occur.",
    "calories": 15, "duration_minutes": 5
  },
  {
    "id": "supported_weight_shift",
    "title": "Supported Weight Shifts",
    "category": "Balance",
    "tags": ["Limited Lower-Body Mobility", "Balance", "Stroke Recovery"],
    "intensity": "Low",
    "instructions": ["Stand holding counter.", "Shift weight to left leg.", "Hold 3s.", "Shift to right leg."],
    "safety_note": "Have a chair behind you for safety.",
    "calories": 25, "duration_minutes": 5
  },

  # --- BED-BOUND / CHRONIC FATIGUE ---
  {
    "id": "bed_ankle_pumps",
    "title": "Supine Ankle Pumps",
    "category": "Mobility",
    "tags": ["Bed-Bound", "Chronic Fatigue", "Post-Injury Recovery"],
    "intensity": "Very Low",
    "instructions": ["Lie on back.", "Point toes down.", "Pull toes up towards shin.", "Repeat."],
    "safety_note": "Keep legs relaxed.",
    "calories": 10, "duration_minutes": 3
  },
  {
    "id": "bed_angels",
    "title": "Bed Angels",
    "category": "Mobility",
    "tags": ["Bed-Bound", "Chronic Fatigue", "Upper Body"],
    "intensity": "Low",
    "instructions": ["Lie flat.", "Slide arms out to sides and up like a snow angel.", "Return."],
    "safety_note": "Stop if shoulders pinch.",
    "calories": 15, "duration_minutes": 5
  },

  # --- SENSORY FRIENDLY / QUIET ---
  {
    "id": "quiet_wall_sit",
    "title": "Silent Wall Sit",
    "category": "Strength",
    "tags": ["Sensory Sensitivity", "Autism/ADHD", "Strength"],
    "intensity": "High",
    "instructions": ["Lean against wall.", "Slide down until knees bent.", "Hold silently."],
    "safety_note": "Breathe deeply.",
    "calories": 60, "duration_minutes": 2
  },
  {
    "id": "tai_chi_push",
    "title": "Tai Chi Energy Push",
    "category": "Mobility",
    "tags": ["Sensory Sensitivity", "Mental Wellbeing", "Balance"],
    "intensity": "Low",
    "instructions": ["Stand/Sit comfortably.", "Push palms forward slowly while exhaling.", "Pull back inhaling."],
    "safety_note": "Focus on breath.",
    "calories": 20, "duration_minutes": 5
  },

  # --- CARDIO (ADAPTIVE) ---
  {
    "id": "seated_boxing",
    "title": "Seated Shadow Boxing",
    "category": "Cardio",
    "tags": ["Wheelchair User", "Cardio", "Stress Relief"],
    "intensity": "High",
    "instructions": ["Punch forward repeatedly.", "Keep core tight.", "Exhale on punch."],
    "safety_note": "Don't hyperextend elbows.",
    "calories": 80, "duration_minutes": 10
  },
  {
    "id": "balloon_tap",
    "title": "Balloon Taps",
    "category": "Cardio",
    "tags": ["Limited Upper-Body Mobility", "Fun", "Coordination"],
    "intensity": "Moderate",
    "instructions": ["Keep a balloon in the air.", "Use hands, head, or shoulders.", "Don't let it touch the ground."],
    "safety_note": "Watch your surroundings.",
    "calories": 50, "duration_minutes": 10
  }
]

# --- RECIPE DATA ---
RECIPES = [
    {
        "id": "r1", "title": "Power Protein Oats", "price": 0.99,
        "image": "https://images.unsplash.com/photo-1517673132405-a56a62b18caf?w=400",
        "desc": "High energy breakfast.", "ingredients": ["Oats", "Protein Powder", "Chia Seeds", "Almond Milk", "Blueberries"]
    },
    {
        "id": "r2", "title": "Green Recovery Smoothie", "price": 0.99,
        "image": "https://images.unsplash.com/photo-1610970881699-44a5587cabec?w=400",
        "desc": "Perfect post-workout.", "ingredients": ["Spinach", "Banana", "Protein Powder", "Coconut Water"]
    },
    {
        "id": "r3", "title": "Quinoa Energy Bowl", "price": 0.99,
        "image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400",
        "desc": "Lunch for stamina.", "ingredients": ["Quinoa", "Chickpeas", "Avocado", "Lemon", "Olive Oil"]
    }
]

SPONSOR_DEALS = {
    "Protein Powder": {"sponsor": "ProteinPlus", "code": "PRO20", "color": "#E3F2FD"},
    "Oats": {"sponsor": "WholeGrainz", "code": "OAT5", "color": "#F1F8E9"}
}

QUOTES = ["Small steps, big changes.", "Your pace is the best pace.", "Fitness is for every body.", "Focus on what you CAN do."]

# --- 2. STYLE & THEME ENGINE ---

def inject_custom_css(mode_active):
    if mode_active:
        # HIGH CONTRAST (STRICT)
        st.markdown(
            """
            <style>
            html, body, .stApp { background-color: #000000 !important; color: #FFFF00 !important; }
            h1, h2, h3, p, div, label, span { color: #FFFF00 !important; }
            .stButton > button { background-color: #000000 !important; color: #FFFF00 !important; border: 3px solid #FFFF00 !important; }
            input, .stSelectbox div { border: 2px solid #FFFF00 !important; }
            </style>
            """, unsafe_allow_html=True
        )
    else:
        # APPLE / CUPERTINO MODERN
        st.markdown(
            """
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
            
            /* GLOBAL RESET */
            html, body, [class*="css"] {
                font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
                color: #1D1D1F;
                background-color: #F5F5F7;
            }
            .stApp { background-color: #F5F5F7; }
            
            /* HEADERS */
            h1, h2, h3 { color: #1D1D1F; font-weight: 700; letter-spacing: -0.02em; }
            
            /* STICKY NAVBAR (Glassmorphism) */
            /* We target the container that holds our navbar buttons */
            div[data-testid="stVerticalBlock"] > div:first-child {
                position: sticky;
                top: 0;
                z-index: 999;
                background: rgba(245, 245, 247, 0.85);
                backdrop-filter: blur(12px);
                border-bottom: 1px solid rgba(0,0,0,0.05);
                padding-top: 10px;
                padding-bottom: 5px;
                margin-bottom: 20px;
            }

            /* MOVING GRADIENT BORDERS FOR INPUTS */
            @keyframes borderRotate {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            
            /* Target Streamlit Input Wrappers */
            .stTextInput > div, .stSelectbox > div, .stMultiSelect > div {
                position: relative;
                border-radius: 14px;
                background: linear-gradient(60deg, #34d399, #3b82f6, #8b5cf6, #f472b6);
                background-size: 300% 300%;
                animation: borderRotate 4s ease infinite;
                padding: 2px; /* Border thickness */
            }
            
            /* Actual Input Field (Inner) */
            .stTextInput > div > div, .stSelectbox > div > div, .stMultiSelect > div > div {
                background: #FFFFFF;
                border-radius: 12px;
                border: none; /* Hide default border */
                color: #1D1D1F;
            }
            
            /* CARDS */
            div[data-testid="stContainer"], div[data-testid="stExpander"] {
                background: #FFFFFF;
                border-radius: 20px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.04);
                border: 1px solid rgba(0,0,0,0.02);
                padding: 24px;
                transition: transform 0.2s ease;
            }
            div[data-testid="stContainer"]:hover { transform: translateY(-2px); }
            
            /* PILL BUTTONS */
            .stButton > button {
                background-color: #0071E3;
                color: white;
                border-radius: 999px;
                border: none;
                font-weight: 500;
                padding: 10px 24px;
                box-shadow: 0 2px 10px rgba(0, 113, 227, 0.2);
                transition: all 0.2s;
            }
            .stButton > button:hover {
                transform: scale(1.03);
                background-color: #0077ED;
                color: white !important;
            }
            
            /* NAVBAR BUTTONS (Text/Icon Only) */
            div[data-testid="column"] button {
                background: transparent !important;
                color: #86868B !important;
                box-shadow: none !important;
                padding: 5px !important;
            }
            div[data-testid="column"] button:hover {
                color: #0071E3 !important;
                background: rgba(0,113,227,0.1) !important;
            }
            </style>
            """, unsafe_allow_html=True
        )

# --- 3. LOGIC ---

def get_audio_html(text):
    try:
        tts = gTTS(text=text, lang='en')
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        audio_base64 = base64.b64encode(mp3_fp.read()).decode()
        return f'<audio controls src="data:audio/mp3;base64,{audio_base64}" style="width: 100%; margin-top: 10px;"></audio>'
    except:
        return "<small>Audio unavailable</small>"

def generate_workout_plan(user_profile):
    """
    STRICT TAILORED LOGIC
    """
    disability = user_profile.get('disability', [])
    equipment = user_profile.get('equipment', [])
    goal = user_profile.get('goal', 'General')
    
    suitable = []
    
    for ex in EXERCISE_LIBRARY:
        # STRICT FILTER: Exercise MUST match at least one disability tag OR be marked 'General'
        # But if user has specific needs like "Bed-Bound", we ONLY show bed-bound stuff.
        
        # 1. Exclusion Logic
        if "Bed-Bound" in disability and "Bed-Bound" not in ex['tags']:
            continue # Skip non-bed exercises
            
        if "Wheelchair User" in disability and "Wheelchair User" not in ex['tags'] and "Upper Body" not in ex['tags']:
            continue # Skip standing exercises
            
        # 2. Equipment Check
        required_eq = [t for t in ex['tags'] if t in ["Resistance Bands", "Light Weights", "Chair"]]
        has_eq = all(eq in equipment for eq in required_eq)
        if not has_eq: continue
        
        # 3. Inclusion Logic (Scoring)
        score = 0
        if any(t in ex['tags'] for t in disability): score += 10
        if goal in ex['tags']: score += 5
        
        if score > 0: suitable.append(ex)
    
    # Sort by relevance
    random.shuffle(suitable)
    return suitable[:3] if len(suitable) >= 3 else suitable

# --- 4. NAVIGATION ---

def navigate_to(page):
    st.session_state.current_page = page
    st.rerun()

def render_navbar():
    # Sticky container defined in CSS
    with st.container():
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            if st.button("🏠\nHome", use_container_width=True): navigate_to("Dashboard")
        with c2:
            if st.button("💪\nWorkouts", use_container_width=True): navigate_to("Library")
        with c3:
            if st.button("📊\nProgress", use_container_width=True): navigate_to("Progress")
        with c4:
            if st.button("🥗\nFood", use_container_width=True): navigate_to("Nutrition")
        with c5:
            if st.button("⚙️\nSettings", use_container_width=True): navigate_to("Settings")

# --- 5. SCREENS ---

def render_onboarding(is_edit=False):
    profile = st.session_state.user_profile if is_edit else {}
    if is_edit:
        st.header("Profile Settings")
    else:
        st.markdown(
            """
            <div style='text-align: center; padding: 40px;'>
                <h1 style='font-size: 3.5rem; margin-bottom: 0;'>FitBod 🥑</h1>
                <p style='color: #86868B; font-size: 1.2rem;'>Fitness for Every Body.</p>
            </div>
            """, unsafe_allow_html=True
        )
    
    with st.container():
        with st.form("profile_form"):
            st.subheader("About You")
            name = st.text_input("Name", value=profile.get("name", ""))
            
            st.subheader("Mobility & Access Needs")
            st.caption("We curate exercises based on this selection.")
            access_opts = [
                "Wheelchair User (Manual)", "Wheelchair User (Power)", 
                "Limited Lower-Body Mobility", "Hemiplegia / One-Sided Weakness",
                "Bed-Bound / Chronic Fatigue", "Sensory Sensitivity",
                "Visual Impairment", "General Fitness"
            ]
            disability = st.multiselect("Select all that apply:", access_opts, default=profile.get("disability", []))
            
            c1, c2 = st.columns(2)
            with c1:
                goal = st.selectbox("Main Goal", ["Strength", "Mobility", "Cardio", "Balance", "Rehab"], index=0)
            with c2:
                eq_opts = ["Resistance Bands", "Light Weights", "Chair", "Yoga Mat"]
                equipment = st.multiselect("Equipment", eq_opts, default=profile.get("equipment", []))
            
            if st.form_submit_button("Save Profile", use_container_width=True):
                st.session_state.user_profile = {"name": name, "disability": disability, "goal": goal, "equipment": equipment}
                st.session_state.current_page = "Dashboard"
                st.rerun()

def render_dashboard():
    profile = st.session_state.user_profile
    st.markdown(f"## Good Morning, {profile.get('name', 'Friend')} ☀️")
    
    # Quote Card
    st.markdown(
        f"""
        <div style='background: white; padding: 20px; border-radius: 18px; margin-bottom: 20px; border: 1px solid #eee;'>
            <p style='font-size: 1.1rem; font-style: italic; color: #1D1D1F; margin: 0;'>"{random.choice(QUOTES)}"</p>
        </div>
        """, unsafe_allow_html=True
    )
    
    # Quick Stats Row
    c1, c2, c3 = st.columns(3)
    c1.metric("Streak", f"{st.session_state.streak} days")
    c2.metric("Workouts", f"{len(st.session_state.journal_entries)}")
    c3.metric("Hydration", f"{st.session_state.hydration}/8 💧")
    
    if st.button("💧 Log Water", use_container_width=True):
        st.session_state.hydration += 1
        st.rerun()

    st.markdown("### Today's Plan")
    if 'current_plan' not in st.session_state:
        st.session_state.current_plan = generate_workout_plan(profile)
    
    plan = st.session_state.current_plan
    if not plan:
        st.info("No specific matches found. Try updating your equipment or needs.")
    else:
        for ex in plan:
            with st.container():
                c_img, c_txt = st.columns([1, 4])
                with c_txt:
                    st.markdown(f"**{ex['title']}**")
                    st.caption(f"{ex['duration_minutes']} min • {ex['intensity']}")
                    with st.expander("Instructions"):
                        for i, step in enumerate(ex['instructions']):
                            st.write(f"{i+1}. {step}")
                        st.info(f"Safety: {ex['safety_note']}")
                        if st.session_state.accessibility_mode:
                            st.markdown(get_audio_html(ex['title'] + ". " + ex['safety_note']), unsafe_allow_html=True)

        if st.button("Complete Workout ✅", type="primary", use_container_width=True):
            st.session_state.streak += 1
            st.balloons()
            st.success("Great job!")
            time.sleep(1)
            st.rerun()
            
    if st.button("🔄 Generate New Routine"):
        st.session_state.current_plan = generate_workout_plan(profile)
        st.rerun()

def render_nutrition():
    st.title("Nutrition Market 🥦")
    st.caption("Unlock recipes for £0.99. Ingredients added to list automatically.")
    
    c1, c2 = st.columns(2)
    for i, r in enumerate(RECIPES):
        col = c1 if i % 2 == 0 else c2
        with col:
            with st.container():
                st.image(r['image'], use_container_width=True)
                st.markdown(f"**{r['title']}**")
                if r['id'] in st.session_state.purchased_recipes:
                    st.success("Owned")
                    with st.expander("Ingredients"):
                        for x in r['ingredients']: st.write(f"• {x}")
                else:
                    if st.button(f"Buy £{r['price']}", key=r['id'], use_container_width=True):
                        st.session_state.purchased_recipes.add(r['id'])
                        for x in r['ingredients']:
                            if x not in st.session_state.shopping_list: st.session_state.shopping_list.append(x)
                        st.rerun()
    
    st.markdown("---")
    st.subheader("Shopping List 🛒")
    if not st.session_state.shopping_list:
        st.info("Empty list.")
    else:
        for item in st.session_state.shopping_list:
            cc1, cc2 = st.columns([1, 2])
            with cc1: st.checkbox(item, key=item)
            with cc2:
                if item in SPONSOR_DEALS:
                    d = SPONSOR_DEALS[item]
                    st.markdown(f"<span style='background:{d['color']}; padding:2px 6px; border-radius:4px; font-size:0.8rem;'>🎁 {d['sponsor']}: {d['code']}</span>", unsafe_allow_html=True)

def render_sponsors():
    st.title("Partners")
    st.info("Discounts available for FitBod members.")
    # Simple list for brevity
    st.markdown("**ProteinPlus**: 20% Off Code PRO20")
    st.markdown("**FlexMat**: BOGO Code FLEX15")

def render_progress():
    st.title("Progress 📈")
    # Simple chart
    data = pd.DataFrame({"Day": ["M", "T", "W", "T", "F", "S", "S"], "Mins": [30, 0, 45, 30, 0, 60, 20]})
    st.bar_chart(data.set_index("Day"))

def render_settings():
    st.title("Settings")
    acc = st.toggle("High Contrast Mode", value=st.session_state.accessibility_mode)
    if acc != st.session_state.accessibility_mode:
        st.session_state.accessibility_mode = acc
        st.rerun()
    st.divider()
    render_onboarding(True)

# --- 7. MAIN ---

if 'user_profile' not in st.session_state: st.session_state.user_profile = None
if 'current_page' not in st.session_state: st.session_state.current_page = "Dashboard"
if 'streak' not in st.session_state: st.session_state.streak = 0
if 'hydration' not in st.session_state: st.session_state.hydration = 0
if 'accessibility_mode' not in st.session_state: st.session_state.accessibility_mode = False
if 'journal_entries' not in st.session_state: st.session_state.journal_entries = []
if 'purchased_recipes' not in st.session_state: st.session_state.purchased_recipes = set()
if 'shopping_list' not in st.session_state: st.session_state.shopping_list = []

inject_custom_css(st.session_state.accessibility_mode)

if not st.session_state.user_profile:
    render_onboarding()
else:
    render_navbar()
    if st.session_state.current_page == "Dashboard": render_dashboard()
    elif st.session_state.current_page == "Library": render_library() # Re-use generic
    elif st.session_state.current_page == "Progress": render_progress()
    elif st.session_state.current_page == "Nutrition": render_nutrition()
    elif st.session_state.current_page == "Sponsors": render_sponsors()
    elif st.session_state.current_page == "Settings": render_settings()
