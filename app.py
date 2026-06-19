from flask import Flask
from flask_login import LoginManager

from config import Config
from models import db

from routes.public import public_bp
from routes.admin import admin_bp

app = Flask(__name__)


app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(public_bp)
app.register_blueprint(admin_bp)

with app.app_context():

    db.create_all()

    from models.rate import Rate

    if Rate.query.count() == 0:

        sample_rate = Rate(
            date="17-Jun-2026",
            market="Amalapuram",
            rate_per_coconut=17,
            remarks="Stable Market"
        )

        db.session.add(sample_rate)
        db.session.commit()

        print("Sample Data Inserted")

if __name__ == "__main__":
    app.run(debug=True)