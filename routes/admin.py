from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from datetime import datetime
from flask import session

import config
from models import db
from models.rate import Rate
from config import Config

admin_bp = Blueprint(
    "admin",
    __name__
)

@admin_bp.route(
    "/admin/update-rate/<int:rate_id>",
    methods=["POST"]
)
def update_rate(rate_id):
    if not session.get(
            "admin_logged_in"
    ):
        return redirect("/login")

    rate = Rate.query.get_or_404(rate_id)

    rate.date = datetime.strptime(
        request.form["date"],
        "%Y-%m-%d"
    ).date()

    rate.market = request.form["market"]

    rate.rate_per_coconut = float(
        request.form["rate"]
    )

    rate.remarks = request.form["remarks"]

    db.session.commit()

    return redirect("/admin")

@admin_bp.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    error = None

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        if (
            username == Config.ADMIN_USERNAME
            and
            password == Config.ADMIN_PASSWORD
        ):

            session["admin_logged_in"] = True

            return redirect("/admin")

        else:
            error = "Invalid Username or Password"

    return render_template(
        "login.html",
        error=error
    )

@admin_bp.route("/admin")
def admin_dashboard():
    if not session.get(
            "admin_logged_in"
    ):
        return redirect("/login")

    rates = Rate.query.order_by(
        Rate.date.desc()
    ).all()

    return render_template(
        "admin_dashboard.html",
        rates=rates
    )


@admin_bp.route(
    "/admin/add-rate",
    methods=["POST"]
)
def add_rate():
    if not session.get(
            "admin_logged_in"
    ):
        return redirect("/login")

    new_rate = Rate(

        date=datetime.strptime(
            request.form["date"],
            "%Y-%m-%d"
        ).date(),

        market=request.form["market"],

        rate_per_coconut=float(
            request.form["rate"]
        ),

        remarks=request.form["remarks"]

    )

    db.session.add(new_rate)

    db.session.commit()

    return redirect("/admin")
@admin_bp.route(
    "/admin/delete-rate/<int:rate_id>"
)
def delete_rate(rate_id):
    if not session.get(
            "admin_logged_in"
    ):
        return redirect("/login")

    rate = Rate.query.get_or_404(rate_id)

    db.session.delete(rate)

    db.session.commit()

    return redirect("/admin")
@admin_bp.route(
    "/admin/edit-rate/<int:rate_id>"
)
def edit_rate(rate_id):
    if not session.get(
            "admin_logged_in"
    ):
        return redirect("/login")

    rate = Rate.query.get_or_404(rate_id)

    rates = Rate.query.order_by(
        Rate.date.desc()
    ).all()

    return render_template(
        "admin_dashboard.html",
        edit_rate=rate,
        rates=rates
    )


@admin_bp.route("/logout")
def logout():
    session.clear()

    return redirect("/login")