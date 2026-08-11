from flask import Blueprint, request, jsonify, session
import sqlite3
import os


admin = Blueprint("admin", __name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "database.db")

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@deepshield.ai")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")


def admin_required():
    return session.get("is_admin") is True


# ==========================================
# ADMIN LOGIN
# ==========================================

@admin.route("/admin/login", methods=["POST"])
def admin_login():

    data = request.get_json() or {}

    email = data.get("email", "").strip()
    password = data.get("password", "")

    if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:

        session["is_admin"] = True
        session["admin_email"] = email

        return jsonify({
            "success": True,
            "message": "Admin login successful."
        }), 200

    return jsonify({
        "success": False,
        "message": "Invalid admin email or password."
    }), 401


# ==========================================
# ADMIN LOGOUT
# ==========================================

@admin.route("/admin/logout", methods=["POST"])
def admin_logout():

    session.pop("is_admin", None)
    session.pop("admin_email", None)

    return jsonify({
        "success": True,
        "message": "Admin logged out successfully."
    }), 200


# ==========================================
# CHECK ADMIN
# ==========================================

@admin.route("/admin/check", methods=["GET"])
def check_admin():

    if not admin_required():

        return jsonify({
            "success": False,
            "message": "Admin authentication required."
        }), 401

    return jsonify({
        "success": True,
        "admin": session.get("admin_email")
    }), 200


# ==========================================
# ADMIN STATISTICS
# ==========================================

@admin.route("/admin/stats", methods=["GET"])
def admin_stats():

    if not admin_required():

        return jsonify({
            "success": False,
            "message": "Admin authentication required."
        }), 401

    try:

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM users
        """)

        total_users = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM scans
        """)

        total_scans = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM scans
            WHERE
                image_name LIKE '%.jpg'
                OR image_name LIKE '%.jpeg'
                OR image_name LIKE '%.png'
        """)

        image_scans = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM scans
            WHERE
                image_name LIKE '%.mp4'
                OR image_name LIKE '%.avi'
                OR image_name LIKE '%.mov'
                OR image_name LIKE '%.mkv'
        """)

        video_scans = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM scans
            WHERE prediction = 'Deepfake'
        """)

        deepfakes = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM scans
            WHERE prediction = 'Real'
        """)

        real = cursor.fetchone()[0]

        conn.close()

        return jsonify({
            "success": True,
            "total_users": total_users,
            "total_scans": total_scans,
            "image_scans": image_scans,
            "video_scans": video_scans,
            "deepfakes": deepfakes,
            "real": real
        }), 200

    except Exception as e:

        print("ADMIN STATS ERROR:", e)

        return jsonify({
            "success": False,
            "message": "Unable to load admin statistics."
        }), 500


# ==========================================
# GET USERS
# ==========================================

@admin.route("/admin/users", methods=["GET"])
def get_users():

    if not admin_required():

        return jsonify({
            "success": False,
            "message": "Admin authentication required."
        }), 401

    try:

        search = request.args.get(
            "search",
            ""
        ).strip()

        conn = sqlite3.connect(DATABASE)

        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        if search:

            search_pattern = f"%{search}%"

            cursor.execute("""
                SELECT
                    users.id,
                    users.name,
                    users.email,
                    COUNT(scans.id) AS scan_count
                FROM users
                LEFT JOIN scans
                    ON users.id = scans.user_id
                WHERE
                    users.name LIKE ?
                    OR users.email LIKE ?
                GROUP BY
                    users.id
                ORDER BY
                    users.id DESC
            """, (
                search_pattern,
                search_pattern
            ))

        else:

            cursor.execute("""
                SELECT
                    users.id,
                    users.name,
                    users.email,
                    COUNT(scans.id) AS scan_count
                FROM users
                LEFT JOIN scans
                    ON users.id = scans.user_id
                GROUP BY
                    users.id
                ORDER BY
                    users.id DESC
            """)

        rows = cursor.fetchall()

        conn.close()

        users = []

        for row in rows:

            users.append({
                "id": row["id"],
                "name": row["name"],
                "email": row["email"],
                "scan_count": row["scan_count"]
            })

        return jsonify({
            "success": True,
            "users": users
        }), 200

    except Exception as e:

        print("ADMIN USERS ERROR:", e)

        return jsonify({
            "success": False,
            "message": "Unable to load users."
        }), 500


# ==========================================
# RECENT DETECTION LOGS
# ==========================================

@admin.route("/admin/logs", methods=["GET"])
def admin_logs():

    if not admin_required():

        return jsonify({
            "success": False,
            "message": "Admin authentication required."
        }), 401

    try:

        conn = sqlite3.connect(DATABASE)

        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                scans.id,
                users.name,
                users.email,
                scans.image_name,
                scans.prediction,
                scans.confidence,
                scans.risk_level,
                scans.scan_time
            FROM scans
            LEFT JOIN users
                ON scans.user_id = users.id
            ORDER BY scans.id DESC
            LIMIT 10
        """)

        rows = cursor.fetchall()

        conn.close()

        logs = []

        for row in rows:

            logs.append({
                "id": row["id"],
                "user": row["name"] or "Unknown",
                "email": row["email"] or "",
                "filename": row["image_name"],
                "prediction": row["prediction"],
                "confidence": row["confidence"],
                "risk_level": row["risk_level"],
                "date": row["scan_time"]
            })

        return jsonify({
            "success": True,
            "logs": logs
        }), 200

    except Exception as e:

        print("ADMIN LOG ERROR:", e)

        return jsonify({
            "success": False,
            "message": "Unable to load detection logs."
        }), 500