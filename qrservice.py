from flask import Flask, request, send_file
from pyzbar.pyzbar import decode
from PIL import Image
import qrcode
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return '''
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
    img = qrcode.make(link)
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
    app.run(host='0.0.0.0')