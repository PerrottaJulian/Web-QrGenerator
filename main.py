from flask import Flask, render_template, send_from_directory, request
import os
import time
import qrcode



app = Flask(__name__)

IMG_FOLDER = os.path.join(app.root_path, 'static/images')

qr = qrcode.QRCode(
    version = 1,
    box_size=10,
    border=2.5
)
os.makedirs(IMG_FOLDER, exist_ok=True)

def clean_qrs():
    now = time.time

    for filename in os.listdir(IMG_FOLDER):
        filepath = os.path.join(IMG_FOLDER,filename)

        if os.path.isfile(filepath):
            creationtime = os.path.getctime(filepath)

            if (now - creationtime) > 3600:
                os.remove(filepath)


def generateQr(url):
    timestamp = int(time.time())  # Genera un número único basado en el tiempo
    img_filename = f'qr_{timestamp}.jpg'  # Crea un nombre único
    
    img_path = os.path.join(IMG_FOLDER, img_filename)
    qr = qrcode.make(url)
    qr.save(img_path)

    return img_filename  # Devuelve solo el nombre de la imagen



@app.route("/", methods=['GET', 'POST'] )
def home():
    clean_qrs()

    qr_filename = None
    if request.method == 'POST':
        #download_file( request.form.get('url') )
        url = request.form.get('url')

        if url:
            qr_filename = generateQr(url)

            return f'''
                <img src="/static/images/{qr_filename}" alt="QR Code">
                <br>
                <a href="/download">Descargar QR</a>
            '''

    return render_template("index.html", qr_filename=qr_filename)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(
        IMG_FOLDER,
        filename,
        as_attachment=True,  # Esto es lo que forzará la descarga
        mimetype='image/jpeg'  # Asegúrate de usar el tipo MIME adecuado para tu imagen
    )

if __name__ == "__main__":
    app.run(debug=True)


# from flask import Flask, render_template, request

# app = Flask(__name__)

# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         nombre = request.form.get("nombre")  # Captura el input
#         return f"Hola, {nombre}!"  # Muestra el resultado en la misma página

#     return render_template("index.html")  # Renderiza el HTML

# if __name__ == "__main__":
#     app.run(debug=True)