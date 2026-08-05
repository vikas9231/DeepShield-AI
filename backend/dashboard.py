from flask import Blueprint, jsonify
import sqlite3

dashboard = Blueprint("dashboard", __name__)

DATABASE = "database.db"


# ==========================================
# Dashboard Statistics
# ==========================================

@dashboard.route("/dashboard/<int:user_id>", methods=["GET"])
def dashboard_stats(user_id):

    try:

        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        # -----------------------------
        # Total Scans
        # -----------------------------

        cursor.execute("""

            SELECT COUNT(*) AS total

            FROM scans

            WHERE user_id=?

        """, (user_id,))

        total_scans = cursor.fetchone()["total"]

        # -----------------------------
        # Real Images
        # -----------------------------

        cursor.execute("""

            SELECT COUNT(*) AS total

            FROM scans

            WHERE user_id=?
            AND prediction='Real'

        """, (user_id,))

        real_images = cursor.fetchone()["total"]

        # -----------------------------
        # Deepfake Images
        # -----------------------------

        cursor.execute("""

            SELECT COUNT(*) AS total

            FROM scans

            WHERE user_id=?
            AND prediction='Deepfake'

        """, (user_id,))

        deepfake_images = cursor.fetchone()["total"]

        # -----------------------------
        # Total Videos
        # -----------------------------

        videos = 0

        # -----------------------------
        # Reports
        # -----------------------------

        reports = total_scans

        # -----------------------------
        # Accuracy
        # -----------------------------

        if total_scans == 0:

            accuracy = 0

        else:

            accuracy = round(
                (real_images / total_scans) * 100,
                2
            )

        conn.close()

        return jsonify({

            "success": True,

            "total_scans": total_scans,

            "images": total_scans,

            "videos": videos,

            "deepfakes": deepfake_images,

            "accuracy": accuracy,

            "reports": reports

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500