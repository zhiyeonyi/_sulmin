from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.sulmin


@app.route('/')
def main():
    alcohols = list(db.alcohols.find({}, {'_id': False}))
    return render_template("index.html", alcohols=alcohols)


@app.route('/detail')
def detail():
    name_receive = request.args.get('name_give')
    alcohol = db.alcohols.find_one({"name": name_receive}, {"_id": False})
    return render_template("detail.html", alcohol=alcohol)


@app.route('/join', methods=['POST'])
def join():
    name_receive = request.form['name_give']
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    doc = {
        'name': name_receive,
        'id': id_receive,
        'pw': pw_receive
    }
    db.users.insert_one(doc)
    return redirect(url_for('login', msg='회원가입 성공'))


@app.route('/login', methods=['GET'])
def login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    user = db.users.find_one({"id": id_receive, 'pw': pw_receive})
    if user:
        return jsonify({'result': 'success', 'msg': '로그인 성공'})
    return jsonify({'result': 'fail', 'msg': '로그인 실패'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
