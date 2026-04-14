from app import app
from models import db, User, Note

with app.app_context():
    db.drop_all()
    db.create_all()

    user = User(username="testuser")
    user.set_password("1234")

    db.session.add(user)
    db.session.commit()

    note1 = Note(title="First Note", content="Hello world", user_id=user.id)
    note2 = Note(title="Second Note", content="Another note", user_id=user.id)

    db.session.add_all([note1, note2])
    db.session.commit()

    print("Database seeded!")