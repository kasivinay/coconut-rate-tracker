from flask import Blueprint, render_template
from models.rate import Rate
from flask import request
public_bp = Blueprint(
    "public",
    __name__
)

@public_bp.route("/")
def home():

    rates = (
        Rate.query
        .order_by(Rate.date.desc())
        .all()
    )

    language = request.args.get(
        "lang",
        "en"
    )
    latest_rate = rates[0] if len(rates) > 0 else None

    yesterday_rate = rates[1] if len(rates) > 1 else None

    difference = 0

    if latest_rate and yesterday_rate:
        difference = round(
            latest_rate.rate_per_coconut
            - yesterday_rate.rate_per_coconut,
            2
        )
    if difference > 0:
        trend = "UP"
    elif difference < 0:
        trend = "DOWN"
    else:
        trend = "STABLE"

    weekly_avg = 0

    if len(rates) > 0:

        last_7_rates = rates[:7]

        weekly_avg = round(
            sum(
                r.rate_per_coconut
                for r in last_7_rates
            ) / len(last_7_rates),
            2
        )

    highest_rate = max(
        r.rate_per_coconut
        for r in rates
    ) if rates else 0

    lowest_rate = min(
        r.rate_per_coconut
        for r in rates
    ) if rates else 0

    monthly_avg = 0

    if rates:
        monthly_avg = round(
            sum(r.rate_per_coconut for r in rates)
            / len(rates),
            2
        )

    from datetime import datetime

    chart_labels = [

        datetime.strptime(
            str(rate.date),
            "%Y-%m-%d"
        ).strftime("%d-%b")

        for rate in reversed(rates[:15])

    ]

    chart_rates = [
        rate.rate_per_coconut
        for rate in reversed(rates[:15])
    ]

    from datetime import datetime

    formatted_date = ""

    if latest_rate:
        try:
            formatted_date = latest_rate.date
        except:
            formatted_date = ""
    return render_template(
        "home.html",

        language=language,

        latest_rate=None,
        yesterday_rate=None,
        difference=difference,
        weekly_avg=weekly_avg,
        highest_rate=highest_rate,
        lowest_rate=lowest_rate,
        trend=trend,
        monthly_avg=monthly_avg,
        chart_labels=chart_labels,
        chart_rates=chart_rates,
        formatted_date= formatted_date,
        rates=rates
    )