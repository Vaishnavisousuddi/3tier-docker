from flask import Flask, jsonify
import mysql.connector
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests

# Environment variables for RDS
db_host = os.environ.get("DB_HOST")
db_user = os.environ.get("DB_USER")
db_pass = os.environ.get("DB_PASS")
db_name = os.environ.get("DB_NAME")

@app.route("/")
def home():
    try:
        # Connect to RDS MySQL
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_pass,
            database=db_name
        )
        cursor = conn.cursor()
        cursor.execute("SELECT NOW();")  # Read-only query
        result = cursor.fetchone()
        conn.close()
        return jsonify({"message": f"Connected to RDS! Current time: {result[0]}"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
