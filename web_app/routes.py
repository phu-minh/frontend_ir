from importlib.resources import path
from wsgiref.util import request_uri
from web_app import app
from flask import render_template, flash, request, redirect, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename
import urllib.request
import sys
import json
import cv2

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index_page():
    return render_template("index.html")

@app.route("/home")
def home_page():
    return render_template("home.html")

@app.route("/upload_image", methods = ['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('no file part')
        file = request.files['file']
        if file.filename == '':
            flash('no selected file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            dirbase = os.path.dirname(os.path.abspath(__file__))
            file.save(os.path.join(dirbase, app.config['UPLOAD_FOLDER'], filename))
            print('file saved at: ', os.path.join(dirbase, app.config['UPLOAD_FOLDER'], filename))
            flash('file uploaded successfully')

            return render_template('home.html',filename=filename)
        else:
            flash('file type not allowed')
            return render_template('home.html')
    else:
        return render_template('home.html')

@app.route('/display_static/<filename>')
def display_image_uploads(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

def paths_return():
    from os import listdir
    from os.path import isfile, join
    mypath = './web_app/static/database'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return onlyfiles

@app.route('/return',methods = ['POST', 'GET'])
def return_file():
    images = paths_return()
    return render_template('return.html',images=images)


@app.route('/display_database/<filename>')
def display_image_database(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='database/' + filename), code=301)

@app.route("/about")
def about_page():
    return render_template('about.html')

@app.errorhandler(500)
def error500(e):
    return render_template('500.html'), 500

#@app.route('/uploads/<name>')
#def download_file(filename):
#    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)