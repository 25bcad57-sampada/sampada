from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)

# Railway MySQL connection
conn = mysql.connector.connect(
    host=os.getenv("MYSQLHOST"),
    user=os.getenv("MYSQLUSER"),
    password=os.getenv("MYSQLPASSWORD"),
    database=os.getenv("MYSQLDATABASE"),
    port=os.getenv("MYSQLPORT")
)

cursor = conn.cursor()

@app.route('/')
def home():
    return "Portfolio Backend Running"

@app.route('/contact', methods=['POST'])
def contact():
    data = request.json
    name = data['name']
    email = data['email']
    message = data['message']

    sql = "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)"
    cursor.execute(sql, (name, email, message))
    conn.commit()

    return jsonify({"message": "Saved successfully"})

if __name__ == '__main__':
    app.run(debug=True)