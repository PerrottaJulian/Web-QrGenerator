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

def generateQr(url):
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image()

    timestamp = int(time.time())
    img_filename = f'qrcode_{timestamp}'

    img_path = os.path.join(IMG_FOLDER, img_filenames)  # Nombre fijo, puedes cambiarlo
    img.save(img_path)

    return img_path


@app.route("/", methods=['GET', 'POST'] )
def home():
    if request.method == 'POST':
        #download_file( request.form.get('url') )
        url = request.form.get('url')
        if url:
            generateQr(url)
            return f'''
                <img src="/static/images/qr_code.jpg" alt="QR Code">
                <br>
                <a href="/download">Descargar QR</a>
            '''

    return render_template("index.html")

@app.route('/download')
def download_file():
    return send_from_directory(
        IMG_FOLDER,
        'qr_code.jpg',
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