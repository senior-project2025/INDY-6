# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify  
from markupsafe import escape
from deep_translator import GoogleTranslator

app = Flask(__name__)
app.secret_key = "replace-with-a-strong-random-secret"

# English source texts (used for automatic translation)
SOURCE_TEXTS = {
    'title': "iKnowIT",
    'mission': "Our mission is to empower people to confidently use their smartphones through clear, step-by-step tutorials.",
    'choose_device': "Select your device",
    'ios': "iOS",
    'android': "Android",
    'testimonies': "Listen to our users' experiences with iKnowIT",
    'login': "Login",
    'create_account': "Create account",
    'forgot_password': "Forgot password?",
    'language': "Language",
    'menu': "Menu",
    'about_us': "About us",
    'contact_us': "Contact us",
    'faq': "Frequently Asked Questions",
    'name': "Name",
    'email': "Email",
    'password': "Password",
    'signup': "Sign Up",
    'send_message': "Send Message",
    'testimonial_1': """iKnowIT helped my grandma learn texting in a week! Now, it's easier for us to communicate when I'm too 
    busy to call or visit her. I've never felt more connected with her, and it's all thanks to iKnowIT.""",
    'testimonial_2': """I used to be so confused on how to use certain features on my phone until my daughter found iKnowIT and
    recommended me to give it a try. Thanks to iKnowIT's tutorials, I no longer need her to do everything for me -- highly recommend.""",
    'testimonial_3': "The device guides are easy to follow for beginners like me. ",
}

# Cache so we don’t retranslate same texts repeatedly
translation_cache = {}

def translate_text(text, target_lang):
    """Translate text using deep-translator and cache it."""
    if target_lang == 'en':
        return text

    cache_key = f"{target_lang}:{text}"
    if cache_key in translation_cache:
        return translation_cache[cache_key]

    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
        print(f"[DEBUG] {text[:40]} → {translated[:40]} ({target_lang})")
    except Exception as e:
        print(f"[Translation Error] {e}")
        translated = text  # fallback

    translation_cache[cache_key] = translated
    return translated

def t(key):
    """Return translated text based on session language."""
    lang = session.get('lang', 'en')
    text = SOURCE_TEXTS.get(key, key)
    return translate_text(text, lang)

@app.context_processor
def inject_translations():
    return dict(t=t)

# Sample testimonies (would come from DB in real app)
TESTIMONIES = [
    {"img": "images/testimony/alice.jpg",
     "name": "Alice", 
     "text": """iKnowIT helped my grandma learn texting in a week! Now, it's easier for us to communicate when I'm too 
    busy to call or visit her. I've never felt more connected with her, and it's all thanks to iKnowIT."""},
    {"img": "images/testimony/miguel.jpg",
     "name": "Miguel", 
     "text": """I used to be so confused on how to use certain features on my phone until my daughter found iKnowIT and
    recommended me to give it a try. Thanks to iKnowIT's tutorials, I no longer need her to do everything for me -- highly recommend."""},
    {"img": "images/testimony/li.webp",
     "name": "Li", 
     "text": """The device guides are easy to follow for beginners like me... I got my first smartphone only two years ago. For a 65 year old like me,
     it's really hard keeping up with all the new technology. These tutorials have made it so much easier to learn at my own pace. With iKnowIT, anyone
     can become tech-savvy!
     """}
]

@app.route('/')
def index():
    lang = session.get('lang', 'en')
    translated_testimonies = []

    for t_item in TESTIMONIES:
        text = t_item["text"]
        translated_text = translate_text(text, lang)
        translated_testimonies.append({
            "img": t_item["img"],
            "name": t_item["name"],
            "text": translated_text
        })

    return render_template('index.html', testimonies=translated_testimonies)

@app.route('/set_language/<lang>')
def set_language(lang):
    lang = escape(lang)
    if lang not in ['en', 'es', 'fr', 'it', 'pt', 'ja', 'ko', 'zh-CN', 'de', 'ar', 'ru', 'hi']:
        lang = 'en'
    session['lang'] = lang
    return redirect(request.referrer or url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username and password:
        session['user'] = username
        flash(f"Logged in as {username}")
        return redirect(url_for('index'))
    else:
        flash("Please enter username and password")
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out")
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        if not name or not email or not password:
            flash("Please fill all required fields.")
            return render_template('signup.html')
        flash("Account created (demo). You can now log in.")
        return redirect(url_for('index'))
    return render_template('signup.html')

@app.route('/ios')
def ios_page():
    tutorials = [
        {'category': 'Text Messaging', 'items': ['Send a message', 'Attach photo', 'Group chat']},
        {'category': 'Contacts', 'items': ['Add contact', 'Import contacts']},
    ]
    return render_template('device.html', device='iOS', tutorials=tutorials)

@app.route('/android')
def android_page():
    tutorials = [
        {'category': 'Calling', 'items': ['Make a call', 'Voicemail']},
        {'category': 'App installation', 'items': ['Install from Play Store']},
    ]
    return render_template('device.html', device='Android', tutorials=tutorials)

@app.route('/about')
def about():
    lang = session.get('lang', 'en')

    team_data = [
        {
            "name": "Julissa Rivera",
            "role": "Developer, Documentation",
            "bio": (
                "As a first-generation Mexican American, I witnessed firsthand how challenging it can be for my parents and relatives to navigate technology. "
                "I often took the time to show them how to use apps on their phones and reassure them that, with a little practice, they could get the hang of it. "
                "I know many other parents and individuals face the same struggle, so I wanted to use this project as an opportunity to help others in similar situations "
                "gain confidence and independence when it comes to using technology. 😊"
            ),
            "img": "images/julissa.jpeg",
            "github": "https://github.com/julissa-r",
            "linkedin": "https://www.linkedin.com/in/rivera-j2911/"
        },
        {
            "name": "David Bazan",
            "role": "Developer, Documentation",
            "bio": (
                "Technology should be accessible to everyone, despite language or past experience. "
                "As a first-generation Hispanic, I understand the frustration of learning the ever-expanding technology. "
                "The other developers and I share this experience and made this project to assist those to develop critical skills that become more relevant by the day."
            ),
            "img": "images/bazan.webp",
            "github": "https://github.com/d-bazan",
            "linkedin": "https://www.linkedin.com/in/d-bazan/"
        },
        {
            "name": "Jacqueline Juarez",
            "role": "Team Lead, Developer",
            "bio": "I focused on making the website intuitive and easy to read.",
            "img": "images/jacqui.webp",
            "github": "https://github.com/Jacqjuarez",
            "linkedin": "https://www.linkedin.com/in/jacqueline-juarez8/"
        }
    ]

    translated_team = []
    for m in team_data:
        translated_role = translate_text(m["role"], lang)
        translated_bio = translate_text(m["bio"], lang)
        translated_team.append({
            "name": m["name"],
            "role": translated_role,
            "bio": translated_bio,
            "img": m["img"],
            "github": m["github"],
            "linkedin": m["linkedin"]
        })

    return render_template('about.html', team=translated_team)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()
        print(f"[Contact] {name} <{email}>: {message}")
        return render_template('contact.html', success=True)
    return render_template('contact.html', success=False)

@app.route('/faq')
def faq():
    faqs = [
        {"q": "How do I choose my device?", "a": "Click the iOS or Android button on the homepage to see device-specific tutorials."},
        {"q": "How do I create an account?", "a": "Open the Login modal and click 'Create account' to sign up."},
    ]
    return render_template('faq.html', faqs=faqs)

# Translation API route for JavaScript
@app.route('/translate', methods=['POST'])
def translate_route():
    data = request.get_json()
    items = data.get('items', [])
    target_lang = data.get('target_language', 'en')

    translated = []
    for item in items:
        key = item.get('key')
        text = item.get('text')
        try:
            translated_text = GoogleTranslator(source='auto', target=target_lang).translate(text)
        except Exception as e:
            print(f"[Translation Error] {e}")
            translated_text = text
        translated.append({'key': key, 'translated_text': translated_text})
    
    print("=== TRANSLATED ITEMS ===")
    print(translated)

    return jsonify({'translated': translated})


if __name__ == '__main__':
    app.run(debug=True)
