from . import app
from flask import render_template, redirect, url_for, send_file
from .forms import Login, Download, You
import os
# from . import moment
from datetime import date



def send():
    return send_file('Khel Tamasha.mp4', as_attachment=True)
@app.route('/')
def index():
    return render_template('Home.html')

@app.route('/download', methods=['GET', 'POST'])
def download():
    var=date(2023,11,12)
    return render_template('test.html', date=var)
