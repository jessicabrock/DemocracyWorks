from flask import Flask, request, render_template
import requests
import json
import dateparser
# import local modules
from demo import create_app
from dotenv import load_dotenv


load_dotenv('.env') # or any other file we need to load
app = create_app()
gunicorn run:app


def parse_date(str_date):
    """ parse input date to MM/DD/YYYYY format """
    new_date = dateparser.parse(str_date).strftime("%m/%d/%Y")
    return new_date


def get_result_items(text):  # response object
    """ custom dict object """
    cd = {}  # custom dict

    j = json.loads(text)
    d = j[0]  # big dict

    i_desc = d["description"]
    cd["i_desc"] = i_desc
    i_date = parse_date(d["date"])
    cd["i_date"] = i_date

    # country code parse out two-letter state code
    i_cc = d["district-divisions"][0]["ocd-id"].split("state:")[1].upper()
    cd["i_state"] = i_cc

    # voting methods
    # TODO: parse list
    i_vm = d["district-divisions"][0]["voting-methods"]
    cd["i_vote_meth"] = i_vm

    # deadline postmarked is date
    i_dp = parse_date(
        d["district-divisions"][0]["voter-registration-methods"][1][
            "deadline-postmarked"
        ]
    )
    cd["i_date_pm"] = i_dp

    # short url
    i_ppus = d["polling-place-url-shortened"]
    cd["i_place_url"] = i_ppus

    return cd  # our custom dict for the template


@app.route("/")
def index():
    return """Hello. <a href="/form/">Search Page</a>"""


@app.route("/form/", methods=["GET", "POST"])
def form():
    # form must be inside "templates" folder
    return render_template("form.html")


@app.route("/form/", methods=["GET", "POST"])
def form():
    # form must be inside "templates" folder
    return render_template("form.html")


@app.route("/results/", methods=["POST", "GET"])
def results():
    """get results based on address"""
    place = request.form["place"].lower().replace(" ", "_")
    state = request.form["state"].lower()

    url = "https://api.turbovote.org/elections/upcoming"

    querystring = {}
    querystring["district-divisions"] = (
        "ocd-division/country:us/state:"
        + state
        + ",ocd-division/country:us/state:"
        + state
        + "/place:"
        + place
    )

    headers = {"Accept": "application/json", "cache-control": "no-cache"}

    try:
        response = requests.request("GET",
                                    url,
                                    headers=headers,
                                    params=querystring
                                    )

        items = {}

        if str(response.text) == str("[]"):
            items["error"] = "error"
            return render_template("results.html", items=items)
        else:
            items = get_result_items(response.text)
            return render_template("results.html", items=items)
    except Exception as err:
        items["error"] = "error"
        return render_template("results.html", items=items)


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run()
