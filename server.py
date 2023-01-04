import socket
import os
from PIL import Image
from waitress import serve
from werkzeug.utils import secure_filename
from flask import Flask, flash, json, send_file, request, redirect, url_for
from contextlib import nullcontext

Prod = True
Port = 80
DevPort = 80
Ip = '192.168.0.123'
DevIP = '192.168.0.124'

COVER_FOLDER = 'levels/cover/'
ICON_FOLDER = 'levels/icon/'
DATA_FOLDER = 'levels/data/'
INFO_FOLDER = 'levels/info/'
USERS_FOLDER = 'levels/users/'
OWNS_FOLDER = 'levels/owns/'
OWNERS_FOLDER = 'levels/owners/'
ALLOWED_EXTENSIONS = {'png', 'json'}

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        users = os.listdir(OWNERS_FOLDER)
        largest = 0
        for x in users:
            x = x.split('.')[0]
            if int(x) > largest:
                largest = int(x)
        id = str(largest + 1)  # generate next free ID
        cover = request.files['cover']
        if cover.filename == '':
            cover = open('DefaultCover.png')
        data = request.files['data']
        info = request.files['info']
        username = str(request.form.get('username'))
        password = str(request.form.get('password'))

        # Check if the user exists
        users = os.listdir(USERS_FOLDER)
        found = False
        for x in users:
            if x == username + '.txt':
                found = True
        if not found:
            return "err000 User not found: \"" + username + "\""  # err000

        MissingData = 'data' not in request.files or 'cover' not in request.files or 'info' not in request.files
        MissingFiles = cover.filename == '' or data.filename == '' or info.filename == '' or username == '' or password == ''
        InvalidFileType = not allowed_file(cover.filename) or not allowed_file(
            data.filename) or not allowed_file(info.filename)
        InvalidLogin = open(os.path.join(
            USERS_FOLDER, username + ".txt")).read() != password
        if MissingData:
            return "err001 Misscommunication"  # err001
        if MissingFiles:
            return "err002 Missing Files"  # err002
        if InvalidFileType:
            return "err003 invalid file type"  # err003
        if InvalidLogin:
            return "err004 incorrect password for user \"" + username + "\""  # err004
        if MissingData or MissingFiles or InvalidFileType or InvalidLogin:
            return open('error.html')
        else:
            imagePath = COVER_FOLDER + id + '.' + cover.filename.split('.')[1]
            cover.save(imagePath)
            info.save(os.path.join(INFO_FOLDER, id +
                      '.' + info.filename.split('.')[1]))
            data.save(os.path.join(DATA_FOLDER, id +
                      '.' + data.filename.split('.')[1]))
            owner = open(os.path.join(OWNERS_FOLDER, id + '.txt'),
                         'x')  # store account information
            owner.write(username)
            # Compress cover as a jpeg file
            img = Image.open(imagePath).convert('RGB')
            img = img.resize((320, 320))
            img.save(os.path.join(ICON_FOLDER, id + ".jpeg"))
            user = open(os.path.join(OWNS_FOLDER, str(username)) + '.txt', 'a')
            user.write(id + "\n")
            return open('Success.html')
    return open('LevelUploadPage.html')


@app.route("/")
def root():
    return open("index.html")


@app.route("/assets")
def assets():
    return send_file(os.path.join("levels", "assets.zip"))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = open(os.path.join(USERS_FOLDER, str(username)) + '.txt', 'x')
        user.write(str(password))
        user = open(os.path.join(OWNS_FOLDER, str(username)) + '.txt', 'x')
        return open('Success.html')
    return open('register.html')


@app.route("/change_password", methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        username = request.form.get('username')
        oldPassowrd = request.form.get('old')
        newPassowrd = request.form.get('new')
        # Check if the user exists
        users = os.listdir(USERS_FOLDER)
        found = False
        for x in users:
            if x == username + '.txt':
                found = True
        if not found:
            return "err000 User not found: \"" + username + "\""  # err000
        ValidLogin = open(os.path.join(
            USERS_FOLDER, username + ".txt")).read() == oldPassowrd
        if not ValidLogin:
            return "err004 incorrect password for user \"" + username + "\""  # err004
        if ValidLogin:
            os.remove(os.path.join(USERS_FOLDER, username + ".txt"))
            user = open(os.path.join(
                USERS_FOLDER, str(username)) + '.txt', 'x')
            user.write(str(newPassowrd))
            return open('Success.html')
    return open('change_password.html')


@app.route("/delete_user", methods=['GET', 'POST'])
def deleteUser():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Check if the user exists
        users = os.listdir(USERS_FOLDER)
        found = False

        # Check for user
        for x in users:
            if x == username + '.txt':
                found = True
        if not found:
            return "err000 User not found: \"" + username + "\""  # err000

        # Check password
        ValidLogin = open(os.path.join(
            USERS_FOLDER, username + ".txt")).read() == password
        if not ValidLogin:
            return "err004 incorrect password for user \"" + username + "\""  # err004

        # delete data
        if ValidLogin:
            os.remove(os.path.join(USERS_FOLDER, username + ".txt"))
            return open('Success.html')
    return open("delete_user.html")


@ app.route("/favicon.ico")
def favicon():
    fav = open("favicon.ico")
    return send_file("favicon.ico", mimetype='image/ico')


@app.route("/owns")
def owns():
    filename = request.args.get('usr') + ".txt"
    return send_file(OWNS_FOLDER + filename)


@app.route("/owner")
def owner():
    filename = request.args.get('id') + ".txt"
    # return 0
    return send_file(OWNERS_FOLDER + filename)


@app.route("/users")
def users():
    return str(os.listdir(USERS_FOLDER)).replace(".txt", "")


# @app.route("/user")
# def user2():
#     return user()


@app.route("/user")
def uses():
    username = request.args.get('usr')
    return str(username)
    # ADD MORE INFO


@ app.route("/cover", methods=['GET', 'POST'])
def cover():
    filename = request.args.get('id') + ".png"
    return send_file(COVER_FOLDER+filename, mimetype='image/png')


@ app.route("/icon", methods=['GET', 'POST'])
def icon():
    filename = request.args.get('id') + ".jpeg"
    return send_file('levels/icon/' + filename, mimetype='image/jpeg')


@ app.route("/uploads", methods=['GET', 'POST'])
def uploads():
    filename = request.args.get('name')
    return send_file('levels/uploads/' + filename)


@ app.route("/info", methods=['GET', 'POST'])
def info():
    filename = request.args.get('id') + ".json"
    return send_file("levels/info/" + filename)

@ app.route("/data")
def data:
    filename = request.args.get('id') + .json
    return send_file("levels/data/" + filename)

if __name__ == '__main__':
    if Prod:
        serve(app, host=Ip, port=Port)
    else:
        app.run(host=DevIP, port=DevPort, debug=True)
