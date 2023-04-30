import qrcode
data = 'https://www.example.com'
img = qrcode.make(data)
img.save('MyQRCode.png')