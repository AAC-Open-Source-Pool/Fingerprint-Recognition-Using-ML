from logic import verifyUser , checkSimilarity , load_data, allowed_file
import numpy as np
from flask import Flask, flash, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename

from keras.models import load_model
import cv2
from keras.utils import to_categorical
import os
from skimage.metrics import structural_similarity

import time


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':

        user_id = request.form.get('user_id')

        file = request.files['fingerprint']
        UPLOAD_FOLDER = r'C:\ONE_DRIVE_DATA\Desktop\GRIET\AAC\PROJECT\CODE\SoCofing_Model\Input' 
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        ALLOWED_EXTENSIONS = {'bmp', 'jpg', 'jpeg','png'}

        try:
            # Convert user_id to an integer (or keep it as a string as needed)
            user_id = int(user_id)

            #Download input image into required Directory
            if file and allowed_file(file.filename):
                # filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'InputImage.'+ file.filename.rsplit('.', 1)[1].lower()))

            s = verifyUser(user_id)

            if s == "Access Granted":
                # return redirect(url_for('success'))
                return render_template('sucess.html')
            else:
                # return redirect(url_for('denied'))
                return render_template("denied.html")
            # time.sleep(3)
            #return redirect(url_for('index'))

        except ValueError:
            # return render_template('index.html', message='Invalid User ID. Please enter a numeric value.')
            return render_template('denied.html')
    # print("Get request recieved")
    return render_template('index.html')

# @app.route('/success')
# def success():
#     return render_template('sucess.html')

# @app.route('/denied')
# def denied():
#     return render_template("denied.html")

# @app.route('/index')
# def index():
#     return render_template("index.html")


if __name__ == '__main__':
    # app.run(host = "127.0.0.1",port = '5000',debug=True)
    app.run(debug=True)