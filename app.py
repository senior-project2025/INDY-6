# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify   # type: ignore
from markupsafe import escape # type: ignore
from deep_translator import GoogleTranslator # type: ignore
import threading   

app = Flask(__name__)
app.secret_key = "replace-with-a-strong-random-secret"


from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///iknowit.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# ---------------------------
# DATABASE MODELS
# ---------------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    join_date = db.Column(db.DateTime, default=datetime.utcnow)

    progress = db.relationship("Progress", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)




class Tutorial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(20), nullable=False)  # 'ios', 'android'
    category = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)


class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tutorial_id = db.Column(db.Integer, db.ForeignKey('tutorial.id'))
    completed = db.Column(db.Boolean, default=False)

    tutorial = db.relationship("Tutorial")


class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150))
    message = db.Column(db.Text)





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
    """Translate text asynchronously (non-blocking) and cache results."""
    if not text or target_lang == 'en':
        return text

    cache_key = f"{target_lang}:{text}"
    if cache_key in translation_cache:
        return translation_cache[cache_key]  # Already done

    # Immediately return the English version (optimistic UI)
    translation_cache[cache_key] = text

    # Background thread to fetch translation
    def async_translate():
        try:
            translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
            translation_cache[cache_key] = translated
            print(f"[Async Translation] Cached: {cache_key}")
        except Exception as e:
            print(f"[Async Translation Error] {e}")

    threading.Thread(target=async_translate, daemon=True).start()
    return text


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
    email = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        session['user_id'] = user.id
        session['user'] = user.name
        flash("Logged in successfully!")
        return redirect(url_for('index'))

    flash("Incorrect email or password.")
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

        # Prevent duplicate emails
        existing = User.query.filter_by(email=email).first()
        if existing:
            flash("Email already registered.")
            return redirect(url_for('signup'))

        # Create user
        user = User(name=name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Account created successfully!")
        return redirect(url_for('index'))

    return render_template('signup.html')

@app.route('/complete_tutorial/<int:tutorial_id>', methods=['POST'])
def complete_tutorial(tutorial_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    user_id = session['user_id']

    progress = Progress.query.filter_by(user_id=user_id, tutorial_id=tutorial_id).first()

    if not progress:
        progress = Progress(user_id=user_id, tutorial_id=tutorial_id, completed=True)
        db.session.add(progress)
    else:
        progress.completed = True

    db.session.commit()

    return jsonify({'success': True})





@app.route('/ios')
def ios_page():
    tutorials = [
        {'category': 'Text Messaging', 'items': ['Send a message', 'Attach photo', 'Group chat']},
        {'category': 'Contacts', 'items': ['Add contact', 'Import contacts']},
    ]
    return render_template('tutorials_ios.html', tutorials=tutorials)

@app.route('/android')
def android_page():
    tutorials = [
        {'category': 'Calling', 'items': ['Make a call', 'Voicemail']},
        {'category': 'App installation', 'items': ['Install from Play Store']},
    ]
    return render_template('tutorials_android.html', tutorials=tutorials)


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
        {"q": "How do can I change the language?", "a": "Click the language button on the top-right to see other languages."},
        {"q": "How do I can I provide feedback?", "a": "Open the Menu modal and click 'Contact Us' to provide any feedback."},
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
@app.route('/debug')
def debug_page():
    return render_template('tutorials_ios.html', tutorials=[{'category':'Test','items':['Item 1','Item 2']}])

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        flash("You must be logged in to view your profile.")
        return redirect(url_for('index'))

    user = User.query.get(session['user_id'])

    # Calculate progress
    completed_count = Progress.query.filter_by(user_id=user.id, completed=True).count()
    total_tutorials = Tutorial.query.count()
    percent = round((completed_count / total_tutorials) * 100, 2) if total_tutorials > 0 else 0

    return render_template('profile.html',
                           user=user,
                           percent=percent,
                           completed=completed_count,
                           total=total_tutorials)
@app.route('/change_password', methods=['POST'])
def change_password():
    if 'user_id' not in session:
        flash("You must be logged in.")
        return redirect(url_for('index'))

    user = User.query.get(session['user_id'])
    old_pass = request.form.get('old_password')
    new_pass = request.form.get('new_password')

    if not user.check_password(old_pass):
        flash("Incorrect current password.")
        return redirect(url_for('profile'))

    user.set_password(new_pass)
    db.session.commit()

    flash("Password updated successfully!")
    return redirect(url_for('profile'))

@app.route('/my_progress')
def my_progress():
    if 'user_id' not in session:
        flash("You must be logged in to view your progress.")
        return redirect(url_for('index'))

    user_id = session['user_id']

    tutorials = Tutorial.query.all()

    progress = Progress.query.filter_by(user_id=user_id).all()
    completed_ids = [p.tutorial_id for p in progress if p.completed]

    return render_template('my_progress.html',
                           tutorials=tutorials,
                           completed_ids=completed_ids)




if __name__ == '__main__':
    app.run(debug=True)
