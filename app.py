from flask import Flask
from applications.database import db
app = None

def create_app():
    app = Flask(__name__)
    app.secret_key = "your_super_secret_key_123"

    app.debug=True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placementportal.sqlite3'
    db.init_app(app)
    app.app_context().push()
    return app

app = create_app()
from applications.controllers import * 


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        Admin=User.query.filter_by(username="Admin1").first()
        if Admin is None:
            Admin=User(username="Admin1", name="Admin", email="admin@user.com", password="1234", role="admin")
            db.session.add(Admin)
            db.session.commit()
    app.run(debug=True)