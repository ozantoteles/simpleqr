from flask import Flask, request, send_file
import qrcode
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return '''
        <form action="/generate" method="post">
            <input type="text" name="link" placeholder="Enter link">
            <input type="submit" value="Generate QR Code">
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

if __name__ == '__main__':
    app.run(host='0.0.0.0')