import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client [DB_NAME]
app = Flask(__name__)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({}, {'_id': False}))
    return jsonify({'articles': articles})


@app.route("/diary", methods=["POST"])
def save_diary():
    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]

    now = datetime.now()
    time = now.strftime('%Y-%m-%d-%H-%M-%S')

    file = request.files["file_give"]
    extension = file.filename.split('.')[-1]
    filename = f'static/post-{time}.{extension}'
    file.save(filename)

    profile = request.files['profile_give']
    extension = profile.filename.split('.')[-1]
    profilename = f'static/profile-{time}.{extension}'
    profile.save(profilename)

    doc = {
        'file': filename,
        'profile': profilename,
        'title': title_receive,
        'content': content_receive,
        'time': now.strftime('%Y-%m-%d')
    }
    db.diary.insert_one(doc)
    return jsonify({'msg': 'data saved.'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
