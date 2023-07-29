from flask import Flask, request, render_template
import pandas

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        pass
    else:
        return render_template("index.html")
