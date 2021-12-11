import os
from flask import request, render_template, url_for, send_from_directory
from flask_login import current_user, login_required
from datetime import datetime

from app import app
from app.email import send_alert_email

@app.route('/')
@login_required
def index():
    return render_template('camera.html')

@app.route('/client')
@login_required
def client():
    return render_template('client.html')

@app.route('/upload', methods=['POST'])
@login_required
def upload():
    if request.method == 'POST':
        fs = request.files.get('image')
        if fs:
            path = os.path.join(app.config['UPLOADS_PATH'], 'images', current_user.get_id())
            if not os.path.exists(path):
            	os.mkdir(path)
            filename = f'image_{datetime.now().strftime("%Y%m%d-%H%M%S.%f")}.jpg'
            fs.save(os.path.join(path, filename))
            if request.form.get('sendNotifications') == 'true':
                send_alert_email(current_user, 'image', filename)
            return f'{{"status": "success", "image": "{filename}"}}'
        fs = request.files.get('video')
        if fs:
            path = os.path.join(app.config['UPLOADS_PATH'], 'videos', current_user.get_id())
            if not os.path.exists(path):
            	os.mkdir(path)
            filename = f'video_{datetime.now().strftime("%Y%m%d-%H%M%S.%f")}.mp4'
            fs.save(os.path.join(path, filename))
            if request.form.get('sendNotifications') == 'true':
                send_alert_email(current_user, 'video', filename)
            return f'{{"status": "success", "video": "{filename}"}}'
        return '{"status": "error"}'

@app.route('/images/<filename>', methods=['GET'])
@login_required
def image(filename):
    return send_from_directory(os.path.join(app.config['UPLOADS_PATH'], 'images', current_user.get_id()), filename)

@app.route('/videos/<filename>', methods=['GET'])
@login_required
def video(filename):
    return send_from_directory(os.path.join(app.config['UPLOADS_PATH'], 'videos', current_user.get_id()), filename)
