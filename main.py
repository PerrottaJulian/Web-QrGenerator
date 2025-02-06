from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(
        os.path.join(app.root_path, 'static', 'images'),
        filename,
        as_attachment=True,  # Esto es lo que forzará la descarga
        mimetype='image/jpeg'  # Asegúrate de usar el tipo MIME adecuado para tu imagen
    )

if __name__ == "__main__":
    app.run(debug=True)
