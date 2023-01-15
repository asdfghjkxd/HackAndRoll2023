import jinja_partials

from flask import Flask, render_template, request

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "/assets"
jinja_partials.register_extensions(app)

@app.route("/")
@app.route("/index")
def home():
    return render_template("home/index.html",
                           title="Wordle",
                           description="Wordle")


@app.route("/solver")
def solver():
    return render_template("home/solver.html",
                           title="Solver")


@app.route("/solver/<query>")
def solver_query(query: str):
    # do some function here
    return render_template("home/solver_page.html",
                           q=query,
                           q_resp="HERE GOES YOUR FUNCTION OUTPUT")


if __name__ == "__main__":
    app.run(debug=True, port=8000)
