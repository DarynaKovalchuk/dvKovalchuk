from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import functools

app = Flask(__name__)
app.secret_key = "lab3-secret-key-2024"

# ─── Mock user database ───────────────────────────────────────────────────────
USERS = {
    "admin": {"password": "admin123", "name": "Адміністратор", "role": "admin"},
    "user":  {"password": "user123",  "name": "Звичайний користувач", "role": "user"},
}

# ─── Auth helper ──────────────────────────────────────────────────────────────
def login_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login_page"))
        return f(*args, **kwargs)
    return decorated

# ─── Pages ────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login_page"))

@app.route("/login")
def login_page():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html",
                           username=session["username"],
                           name=session["name"],
                           role=session["role"])

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html",
                           username=session["username"],
                           name=session["name"],
                           role=session["role"])

@app.route("/notes")
@login_required
def notes():
    return render_template("notes.html",
                           username=session["username"],
                           name=session["name"],
                           role=session["role"])

# ─── API endpoints ────────────────────────────────────────────────────────────
@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json()
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        return jsonify({"ok": False, "error": "Заповніть усі поля"}), 400

    user = USERS.get(username)
    if not user or user["password"] != password:
        return jsonify({"ok": False, "error": "Невірний логін або пароль"}), 401

    session["username"] = username
    session["name"]     = user["name"]
    session["role"]     = user["role"]
    # token = username (simplified demo token)
    token = f"token_{username}_2024"
    return jsonify({"ok": True, "token": token, "name": user["name"], "role": user["role"]})

@app.route("/api/logout", methods=["POST"])
def api_logout():
    session.clear()
    return jsonify({"ok": True})

@app.route("/api/user")
@login_required
def api_user():
    return jsonify({
        "username": session["username"],
        "name":     session["name"],
        "role":     session["role"],
    })

@app.route("/api/notes", methods=["GET"])
@login_required
def api_notes_get():
    # In-memory notes per user stored in session
    notes = session.get("notes", [])
    return jsonify({"ok": True, "notes": notes})

@app.route("/api/notes", methods=["POST"])
@login_required
def api_notes_post():
    data  = request.get_json()
    text  = data.get("text", "").strip()
    if not text:
        return jsonify({"ok": False, "error": "Нотатка не може бути порожньою"}), 400
    notes = session.get("notes", [])
    note  = {"id": len(notes) + 1, "text": text}
    notes.append(note)
    session["notes"] = notes
    return jsonify({"ok": True, "note": note})

@app.route("/api/notes/<int:note_id>", methods=["DELETE"])
@login_required
def api_notes_delete(note_id):
    notes = session.get("notes", [])
    notes = [n for n in notes if n["id"] != note_id]
    session["notes"] = notes
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(debug=True)
