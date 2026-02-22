# i18n Translation Dictionary for SkillSync AI Copilot
# Supports English (en), Hindi (hi), and Odia (or)

translations = {
    "en": {
        "nav_dashboard": "Dashboard",
        "nav_diagnostic": "Diagnostic",
        "nav_roadmap": "Learning Roadmap",
        "nav_career": "Career",
        "nav_module": "Module Engine",
        "nav_mentor": "AI Mentor",
        "nav_profile": "Profile",
        "nav_certs": "Certifications & Interns",
        "title_skillsync": "SkillSync AI Copilot",
        "dashboard_controls": "Dashboard Controls",
        "level": "Level",
        "xp": "XP",
        "streak": "Streak",
        "logout": "Logout",
        "days": "Days"
    },
    "hi": {
        "nav_dashboard": "डैशबोर्ड",
        "nav_diagnostic": "निदान",
        "nav_roadmap": "सीखने का रोडमैप",
        "nav_career": "करियर",
        "nav_module": "मॉड्यूल इंजन",
        "nav_mentor": "एआई मेंटर",
        "nav_profile": "प्रोफ़ाइल",
        "nav_certs": "प्रमाणपत्र और इंटर्नशिप",
        "title_skillsync": "स्किलसिंक एआई कोपायलट",
        "dashboard_controls": "डैशबोर्ड नियंत्रण",
        "level": "स्तर",
        "xp": "एक्सपी",
        "streak": "स्ट्रीक",
        "logout": "लॉग आउट",
        "days": "दिन"
    },
    "or": {
        "nav_dashboard": "ଡ୍ୟାସବୋର୍ଡ (Dashboard)",
        "nav_diagnostic": "ନିଦାନ (Diagnostic)",
        "nav_roadmap": "ଶିକ୍ଷା ରୋଡମ୍ୟାପ୍ (Roadmap)",
        "nav_career": "କ୍ୟାରିୟର୍ (Career)",
        "nav_module": "ମଡ୍ୟୁଲ୍ ଇଞ୍ଜିନ୍ (Module Engine)",
        "nav_mentor": "ଏଆଇ ମେଣ୍ଟର୍ (AI Mentor)",
        "nav_profile": "ପ୍ରୋଫାଇଲ୍ (Profile)",
        "nav_certs": "ପ୍ରମାଣପତ୍ର ଏବଂ ଇଣ୍ଟର୍ନସିପ୍ (Certs)",
        "title_skillsync": "ସ୍କିଲସିଙ୍କ୍ ଏଆଇ (SkillSync AI)",
        "dashboard_controls": "ଡ୍ୟାସବୋର୍ଡ ନିୟନ୍ତ୍ରଣ (Controls)",
        "level": "ସ୍ତର (Level)",
        "xp": "ଏକ୍ସପି (XP)",
        "streak": "ଷ୍ଟ୍ରିକ୍ (Streak)",
        "logout": "ଲଗଆଉଟ୍ (Logout)",
        "days": "ଦିନ (Days)"
    }
}

def get_t(lang_code, key):
    """Retrieves the translation for a given key, falling back to English if missing."""
    lang_dict = translations.get(lang_code, translations["en"])
    return lang_dict.get(key, translations["en"].get(key, key))
