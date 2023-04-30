# QR Code Service

This is a simple Flask app that allows users to generate and decode QR codes.

## Installation

To run this app, you'll need to have Flask, qrcode, pyzbar, and Pillow installed. You can install these libraries using pip by running the following commands:

## Usage

Then, run the app using the command python 'qrservice.py'. The app should now be running and accessible at http://localhost:7080.

## Create a Service in Linux

Here’s how you can create a service file to run the Flask app as a service on Ubuntu Linux:

Change the 'qrservice.service' accordingly and copy into the /etc/systemd/system directory with the following content:

Be sure to replace your_username with your own username and /path/to/app with the path to the directory where you saved the qrservice.py file.

Reload the systemd manager configuration by running the following command:

'sudo systemctl daemon-reload'
Start the QR Code Service by running the following command:

'sudo systemctl start qrservice'
To automatically start the service at boot, run the following command:

'sudo systemctl enable qrservice'
After completing these steps, the Flask app should be running as a service on your Ubuntu Linux system and should automatically start at boot.

## License

This project is licensed under the MIT License.
