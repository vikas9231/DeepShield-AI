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

# ==========================================
# Get User Profile
# ==========================================

@auth.route("/profile/<int:user_id>", methods=["GET"])
def get_profile(user_id):

    try:

        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute("""

            SELECT

                id,
                name,
                email,
                phone

            FROM users

            WHERE id=?

        """, (user_id,))

        user = cursor.fetchone()

        conn.close()

        if user is None:

            return jsonify({

                "success": False,

                "message": "User not found."

            }), 404

        return jsonify({

            "success": True,

            "user": {

                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "phone": user["phone"]

            }

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500

    # ==========================================
# Update User Profile
# ==========================================

@auth.route("/profile/<int:user_id>", methods=["PUT"])
def update_profile(user_id):

    try:

        data = request.get_json()

        name = data.get("name")
        phone = data.get("phone")

        conn = sqlite3.connect(DATABASE)

        cursor = conn.cursor()

        cursor.execute("""

            UPDATE users

            SET

                name=?,
                phone=?

            WHERE id=?

        """, (

            name,
            phone,
            user_id

        ))

        conn.commit()

        conn.close()

        return jsonify({

            "success": True,

            "message": "Profile updated successfully."

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500

# ==========================================
# Get User Settings
# ==========================================

@auth.route("/settings/<int:user_id>", methods=["GET"])
def get_settings(user_id):

    try:

        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute("""

            SELECT *

            FROM user_settings

            WHERE user_id=?

        """, (user_id,))

        settings = cursor.fetchone()

        # Create default settings if not found
        if settings is None:

            cursor.execute("""

                INSERT INTO user_settings(

                    user_id

                )

                VALUES(?)

            """, (user_id,))

            conn.commit()

            cursor.execute("""

                SELECT *

                FROM user_settings

                WHERE user_id=?

            """, (user_id,))

            settings = cursor.fetchone()

        conn.close()

        return jsonify({

            "success": True,

            "settings": {

                "dark_mode": bool(settings["dark_mode"]),

                "email_notifications": bool(settings["email_notifications"]),

                "detection_alerts": bool(settings["detection_alerts"]),

                "language": settings["language"]

            }

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500

    # ==========================================
# Update User Settings
# ==========================================

@auth.route("/settings/<int:user_id>", methods=["PUT"])
def update_settings(user_id):

    try:

        data = request.get_json()

        conn = sqlite3.connect(DATABASE)

        cursor = conn.cursor()

        cursor.execute("""

            UPDATE user_settings

            SET

                dark_mode=?,

                email_notifications=?,

                detection_alerts=?,

                language=?

            WHERE user_id=?

        """, (

            int(data["dark_mode"]),

            int(data["email_notifications"]),

            int(data["detection_alerts"]),

            data["language"],

            user_id

        ))

        conn.commit()

        conn.close()

        return jsonify({

            "success": True,

            "message": "Settings updated successfully."

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500

# ==========================================
# Change Password
# ==========================================

@auth.route("/change-password", methods=["POST"])
def change_password():

    try:

        data = request.get_json()

        user_id = data["user_id"]

        current_password = data["current_password"]

        new_password = data["new_password"]

        conn = sqlite3.connect(DATABASE)

        cursor = conn.cursor()

        cursor.execute("""

            SELECT password

            FROM users

            WHERE id=?

        """, (user_id,))

        row = cursor.fetchone()

        if row is None:

            conn.close()

            return jsonify({

                "success": False,

                "message": "User not found."

            }), 404

        if row[0] != current_password:

            conn.close()

            return jsonify({

                "success": False,

                "message": "Current password is incorrect."

            }), 400

        cursor.execute("""

            UPDATE users

            SET password=?

            WHERE id=?

        """, (

            new_password,

            user_id

        ))

        conn.commit()

        conn.close()

        return jsonify({

            "success": True,

            "message": "Password changed successfully."

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500