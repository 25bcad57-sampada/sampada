from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)

# MySQL (safe connect)
try:
    conn = mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE"),
        port=os.getenv("MYSQLPORT")
    )
    cursor = conn.cursor()
    print("MySQL Connected")
except:
    print("MySQL connection failed")

# ✅ SERVE HTML
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

# ✅ SERVE STATIC FILES (CSS + IMAGE automatically)
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

# ✅ CONTACT API
@app.route('/contact', methods=['POST'])
def contact():
    try:
        data = request.json
        sql = "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)"
        cursor.execute(sql, (data['name'], data['email'], data['message']))
        conn.commit()
        return jsonify({"message": "Message sent successfully!"})
    except Exception as e:
        return jsonify({"message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)