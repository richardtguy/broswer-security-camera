from flask import Flask, request, render_template
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('motion-detect.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        fs = request.files.get('image')
        if fs:
            filename = f'images/image_{datetime.now().strftime("%Y%m%d-%H%M%S.%f")}.jpg'
            fs.save(filename)
            return f'{{"status": "success", "image": "{filename}"}}'
        fs = request.files.get('video')
        if fs:
            filename = f'videos/video_{datetime.now().strftime("%Y%m%d-%H%M%S.%f")}.mp4'
            fs.save(filename)
            return f'{{"status": "success", "video": "{filename}"}}'
        return '{"status": "error"}'
