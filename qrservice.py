from flask import Flask, request, send_file
from pyzbar.pyzbar import decode
from PIL import Image
import qrcode
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return '''
        <!DOCTYPE html>
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
                    font-size: 24px;
                }
                h3 {
                    margin-left: 20px;
                }
                form {
                    margin-left: 20px;
                }
                input[type=text], input[type=file] {
                    width: 100%;
                    max-width: 400px;
                    box-sizing: border-box;
                    padding: 12px 20px;
                    margin: 8px 0;
                    display: inline-block;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                }
                input[type=submit] {
                    width: 100%;
                    max-width: 400px;
                    background-color: #4CAF50;
                    color: white;
                    padding: 14px 20px;
                    margin: 8px 0;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                }
                input[type=submit]:hover {
                    background-color: #45a049;
                }
                p {
                  margin-left: 20px;
                  margin-right: 20px;
                }
                form {
                  margin-right: 20px;
                }
                @media only screen and (max-width: 600px) {
                  input[type=submit] {
                      padding-top: 20px;
                      padding-bottom: 20px;
                  }
                }
            </style>
        </head>
        <body>
            <h1>A Simple QR Code Generator and Decoder</h1>
            <h3>Generate QR Code</h3>
            <p>To generate a QR code, enter a link in the text field and (optionally) upload a logo.</p> 
            <p>Then click the "Generate QR Code" button. The generated QR code will be displayed on the screen.</p>
            <form action="/generate" method="post" enctype="multipart/form-data">
                <input type="text" name="link" placeholder="Enter link"><br>
                <label for="logo">Choose a PNG Logo File:</label><br>
                <input type="file" id="logo" name="logo" accept="image/*"><br>
                <input type="submit" value="Generate QR Code">
            </form>
            <br>
            <h3>Decode QR Code</h3>
            <p>To decode a QR code, upload an image of the QR code and click the "Decode QR Code" button.</p>
            <p>The decoded data will be displayed on the screen.</p>
            <form action="/decode" method="post" enctype="multipart/form-data">
                <input type="file" name="qr_code" accept="image/*"><br>
                <input type="submit" value="Decode QR Code"><br>
            </form>
        </body>
        </html>
    '''

@app.route('/generate', methods=['POST'])
def generate():
    link = request.form['link']
    logo = request.files.get('logo')
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
    logo_img = Image.open(logo) if logo else Image.open('logo.png')
    logo_img.thumbnail((width/3, height/3))
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