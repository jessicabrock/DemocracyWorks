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


@app.route("/")
def index():
    return """Hello. <a href="/form/">Search Page</a>"""


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(debug=True, host="0.0.0.0")
