from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__, static_folder='.')
CORS(app)

# MySQL Connection
conn = mysql.connector.connect(
    host=os.getenv("MYSQLHOST"),
    user=os.getenv("MYSQLUSER"),
    password=os.getenv("MYSQLPASSWORD"),
    database=os.getenv("MYSQLDATABASE"),
    port=os.getenv("MYSQLPORT")
)

cursor = conn.cursor()

# ✅ MAIN PAGE (FIXES NOT FOUND)
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

# ✅ CSS FILE
@app.route('/style.css')
def css():
    return send_from_directory('.', 'style.css')

# ✅ IMAGE FILE (PROFILE PHOTO)
@app.route('/profile.jpg')
def image():
    return send_from_directory('.', 'profile.jpg')

# ✅ CONTACT FORM (POST ONLY)
@app.route('/contact', methods=['POST'])
def contact():
    data = request.json

    sql = "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)"
    cursor.execute(sql, (data['name'], data['email'], data['message']))
    conn.commit()

    return jsonify({"message": "Message sent successfully!"})

# OPTIONAL TEST ROUTE
@app.route('/test')
def test():
    return "Server working fine!"

# RUN SERVER
if __name__ == '__main__':
    app.run(debug=True)