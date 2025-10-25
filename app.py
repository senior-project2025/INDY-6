# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, session, flash
from markupsafe import escape

app = Flask(__name__)
app.secret_key = "replace-with-a-strong-random-secret"

# Simple translations dictionary (English, Spanish, Chinese)
TRANSLATIONS = {
    'en': {
        'title': "iKnowIT",
        'mission': "Our mission is to empower people to confidently use their smartphones through clear, step-by-step tutorials.",
        'choose_device': "Select your device",
        'ios': "iOS",
        'android': "Android",
        'testimonies': "What people say",
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
    },
    'es': {
        'title': "iKnowIT",
        'mission': "Nuestra misión es capacitar a las personas para que usen sus teléfonos inteligentes con confianza mediante tutoriales claros paso a paso.",
        'choose_device': "Seleccione su dispositivo",
        'ios': "iOS",
        'android': "Android",
        'testimonies': "Lo que dicen las personas",
        'login': "Iniciar sesión",
        'create_account': "Crear cuenta",
        'forgot_password': "¿Olvidó su contraseña?",
        'language': "Idioma",
        'menu': "Menú",
        'about_us': "Acerca de nosotros",
        'contact_us': "Contáctanos",
        'faq': "Preguntas frecuentes",
        'name': "Nombre",
        'email': "Correo electrónico",
        'password': "Contraseña",
        'signup': "Registrarse",
        'send_message': "Enviar mensaje",
    },
    'zh': {
        'title': "iKnowIT",
        'mission': "我们的使命是通过清晰的逐步教程帮助人们自信地使用智能手机。",
        'choose_device': "请选择您的设备",
        'ios': "iOS",
        'android': "安卓",
        'testimonies': "用户评价",
        'login': "登录",
        'create_account': "创建账户",
        'forgot_password': "忘记密码？",
        'language': "语言",
        'menu': "菜单",
        'about_us': "关于我们",
        'contact_us': "联系我们",
        'faq': "常见问题",
        'name': "姓名",
        'email': "电子邮件",
        'password': "密码",
        'signup': "注册",
        'send_message': "发送消息",
    }
}

def t(key):
    lang = session.get('lang', 'en')
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key)

# sample testimonies (would come from DB in real app)
TESTIMONIES = [
    {"name": "Alice", "text": "iKnowIT helped my grandma learn texting in a week!"},
    {"name": "Miguel", "text": "Clear videos and step captions -- highly recommend."},
    {"name": "Li", "text": "The device guides are easy to follow for beginners."}
]

@app.context_processor
def inject_translations():
    # make t(...) available inside templates easily
    return dict(t=t)

@app.route('/')
def index():
    return render_template('index.html', testimonies=TESTIMONIES)

@app.route('/set_language/<lang>')
def set_language(lang):
    lang = escape(lang)
    if lang not in TRANSLATIONS:
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
        # In a real app: save user to DB
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
    # info about everyone on our team along with our headshots (makes it more personal)
    team = [
        {"name": "Julissa Rivera", "role": "Developer, Documentation", "bio":
         """
         As a first-generation Mexican American, I witnessed firsthand how challenging it can be for my parents and relatives to navigate technology. 
         I often took the time to show them how to use apps on their phones and reassure them that, with a little practice, they could get the hang of it. 
         I know many other parents and individuals face the same struggle, so I wanted to use this project as an opportunity to help others in similar situations 
         gain confidence/independence when it comes to using technology. 😊.
         """
         , "img": "images/julissa.jpeg"},
        {"name": "David Bazan", "role": "Developer, Documentation", "bio": "Teaching tech should be simple, visual, and friendly.", "img": "images/bazan.webp"},
        {"name": "Jacqueline Juarez", "role": "Team Lead, Developer", "bio": "I focused on making the website intuitive and easy to read.", "img": "images/jacqui.webp"}
    ]
    return render_template('about.html', team=team)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()
        # For demo: print message to console; in production, save to DB or send email
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

if __name__ == '__main__':
    app.run(debug=True)