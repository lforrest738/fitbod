# FitBod - Accessible Fitness (Revamped UI)
# Filename: fitbod_streamlit_improved.py
# Purpose: A cleaned, modular and significantly restyled Streamlit app for FitBod
# - Improved visual design and accessibility
# - Cleaner componentization and comments
# - Safer audio handling and offline-friendly fallback
# - Accessibility toggle and large-text mode
# - Better navigation and responsive layout

import streamlit as st
import pandas as pd
import numpy as np
import random
import datetime
import base64
import io
import time
from gtts import gTTS

# ----------------------
# Configuration
# ----------------------
st.set_page_config(
    page_title="FitBod - Accessible Fitness",
    page_icon="🥑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------
# Constants - Exercise Library & Data
# ----------------------
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

# ----------------------
# Styling - improved, accessible, modern
# ----------------------

def inject_custom_css(accessibility_mode: bool):
    # Note - fonts are chosen for legibility and contrast
    if accessibility_mode:
        css = """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&display=swap');
        html, body, [class*='css'] { font-family: 'Atkinson Hyperlegible', sans-serif; }
        .stApp { background: #000; color: #fff; }
        /* Large readable content */
        h1, h2, h3, p, label { color: #fff !important; }
        .big-button > button { background: #ffd400 !important; color: #000 !important; font-weight: 700 !important; padding: 12px 18px !important; border-radius: 6px !important; }
        .card { background: #111; border: 3px solid #ffd400; padding: 18px; border-radius: 8px; }
        .focus-outline:focus { outline: 4px solid #ffd400 !important; }
        </style>
        """
    else:
        css = """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Poppins:wght@500;700&display=swap');
        html, body, [class*='css'] { font-family: 'Inter', sans-serif; }
        .stApp { background: linear-gradient(180deg, #050505 0%, #0b0b0b 100%); color: #e6eef6; }

        /* Header gradient text */
        .hero-title { font-family: 'Poppins', sans-serif; font-weight:800; font-size:48px; background: linear-gradient(90deg, #34d399, #60a5fa); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }

        /* Card surfaces */
        .card { background: linear-gradient(180deg, #0f1720, #111827); border-radius: 14px; padding: 18px; box-shadow: 0 6px 24px rgba(0,0,0,0.6); border: 1px solid rgba(255,255,255,0.03); }
        .card h3 { font-family: 'Poppins', sans-serif; }

        /* Buttons */
        .primary-btn > button { background: linear-gradient(90deg,#34d399,#10b981) !important; color: #000 !important; border-radius: 12px !important; padding: 10px 14px !important; font-weight:700 !important; }
        .ghost-btn > button { background: transparent !important; color: #9ca3af !important; border: 1px solid rgba(156,163,175,0.08) !important; }

        /* subtle focus ring for keyboard users */
        .focus-outline:focus { outline: 3px solid rgba(59,130,246,0.35) !important; }

        /* small responsive tweaks */
        @media (max-width: 700px) {
            .hero-title { font-size: 34px; }
        }
        </style>
        """
    st.markdown(css, unsafe_allow_html=True)

# ----------------------
# Utilities
# ----------------------

def get_greeting(name: str):
    hour = datetime.datetime.now().hour
    if hour < 12:
        msg = "Good Morning"
    elif hour < 18:
        msg = "Good Afternoon"
    else:
        msg = "Good Evening"
    return f"{msg}, {name}!" if name else msg


def safe_text_to_speech(text: str):
    """Return an html audio tag for generated speech. If audio generation fails, return None."""
    try:
        tts = gTTS(text=text, lang='en')
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        audio_base64 = base64.b64encode(mp3_fp.read()).decode()
        return f'<audio controls src="data:audio/mp3;base64,{audio_base64}" style="width:100%; margin-top:10px"></audio>'
    except Exception:
        return None


def generate_workout_plan(user_profile: dict):
    disability = user_profile.get('disability', [])
    equipment = user_profile.get('equipment', [])
    goal = user_profile.get('goal', 'Mobility & Flexibility')

    suitable = []
    for ex in EXERCISE_LIBRARY:
        score = 0
        # match tags loosely
        if any(d in ex['tags'] for d in disability):
            score += 2
        # equipment check
        required_eq = [t for t in ex['tags'] if t in ["Resistance Bands", "Light Weights (Dumbbells)", "Chair (Sturdy)", "Light Weights"]]
        # consider 'None' as always satisfied
        if "None" in ex['tags'] or not required_eq or any(eq in equipment for eq in required_eq) or "None (Bodyweight Only)" in equipment:
            score += 1
        # goal matching
        if goal in ex['tags'] or goal in ex['category']:
            score += 1
        if score > 0:
            suitable.append(ex)

    # Return a short routine - try for 3 exercises
    if len(suitable) >= 3:
        return random.sample(suitable, 3)
    return suitable


def generate_dummy_history():
    dates = pd.date_range(end=datetime.date.today(), periods=30)
    data = {
        "Date": dates,
        "Minutes": np.random.randint(10, 60, size=30),
        "Calories": np.random.randint(80, 350, size=30),
        "Mood": np.random.choice(["Energized", "Tired", "Happy", "Strong"], size=30)
    }
    # rest days
    mask = np.random.choice([True, False], size=30, p=[0.15, 0.85])
    data['Minutes'][mask] = 0
    data['Calories'][mask] = 0
    return pd.DataFrame(data)

# ----------------------
# UI Components - cleaned and accessible
# ----------------------

def app_header():
    left, right = st.columns([3,1])
    with left:
        st.markdown('<div class="hero-title">FitBod <span style="font-size:28px;">🥑</span></div>', unsafe_allow_html=True)
        st.markdown('<p style="color:#9CA3AF; margin-top:6px">Adaptive workouts for every body - accessible by design.</p>', unsafe_allow_html=True)
    with right:
        st.session_state.streak = st.session_state.get('streak', 0)
        st.metric('Streak', f'{st.session_state.streak} 🔥')


def nav_menu():
    # Sidebar navigation - clearer and keyboard friendly
    st.sidebar.header('Navigation')
    pages = ['Dashboard', 'Library', 'Progress', 'Nutrition', 'Sponsors', 'Settings']
    choice = st.sidebar.radio('Go to', pages, index=pages.index(st.session_state.get('current_page', 'Dashboard')))
    st.session_state.current_page = choice


def render_profile_onboard(edit: bool=False):
    profile = st.session_state.get('user_profile') or {}
    title = 'Edit Profile' if edit else 'Create Your Profile'
    st.header(title)

    with st.form('profile-form'):
        name = st.text_input('First Name', value=profile.get('name', ''))
        age_group = st.selectbox('Age Category', ['Under 18','18-24','25-34','35-44','45-54','55-64','65+'], index=0 if not profile else ['Under 18','18-24','25-34','35-44','45-54','55-64','65+'].index(profile.get('age_group','25-34')))

        options = [
            'Wheelchair User', 'Limited Upper-Body Mobility', 'Limited Lower-Body Mobility', 'Limited Grip Strength',
            'Balance Issues / Vertigo','Chronic Pain / Fatigue','Visual Impairment','Neurodivergent','Post-Injury Recovery','None / General Fitness'
        ]
        disability = st.multiselect('Access & Mobility - select all that apply', options, default=profile.get('disability', []))

        goal_opts = ['Strength', 'Mobility & Flexibility', 'Balance & Stability', 'Cardiovascular Health', 'Weight Management', 'Mental Wellbeing']
        goal = st.selectbox('Main Goal', goal_opts, index=goal_opts.index(profile.get('goal','Mobility & Flexibility')) if profile.get('goal') in goal_opts else 1)

        equipment_opts = ['Resistance Bands', 'Light Weights', 'Chair', 'Yoga Mat', 'None (Bodyweight Only)']
        equipment = st.multiselect('Available equipment', equipment_opts, default=profile.get('equipment', []))

        style = st.select_slider('Coaching style', ['Gentle','Direct','Energetic'], value=profile.get('style','Gentle'))
        diet = st.selectbox('Dietary preference', ['No Preference','Vegetarian','Vegan','Gluten-Free','High Protein'], index=0 if not profile else ['No Preference','Vegetarian','Vegan','Gluten-Free','High Protein'].index(profile.get('diet','No Preference')))

        submitted = st.form_submit_button('Save Profile')
        if submitted:
            if not name:
                st.error('Please add your name')
            else:
                st.session_state.user_profile = {
                    'name': name,
                    'age_group': age_group,
                    'disability': disability,
                    'goal': goal,
                    'equipment': equipment,
                    'style': style,
                    'diet': diet
                }
                st.success('Profile saved')
                # set defaults
                st.session_state.current_page = 'Dashboard'
                st.session_state.current_plan = None
                st.experimental_rerun()


def exercise_card(ex):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"### {ex['title']}")
    st.markdown(f"**{ex['category']}**  •  *{ex['intensity']} intensity*")
    st.write('')
    cols = st.columns([3,1])
    with cols[0]:
        st.markdown('**Instructions**')
        for i, step in enumerate(ex['instructions']):
            st.write(f"{i+1}. {step}")
    with cols[1]:
        st.markdown('**Safety**')
        st.info(ex['safety_note'])
        st.markdown(f"**Estimated**: {ex['duration_minutes']}m • {ex['calories']} kcal")

    # Accessibility - simple audio option
    if st.session_state.get('accessibility_mode'):
        speech_html = safe_text_to_speech(f"{ex['title']}. {' '.join(ex['instructions'])}")
        if speech_html:
            st.markdown(speech_html, unsafe_allow_html=True)
        else:
            st.caption('Audio unavailable')
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------
# Page renderers
# ----------------------

def page_dashboard():
    profile = st.session_state.get('user_profile', {})
    name = profile.get('name', 'Friend')
    st.subheader(get_greeting(name))

    # Motivation bar
    quote = random.choice(QUOTES)
    st.info(f'"{quote}"')

    # Quick actions row
    col1, col2, col3 = st.columns([2,1,1])
    with col1:
        st.metric('Current Focus', profile.get('goal','General Fitness'))
    with col2:
        hyd = st.session_state.get('hydration', 0)
        st.metric('Hydration', f'{hyd}/8')
        if st.button('Drink Water'):
            st.session_state.hydration = hyd + 1
            st.experimental_rerun()
    with col3:
        st.metric('Streak', st.session_state.get('streak', 0))

    st.markdown('---')

    # Today's Plan
    st.header("Today's Plan")
    if st.session_state.get('current_plan') is None:
        st.session_state.current_plan = generate_workout_plan(st.session_state.get('user_profile', {}))

    plan = st.session_state.current_plan or []
    if not plan:
        st.warning('No tailored plan found - showing gentle mobility starters')
        plan = [e for e in EXERCISE_LIBRARY if 'Mobility' in e['category'] or 'Mobility' in e['tags']][:2]

    for ex in plan:
        exercise_card(ex)

    if st.button('Complete Workout'):
        st.session_state.streak = st.session_state.get('streak', 0) + 1
        st.session_state.workout_completed = True
        st.success('Well done! Workout logged.')

    if st.session_state.get('workout_completed'):
        feeling = st.text_area('How are you feeling after that?')
        if st.button('Save Note'):
            note = {'date': datetime.datetime.now().isoformat(timespec='minutes'), 'note': feeling}
            st.session_state.journal_entries.append(note)
            st.success('Saved to journal')


def page_library():
    st.header('Exercise Library')
    search = st.text_input('Search...')
    categories = ['All'] + sorted(list({e['category'] for e in EXERCISE_LIBRARY}))
    category = st.selectbox('Category', categories)

    filtered = EXERCISE_LIBRARY
    if category != 'All':
        filtered = [e for e in filtered if e['category'] == category]
    if search:
        filtered = [e for e in filtered if search.lower() in e['title'].lower()]

    for e in filtered:
        exercise_card(e)


def page_progress():
    st.header('Your Progress')
    if 'history' not in st.session_state:
        st.session_state.history = generate_dummy_history()
    df = st.session_state.history

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric('Total Active Mins', int(df['Minutes'].sum() + st.session_state.get('streak', 0)*15))
    with c2:
        st.metric('Calories', int(df['Calories'].sum()))
    with c3:
        st.metric('Workouts', int((df['Minutes']>0).sum()))

    st.area_chart(df.set_index('Date')['Minutes'])
    st.bar_chart(df.set_index('Date')['Calories'])

    st.header('Journal')
    if st.session_state.get('journal_entries'):
        for j in reversed(st.session_state['journal_entries']):
            with st.expander(j['date']):
                st.write(j['note'])
    else:
        st.info('No journal entries yet - finish a workout to add one')


def page_nutrition():
    st.header('Nutrition & Meal Plans')
    if st.session_state.get('premium_unlocked'):
        st.success('Premium unlocked - showing personalized plans')
        st.write('Daily meal example:')
        st.write('- Breakfast: Power oats')
        st.write('- Lunch: Energy bowl')
        st.write('- Dinner: Recovery stew')
    else:
        st.info('Premium content - 50+ recipes and personalised meal plans')
        if st.button('Unlock Premium - $4.99'):
            with st.spinner('Processing...'):
                time.sleep(1)
            st.session_state.premium_unlocked = True
            st.experimental_rerun()


def page_sponsors():
    st.header('Sponsors')
    st.write('Our partners help keep FitBod free for everyone')
    sponsors = [
        ('EcoHydrate', '20% OFF Smart Bottles'),
        ('FlexMat', 'Buy 1 Get 1 Free'),
        ('ProteinPlus', 'Free Sample Pack')
    ]
    for name, offer in sponsors:
        st.markdown(f'**{name}** - {offer}')


def page_settings():
    st.header('Settings')
    access = st.checkbox('Accessibility mode - high contrast and large text', value=st.session_state.get('accessibility_mode', False))
    if access != st.session_state.get('accessibility_mode', False):
        st.session_state['accessibility_mode'] = access
        st.experimental_rerun()

    if st.button('Edit profile'):
        render_profile_onboard(edit=True)

# ----------------------
# Bootstrap / Routing
# ----------------------

# Session defaults
if 'user_profile' not in st.session_state: st.session_state['user_profile'] = None
if 'current_page' not in st.session_state: st.session_state['current_page'] = 'Dashboard'
if 'streak' not in st.session_state: st.session_state['streak'] = 0
if 'hydration' not in st.session_state: st.session_state['hydration'] = 0
if 'accessibility_mode' not in st.session_state: st.session_state['accessibility_mode'] = False
if 'premium_unlocked' not in st.session_state: st.session_state['premium_unlocked'] = False
if 'workout_completed' not in st.session_state: st.session_state['workout_completed'] = False
if 'journal_entries' not in st.session_state: st.session_state['journal_entries'] = []

# inject styles
inject_custom_css(st.session_state.get('accessibility_mode', False))

# top header
app_header()

# sidebar nav and quick profile creation
nav_menu()

# Force onboarding if no profile
if not st.session_state.get('user_profile'):
    st.info('Welcome - let us set up your FitBod account')
    render_profile_onboard(edit=False)
else:
    page = st.session_state.get('current_page', 'Dashboard')
    if page == 'Dashboard':
        page_dashboard()
    elif page == 'Library':
        page_library()
    elif page == 'Progress':
        page_progress()
    elif page == 'Nutrition':
        page_nutrition()
    elif page == 'Sponsors':
        page_sponsors()
    elif page == 'Settings':
        page_settings()

# End of file
