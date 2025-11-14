# ------------------------------------------------------------
# Copyright (c) 2025 Sumanth
# Licensed under the MIT License. See /license for details.
# ------------------------------------------------------------

from flask import Flask, render_template, request, jsonify, send_from_directory
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

# ---------------------------
# MONGODB CONNECTION
# ---------------------------
client = MongoClient("mongodb://localhost:27017/")
db = client["getitback_db"]

lost_collection = db["lost_items"]

# ---------------------------
# LICENSE FILE ROUTE
# ---------------------------
@app.route("/license")
def license_file():
    root_dir = os.path.abspath(os.path.dirname(__file__))
    return send_from_directory(root_dir, "LICENSE")


# ---------------------------
# HOME PAGE
# ---------------------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------------------
# PAGE: ADD LOST ITEM
# ---------------------------
@app.route("/lost")
def lost_page():
    return render_template("lost.html")


# ---------------------------
# PAGE: REPORT FOUND
# ---------------------------
@app.route("/found")
def found_page():
    return render_template("found.html")


# ---------------------------
# API: LIST LOST ITEMS + FOUND REPORTS
# ---------------------------
@app.route("/api/list-lost")
def list_lost_items():
    items = list(lost_collection.find({}, {"_id": 0}))
    return jsonify(items)


# ---------------------------
# API: ADD LOST ITEM
# ---------------------------
@app.route("/api/lost", methods=["POST"])
def submit_lost():
    data = request.form.to_dict()
    data["date"] = str(datetime.now().date())
    data["found_reports"] = []  # list of people who found it

    lost_collection.insert_one(data)

    return jsonify({"status": "success", "message": "Lost item added successfully!"})


# ---------------------------
# API: REPORT FOUND
# ---------------------------
@app.route("/api/found", methods=["POST"])
def submit_found():
    data = request.form.to_dict()
    item = data["item_name"]

    report = {
        "finder_name": data["finder_name"],
        "email": data["email"],
        "description": data.get("description", ""),
        "found_place": data["found_place"],
        "date": str(datetime.now().date())
    }

    lost_collection.update_one(
        {"item_name": item},
        {"$push": {"found_reports": report}}
    )

    return jsonify({"status": "success", "message": "Found item reported successfully!"})


# ---------------------------
# RUN
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
