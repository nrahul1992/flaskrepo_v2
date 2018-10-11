import HandleName
import FileHandler

from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
app.debug = True
client = MongoClient('localhost', 27017)
db = client.APP_USERS
op = None


@app.before_first_request
def setupconnection():
    users = db.userlogindata.find()
    data = 'Name of Users:'
    creds = {}
    for user in users:
        data = data + user['username']
        creds = {"username": user['username'], "password": user['password']}
    global op
    op = creds
    return data


@app.route("/")
@app.route("/redirect")
def home():
    return render_template("home.html", title='templates\\userpages')


@app.route("/redirect/login")
def login():
    return render_template("login.html", title='userpages')


@app.route("/redirect/signup")
def signup():
    return render_template("signup.html", title='userpages')


@app.route("/*/params", methods=['GET'])
def dosomething():
    abc = request.args.get('name', None)
    defe = request.args.get('place', None)
    return render_template('test.html', **locals())


@app.route("/hello/<string:name>/")
def hello(name):
    vals = HandleName.hellothere(name=name)
    vals['name'] = name
    print("printed something below \n" + vals['quote'] + "----" + vals['xyz'] + "----" + vals['name'])
    #   return render_template('test.html', name=name)
    return render_template('test.html', **locals())


@app.route("/redirect/userhome", methods=['GET', 'POST'])
def formaction():
    authToken = HandleName.userAuthentication(db, request)
    username = request.form.get('username')
    if authToken == 'pass':
        return render_template('homepage.html', title="functional", **locals())
    else:
        errormessage = "Invalid username and password"
        return render_template('login.html', title="functional", **locals())


@app.route("/redirect/type1")
def renderType1():
    return render_template("type1.html", title='functional')


@app.route("/redirect/type1/handler",  methods=['GET', 'POST'])
def handleType1():
    print("called type1-one source one destination handler")
    entry_number = FileHandler.type1Handler(request)
    print("entry_number ---- ", entry_number)
    if entry_number is not None:
        message = "success"
    else:
        message = "Something is wrong! "
    return render_template("homepage.html", title='functional', **locals())


@app.route("/redirect/type2")
def handleType2():
    return render_template("type2.html", title='functional')


@app.route("/redirect/type3")
def handleType3():
    return render_template("type3.html", title='functional')


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=80)

