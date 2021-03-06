import HandleUser
import FileHandler
import SessionManager
import ChatHandler
import ChatTrainer
# import JiraHandler
import nltk

from flask import Flask, render_template, request, session, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)
app.debug = True
app.secret_key = "topsecretnonsharablekey"
client = MongoClient('localhost', 27017)
db = client.APP_USERS
db2 = client.CHATAPP
op = None
#nltk.download() # uncomment and run this in the first run

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


@app.route("/chatapp")
def chatappHome():
    return render_template("chathome.html", title='templates')


@app.route("/chatapp/trainingground")
def chatappTrainingHome():
    return render_template("chattrain.html", title='templates')


@app.route("/chatapp/train")
def chatappTraining():
    userText = request.args.get('msg')
    return ChatTrainer.parseUsertext(userText, db2)
    #return ChatHandler.sayHi()


@app.route("/chatapp/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(ChatHandler.parseText(userText))


@app.route("/")
@app.route("/redirect")
def home():
    return render_template("home.html", title='templates', **locals())


@app.route("/redirect/login")
def login():
    return render_template("login.html", title='templates')


@app.route("/redirect/signup")
def signup():
    return render_template("signup.html", title='userpages')


@app.route("/redirect/logout")
def logout():
    if session['userToken'] is not None:
        userToken = str(session['userToken']).split("--")[1]
        username = str(session['userToken']).split("--")[0]
        if userToken is not None and \
            username is not None:
            SessionManager.deleteSession(db, username, userToken)
            errormessage = "Successfully logged out. "
    session.clear()
    return redirect(url_for('.home'))



@app.route("/hello/<string:name>/")
def hello(name):
    vals = HandleName.hellothere(name=name)
    vals['name'] = name
    print("printed something below \n" + vals['quote'] + "----" + vals['xyz'] + "----" + vals['name'])
    #   return render_template('test.html', name=name)
    return render_template('test.html', **locals())


@app.route("/redirect/userregister", methods=['GET', 'POST'])
def userRegister():
    status = HandleUser.userRegistration(db, request)
    print("status is ----", status)
    if status is not None and str(status).lower() == "new":
        errormessage = "User registered"
        return render_template('login.html', title="templates", **locals())
    elif status is not None and str(status).lower() == "existing":
        errormessage = "User already present in DB"
        return render_template('signup.html', title="templates", **locals())
    else:
        errormessage = "Something went wrong. Status ---- " + status
        return render_template('login.html', title="templates", **locals())


@app.route("/redirect/userhome", methods=['GET', 'POST'])
def userhome():
    session.clear()
    authToken = HandleUser.userAuthentication(db, request)
    username = request.form.get('username')
    print("authToken is ", authToken)
    if authToken != 'fail' and username is not None:
        session['userToken'] = str(authToken)
        return render_template('homepage.html', title="functional", **locals())
    elif username is None and authToken == 'fail':
        errormessage = "Please login to view ahead."
        return render_template('login.html', title="functional", **locals())
    elif username is not None and authToken == 'fail':
        errormessage = "Invalid username and password"
        return render_template('login.html', title="functional", **locals())


@app.route("/redirect/type1")
def renderType1():
    isValidSession = None
    isValidSession = SessionManager.checkValidSession(db, session)
    print("validation check is ---- ", isValidSession)
    if isValidSession == "valid":
        return render_template("type1.html", title='functional')
    else:
        errormessage = "Invalid session encountered, please login again."
        return render_template('login.html', title="functional", **locals())


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

