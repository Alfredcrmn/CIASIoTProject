from flask import Flask, request, jsonify
import os
import cv2
from werkzeug.utils import secure_filename
import database as db  # Your database helper functions
from facial_recognition import process_face, compare_faces  # Use the provided face detection and comparison logic

app = Flask(__name__)

# Configuration for file uploads
UPLOAD_FOLDER = "./uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/register", methods=["POST"])
def register():
    try:
        # Check if a file is uploaded
        if "file" not in request.files:
            return jsonify({"status": "error", "message": "No file uploaded"}), 400
        
        file = request.files["file"]
        username = request.form["username"]
        
        if file.filename == "":
            return jsonify({"status": "error", "message": "No selected file"}), 400
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        
        # Process the face using the provided logic
        processed_face_path = process_face(filepath)

        if not processed_face_path:
            return jsonify({"status": "error", "message": "No face detected in the uploaded image"}), 400

        # Save to the database
        result = db.registerUser(username, processed_face_path)

        # Clean up uploaded and processed files
        os.remove(filepath)
        if os.path.exists(processed_face_path):
            os.remove(processed_face_path)

        if result["affected"] > 0:
            return jsonify({"status": "success", "message": "Face registered successfully", "user_id": result["id"]})
        else:
            return jsonify({"status": "error", "message": "Failed to register face"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/login", methods=["POST"])
def login():
    try:
        # Check if a file is uploaded
        if "file" not in request.files:
            return jsonify({"status": "error", "message": "No file uploaded"}), 400

        file = request.files["file"]
        username = request.form["username"]

        if file.filename == "":
            return jsonify({"status": "error", "message": "No selected file"}), 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        # Retrieve the stored face from the database
        user_photo_path = f"{username}_stored.jpg"
        result = db.getUser(username, user_photo_path)

        if result["affected"] == 0:
            os.remove(filepath)
            return jsonify({"status": "error", "message": "User not found"}), 404

        # Compare the uploaded face with the stored face
        match = compare_faces(filepath, user_photo_path)

        # Clean up temporary files
        os.remove(filepath)
        if os.path.exists(user_photo_path):
            os.remove(user_photo_path)

        if match:
            return jsonify({"status": "success", "message": "Login successful"})
        else:
            return jsonify({"status": "error", "message": "Face does not match"}), 401
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
