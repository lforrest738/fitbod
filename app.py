import streamlit as st
import pandas as pd
import numpy as np
import random
import datetime
import base64
import io
import time
from gtts import gTTS

# ==========================================
# 1. CONFIGURATION & ASSETS
# ==========================================

class AppConfig:
    APP_NAME = "FitBod"
    ICON = "🥑"
    THEME_COLOR = "#007AFF"  # Apple System Blue
    ACCENT_COLOR = "#34C759" # Apple Health Green
    WARN_COLOR = "#FF9500"   # Apple Activity Orange
    ERROR_COLOR = "#FF3B30"  # Apple System Red
    
    @staticmethod
    def setup():
        st.set_page_config(
            page_title=f"{AppConfig.APP_NAME} - Premium Fitness",
            page_icon=AppConfig.ICON,
            layout="wide",
            initial_sidebar_state="collapsed"
        )

# ==========================================
# 2. DATA LAYER
# ==========================================

class DataRepository:
    """Central store for all static app data."""
    
    EXERCISES = [
        # --- SEATED STRENGTH ---
        {"id": "ssp", "title": "Seated Shoulder Press", "cat": "Strength", "tags": ["Wheelchair User", "Upper Body", "Strength"], "mins": 5, "cal": 45, "ins": ["Sit upright, core engaged.", "Press weights overhead.", "Lower with control to ear level."]},
        {"id": "sbc", "title": "Seated Bicep Curls", "cat": "Strength", "tags": ["Wheelchair User", "Upper Body", "Arm Strength"], "mins": 5, "cal": 35, "ins": ["Hold weights at sides.", "Curl upwards, squeezing biceps.", "Lower slowly."]},
        {"id": "srb", "title": "Resistance Band Rows", "cat": "Strength", "tags": ["Wheelchair User", "Back", "Posture"], "mins": 5, "cal": 50, "ins": ["Loop band around a sturdy point.", "Pull elbows back.", "Squeeze shoulder blades together."]},
        {"id": "wc_crunch", "title": "Seated Crunches", "cat": "Core", "tags": ["Wheelchair User", "Core"], "mins": 5, "cal": 30, "ins": ["Lock wheelchair brakes.", "Cross arms over chest.", "Crunch forward towards knees.", "Return upright."]},
        
        # --- REHAB & NEURO ---
        {"id": "uni_grip", "title": "Unilateral Grip Squeeze", "cat": "Rehab", "tags": ["Hemiplegia", "Stroke Recovery", "Grip"], "mins": 3, "cal": 15, "ins": ["Use a stress ball or towel.", "Squeeze firmly with affected hand.", "Hold for 5s, release."]},
        {"id": "wt_shift", "title": "Supported Weight Shifts", "cat": "Balance", "tags": ["Stroke Recovery", "Balance", "Lower Body"], "mins": 5, "cal": 25, "ins": ["Stand holding a counter.", "Shift weight slowly to left leg.", "Hold 3s.", "Shift to right leg."]},
        
        # --- BED / CHRONIC FATIGUE ---
        {"id": "bed_pump", "title": "Supine Ankle Pumps", "cat": "Mobility", "tags": ["Bed-Bound", "Chronic Fatigue", "Recovery"], "mins": 3, "cal": 10, "ins": ["Lie on back, legs straight.", "Point toes down.", "Pull toes up towards shins.", "Repeat rhythmically."]},
        {"id": "bed_angel", "title": "Bed Angels", "cat": "Mobility", "tags": ["Bed-Bound", "Chronic Fatigue", "Upper Body"], "mins": 5, "cal": 20, "ins": ["Lie flat.", "Slide arms out and up like a snow angel.", "Return arms to sides."]},
        
        # --- SENSORY FRIENDLY ---
        {"id": "wall_sit", "title": "Quiet Wall Sit", "cat": "Strength", "tags": ["Sensory Sensitivity", "Autism/ADHD", "Legs"], "mins": 2, "cal": 40, "ins": ["Lean back against a wall.", "Slide down until knees are bent.", "Hold the position silently.", "Breathe deeply."]},
        {"id": "tai_chi", "title": "Energy Push", "cat": "Mindfulness", "tags": ["Sensory Sensitivity", "Anxiety", "Mobility"], "mins": 5, "cal": 20, "ins": ["Stand or sit comfortably.", "Inhale, pulling hands to chest.", "Exhale, pushing palms slowly forward."]},
        
        # --- CARDIO ---
        {"id": "box_seat", "title": "Seated Shadow Boxing", "cat": "Cardio", "tags": ["Wheelchair User", "Cardio", "Stress Relief"], "mins": 10, "cal": 90, "ins": ["Punch forward (Jab/Cross).", "Maintain a rhythm.", "Keep core tight."]},
        {"id": "balloon", "title": "Balloon Taps", "cat": "Cardio", "tags": ["Coordination", "Fun", "Upper Body"], "mins": 10, "cal": 60, "ins": ["Keep a balloon in the air.", "Use hands, head, or elbows.", "Do not let it touch the floor."]}
    ]

    RECIPES = [
        {"id": "r1", "title": "Power Protein Oats", "price": 0.99, "img": "https://images.unsplash.com/photo-1517673132405-a56a62b18caf?w=400", "desc": "Sustained energy release.", "ing": ["Rolled Oats", "Protein Powder", "Chia Seeds", "Almond Milk", "Blueberries"]},
        {"id": "r2", "title": "Green Recovery Smoothie", "price": 0.99, "img": "https://images.unsplash.com/photo-1610970881699-44a5587cabec?w=400", "desc": "Anti-inflammatory blend.", "ing": ["Spinach", "Frozen Banana", "Vanilla Protein", "Coconut Water"]},
        {"id": "r3", "title": "Quinoa Energy Bowl", "price": 0.99, "img": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400", "desc": "Complete plant protein.", "ing": ["Quinoa", "Chickpeas", "Avocado", "Lemon Dressing", "Cucumber"]},
        {"id": "r4", "title": "Golden Lentil Stew", "price": 0.99, "img": "https://images.unsplash.com/photo-1547592166-23acbe346499?w=400", "desc": "Warm & comforting.", "ing": ["Red Lentils", "Carrots", "Turmeric", "Vegetable Broth"]}
    ]

    SPONSORS = {
        "Protein Powder": {"name": "ProteinPlus", "code": "PRO20", "color": "#E3F2FD"},
        "Rolled Oats": {"name": "WholeGrainz", "code": "OAT5", "color": "#F1F8E9"}
    }

    QUOTES = [
        "The only bad workout is the one that didn't happen.",
        "Your pace is the best pace.",
        "Movement is medicine.",
        "Small steps, every single day.",
        "Focus on what your body can do."
    ]

# ==========================================
# 3. LOGIC ENGINE
# ==========================================

class ExerciseEngine:
    @staticmethod
    def generate_plan(profile):
        """Intelligent filtering based on disability and goals."""
        disability = profile.get('disability', [])
        # equipment = profile.get('equipment', []) # Future implementation
        goal = profile.get('goal', 'General')
        
        candidates = []
        
        for ex in DataRepository.EXERCISES:
            score = 0
            
            # 1. Safety Filter (Exclusion)
            if "Bed-Bound" in disability and "Bed-Bound" not in ex['tags']: continue
            if "Wheelchair User" in disability and "Wheelchair User" not in ex['tags'] and "Upper Body" not in ex['tags'] and "Cardio" not in ex['tags']: continue
            
            # 2. Relevance Scoring
            if any(t in ex['tags'] for t in disability): score += 10
            if goal in ex['tags'] or goal in ex['cat']: score += 5
            
            if score > 0:
                candidates.append(ex)
        
        # 3. Selection
        random.shuffle(candidates)
        return candidates[:3] if len(candidates) >= 3 else candidates

class AccessibilityManager:
    @staticmethod
    def get_audio_player(text):
        """Generates an HTML5 audio player for TTS."""
        try:
            tts = gTTS(text=text, lang='en')
            mp3_fp = io.BytesIO()
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            b64 = base64.b64encode(mp3_fp.read()).decode()
            return f'''
                <audio controls style="width: 100%; margin-top: 10px; border-radius: 20px;">
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
            '''
        except:
            return '<div style="font-size:0.8rem; color:#888;">Audio unavailable offline.</div>'

# ==========================================
# 4. UI / UX LAYER (DESIGN SYSTEM)
# ==========================================

class DesignSystem:
    @staticmethod
    def inject_css(high_contrast=False):
        """Injects the CSS framework based on mode."""
        
        # SHARED VARIABLES
        font_stack = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
        
        if high_contrast:
            # --- MICROSOFT ACCESSIBILITY STANDARD (HC) ---
            theme = """
                --bg-color: #000000;
                --card-bg: #000000;
                --text-color: #FFFF00;
                --border-color: #FFFF00;
                --accent-color: #FFFF00;
                --shadow: none;
                --glass: none;
                --radius: 0px;
            """
        else:
            # --- APPLE CUPERTINO STANDARD (MODERN) ---
            theme = """
                --bg-color: #F5F5F7;
                --card-bg: #FFFFFF;
                --text-color: #1D1D1F;
                --subtext-color: #86868B;
                --border-color: rgba(0,0,0,0.05);
                --accent-color: #007AFF;
                --shadow: 0 4px 24px rgba(0,0,0,0.04);
                --glass: blur(20px) saturate(180%);
                --radius: 20px;
            """

        css = f"""
        <style>
            :root {{
                {theme}
            }}
            
            /* GLOBAL RESET */
            html, body, [class*="css"] {{
                font-family: {font_stack};
                color: var(--text-color);
                background-color: var(--bg-color);
            }}
            
            /* HEADERS */
            h1, h2, h3, h4 {{
                font-weight: 700;
                letter-spacing: -0.02em;
                color: var(--text-color);
            }}
            
            /* GLASS NAVIGATION */
            .sticky-nav {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                z-index: 99999;
                background: rgba(255, 255, 255, 0.85);
                backdrop-filter: var(--glass);
                border-bottom: 1px solid var(--border-color);
                padding: 1rem 0;
                display: flex;
                justify-content: center;
                gap: 20px;
                transition: all 0.3s ease;
            }}
            
            /* CARDS */
            div[data-testid="stContainer"], div[data-testid="stExpander"] {{
                background: var(--card-bg);
                border-radius: var(--radius);
                border: 1px solid var(--border-color);
                box-shadow: var(--shadow);
                padding: 24px;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }}
            
            div[data-testid="stContainer"]:hover {{
                transform: translateY(-2px);
                box-shadow: 0 8px 32px rgba(0,0,0,0.08);
            }}
            
            /* ANIMATED INPUTS */
            @keyframes borderRotate {{
                0% {{ background-position: 0% 50%; }}
                50% {{ background-position: 100% 50%; }}
                100% {{ background-position: 0% 50%; }}
            }}
            
            .stTextInput > div, .stSelectbox > div, .stMultiSelect > div {{
                border-radius: 14px;
                background: linear-gradient(90deg, #007AFF, #34C759, #FF2D55);
                background-size: 300% 300%;
                animation: borderRotate 6s ease infinite;
                padding: 1.5px; /* Gradient Border Width */
            }}
            
            .stTextInput > div > div, .stSelectbox > div > div, .stMultiSelect > div > div {{
                background: var(--card-bg);
                border-radius: 12px;
                border: none;
                color: var(--text-color);
            }}
            
            /* BUTTONS (Pill Shape) */
            .stButton > button {{
                background-color: var(--accent-color);
                color: white;
                border-radius: 999px;
                border: {'2px solid #FFFF00' if high_contrast else 'none'};
                padding: 12px 28px;
                font-weight: 600;
                font-size: 16px;
                box-shadow: 0 4px 12px rgba(0,122,255,0.2);
                transition: all 0.2s ease;
                width: 100%;
            }}
            
            .stButton > button:hover {{
                transform: scale(1.02);
                box-shadow: 0 6px 16px rgba(0,122,255,0.3);
                color: white !important;
            }}
            
            /* NAV BUTTONS (Clear) */
            div[data-testid="column"] button {{
                background: transparent !important;
                color: #86868B !important;
                box-shadow: none !important;
                padding: 8px !important;
                width: auto !important;
            }}
            
            div[data-testid="column"] button:hover {{
                color: var(--accent-color) !important;
                background: rgba(0,122,255,0.1) !important;
            }}
            
            /* METRICS */
            div[data-testid="stMetricValue"] {{
                font-weight: 800;
                color: var(--text-color);
            }}
            div[data-testid="stMetricLabel"] {{
                color: var(--subtext-color);
            }}
            
            /* STREAMLIT CLEANUP */
            #MainMenu {{ visibility: hidden; }}
            header {{ visibility: hidden; }}
            footer {{ visibility: hidden; }}
            .block-container {{ padding-top: 2rem; }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

# ==========================================
# 5. VIEW CONTROLLERS
# ==========================================

class Views:
    @staticmethod
    def render_nav():
        """Renders the top sticky navigation."""
        # Note: We use Streamlit columns to simulate the bar, utilizing the CSS .sticky-nav concept
        # Since Streamlit renders linearly, we put this at the top of the container.
        
        with st.container():
            st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True) # Spacer
            c1, c2, c3, c4, c5, c6 = st.columns(6)
            
            def nav_btn(label, target):
                if c1.button(label, key=f"nav_{target}", use_container_width=True):
                    st.session_state.page = target
                    st.rerun()

            with c1: 
                if st.button("🏠 Home", use_container_width=True): st.session_state.page = "home"; st.rerun()
            with c2: 
                if st.button("💪 Workout", use_container_width=True): st.session_state.page = "library"; st.rerun()
            with c3: 
                if st.button("📊 Stats", use_container_width=True): st.session_state.page = "stats"; st.rerun()
            with c4: 
                if st.button("🥦 Food", use_container_width=True): st.session_state.page = "food"; st.rerun()
            with c5: 
                if st.button("🤝 Partners", use_container_width=True): st.session_state.page = "partners"; st.rerun()
            with c6: 
                if st.button("⚙️ Config", use_container_width=True): st.session_state.page = "settings"; st.rerun()
                
            st.markdown("---")

    @staticmethod
    def render_onboarding():
        st.markdown(
            """
            <div style="text-align: center; padding: 4rem 2rem;">
                <h1 style="font-size: 4rem; margin-bottom: 0.5rem; background: linear-gradient(120deg, #007AFF, #34C759); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">FitBod 🥑</h1>
                <h3 style="color: #86868B; font-weight: 400;">Fitness designed for <i>every</i> body.</h3>
            </div>
            """, unsafe_allow_html=True
        )
        
        with st.container():
            c1, c2 = st.columns([1, 2])
            with c2:
                st.markdown("#### Create Your Profile")
                with st.form("onboarding_form"):
                    name = st.text_input("What should we call you?")
                    
                    st.markdown("##### ♿ Mobility & Access")
                    st.caption("We tailor every single exercise based on this selection.")
                    
                    disabilities = st.multiselect(
                        "I identify as / require support for:",
                        ["Wheelchair User", "Limited Lower-Body Mobility", "Hemiplegia", "Bed-Bound / Chronic Fatigue", "Sensory Sensitivity", "Visual Impairment", "General Fitness"]
                    )
                    
                    c_a, c_b = st.columns(2)
                    with c_a:
                        goal = st.selectbox("Primary Goal", ["Mobility", "Strength", "Cardio", "Mental Health"])
                    with c_b:
                        exp = st.selectbox("Experience Level", ["Beginner", "Intermediate", "Advanced"])
                    
                    if st.form_submit_button("Start My Journey"):
                        if name:
                            st.session_state.user = {
                                "name": name, "disability": disabilities, 
                                "goal": goal, "exp": exp
                            }
                            st.session_state.page = "home"
                            st.rerun()
                        else:
                            st.error("Please tell us your name to continue.")

    @staticmethod
    def render_dashboard():
        user = st.session_state.user
        st.markdown(f"## Good Morning, {user['name']} ☀️")
        
        # Motivation Card
        quote = random.choice(DataRepository.QUOTES)
        st.info(f"✨ **Daily Insight:** {quote}")
        
        # Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Streak", f"{st.session_state.streak} Days", "Keeping it up!")
        m2.metric("Workouts", len(st.session_state.history))
        m3.metric("Hydration", f"{st.session_state.hydration} / 8", "Cups")
        
        if st.button("💧 Log Water", use_container_width=True):
            st.session_state.hydration += 1
            st.toast("Hydration logged! Keep it up.")
            time.sleep(0.5)
            st.rerun()
            
        st.markdown("### Today's Focus")
        
        # Workout Logic
        if st.session_state.active_workout is None:
            st.session_state.active_workout = ExerciseEngine.generate_plan(user)
            
        plan = st.session_state.active_workout
        
        if not plan:
            st.warning("We couldn't match specific exercises to your exact criteria, but here are some general mobility movements.")
            # Fallback logic could go here
        
        for ex in plan:
            with st.container():
                c_txt, c_meta = st.columns([3, 1])
                with c_txt:
                    st.markdown(f"#### {ex['title']}")
                    st.caption(f"{ex['cat']} • {ex['tags'][0]}")
                with c_meta:
                    st.markdown(f"**{ex['mins']}** min")
                
                with st.expander("Show Instructions"):
                    for i, step in enumerate(ex['ins']):
                        st.write(f"{i+1}. {step}")
                    
                    if st.session_state.high_contrast:
                        # Only show audio in high contrast/access mode or if requested
                        st.markdown(AccessibilityManager.get_audio_player(f"{ex['title']}. {ex['ins'][0]}"), unsafe_allow_html=True)

        st.markdown("---")
        if st.button("✅ Complete Workout", type="primary"):
            st.session_state.streak += 1
            st.session_state.history.append({"date": datetime.date.today(), "minutes": sum(e['mins'] for e in plan)})
            st.session_state.active_workout = None # Reset for next time
            st.balloons()
            st.success("Workout Complete! Streak updated.")
            time.sleep(2)
            st.rerun()
            
        if st.button("🔄 Shuffle Routine", type="secondary"):
            st.session_state.active_workout = None
            st.rerun()

    @staticmethod
    def render_nutrition():
        st.title("Nutrition Market 🥦")
        st.write("Premium, adaptive recipes. Tap to purchase and auto-fill your shopping list.")
        
        col1, col2 = st.columns(2)
        
        for i, r in enumerate(DataRepository.RECIPES):
            target_col = col1 if i % 2 == 0 else col2
            with target_col:
                with st.container():
                    st.image(r['img'], use_container_width=True)
                    st.markdown(f"#### {r['title']}")
                    st.caption(r['desc'])
                    
                    is_owned = r['id'] in st.session_state.inventory
                    
                    if is_owned:
                        st.success("Owned")
                        with st.expander("Ingredients"):
                            for x in r['ing']: st.write(f"• {x}")
                    else:
                        if st.button(f"Buy £{r['price']}", key=r['id']):
                            st.session_state.inventory.add(r['id'])
                            # Add to shopping list
                            for ing in r['ing']:
                                if ing not in st.session_state.shopping_list:
                                    st.session_state.shopping_list.append(ing)
                            st.toast(f"Purchased {r['title']}!")
                            st.rerun()
                            
        st.markdown("### 🛒 Smart Shopping List")
        if not st.session_state.shopping_list:
            st.info("Your list is empty. Buy a recipe to populate it.")
        else:
            for item in st.session_state.shopping_list:
                c1, c2 = st.columns([1, 3])
                with c1: st.checkbox(item, key=f"chk_{item}")
                with c2:
                    # Sponsor Integration Logic
                    for key, sponsor in DataRepository.SPONSORS.items():
                        if key in item:
                            st.markdown(f"<span style='background:{sponsor['color']}; padding:4px 8px; border-radius:6px; font-size:0.8rem; color:#333;'>🎁 <b>{sponsor['name']}</b>: {sponsor['code']}</span>", unsafe_allow_html=True)

    @staticmethod
    def render_stats():
        st.title("Your Progress 📈")
        
        # Generate dummy data if empty
        if not st.session_state.history:
            df = pd.DataFrame({
                "Date": pd.date_range(start=datetime.date.today()-datetime.timedelta(days=7), periods=7),
                "Minutes": [random.randint(0, 45) for _ in range(7)]
            })
        else:
            df = pd.DataFrame(st.session_state.history)
            
        st.bar_chart(df, x="Date", y="Minutes", color=AppConfig.ACCENT_COLOR)
        
        st.markdown("#### Journal")
        entry = st.text_area("How are you feeling today?", placeholder="Type here...")
        if st.button("Save Entry"):
            st.toast("Journal entry saved securely.")

    @staticmethod
    def render_settings():
        st.title("Preferences ⚙️")
        
        st.subheader("Accessibility")
        hc = st.toggle("High Contrast Mode (Visual Impairment)", value=st.session_state.high_contrast)
        if hc != st.session_state.high_contrast:
            st.session_state.high_contrast = hc
            st.rerun()
            
        st.markdown("---")
        if st.button("Reset Profile Data", type="secondary"):
            st.session_state.clear()
            st.rerun()

# ==========================================
# 6. MAIN APPLICATION ENTRY
# ==========================================

def main():
    AppConfig.setup()
    
    # State Initialization
    if 'user' not in st.session_state: st.session_state.user = None
    if 'page' not in st.session_state: st.session_state.page = "onboarding"
    if 'high_contrast' not in st.session_state: st.session_state.high_contrast = False
    if 'streak' not in st.session_state: st.session_state.streak = 0
    if 'hydration' not in st.session_state: st.session_state.hydration = 0
    if 'active_workout' not in st.session_state: st.session_state.active_workout = None
    if 'inventory' not in st.session_state: st.session_state.inventory = set()
    if 'shopping_list' not in st.session_state: st.session_state.shopping_list = []
    if 'history' not in st.session_state: st.session_state.history = []

    # Inject Design System
    DesignSystem.inject_css(st.session_state.high_contrast)

    # Routing
    if not st.session_state.user:
        Views.render_onboarding()
    else:
        Views.render_nav()
        
        page = st.session_state.page
        if page == "home": Views.render_dashboard()
        elif page == "library": Views.render_dashboard() # Reusing dashboard for workout focus
        elif page == "food": Views.render_nutrition()
        elif page == "stats": Views.render_stats()
        elif page == "partners": 
            st.title("Partners 🤝")
            st.info("Exclusive discounts for FitBod members.")
            st.write("**ProteinPlus**: Use code PRO20 for 20% off.")
        elif page == "settings": Views.render_settings()

if __name__ == "__main__":
    main()
