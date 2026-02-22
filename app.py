import streamlit as st
import database as db
import auth
from datetime import date
import streamlit.components.v1 as components
from i18n_dict import get_t

# --- Page Configuration ---
st.set_page_config(
    page_title="SkillSync AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Session State Initialization ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'
if 'language' not in st.session_state:
    st.session_state.language = 'en'

# --- Massive Elite Hackathon UI/UX CSS Injection ---
def load_css():
    theme = st.session_state.get('theme', 'dark')
    
    if theme == 'dark':
        theme_vars = """
        :root {
            --bg-color: #0B0F19;
            --surface-color: #111827;
            --elevated-color: #1F2937;
            --border-color: rgba(255,255,255,0.06);
            --text-primary: #F9FAFB;
            --text-secondary: #9CA3AF;
            --accent-gradient: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%);
            --success: #22C55E;
            --warning: #F59E0B;
            --danger: #EF4444;
        }
        """
    else:
        theme_vars = """
        :root {
            --bg-color: #F8FAFC;
            --surface-color: #FFFFFF;
            --elevated-color: #F1F5F9;
            --border-color: rgba(0,0,0,0.12); /* darker border for visibility */
            --text-primary: #0F172A;
            --text-secondary: #475569;
            --accent-gradient: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%);
            --success: #22C55E;
            --warning: #F59E0B;
            --danger: #EF4444;
        }
        """

    base_css = """
    <style>
        /* 1. Global Typography: Inter */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        html, body, [class*="css"], .stApp, .stMarkdown p, .stMarkdown span, .stMarkdown li {
            font-family: 'Inter', system-ui, ui-sans-serif, sans-serif !important;
            color: var(--text-primary) !important;
        }
        
        .stApp {
            background-color: var(--bg-color) !important;
        }
        
        /* Typography Hierarchy */
        h1 { font-size: 32px !important; font-weight: 700 !important; letter-spacing: -0.02em !important; line-height: 1.2 !important; color: var(--text-primary) !important; }
        h2 { font-size: 24px !important; font-weight: 600 !important; letter-spacing: -0.015em !important; line-height: 1.3 !important; color: var(--text-primary) !important; }
        h3 { font-size: 18px !important; font-weight: 600 !important; line-height: 1.4 !important; color: var(--text-primary) !important; }
        
        /* 2. Layout & Spacing */
        .block-container {
            max-width: 1280px !important;
            padding-top: 2rem !important;
            padding-left: 24px !important;
            padding-right: 24px !important;
        }
        
        /* 3. Cards & Expanders */
        .st-emotion-cache-1y4p8pa, .st-emotion-cache-16idsys p, [data-testid="stExpander"] {
            background-color: var(--surface-color) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 16px !important;
            padding: 24px !important;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05) !important;
            transition: all 0.3s ease !important;
        }
        
        [data-testid="stExpander"]:hover, .st-emotion-cache-1y4p8pa:hover {
            transform: translateY(-4px) !important;
            box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1), 0 0 15px rgba(59, 130, 246, 0.1) !important;
            border-color: rgba(59, 130, 246, 0.3) !important;
            background-color: var(--elevated-color) !important;
        }
        
        /* 4. Buttons */
        .stButton > button {
            background: var(--surface-color) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 12px !important;
            padding: 0.5rem 1rem !important;
            transition: all 0.3s ease !important;
            font-weight: 500 !important;
        }
        
        .stButton > button:hover {
            background: var(--accent-gradient) !important;
            color: white !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
            border-color: transparent !important;
        }
        
        /* 5. Inputs */
        .stTextInput > div > div > input, .stSelectbox > div > div, .stTextArea > div > div > textarea {
            background-color: var(--elevated-color) !important;
            border: 1px solid var(--border-color) !important;
            color: var(--text-primary) !important;
            border-radius: 12px !important;
            padding: 12px 16px !important;
            transition: all 0.3s ease !important;
        }
        
        .stTextInput > div > div > input:focus, .stSelectbox > div > div:focus, .stTextArea > div > div > textarea:focus {
            border-color: #3B82F6 !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
        }
        
        /* Metrics */
        [data-testid="stMetricValue"] {
            background: var(--accent-gradient) !important;
            -webkit-background-clip: text !important;
            background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            font-weight: 700 !important;
        }
        [data-testid="stMetricLabel"] {
            color: var(--text-secondary) !important;
        }
        
        /* Hide Default Sidebar Nav */
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        
        /* 5.5 Horizontal Radio Faux-Navbar */
        div[role='radiogroup'] {
            display: flex;
            flex-direction: row;
            gap: 4px;
            align-items: center;
            flex-wrap: wrap !important;
            justify-content: center;
        }
        div[role='radiogroup'] > label {
            background-color: transparent !important;
            border: 1px solid transparent !important;
            padding: 6px 10px !important;
            border-radius: 8px !important;
            color: var(--text-secondary) !important;
            font-weight: 500 !important;
            font-size: 13px !important;
            white-space: nowrap !important;
            transition: all 0.3s ease !important;
            margin: 0 !important;
            cursor: pointer;
        }
        div[role='radiogroup'] > label:hover {
            color: var(--text-primary) !important;
            background-color: var(--elevated-color) !important;
        }
        /* Active Radio State */
        div[role='radiogroup'] > label[data-checked="true"] {
            background: var(--elevated-color) !important;
            border: 1px solid var(--border-color) !important;
            color: var(--text-primary) !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05) !important;
        }
        /* Hide default radio circles completely */
        div[role='radiogroup'] > label > div:first-child {
            display: none !important;
        }
        
        /* 6. Animations */
        @keyframes fadeSlideUp {
            from { opacity: 0; transform: translateY(20px); filter: blur(4px); }
            to { opacity: 1; transform: translateY(0); filter: blur(0); }
        }
        .block-container {
            animation: fadeSlideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }
        
        /* Top Navbar Helper */
        .top-nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 16px 24px;
            background-color: var(--surface-color);
            border-bottom: 1px solid var(--border-color);
            border-radius: 16px;
            margin-bottom: 24px;
        }
    </style>
    """
    st.markdown(f"<style>{theme_vars}</style>", unsafe_allow_html=True)
    st.markdown(base_css, unsafe_allow_html=True)

load_css()

# --- Initialize Database ---
db.init_db()

def login_form():
    """Renders the elite SaaS split-screen login and registration forms."""
    
    logo_svg = """<svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-bottom: -15px;"><defs><linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#3B82F6" /><stop offset="100%" stop-color="#8B5CF6" /></linearGradient><linearGradient id="grad2" x1="100%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#00C9A7" /><stop offset="100%" stop-color="#3B82F6" /></linearGradient></defs><path d="M12 2L2 7L12 12L22 7L12 2Z" fill="url(#grad1)"/><path d="M2 17L12 22L22 17V12L12 17L2 12V17Z" fill="url(#grad2)"/><path d="M2 12L12 17L22 12V7L12 12L2 7V12Z" fill="url(#grad1)" opacity="0.8"/></svg>"""
    
    st.markdown(f"""<div style="text-align: center; margin-bottom: 2rem; animation: fadeSlideUp 0.5s ease-out;">{logo_svg}<h1 style="background: var(--accent-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 42px !important; margin-bottom: 0px !important;">SkillSync AI Copilot</h1><h3 style="color: var(--text-secondary) !important; font-weight: 400 !important; margin-top: 5px !important;">Unlock Your Autonomous Tech Career.</h3></div>""", unsafe_allow_html=True)
    
    col_marketing, col_auth = st.columns([1.2, 1], gap="large")
    
    with col_marketing:
        st.markdown("""
        <div style="background: var(--accent-gradient); border-radius: 20px; padding: 40px; height: 100%; display: flex; flex-direction: column; justify-content: center; color: white; box-shadow: 0 10px 30px rgba(59, 130, 246, 0.2);">
            <h2 style="color: white !important; font-size: 32px !important; line-height: 1.2 !important; margin-bottom: 15px;">The Next Generation<br>of Learning.</h2>
            <p style="font-size: 15px; opacity: 0.9; line-height: 1.6; color: white !important;">SkillSync bridges the gap between academic theory and industry demands using autonomous GenAI roadmaps, perfect CV generation, and real-time skill tracking.</p>
            <div style="margin-top: 30px; padding: 20px; background: rgba(255,255,255,0.1); border-radius: 12px; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2);">
                <div style="display: flex; align-items: center; margin-bottom: 12px;">
                    <span style="font-size: 20px; margin-right: 12px;">🚀</span>
                    <strong style="color: white; font-size: 14px;">14+ Hackathon-Ready Roadmaps</strong>
                </div>
                <div style="display: flex; align-items: center; margin-bottom: 12px;">
                    <span style="font-size: 20px; margin-right: 12px;">🧠</span>
                    <strong style="color: white; font-size: 14px;">Interactive AI Mentor</strong>
                </div>
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 20px; margin-right: 12px;">📄</span>
                    <strong style="color: white; font-size: 14px;">Smart ATS Resume Generator</strong>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_auth:
        tabs = st.tabs(["🔒 Sign In", "✨ Create Account"])
        
        with tabs[0]:
            st.markdown("<h3 style='margin-bottom: 15px;'>Welcome Back</h3>", unsafe_allow_html=True)
            with st.form("login_form"):
                login_user = st.text_input("Username", placeholder="Enter your username")
                login_pass = st.text_input("Password", type="password", placeholder="Enter your password")
                submit_login = st.form_submit_button("Sign In →")
                
                if submit_login:
                    user = auth.authenticate_user(login_user, login_pass)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user = dict(user) # Convert Row to dict
                        db.update_streak(user['id'], date.today().isoformat())
                        st.success("Logged in successfully!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                        
        with tabs[1]:
            st.markdown("<h3 style='margin-bottom: 15px;'>Join the Platform</h3>", unsafe_allow_html=True)
            with st.form("register_form"):
                reg_user = st.text_input("Choose Username", placeholder="e.g. dev_master")
                reg_email = st.text_input("Email", placeholder="you@university.edu")
                reg_pass = st.text_input("Choose Password", type="password", placeholder="Minimum 8 characters")
                submit_reg = st.form_submit_button("Create Account ✨")
                
                if submit_reg:
                    if reg_user and reg_email and reg_pass:
                        if auth.register_user(reg_user, reg_email, reg_pass):
                            st.success("Registration successful! Please sign in on the other tab.")
                        else:
                            st.error("Username or email already exists.")
                    else:
                        st.error("Please fill all fields.")

def main_app():
    """Main application loop after login."""
    
    logo_svg_small = """<svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-right: 8px;"><defs><linearGradient id="grad_small1" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#3B82F6" /><stop offset="100%" stop-color="#8B5CF6" /></linearGradient><linearGradient id="grad_small2" x1="100%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#00C9A7" /><stop offset="100%" stop-color="#3B82F6" /></linearGradient></defs><path d="M12 2L2 7L12 12L22 7L12 2Z" fill="url(#grad_small1)"/><path d="M2 17L12 22L22 17V12L12 17L2 12V17Z" fill="url(#grad_small2)"/><path d="M2 12L12 17L22 12V7L12 12L2 7V12Z" fill="url(#grad_small1)" opacity="0.8"/></svg>"""
    globe_svg = f"""<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 4px; color: var(--text-secondary);"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>"""
    
    # Generate specific translation function reference for brevity
    t = lambda key: get_t(st.session_state.language, key)
    
    # Navigation with i18n translation - Reordered per requirement 1
    nav_keys = ["nav_dashboard", "nav_diagnostic", "nav_roadmap", "nav_certs", "nav_career", "nav_module", "nav_mentor", "nav_profile"]
    menu = [t(k) for k in nav_keys]
    
    icons_map = {
        "nav_dashboard": "🧭",
        "nav_diagnostic": "⚡",
        "nav_roadmap": "🗺️",
        "nav_certs": "🎓",
        "nav_career": "📄",
        "nav_module": "🧠",
        "nav_mentor": "💬",
        "nav_profile": "👤"
    }
    
    # Map translated string backwards to the icon key
    display_to_key = {t(k): k for k in nav_keys}

    # 1. Tier 1: Upper Centered Utility Bar
    st.markdown("""
    <style>
        .lang-container { position: relative; display: flex; align-items: center; justify-content: center; background: transparent; border-radius: 8px; border: 1px solid transparent; transition: all 0.2s; padding: 4px 8px; cursor: pointer; margin-top: 4px; }
        .lang-container:hover { background: var(--elevated-color); border-color: var(--border-color); }
        .lang-container div[data-baseweb="select"] { width: 45px !important; min-width: 45px !important; background: transparent !important; }
        .lang-container div[data-baseweb="select"] > div { border: none !important; background: transparent !important; padding: 0 !important; cursor: pointer !important; font-weight: 600 !important;}
        .lang-container div[data-baseweb="select"] svg { display: none !important; }
        
        /* Tier 2 Menu Row Centering Fix */
        div[role='radiogroup'] {
            justify-content: center !important;
            border-bottom: 2px solid transparent;
            padding-bottom: 12px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Precise Centering Columns: [Left (Logo)] [Center (Clock)] [Right (Utils)]
    # We inject global style to force vertical alignment of the columns themselves
    st.markdown("""
        <style>
            div[data-testid="column"] {
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                padding-top: 0 !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    c_logo, c_clock, c_utils = st.columns([1, 1, 1], gap="small")
    
    with c_logo:
        # Left Aligned
        st.markdown(f"""
        <div style="display:flex; justify-content:flex-start; align-items:center; width:100%; height:64px; padding-left: 10px;">
            {logo_svg_small}
            <h2 style="margin:0px !important; font-weight: 800; font-size: 22px !important; background: var(--accent-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent; white-space: nowrap; letter-spacing: -0.5px;">SkillSync</h2>
        </div>
        """, unsafe_allow_html=True)
        
    with c_clock:
        # Perfectly Center Aligned JS Clock, strictly tied to CSS Variables for contrast. NO BACKGROUNDS.
        components.html("""
            <div style="font-family: 'Inter', sans-serif; text-align: center; display: flex; flex-direction: column; justify-content: center; height: 64px; white-space: nowrap; background: transparent !important;">
                <div id="navTime" style="color: var(--text-primary); font-weight: 700; font-size: 16px; animation: fadeIn 1s ease-in-out;"></div>
                <div id="navDate" style="color: var(--text-secondary); font-size: 12px; font-weight: 500; margin-top: 2px;"></div>
            </div>
            <script>
                function updateNavTime() {
                    var now = new Date();
                    document.getElementById('navTime').innerText = now.toLocaleTimeString('en-US', { hour12: true, hour: 'numeric', minute:'2-digit' });
                    document.getElementById('navDate').innerText = now.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
                }
                setInterval(updateNavTime, 1000);
                updateNavTime();
            </script>
        """, height=64)
        
    with c_utils:
        # Right Aligned Flexbox for Lang, Theme, User
        st.markdown("""
        <style>
            .right-utils-container {
                display:flex; 
                justify-content:flex-end; 
                align-items:center; 
                height:64px; 
                gap: 12px;
                padding-right: 10px;
                width: 100%;
            }
            .theme-toggle-container {
                display: flex;
                align-items: center;
                justify-content: center;
                height: 36px;
                width: 36px;
                margin: 0 !important;
                padding: 0 !important;
            }
            .theme-toggle-container button {
                padding: 0 !important;
                height: 36px !important;
                width: 36px !important;
                min-height: 36px !important;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 6px !important;
                margin: 0 !important;
            }
            .lang-container { 
                position: relative; 
                display: flex; 
                align-items: center; 
                justify-content: center; 
                background: transparent; 
                border-radius: 6px; 
                border: 1px solid var(--border-color); 
                transition: all 0.2s; 
                height: 36px !important;
                width: 36px !important;
                cursor: pointer; 
                margin: 0 !important;
                padding: 0 !important;
            }
            .lang-container:hover { background: var(--elevated-color); border-color: rgba(59, 130, 246, 0.5); transform: translateY(-1px); box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
            /* Force the streamlit selectbox to hover purely over the globe without displacing the grid */
            .lang-selectbox-overlay > div { margin-top: -36px !important; opacity: 0; }
        </style>
        """, unsafe_allow_html=True)
        
        # We need overlapping columns purely for rendering the Streamlit widgets
        u_lang, u_theme, u_user = st.columns([1,1,2], gap="small")
        
        with u_lang:
            st.markdown(f"""
            <div style="display:flex; justify-content:flex-end; align-items:center; width:100%; height:64px;">
                <div class='lang-container'>{globe_svg}</div>
            </div>
            <div class="lang-selectbox-overlay">
            """, unsafe_allow_html=True)
            
            lang_options = {"en": "EN", "hi": "HI", "or": "OR"}
            selected_lang = st.selectbox(
                "Language", 
                options=list(lang_options.keys()), 
                format_func=lambda x: lang_options[x],
                index=list(lang_options.keys()).index(st.session_state.language),
                label_visibility="collapsed",
                key="lang_select"
            )
            st.markdown("</div>", unsafe_allow_html=True)
            if selected_lang != st.session_state.language:
                st.session_state.language = selected_lang
                st.rerun()
                
        with u_theme:
            st.markdown("""
            <div style="display:flex; justify-content:center; align-items:center; width:100%; height:64px;">
                <div class='theme-toggle-container'>
            """, unsafe_allow_html=True)
            theme_icon = "🌞" if st.session_state.theme == "dark" else "🌙"
            if st.button(theme_icon, key="theme_toggle", help="Toggle Light/Dark Mode"):
                st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
                st.rerun()
            st.markdown("</div></div>", unsafe_allow_html=True)
            
        with u_user:
            st.markdown(f"""
            <div style="display:flex; align-items:center; justify-content:flex-end; height:64px;">
                <div style="padding: 6px 14px; background: var(--surface-color); border: 1px solid var(--border-color); border-radius: 20px; font-size: 14px; font-weight: 600; color: var(--text-primary); white-space: nowrap; box-shadow: 0 2px 4px rgba(0,0,0,0.05); transition: transform 0.2s; cursor: pointer;">
                    👤 {st.session_state.user['username']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr style='margin-top: 10px; margin-bottom: 16px; border-color: var(--border-color); opacity: 0.5;'>", unsafe_allow_html=True)
    
    # 2. Tier 2: Lower Navigation Menu Bar (Full Width & Centered)
    if 'change_page_to' in st.session_state:
        st.session_state['nav_radio'] = st.session_state['change_page_to']
        del st.session_state['change_page_to']
    
    choice = st.radio("Navigation", menu, key="nav_radio", horizontal=True, label_visibility="collapsed", format_func=lambda x: f"{icons_map[display_to_key[x]]}  {x}")
    st.markdown("<hr style='margin-top: 0px; margin-bottom: 24px; border: 0; height: 1px; background: linear-gradient(to right, transparent, var(--border-color), transparent);'>", unsafe_allow_html=True)

    # 2. Clean Collapsible Sidebar (Stripped of the Clock)
    st.sidebar.markdown(f"<h3 style='margin-bottom: 20px;'>{t('dashboard_controls')}</h3>", unsafe_allow_html=True)
    st.sidebar.markdown(f"**{t('level')}:** {st.session_state.user['level']}")
    st.sidebar.markdown(f"**{t('xp')}:** {st.session_state.user['xp']}")
    st.sidebar.markdown(f"🔥 **{t('streak')}:** {st.session_state.user['streak']} {t('days')}")
    st.sidebar.markdown("---")
    
    if st.sidebar.button(t("logout")):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()
        
    st.title(choice)
    
    c_key = display_to_key[choice]
    
    if c_key == "nav_dashboard":
        from pages.dashboard import render_dashboard
        render_dashboard()
    elif c_key == "nav_diagnostic":
        from pages.diagnostic import render_diagnostic
        render_diagnostic()
    elif c_key == "nav_roadmap":
        from pages.roadmap import render_roadmap
        render_roadmap()
    elif c_key == "nav_career":
        from pages.career import render_career
        render_career()
    elif c_key == "nav_module":
        from pages.learning_engine import render_learning_engine
        render_learning_engine()
    elif c_key == "nav_mentor":
        from pages.mentor_chat import render_mentor
        render_mentor()
    elif c_key == "nav_profile":
        from pages.profile import render_profile
        render_profile()
    elif c_key == "nav_certs":
        from pages.cert_intern import render_certs
        render_certs()

# --- Main Execution ---
if __name__ == "__main__":
    if not st.session_state.logged_in:
        login_form()
    else:
        main_app()
