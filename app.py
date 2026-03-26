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
@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

# ================= STATIC FILES =================
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

# ================= CONTACT =================
@app.route('/contact', methods=['POST'])
def contact():
    data = request.json
    sql = "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)"
    cursor.execute(sql, (data['name'], data['email'], data['message']))
    conn.commit()
    return jsonify({"message": "Message sent successfully!"})

# ================= RUN =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)