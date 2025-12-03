from app import app, db, Tutorial

tutorials = [
    # iOS Tutorials
    Tutorial(platform="ios", category="Text Messaging", title="Send a message"),
    Tutorial(platform="ios", category="Text Messaging", title="Attach a photo"),
    Tutorial(platform="ios", category="Contacts", title="Add a contact"),
    Tutorial(platform="ios", category="Contacts", title="Import contacts"),

    # Android Tutorials
    Tutorial(platform="android", category="Calling", title="Make a call"),
    Tutorial(platform="android", category="Calling", title="Voicemail"),
    Tutorial(platform="android", category="App Installation", title="Install from Play Store"),
]

with app.app_context():
    db.session.add_all(tutorials)
    db.session.commit()

print("Tutorials have been added!")
