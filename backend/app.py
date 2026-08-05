from flask import Flask, render_template
from flask_cors import CORS

from auth import auth
from upload import upload

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

CORS(app)

app.register_blueprint(auth, url_prefix="/api")
app.register_blueprint(upload, url_prefix="/api")


# =============================
# Pages
# =============================

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/forgot-password")
def forgot_password():
    return render_template("forgot-password.html")


@app.route("/reset-password")
def reset_password():
    return render_template("reset-password.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/image-detection")
def image_detection():
    return render_template("image-detection.html")


@app.route("/video-detection")
def video_detection():
    return render_template("video-detection.html")


@app.route("/history")
def history():
    return render_template("history.html")


@app.route("/reports")
def reports():
    return render_template("reports.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/settings")
def settings():
    return render_template("settings.html")


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )