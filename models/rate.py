from models import db


class Rate(db.Model):
    __tablename__ = "rates"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    date = db.Column(
        db.String(20),
        nullable=False
    )

    market = db.Column(
        db.String(100),
        nullable=False
    )

    rate_per_coconut = db.Column(
        db.Float,
        nullable=False
    )

    remarks = db.Column(
        db.String(255)
    )