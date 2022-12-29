from flask import Flask, flash, json, send_file, request, redirect, url_for
from werkzeug.utils import secure_filename
import os, socket

Prod = True
Port = 80
DevPort = 9999
IP = "192.168.0.123"
DevIP = "192.168.0.124"

UPLOAD_FOLDER = 'levels/uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'heic', 'mp4', 'mov', 'webm', 'mpg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
 return '.' in filename and \
 filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(request.url + "s?name=" + filename)

    return open('LevelUploadPage.html')

@app.route("/2")
def root():
 return "<h1>This is the server for the test level select screen!</h1>"


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
  serve(app,host=IP, port=Port)
 else:
  app.run(host=DevIP, port=DevPort, debug=True)
