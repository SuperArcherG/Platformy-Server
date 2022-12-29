from flask import Flask, flash, json, send_file, request, redirect, url_for
from werkzeug.utils import secure_filename
import os, socket

Prod = False
Port = 80
DevPort = 9999
Ip = '192.168.0.123'
DevIP = '192.168.0.124'

COVER_FOLDER = 'levels/cover/'
ICON_FOLDER = 'levels/icon/'
DATA_FOLDER = 'levels/data/'
INFO_FOLDER = 'levels/info/'
USERS_FOLDER = 'levels/users/'
ALLOWED_EXTENSIONS = {'png', 'json'}

app = Flask(__name__)

def allowed_file(filename):
 return '.' in filename and \
 filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        id = "11" # generate next free ID
        cover = request.files['cover']
        if cover.filename == '':
            cover = open('DefaultCover.png')
        data = request.files['data']
        info = request.files['info']
        username = str(request.form.get('username'))
        password = str(request.form.get('password'))

        invalidSearch1 = 'data' not in request.files or 'cover' not in request.files or 'info' not in request.files
        invalidSearch2 = cover.filename == '' or data.filename == '' or info.filename == '' or username == '' or password == ''
        invalidSearch3 = not allowed_file(cover.filename) or not allowed_file(data.filename) or not allowed_file(info.filename)
        invalidSearch4 = open(os.path.join(USERS_FOLDER, username+ ".txt")).read() != password
        print(invalidSearch1)
        print(invalidSearch2)
        print(invalidSearch3)
        print(invalidSearch4)
        if invalidSearch1 or invalidSearch2 or invalidSearch3 or invalidSearch4:
            return open('error.html')
        else:
            cover.save(os.path.join(COVER_FOLDER, id + '.' + cover.filename.split('.')[1]))
            info.save(os.path.join(INFO_FOLDER, id + '.' + info.filename.split('.')[1]))
            data.save(os.path.join(DATA_FOLDER, id + '.' + data.filename.split('.')[1]))
            #store account information
            return open('Success.html')
    return open('LevelUploadPage.html')

@app.route("/")
def root():
 return "<h1>Thank you for your help testing!</h1>"

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = open(os.path.join(USERS_FOLDER, str(username)) + '.txt', 'x')
        user.write(str(password))
        return open('Success.html')
    return open('register.html')

@app.route("/favicon.ico")
def favicon():
 fav = open("favicon.ico")
 return send_file("favicon.ico", mimetype='image/ico')


@app.route("/cover", methods=['GET','POST'])
def cover():
 filename = request.args.get('id') + ".png"
 return send_file('levels/cover/'+filename, mimetype='image/png')

@app.route("/icon", methods=['GET','POST'])
def icon():
 filename = request.args.get('id') + ".jpeg"
 return send_file('levels/icon/' + filename, mimetype='image/jpeg')

@app.route("/uploads", methods=['GET','POST'])
def uploads():
 filename = request.args.get('name')
 return send_file('levels/uploads/' + filename)

@app.route("/info", methods=['GET','POST'])
def info():
 filename = request.args.get('id') + ".json"
 return send_file("levels/info/" + filename)


if __name__ == '__main__':
 if Prod:
  from waitress import serve
  serve(app,host=Ip, port=Port)
 else:
  app.run(host=DevIP, port=DevPort, debug=True)
