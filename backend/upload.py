# from flask import Blueprint, request, jsonify
# from werkzeug.utils import secure_filename

# import os
# import sqlite3

# from predict import predict_image
# from predict_video import predict_video


# # ==========================================
# # Blueprint
# # ==========================================

# upload = Blueprint("upload", __name__)


# # ==========================================
# # Paths
# # ==========================================

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# DATABASE = os.path.join(BASE_DIR, "database.db")

# UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")


# # Create uploads folder if it doesn't exist

# os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# # ==========================================
# # Allowed Extensions
# # ==========================================

# ALLOWED_IMAGE_EXTENSIONS = {
#     "jpg",
#     "jpeg",
#     "png"
# }

# ALLOWED_VIDEO_EXTENSIONS = {
#     "mp4",
#     "avi",
#     "mov",
#     "mkv"
# }


# # ==========================================
# # Check Image Extension
# # ==========================================

# def allowed_file(filename):

#     if not filename:
#         return False

#     if "." not in filename:
#         return False

#     extension = filename.rsplit(".", 1)[1].lower()

#     return extension in ALLOWED_IMAGE_EXTENSIONS


# # ==========================================
# # Check Video Extension
# # ==========================================

# def allowed_video(filename):

#     if not filename:
#         return False

#     if "." not in filename:
#         return False

#     extension = filename.rsplit(".", 1)[1].lower()

#     return extension in ALLOWED_VIDEO_EXTENSIONS


# # ==========================================
# # Upload & Detect Image
# # ==========================================

# @upload.route("/upload-image", methods=["POST"])
# def upload_image():

#     try:

#         # --------------------------------------
#         # Check Image
#         # --------------------------------------

#         if "image" not in request.files:

#             return jsonify({
#                 "success": False,
#                 "message": "No image selected."
#             }), 400

#         image = request.files["image"]

#         if image.filename == "":

#             return jsonify({
#                 "success": False,
#                 "message": "Please choose an image."
#             }), 400

#         # --------------------------------------
#         # Validate Image
#         # --------------------------------------

#         if not allowed_file(image.filename):

#             return jsonify({
#                 "success": False,
#                 "message": "Only JPG, JPEG and PNG images are allowed."
#             }), 400

#         # --------------------------------------
#         # User ID
#         # --------------------------------------

#         user_id = request.form.get("user_id")

#         if not user_id:

#             return jsonify({
#                 "success": False,
#                 "message": "User ID is missing."
#             }), 400

#         # --------------------------------------
#         # Secure Filename
#         # --------------------------------------

#         filename = secure_filename(image.filename)

#         if not filename:

#             return jsonify({
#                 "success": False,
#                 "message": "Invalid filename."
#             }), 400

#         # --------------------------------------
#         # Save Image
#         # --------------------------------------

#         image_path = os.path.join(
#             UPLOAD_FOLDER,
#             filename
#         )

#         image.save(image_path)

#         # --------------------------------------
#         # AI Prediction
#         # --------------------------------------

#         result = predict_image(image_path)

#         # --------------------------------------
#         # Save Scan
#         # --------------------------------------

#         conn = sqlite3.connect(DATABASE)

#         cursor = conn.cursor()

#         cursor.execute("""
#             INSERT INTO scans (
#                 user_id,
#                 image_name,
#                 prediction,
#                 confidence,
#                 raw_prediction,
#                 risk_level
#             )
#             VALUES (?, ?, ?, ?, ?, ?)
#         """, (

#             int(user_id),

#             filename,

#             result["prediction"],

#             result["confidence"],

#             result["raw_prediction"],

#             result["risk_level"]

#         ))

#         conn.commit()

#         scan_id = cursor.lastrowid

#         conn.close()

#         print("\n========== IMAGE SCAN ==========")
#         print("User ID     :", user_id)
#         print("Filename    :", filename)
#         print("Prediction  :", result["prediction"])
#         print("Confidence  :", result["confidence"])
#         print("Scan ID     :", scan_id)
#         print("================================\n")

#         # --------------------------------------
#         # Response
#         # --------------------------------------

#         return jsonify({

#             "success": True,

#             "scan_id": scan_id,

#             "filename": filename,

#             "prediction": result["prediction"],

#             "confidence": result["confidence"],

#             "raw_prediction": result["raw_prediction"],

#             "risk_level": result["risk_level"]

#         }), 200

#     except Exception as e:

#         print("\nIMAGE UPLOAD ERROR:")
#         print(e)

#         return jsonify({

#             "success": False,

#             "message": str(e)

#         }), 500


# # ==========================================
# # Upload & Detect Video
# # ==========================================

# @upload.route("/upload-video", methods=["POST"])
# def upload_video():

#     try:

#         # --------------------------------------
#         # Check Video
#         # --------------------------------------

#         if "video" not in request.files:

#             return jsonify({
#                 "success": False,
#                 "message": "No video selected."
#             }), 400

#         video = request.files["video"]

#         if video.filename == "":

#             return jsonify({
#                 "success": False,
#                 "message": "Please choose a video."
#             }), 400

#         # --------------------------------------
#         # Validate Video
#         # --------------------------------------

#         if not allowed_video(video.filename):

#             return jsonify({
#                 "success": False,
#                 "message": (
#                     "Only MP4, AVI, MOV and MKV videos "
#                     "are allowed."
#                 )
#             }), 400

#         # --------------------------------------
#         # User ID
#         # --------------------------------------

#         user_id = request.form.get("user_id")

#         if not user_id:

#             return jsonify({
#                 "success": False,
#                 "message": "User ID is missing."
#             }), 400

#         # --------------------------------------
#         # Secure Filename
#         # --------------------------------------

#         filename = secure_filename(video.filename)

#         if not filename:

#             return jsonify({
#                 "success": False,
#                 "message": "Invalid filename."
#             }), 400

#         # --------------------------------------
#         # Save Video
#         # --------------------------------------

#         video_path = os.path.join(
#             UPLOAD_FOLDER,
#             filename
#         )

#         video.save(video_path)

#         # --------------------------------------
#         # AI Prediction
#         # --------------------------------------

#         result = predict_video(video_path)

#         # --------------------------------------
#         # Save Scan
#         # --------------------------------------

#         conn = sqlite3.connect(DATABASE)

#         cursor = conn.cursor()

#         cursor.execute("""
#             INSERT INTO scans (
#                 user_id,
#                 image_name,
#                 prediction,
#                 confidence,
#                 raw_prediction,
#                 risk_level
#             )
#             VALUES (?, ?, ?, ?, ?, ?)
#         """, (

#             int(user_id),

#             filename,

#             result["prediction"],

#             result["confidence"],

#             result["raw_prediction"],

#             result["risk_level"]

#         ))

#         conn.commit()

#         scan_id = cursor.lastrowid

#         conn.close()

#         print("\n========== VIDEO SCAN ==========")
#         print("User ID     :", user_id)
#         print("Filename    :", filename)
#         print("Prediction  :", result["prediction"])
#         print("Confidence  :", result["confidence"])
#         print("Scan ID     :", scan_id)
#         print("================================\n")

#         # --------------------------------------
#         # Response
#         # --------------------------------------

#         return jsonify({

#             "success": True,

#             "scan_id": scan_id,

#             "filename": filename,

#             "prediction": result["prediction"],

#             "confidence": result["confidence"],

#             "raw_prediction": result["raw_prediction"],

#             "risk_level": result["risk_level"]

#         }), 200

#     except Exception as e:

#         print("\nVIDEO UPLOAD ERROR:")
#         print(e)

#         return jsonify({

#             "success": False,

#             "message": str(e)

#         }), 500


# # ==========================================
# # Get User Scan History
# # ==========================================

# @upload.route("/history/<int:user_id>", methods=["GET"])
# def get_history(user_id):

#     try:

#         conn = sqlite3.connect(DATABASE)

#         conn.row_factory = sqlite3.Row

#         cursor = conn.cursor()

#         cursor.execute("""
#             SELECT
#                 id,
#                 image_name,
#                 prediction,
#                 confidence,
#                 raw_prediction,
#                 risk_level,
#                 scan_time
#             FROM scans
#             WHERE user_id = ?
#             ORDER BY scan_time DESC
#         """, (user_id,))

#         scans = cursor.fetchall()

#         conn.close()

#         history = []

#         for scan in scans:

#             filename = scan["image_name"]

#             extension = ""

#             if "." in filename:

#                 extension = (
#                     filename.rsplit(".", 1)[1]
#                     .lower()
#                 )

#             if extension in ALLOWED_VIDEO_EXTENSIONS:

#                 file_type = "Video"

#             else:

#                 file_type = "Image"

#             history.append({

#                 "id": scan["id"],

#                 "filename": filename,

#                 "type": file_type,

#                 "prediction": scan["prediction"],

#                 "confidence": scan["confidence"],

#                 "raw_prediction": scan["raw_prediction"],

#                 "risk_level": scan["risk_level"],

#                 "date": scan["scan_time"]

#             })

#         return jsonify({

#             "success": True,

#             "history": history

#         }), 200

#     except Exception as e:

#         print("\nHISTORY ERROR:")
#         print(e)

#         return jsonify({

#             "success": False,

#             "message": str(e)

#         }), 500


# # ==========================================
# # Delete Scan
# # ==========================================

# @upload.route("/history/<int:scan_id>", methods=["DELETE"])
# def delete_scan(scan_id):

#     try:

#         conn = sqlite3.connect(DATABASE)

#         cursor = conn.cursor()

#         # --------------------------------------
#         # Get File Before Deleting DB Record
#         # --------------------------------------

#         cursor.execute("""
#             SELECT image_name
#             FROM scans
#             WHERE id = ?
#         """, (scan_id,))

#         scan = cursor.fetchone()

#         if scan is None:

#             conn.close()

#             return jsonify({

#                 "success": False,

#                 "message": "Scan not found."

#             }), 404

#         filename = scan[0]

#         # --------------------------------------
#         # Delete Database Record
#         # --------------------------------------

#         cursor.execute(
#             "DELETE FROM scans WHERE id = ?",
#             (scan_id,)
#         )

#         conn.commit()

#         conn.close()

#         # --------------------------------------
#         # Delete Uploaded File
#         # --------------------------------------

#         file_path = os.path.join(
#             UPLOAD_FOLDER,
#             filename
#         )

#         if os.path.exists(file_path):

#             os.remove(file_path)

#         return jsonify({

#             "success": True,

#             "message": "Scan deleted successfully."

#         }), 200

#     except Exception as e:

#         print("\nDELETE SCAN ERROR:")
#         print(e)

#         return jsonify({

#             "success": False,

#             "message": str(e)

#         }), 500


# # ==========================================
# # Recent Dashboard Activity
# # ==========================================

# @upload.route(
#     "/dashboard/recent/<int:user_id>",
#     methods=["GET"]
# )
# def dashboard_recent(user_id):

#     try:

#         conn = sqlite3.connect(DATABASE)

#         conn.row_factory = sqlite3.Row

#         cursor = conn.cursor()

#         cursor.execute("""
#             SELECT
#                 image_name,
#                 prediction,
#                 confidence,
#                 scan_time
#             FROM scans
#             WHERE user_id = ?
#             ORDER BY id DESC
#             LIMIT 5
#         """, (user_id,))

#         rows = cursor.fetchall()

#         conn.close()

#         recent = []

#         for row in rows:

#             recent.append({

#                 "filename": row["image_name"],

#                 "prediction": row["prediction"],

#                 "confidence": row["confidence"],

#                 "date": row["scan_time"]

#             })

#         return jsonify({

#             "success": True,

#             "recent": recent

#         }), 200

#     except Exception as e:

#         print("\nRECENT ACTIVITY ERROR:")
#         print(e)

#         return jsonify({

#             "success": False,

#             "message": str(e)

#         }), 500


# # ==========================================
# # Dashboard Statistics
# # ==========================================

# @upload.route(
#     "/dashboard/<int:user_id>",
#     methods=["GET"]
# )
# def dashboard(user_id):

#     try:

#         conn = sqlite3.connect(DATABASE)

#         cursor = conn.cursor()

#         # --------------------------------------
#         # Total Scans
#         # --------------------------------------

#         cursor.execute("""
#             SELECT COUNT(*)
#             FROM scans
#             WHERE user_id = ?
#         """, (user_id,))

#         total_scans = cursor.fetchone()[0]

#         # --------------------------------------
#         # Images
#         # --------------------------------------

#         cursor.execute("""
#             SELECT COUNT(*)
#             FROM scans
#             WHERE user_id = ?
#             AND (
#                 image_name LIKE '%.jpg'
#                 OR image_name LIKE '%.jpeg'
#                 OR image_name LIKE '%.png'
#             )
#         """, (user_id,))

#         images = cursor.fetchone()[0]

#         # --------------------------------------
#         # Videos
#         # --------------------------------------

#         cursor.execute("""
#             SELECT COUNT(*)
#             FROM scans
#             WHERE user_id = ?
#             AND (
#                 image_name LIKE '%.mp4'
#                 OR image_name LIKE '%.avi'
#                 OR image_name LIKE '%.mov'
#                 OR image_name LIKE '%.mkv'
#             )
#         """, (user_id,))

#         videos = cursor.fetchone()[0]

#         # --------------------------------------
#         # Deepfakes
#         # --------------------------------------

#         cursor.execute("""
#             SELECT COUNT(*)
#             FROM scans
#             WHERE user_id = ?
#             AND prediction = 'Deepfake'
#         """, (user_id,))

#         deepfakes = cursor.fetchone()[0]

#         # --------------------------------------
#         # Reports
#         # --------------------------------------

#         reports = total_scans

#         # --------------------------------------
#         # Average Confidence
#         # --------------------------------------

#         cursor.execute("""
#             SELECT AVG(confidence)
#             FROM scans
#             WHERE user_id = ?
#         """, (user_id,))

#         avg_confidence = cursor.fetchone()[0]

#         accuracy = (
#             round(avg_confidence, 2)
#             if avg_confidence is not None
#             else 0
#         )

#         conn.close()

#         return jsonify({

#             "success": True,

#             "total_scans": total_scans,

#             "images": images,

#             "videos": videos,

#             "deepfakes": deepfakes,

#             "reports": reports,

#             "accuracy": accuracy

#         }), 200

#     except Exception as e:

#         print("\nDASHBOARD ERROR:")
#         print(e)

#         return jsonify({

#             "success": False,

#             "message": str(e)

#         }), 500


# # ==========================================
# # Get Latest Report
# # ==========================================

# @upload.route(
#     "/report/<int:user_id>",
#     methods=["GET"]
# )
# def get_report(user_id):

#     try:

#         conn = sqlite3.connect(DATABASE)

#         conn.row_factory = sqlite3.Row

#         cursor = conn.cursor()

#         cursor.execute("""
#             SELECT
#                 id,
#                 image_name,
#                 prediction,
#                 confidence,
#                 raw_prediction,
#                 risk_level,
#                 scan_time
#             FROM scans
#             WHERE user_id = ?
#             ORDER BY id DESC
#             LIMIT 1
#         """, (user_id,))

#         scan = cursor.fetchone()

#         conn.close()

#         if scan is None:

#             return jsonify({

#                 "success": False,

#                 "message": "No reports found."

#             }), 404

#         filename = scan["image_name"]

#         extension = ""

#         if "." in filename:

#             extension = (
#                 filename.rsplit(".", 1)[1]
#                 .lower()
#             )

#         if extension in ALLOWED_VIDEO_EXTENSIONS:

#             file_type = "Video"

#         else:

#             file_type = "Image"

#         return jsonify({

#             "success": True,

#             "report": {

#                 "id": scan["id"],

#                 "filename": filename,

#                 "type": file_type,

#                 "prediction": scan["prediction"],

#                 "confidence": scan["confidence"],

#                 "raw_prediction": scan["raw_prediction"],

#                 "risk_level": scan["risk_level"],

#                 "date": scan["scan_time"],

#                 "model": "CNN Model",

#                 "resolution": "-"

#             }

#         }), 200

#     except Exception as e:

#         print("\nREPORT ERROR:")
#         print(e)

#         return jsonify({

#             "success": False,

#             "message": str(e)

#         }), 500
    

from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

import os
import sqlite3
import uuid
import cv2

from predict import predict_image
from predict_video import predict_video


# ==========================================
# Blueprint
# ==========================================

upload = Blueprint("upload", __name__)


# ==========================================
# Paths
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE = os.path.join(BASE_DIR, "database.db")

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ==========================================
# File Size Limits
# ==========================================

MAX_IMAGE_SIZE = 10 * 1024 * 1024       # 10 MB
MAX_VIDEO_SIZE = 200 * 1024 * 1024      # 200 MB


# ==========================================
# Allowed Extensions
# ==========================================

ALLOWED_IMAGE_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png"
}

ALLOWED_VIDEO_EXTENSIONS = {
    "mp4",
    "avi",
    "mov",
    "mkv"
}


# ==========================================
# Check Image Extension
# ==========================================

def allowed_file(filename):

    if not filename:
        return False

    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in ALLOWED_IMAGE_EXTENSIONS


# ==========================================
# Check Video Extension
# ==========================================

def allowed_video(filename):

    if not filename:
        return False

    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in ALLOWED_VIDEO_EXTENSIONS


# ==========================================
# Generate Safe Unique Filename
# ==========================================

def generate_safe_filename(filename):

    filename = secure_filename(filename)

    if not filename:
        return None

    extension = filename.rsplit(".", 1)[1].lower()

    unique_name = (
        f"{uuid.uuid4().hex}.{extension}"
    )

    return unique_name


# ==========================================
# Validate User ID
# ==========================================

def validate_user_id(user_id):

    if not user_id:
        return None

    try:

        user_id = int(user_id)

        if user_id <= 0:
            return None

        return user_id

    except (ValueError, TypeError):

        return None


# ==========================================
# Check Request Size
# ==========================================

def request_too_large(max_size):

    content_length = request.content_length

    if content_length is not None:
        return content_length > max_size

    return False


# ==========================================
# Validate Image Content
# ==========================================

def validate_image_content(file_path):

    try:

        image = cv2.imread(file_path)

        if image is None:
            return False

        if image.size == 0:
            return False

        return True

    except Exception:

        return False


# ==========================================
# Validate Video Content
# ==========================================

def validate_video_content(file_path):

    cap = None

    try:

        cap = cv2.VideoCapture(file_path)

        if not cap.isOpened():
            return False

        total_frames = int(
            cap.get(cv2.CAP_PROP_FRAME_COUNT)
        )

        return total_frames > 0

    except Exception:

        return False

    finally:

        if cap is not None:
            cap.release()


# ==========================================
# Upload & Detect Image
# ==========================================

@upload.route("/upload-image", methods=["POST"])
def upload_image():

    image_path = None

    try:

        # --------------------------------------
        # Request Size
        # --------------------------------------

        if request_too_large(MAX_IMAGE_SIZE):

            return jsonify({
                "success": False,
                "message": "Image file is too large. Maximum size is 10 MB."
            }), 413

        # --------------------------------------
        # Check Image
        # --------------------------------------

        if "image" not in request.files:

            return jsonify({
                "success": False,
                "message": "No image selected."
            }), 400

        image = request.files["image"]

        if not image.filename:

            return jsonify({
                "success": False,
                "message": "Please choose an image."
            }), 400

        # --------------------------------------
        # Validate Extension
        # --------------------------------------

        if not allowed_file(image.filename):

            return jsonify({
                "success": False,
                "message": "Only JPG, JPEG and PNG images are allowed."
            }), 400

        # --------------------------------------
        # User ID
        # --------------------------------------

        user_id = validate_user_id(
            request.form.get("user_id")
        )

        if user_id is None:

            return jsonify({
                "success": False,
                "message": "Invalid or missing User ID."
            }), 400

        # --------------------------------------
        # Generate Unique Filename
        # --------------------------------------

        filename = generate_safe_filename(
            image.filename
        )

        if not filename:

            return jsonify({
                "success": False,
                "message": "Invalid filename."
            }), 400

        # --------------------------------------
        # Save Image
        # --------------------------------------

        image_path = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        image.save(image_path)

        # --------------------------------------
        # Check Actual File Size
        # --------------------------------------

        file_size = os.path.getsize(image_path)

        if file_size > MAX_IMAGE_SIZE:

            os.remove(image_path)

            return jsonify({
                "success": False,
                "message": "Image file is too large. Maximum size is 10 MB."
            }), 413

        if file_size == 0:

            os.remove(image_path)

            return jsonify({
                "success": False,
                "message": "Uploaded image is empty."
            }), 400

        # --------------------------------------
        # Validate Image Content
        # --------------------------------------

        if not validate_image_content(image_path):

            os.remove(image_path)

            return jsonify({
                "success": False,
                "message": "Invalid or corrupted image file."
            }), 400

        # --------------------------------------
        # AI Prediction
        # --------------------------------------

        result = predict_image(image_path)

        # --------------------------------------
        # Save Scan
        # --------------------------------------

        conn = sqlite3.connect(DATABASE)

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO scans (
                user_id,
                image_name,
                prediction,
                confidence,
                raw_prediction,
                risk_level
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
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

        # --------------------------------------
        # Log
        # --------------------------------------

        print("\n========== IMAGE SCAN ==========")
        print("User ID     :", user_id)
        print("Filename    :", filename)
        print("Prediction  :", result["prediction"])
        print("Confidence  :", result["confidence"])
        print("Scan ID     :", scan_id)
        print("================================\n")

        # --------------------------------------
        # Response
        # --------------------------------------

        return jsonify({

            "success": True,

            "scan_id": scan_id,

            "filename": filename,

            "prediction": result["prediction"],

            "confidence": result["confidence"],

            "raw_prediction": result["raw_prediction"],

            "risk_level": result["risk_level"]

        }), 200

    except Exception as e:

        if image_path and os.path.exists(image_path):

            try:
                os.remove(image_path)
            except Exception:
                pass

        print("\nIMAGE UPLOAD ERROR:")
        print(e)

        return jsonify({

            "success": False,

            "message": "Image processing failed."

        }), 500


# ==========================================
# Upload & Detect Video
# ==========================================

@upload.route("/upload-video", methods=["POST"])
def upload_video():

    video_path = None

    try:

        # --------------------------------------
        # Request Size
        # --------------------------------------

        if request_too_large(MAX_VIDEO_SIZE):

            return jsonify({
                "success": False,
                "message": "Video file is too large. Maximum size is 200 MB."
            }), 413

        # --------------------------------------
        # Check Video
        # --------------------------------------

        if "video" not in request.files:

            return jsonify({
                "success": False,
                "message": "No video selected."
            }), 400

        video = request.files["video"]

        if not video.filename:

            return jsonify({
                "success": False,
                "message": "Please choose a video."
            }), 400

        # --------------------------------------
        # Validate Extension
        # --------------------------------------

        if not allowed_video(video.filename):

            return jsonify({
                "success": False,
                "message": (
                    "Only MP4, AVI, MOV and MKV videos are allowed."
                )
            }), 400

        # --------------------------------------
        # User ID
        # --------------------------------------

        user_id = validate_user_id(
            request.form.get("user_id")
        )

        if user_id is None:

            return jsonify({
                "success": False,
                "message": "Invalid or missing User ID."
            }), 400

        # --------------------------------------
        # Generate Unique Filename
        # --------------------------------------

        filename = generate_safe_filename(
            video.filename
        )

        if not filename:

            return jsonify({
                "success": False,
                "message": "Invalid filename."
            }), 400

        # --------------------------------------
        # Save Video
        # --------------------------------------

        video_path = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        video.save(video_path)

        # --------------------------------------
        # Check Actual File Size
        # --------------------------------------

        file_size = os.path.getsize(video_path)

        if file_size > MAX_VIDEO_SIZE:

            os.remove(video_path)

            return jsonify({
                "success": False,
                "message": "Video file is too large. Maximum size is 200 MB."
            }), 413

        if file_size == 0:

            os.remove(video_path)

            return jsonify({
                "success": False,
                "message": "Uploaded video is empty."
            }), 400

        # --------------------------------------
        # Validate Video Content
        # --------------------------------------

        if not validate_video_content(video_path):

            os.remove(video_path)

            return jsonify({
                "success": False,
                "message": "Invalid or corrupted video file."
            }), 400

        # --------------------------------------
        # AI Prediction
        # --------------------------------------

        result = predict_video(video_path)

        # --------------------------------------
        # Save Scan
        # --------------------------------------

        conn = sqlite3.connect(DATABASE)

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO scans (
                user_id,
                image_name,
                prediction,
                confidence,
                raw_prediction,
                risk_level
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
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

        # --------------------------------------
        # Log
        # --------------------------------------

        print("\n========== VIDEO SCAN ==========")
        print("User ID     :", user_id)
        print("Filename    :", filename)
        print("Prediction  :", result["prediction"])
        print("Confidence  :", result["confidence"])
        print("Scan ID     :", scan_id)
        print("================================\n")

        # --------------------------------------
        # Response
        # --------------------------------------

        return jsonify({

            "success": True,

            "scan_id": scan_id,

            "filename": filename,

            "prediction": result["prediction"],

            "confidence": result["confidence"],

            "raw_prediction": result["raw_prediction"],

            "risk_level": result["risk_level"]

        }), 200

    except Exception as e:

        if video_path and os.path.exists(video_path):

            try:
                os.remove(video_path)
            except Exception:
                pass

        print("\nVIDEO UPLOAD ERROR:")
        print(e)

        return jsonify({

            "success": False,

            "message": "Video processing failed."

        }), 500


# ==========================================
# Get User Scan History
# ==========================================

@upload.route("/history/<int:user_id>", methods=["GET"])
def get_history(user_id):

    try:

        conn = sqlite3.connect(DATABASE)

        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                image_name,
                prediction,
                confidence,
                raw_prediction,
                risk_level,
                scan_time
            FROM scans
            WHERE user_id = ?
            ORDER BY scan_time DESC
        """, (user_id,))

        scans = cursor.fetchall()

        conn.close()

        history = []

        for scan in scans:

            filename = scan["image_name"]

            extension = ""

            if "." in filename:

                extension = (
                    filename.rsplit(".", 1)[1]
                    .lower()
                )

            if extension in ALLOWED_VIDEO_EXTENSIONS:

                file_type = "Video"

            else:

                file_type = "Image"

            history.append({

                "id": scan["id"],

                "filename": filename,

                "type": file_type,

                "prediction": scan["prediction"],

                "confidence": scan["confidence"],

                "raw_prediction": scan["raw_prediction"],

                "risk_level": scan["risk_level"],

                "date": scan["scan_time"]

            })

        return jsonify({

            "success": True,

            "history": history

        }), 200

    except Exception as e:

        print("\nHISTORY ERROR:")
        print(e)

        return jsonify({

            "success": False,

            "message": "Unable to load scan history."

        }), 500


# ==========================================
# Delete Scan
# ==========================================

@upload.route("/history/<int:scan_id>", methods=["DELETE"])
def delete_scan(scan_id):

    try:

        conn = sqlite3.connect(DATABASE)

        cursor = conn.cursor()

        # --------------------------------------
        # Get File Before Deleting DB Record
        # --------------------------------------

        cursor.execute("""
            SELECT image_name
            FROM scans
            WHERE id = ?
        """, (scan_id,))

        scan = cursor.fetchone()

        if scan is None:

            conn.close()

            return jsonify({

                "success": False,

                "message": "Scan not found."

            }), 404

        filename = scan[0]

        # --------------------------------------
        # Delete Database Record
        # --------------------------------------

        cursor.execute(
            "DELETE FROM scans WHERE id = ?",
            (scan_id,)
        )

        conn.commit()

        conn.close()

        # --------------------------------------
        # Delete Uploaded File
        # --------------------------------------

        safe_filename = secure_filename(filename)

        file_path = os.path.join(
            UPLOAD_FOLDER,
            safe_filename
        )

        # Ensure the resolved path stays inside uploads
        upload_folder_real = os.path.realpath(
            UPLOAD_FOLDER
        )

        file_path_real = os.path.realpath(
            file_path
        )

        if (
            file_path_real.startswith(
                upload_folder_real + os.sep
            )
            and os.path.exists(file_path_real)
        ):

            os.remove(file_path_real)

        return jsonify({

            "success": True,

            "message": "Scan deleted successfully."

        }), 200

    except Exception as e:

        print("\nDELETE SCAN ERROR:")
        print(e)

        return jsonify({

            "success": False,

            "message": "Unable to delete scan."

        }), 500


# ==========================================
# Recent Dashboard Activity
# ==========================================

@upload.route(
    "/dashboard/recent/<int:user_id>",
    methods=["GET"]
)
def dashboard_recent(user_id):

    try:

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
            WHERE user_id = ?
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

        }), 200

    except Exception as e:

        print("\nRECENT ACTIVITY ERROR:")
        print(e)

        return jsonify({

            "success": False,

            "message": "Unable to load recent activity."

        }), 500


# ==========================================
# Dashboard Statistics
# ==========================================

@upload.route(
    "/dashboard/<int:user_id>",
    methods=["GET"]
)
def dashboard(user_id):

    try:

        conn = sqlite3.connect(DATABASE)

        cursor = conn.cursor()

        # --------------------------------------
        # Total Scans
        # --------------------------------------

        cursor.execute("""
            SELECT COUNT(*)
            FROM scans
            WHERE user_id = ?
        """, (user_id,))

        total_scans = cursor.fetchone()[0]

        # --------------------------------------
        # Images
        # --------------------------------------

        cursor.execute("""
            SELECT COUNT(*)
            FROM scans
            WHERE user_id = ?
            AND (
                image_name LIKE '%.jpg'
                OR image_name LIKE '%.jpeg'
                OR image_name LIKE '%.png'
            )
        """, (user_id,))

        images = cursor.fetchone()[0]

        # --------------------------------------
        # Videos
        # --------------------------------------

        cursor.execute("""
            SELECT COUNT(*)
            FROM scans
            WHERE user_id = ?
            AND (
                image_name LIKE '%.mp4'
                OR image_name LIKE '%.avi'
                OR image_name LIKE '%.mov'
                OR image_name LIKE '%.mkv'
            )
        """, (user_id,))

        videos = cursor.fetchone()[0]

        # --------------------------------------
        # Deepfakes
        # --------------------------------------

        cursor.execute("""
            SELECT COUNT(*)
            FROM scans
            WHERE user_id = ?
            AND prediction = 'Deepfake'
        """, (user_id,))

        deepfakes = cursor.fetchone()[0]

        # --------------------------------------
        # Reports
        # --------------------------------------

        reports = total_scans

        # --------------------------------------
        # Average Confidence
        # --------------------------------------

        cursor.execute("""
            SELECT AVG(confidence)
            FROM scans
            WHERE user_id = ?
        """, (user_id,))

        avg_confidence = cursor.fetchone()[0]

        accuracy = (
            round(avg_confidence, 2)
            if avg_confidence is not None
            else 0
        )

        conn.close()

        return jsonify({

            "success": True,

            "total_scans": total_scans,

            "images": images,

            "videos": videos,

            "deepfakes": deepfakes,

            "reports": reports,

            "accuracy": accuracy

        }), 200

    except Exception as e:

        print("\nDASHBOARD ERROR:")
        print(e)

        return jsonify({

            "success": False,

            "message": "Unable to load dashboard statistics."

        }), 500


# ==========================================
# Get Latest Report
# ==========================================

@upload.route(
    "/report/<int:user_id>",
    methods=["GET"]
)
def get_report(user_id):

    try:

        conn = sqlite3.connect(DATABASE)

        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                image_name,
                prediction,
                confidence,
                raw_prediction,
                risk_level,
                scan_time
            FROM scans
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT 1
        """, (user_id,))

        scan = cursor.fetchone()

        conn.close()

        if scan is None:

            return jsonify({

                "success": False,

                "message": "No reports found."

            }), 404

        filename = scan["image_name"]

        extension = ""

        if "." in filename:

            extension = (
                filename.rsplit(".", 1)[1]
                .lower()
            )

        if extension in ALLOWED_VIDEO_EXTENSIONS:

            file_type = "Video"
            model_name = "VideoMAE Large"

        else:

            file_type = "Image"
            model_name = "CNN Model"

        return jsonify({

            "success": True,

            "report": {

                "id": scan["id"],

                "filename": filename,

                "type": file_type,

                "prediction": scan["prediction"],

                "confidence": scan["confidence"],

                "raw_prediction": scan["raw_prediction"],

                "risk_level": scan["risk_level"],

                "date": scan["scan_time"],

                "model": model_name,

                "resolution": "-"

            }

        }), 200

    except Exception as e:

        print("\nREPORT ERROR:")
        print(e)

        return jsonify({

            "success": False,

            "message": "Unable to load report."

        }), 500

    