from flask import Flask, render_template, request, redirect, url_for
from detect import FaceDetection  # Assuming detect.py contains your image detection logic
import sqlite3
import os

app = Flask(__name__)

# Function to create SQLite3 connection and cursor
def create_connection():
    conn = sqlite3.connect('images2.db')
    cursor = conn.cursor()
    return conn, cursor

# Create images table if it doesn't exist
def create_table():
    conn, cursor = create_connection()
    cursor.execute('''CREATE TABLE IF NOT EXISTS images (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        data BLOB,
                        filepath TEXT
                    )''')
    conn.commit()
    conn.close()

create_table()  # Call create_table to ensure table exists

@app.route('/')
def home():
    return render_template("index.html")

# Set up directories for storing uploads
static_dir = os.path.join(os.path.dirname(__file__), 'static')
uploads_dir = os.path.join(static_dir, 'uploads')
os.makedirs(uploads_dir, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            name = file.filename
            filepath = os.path.join(uploads_dir, name)  # Save file to static/uploads directory
            file.save(filepath)
            conn, cursor = create_connection()
            cursor.execute("INSERT INTO images (name, filepath) VALUES (?, ?)", (name, filepath))
            conn.commit()
            conn.close()
            return redirect(url_for('wannatry'))
    return redirect(url_for('home'))
import json
@app.route('/wannatry.html')
def wannatry():
    conn, cursor = create_connection()
    cursor.execute("SELECT filepath FROM images ORDER BY id DESC LIMIT 1")  # Fetch the latest uploaded image
    filepath = cursor.fetchone()
    conn.close()

    if filepath:
        filepath = filepath[0]  # Fetch the filepath from the result tuple
        Face = FaceDetection(path_to_image=filepath)
        result = Face.analyse_image()
        parsed_data = json.loads(result)
        return render_template("wannatry.html", parsed_data=parsed_data)
    else:
        return render_template("wannatry.html")  # No image uploaded yet

if __name__ == "__main__":
    app.run(debug=True)
