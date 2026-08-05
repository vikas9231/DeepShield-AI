from flask import Blueprint, request, jsonify
import sqlite3

auth = Blueprint("auth", __name__)

DATABASE = "database.db"


# ==========================
# REGISTER
# ==========================

@auth.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    password = data.get("password")

    if not name or not email or not password:

        return jsonify({
            "success": False,
            "message": "Please fill all required fields."
        }), 400

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE email=?",
        (email,)
    )

    if cursor.fetchone():

        conn.close()

        return jsonify({
            "success": False,
            "message": "Email already registered."
        }), 409

    cursor.execute(
        """
        INSERT INTO users(name,email,phone,password)
        VALUES(?,?,?,?)
        """,
        (name, email, phone, password)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Registration Successful"
    }), 201


# ==========================
# LOGIN
# ==========================

@auth.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id,name,email
        FROM users
        WHERE email=? AND password=?
        """,
        (email, password)
    )

    user = cursor.fetchone()

    conn.close()

    if user:

        return jsonify({

            "success": True,

            "message": "Login Successful",

            "user": {

                "id": user[0],

                "name": user[1],

                "email": user[2]

            }

        }), 200

    return jsonify({

        "success": False,

        "message": "Invalid Email or Password"

    }), 401

# ==========================================
# Forgot Password
# ==========================================

@auth.route("/forgot-password", methods=["POST"])
def forgot_password():

    data = request.get_json()

    email = data.get("email")

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute(

        "SELECT id FROM users WHERE email=?",

        (email,)

    )

    user = cursor.fetchone()

    conn.close()

    if user:

        return jsonify({

            "success": True,

            "message": "Email verified."

        }), 200

    return jsonify({

        "success": False,

        "message": "Email not found."

    }), 404

# ==========================================
# Reset Password
# ==========================================

@auth.route("/reset-password", methods=["POST"])
def reset_password_api():

    data = request.get_json()

    email = data.get("email")

    password = data.get("password")

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute(

        """

        UPDATE users

        SET password=?

        WHERE email=?

        """,

        (

            password,

            email

        )

    )

    conn.commit()

    conn.close()

    return jsonify({

        "success": True,

        "message": "Password updated successfully."

    }), 200

