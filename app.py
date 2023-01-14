import jinja_partials

from flask import Flask, render_template

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "/assets"
jinja_partials.register_extension(app)

@app.route("/")
@app.route("/index")
def home():
    return render_template("home/index.html",
                           title="Wordle",
                           description="Wordle")

if __name__ == "__main__":
    app.run(debug=True, port=8000)
