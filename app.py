from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)

# ================= DATABASE CONNECTION =================
try:
    conn = mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE"),
        port=int(os.getenv("MYSQLPORT", 3306))
    )
    cursor = conn.cursor()
    print("✅ MySQL Connected Successfully")
except Exception as e:
    print("❌ MySQL Connection Failed:", e)

# ================= SERVE FRONTEND =================
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

# Serve CSS, images, JS automatically
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

# ================= CONTACT FORM =================
@app.route('/contact', methods=['POST'])
def contact():
    try:
        data = request.json

        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        sql = "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)"
        cursor.execute(sql, (name, email, message))
        conn.commit()

        return jsonify({"message": "Message sent successfully!"})

    except Exception as e:
        return jsonify({"message": str(e)})

# ================= TEST ROUTE =================
@app.route('/test')
def test():
    return "Server is working ✅"

# ================= RUN (RENDER FIX) =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render provides PORT
    app.run(host='0.0.0.0', port=port)