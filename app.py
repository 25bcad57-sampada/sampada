from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)

# ================= DATABASE =================
conn = None
cursor = None

try:
    conn = mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE"),
        port=int(os.getenv("MYSQLPORT", 3306))
    )
    cursor = conn.cursor()
    print("✅ MySQL Connected")
except Exception as e:
    print("❌ MySQL Error:", e)

# ================= HOME =================
@app.route("/")
def home():
    return render_template("index.html")   # templates folder

# ================= CONTACT =================
@app.route("/contact", methods=["POST"])
def contact():
    print("🔥 ROUTE HIT")

    try:
        if cursor is None:
            return jsonify({"message": "Database not connected"})

        data = request.get_json()
        print("DATA:", data)

        cursor.execute(
            "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)",
            (data["name"], data["email"], data["message"])
        )
        conn.commit()   # ✅ FIXED

        print("✅ INSERTED")

        return jsonify({"message": "Saved successfully!"})

    except Exception as e:
        print("❌ ERROR:", e)
        return jsonify({"message": str(e)})

# NO app.run here