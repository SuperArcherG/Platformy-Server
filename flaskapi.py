from flask import Flask, json, send_file, request
import os

companies = [{"id": 1, "name": "Company One"}, {"id": 2, "name": "Company Two"}]

app = Flask(__name__)

@app.route("/")
def hello():
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

@app.route("/info", methods=['GET','POST'])
def info():
 filename = request.args.get('id') + ".json"
 return send_file("levels/info/" + filename)


if __name__ == '__main__':
 app.run(host='localhost', port=80, debug=True)



