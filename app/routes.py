from flask import request, render_template, url_for
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
            filename = f'images/image_{datetime.now().strftime("%Y%m%d-%H%M%S.%f")}.jpg'
            fs.save(filename)
            send_alert_email(current_user)
            return f'{{"status": "success", "image": "{filename}"}}'
        fs = request.files.get('video')
        if fs:
            filename = f'videos/video_{datetime.now().strftime("%Y%m%d-%H%M%S.%f")}.mp4'
            fs.save(filename)
            return f'{{"status": "success", "video": "{filename}"}}'
        return '{"status": "error"}'
