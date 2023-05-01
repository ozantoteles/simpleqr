from flask import Flask, request, send_file
from pyzbar.pyzbar import decode
from PIL import Image
import qrcode
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    with open('qrservice.html', 'r') as f:
        html_content = f.read()
    return html_content

@app.route('/generate', methods=['POST'])
def generate():
    link = request.form['link']
    logo = request.files.get('logo')
    add_logo = request.form.get('add_logo')
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=1,
    )
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
    width, height = img.size
    if add_logo:
        logo_img = Image.open(logo) if logo else Image.open('logo.png')
        logo_img = logo_img.convert('RGBA')
        logo_img.thumbnail((width/3.2, height/3.2))
        logo_width, logo_height = logo_img.size
        x, y = int((width - logo_width) / 2), int((height - logo_height) / 2)
        img.paste(logo_img, (x, y))
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
    app.run(debug=False, host='0.0.0.0', port=7080)