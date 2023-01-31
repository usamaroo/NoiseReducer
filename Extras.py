from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///audio_files.db'
app.config['UPLOAD_FOLDER'] = '/path/to/audio/files'
db = SQLAlchemy(app)

class AudioFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    date_uploaded = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<AudioFile {self.filename}>'

db.create_all()

@app.route('/upload', methods=['POST'])
def upload_audio_file():
    file = request.files['audio_file']
    filename = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    audio_file = AudioFile(filename=filename, date_uploaded=datetime.now())
    db.session.add(audio_file)
    db.session.commit()

    return f'Audio file {filename} uploaded successfully!'

@app.route('/download/<int:id>')
def download_audio_file(id):
    audio_file = AudioFile.query.get(id)
    return send_from_directory(app.config['UPLOAD_FOLDER'], audio_file.filename)

if __name__ == '__main__':
    app.run()
