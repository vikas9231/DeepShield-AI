from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

import os
import sqlite3

from predict import predict_image
from predict_video import predict_video

upload = Blueprint("upload", __name__)

DATABASE = "database.db"

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ==========================================
# Allowed Extensions
# ==========================================

IMAGE_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png"
}

VIDEO_EXTENSIONS = {
    "mp4",
    "avi",
    "mov",
    "mkv"
}


def allowed_image(filename):

    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in IMAGE_EXTENSIONS
    )


def allowed_video(filename):

    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in VIDEO_EXTENSIONS
    )


# ==========================================
# Upload Image
# ==========================================

@upload.route("/upload-image", methods=["POST"])
def upload_image():

    if "image" not in request.files:

        return jsonify({

            "success": False,

            "message": "No image selected."

        }), 400

    image = request.files["image"]

    if image.filename == "":

        return jsonify({

            "success": False,

            "message": "Please choose an image."

        }), 400

    if not allowed_file(image.filename):

        return jsonify({

            "success": False,

            "message": "Only JPG, JPEG and PNG images are allowed."

        }), 400

    filename = secure_filename(image.filename)

    image_path = os.path.join(UPLOAD_FOLDER, filename)

    image.save(image_path)

    result = predict_image(image_path)

    user_id = request.form.get("user_id", 1)

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO scans(

            user_id,
            image_name,
            prediction,
            confidence,
            raw_prediction,
            risk_level

        )

        VALUES(?,?,?,?,?,?)

    """,(

        user_id,

        filename,

        result["prediction"],

        result["confidence"],

        result["raw_prediction"],

        result["risk_level"]

    ))

    conn.commit()

    scan_id = cursor.lastrowid

    conn.close()

    return jsonify({

        "success": True,

        "scan_id": scan_id,

        "filename": filename,

        "prediction": result["prediction"],

        "confidence": result["confidence"],

        "raw_prediction": result["raw_prediction"],

        "risk_level": result["risk_level"]

    })

# ==========================================
# Upload Video
# ==========================================

@upload.route("/upload-video", methods=["POST"])
def upload_video():

    if "video" not in request.files:

        return jsonify({

            "success": False,

            "message": "No video selected."

        }), 400

    video = request.files["video"]

    if video.filename == "":

        return jsonify({

            "success": False,

            "message": "Please choose a video."

        }), 400

    if not allowed_video(video.filename):

        return jsonify({

            "success": False,

            "message": "Only MP4, AVI, MOV and MKV videos are allowed."

        }), 400

    filename = secure_filename(video.filename)

    video_path = os.path.join(UPLOAD_FOLDER, filename)

    video.save(video_path)

    # AI Prediction
    result = predict_video(video_path)

    user_id = request.form.get("user_id", 1)

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO scans(

            user_id,
            image_name,
            prediction,
            confidence,
            raw_prediction,
            risk_level

        )

        VALUES(?,?,?,?,?,?)

    """,(

        user_id,

        filename,

        result["prediction"],

        result["confidence"],

        result["raw_prediction"],

        result["risk_level"]

    ))

    conn.commit()

    scan_id = cursor.lastrowid

    conn.close()

    return jsonify({

        "success": True,

        "scan_id": scan_id,

        "filename": filename,

        "prediction": result["prediction"],

        "confidence": result["confidence"],

        "raw_prediction": result["raw_prediction"],

        "risk_level": result["risk_level"]

    })


# ==========================================
# Scan History
# ==========================================

@upload.route("/history/<int:user_id>", methods=["GET"])
def get_history(user_id):

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM scans

        WHERE user_id=?

        ORDER BY scan_time DESC

    """,(user_id,))

    rows = cursor.fetchall()

    conn.close()

    history = []

    for row in rows:

        filename = row["image_name"]

        extension = filename.split(".")[-1].lower()

        if extension in VIDEO_EXTENSIONS:

            media_type = "Video"
        else:
            media_type = "Image"

        history.append({

            "id": row["id"],

            "filename": filename,

            "type": media_type,

            "prediction": row["prediction"],

            "confidence": row["confidence"],

            "raw_prediction": row["raw_prediction"],

            "risk_level": row["risk_level"],

            "date": row["scan_time"]

        })

    return jsonify({

        "success": True,

        "history": history

    })


# ==========================================
# Delete Scan
# ==========================================

@upload.route("/history/<int:scan_id>", methods=["DELETE"])
def delete_scan(scan_id):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute(

        "DELETE FROM scans WHERE id=?",

        (scan_id,)

    )

    conn.commit()

    conn.close()

    return jsonify({

        "success": True,

        "message": "Scan deleted successfully."

    })

# ==========================================
# Dashboard Recent Activity
# ==========================================

@upload.route("/dashboard/recent/<int:user_id>", methods=["GET"])
def dashboard_recent(user_id):

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            image_name,
            prediction,
            confidence,
            scan_time

        FROM scans

        WHERE user_id=?

        ORDER BY id DESC

        LIMIT 5

    """, (user_id,))

    rows = cursor.fetchall()

    conn.close()

    recent = []

    for row in rows:

        recent.append({

            "filename": row["image_name"],

            "prediction": row["prediction"],

            "confidence": row["confidence"],

            "date": row["scan_time"]

        })

    return jsonify({

        "success": True,

        "recent": recent

    })


# ==========================================
# Dashboard Statistics
# ==========================================

@upload.route("/dashboard/<int:user_id>", methods=["GET"])
def dashboard(user_id):

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            image_name,
            prediction,
            confidence

        FROM scans

        WHERE user_id=?

    """,(user_id,))

    rows = cursor.fetchall()

    conn.close()

    total_scans = len(rows)

    images = 0

    videos = 0

    deepfakes = 0

    confidence_sum = 0

    for row in rows:

        filename = row["image_name"].lower()

        if filename.endswith((".mp4", ".avi", ".mov", ".mkv")):

            videos += 1

        else:

            images += 1

        if row["prediction"] == "Deepfake":

            deepfakes += 1

        confidence_sum += row["confidence"]

    accuracy = 0

    if total_scans > 0:

        accuracy = round(confidence_sum / total_scans, 2)

    return jsonify({

        "success": True,

        "total_scans": total_scans,

        "images": images,

        "videos": videos,

        "deepfakes": deepfakes,

        "reports": total_scans,

        "accuracy": accuracy

    })

@upload.route("/report/<int:user_id>", methods=["GET"])
def get_latest_report(user_id):

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM scans
        WHERE user_id=?
        ORDER BY id DESC
        LIMIT 1
    """, (user_id,))

    row = cursor.fetchone()

    conn.close()

    if row is None:

        return jsonify({

            "success": False,

            "message": "No reports found."

        }), 404

    filename = row["image_name"]

    extension = filename.split(".")[-1].lower()

    if extension in ["mp4", "avi", "mov", "mkv"]:

        media_type = "Video"

    else:

        media_type = "Image"

    return jsonify({

        "success": True,

        "report": {

            "id": row["id"],

            "filename": filename,

            "type": media_type,

            "prediction": row["prediction"],

            "confidence": row["confidence"],

            "risk_level": row["risk_level"],

            "date": row["scan_time"],

            "image": "/uploads/" + filename,

            "model": "CNN Model"

        }

    })