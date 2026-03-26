from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__, static_folder='static')
CORS(app)

# ================= DATABASE =================
conn = mysql.connector.connect(
    host=os.getenv("MYSQLHOST"),
    user=os.getenv("MYSQLUSER"),
    password=os.getenv("MYSQLPASSWORD"),
    database=os.getenv("MYSQLDATABASE"),
    port=int(os.getenv("MYSQLPORT", 3306))
)

cursor = conn.cursor()

# ================= SERVE HTML =================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact", methods=["POST"])
def contact():
    print("🔥 ROUTE HIT")   # MUST PRINT

    try:
        data = request.get_json()
        print("DATA:", data)

        cursor.execute(
            "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)",
            (data["name"], data["email"], data["message"])
        )
        db.commit()

        print("✅ INSERTED")

        return jsonify({"message": "Saved successfully!"})

    except Exception as e:
        print("❌ ERROR:", e)
        return jsonify({"message": "Error"})
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)