import random, csv, hashlib, sqlite3
from flask import Flask, render_template, request,redirect,url_for,session
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.secret_key = 'password'
socketio = SocketIO(app)

DB_NAME = 'users.db'

@app.route("/jacobo")
def js():
    return "url :" + url_for('sort')

@app.route("/")
def pagetwo():
    print("\n\n\n")
    print(":::DIAG::: this flask obj")
    print(app)
    print(":::DIAG::: this request object obj")
    print(request)
    print(":::DIAG::: this request.args object obj")
    #print request.args["username"]
    if('username' in session):
        session.pop('username')
    return render_template("login.html")

@app.route("/sessionspage", methods=['POST','GET'])
def sessions_page():
    print("\n\n\n")
    print("testing sessoins")
    return render_template("sessions.html")


def checkexist_password(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("SELECT password FROM users where username = '" + username + "'")
    password = ""
    count = 0
    for row in cursor:
        password = row[0]
        count+=1
    if(count != 0):
        return (True, password)
    else:
        return(False, password)
    conn.close()
    
def create_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("INSERT into users(username, password) VALUES('" + username + "', '" + password + "')")
    conn.commit()
    if(conn.total_changes > 0):
        print(conn.total_changes)
        return (True, "successful!")
    else:
        return (False, "db error")
    conn.close()

    
    
@app.route("/sort", methods=['POST','GET'])
def sort():
    username = request.form["username"]
    password = request.form["password"]
    if (request.form["go"] == "login"):
        result = checkexist_password(username)
        if(result[0]):
            hashedpw = password
            print(result)
            if(result[1] == hashedpw):
                session["username"] = username 
                return redirect(url_for('home'))
            else:
                return render_template("login.html",displaymessage = "Incorrect password")
                
        else:
            return render_template("login.html",displaymessage = "That username doesnt exist")
    else:
        if(checkexist_password(username)[0]):
            return render_template("login.html",displaymessage = "That username already exists")
        else:
            hashedpw = password
            result = create_user(username,hashedpw)
            print(result)
            if(result[0]):
                return render_template("login.html",displaymessage = "Account successfully created")
            else:
                return render_template("login.html",displaymessage = result[1])
        
    
@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
    send(message, broadcast=True)
    
@socketio.on('connect')
def connect_handler():
    send(session["username"] + " has connected!", broadcast=True)


@app.route("/home", methods=['POST','GET'])
def home():
    if ("username" in session):
        return render_template('welcome.html', username = session["username"])
    else:
        return redirect('/')


if __name__=="__main__":
    socketio.run(app, debug=True)

