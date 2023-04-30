from flask import Flask, request, send_file
from pyzbar.pyzbar import decode
from PIL import Image
import qrcode
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return '''
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
            }
            h1 {
                background-color: #4CAF50;
                color: white;
                padding: 20px;
                text-align: center;
            }
            h3 {
                margin-left: 20px;
            }
            form {
                margin-left: 20px;
            }
        </style>
        <h1>A Simple QR Code Generator and Decoder</h1>
        <h3>Generate QR Code</h3>
        <form action="/generate" method="post">
            <input type="text" name="link" placeholder="Enter link">
            <input type="submit" value="Generate QR Code">
        </form>
        <br>
        <h3>Decode QR Code</h3>
        <form action="/decode" method="post" enctype="multipart/form-data">
            <input type="file" name="qr_code">
            <input type="submit" value="Decode QR Code">
        </form>
    '''

@app.route('/generate', methods=['POST'])
def generate():
    link = request.form['link']
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=0,
    )
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img = img.convert("RGBA")
    width, height = img.size

    # Add logo to center of QR code
    logo = Image.open("logo.png")
    logo.thumbnail((width/3, height/3))
    logo_width, logo_height = logo.size
    x = int((width - logo_width) / 2)
    y = int((height - logo_height) / 2)
    img.paste(logo, (x, y), mask=logo)

    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

@app.route('/decode', methods=['POST'])
def decode_qr():
    qr_code = request.files['qr_code']
    img = Image.open(qr_code)
    data = decode(img)
    if data:
        return data[0].data.decode('utf-8')
    else:
        return 'No QR code detected'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7080)