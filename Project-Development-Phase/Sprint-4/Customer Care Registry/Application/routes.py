# from crypt import methods
from flask import request, jsonify, render_template, session, redirect, url_for
from functools import wraps
from Application import app
from Application.models import User
from Application.database import db


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/login')

    return wrap

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/dashboard/<userid>')
@login_required
def dashboard(userid):
    logger = db['users'].find_one({ "email": userid })
    if logger['role'] == 'agent':

        collection = db['query_table']
        queries = []
        for query in collection.find({}):
            queries.append(query)
            
        return render_template('admindashboard.html', queries = queries)
    else:
        return render_template('dashboard.html')

@app.route('/signup', methods=['GET','POST'])
def CreateUser():
    if request.method == 'POST':
        res = User().signup()
        if res == "Successfully Registered! Login to go to Dashboard!":
            return render_template('signup.html', msg = res)
        else:
            return render_template('signup.html', msg = res)

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        res = User().login()
        if res != "User Doesn't Exist":
            logger = db['users'].find_one({ "email": request.form.get('email') })
            if logger['role'] == 'agent':

                collection = db['query_table']
                queries = []
                for query in collection.find({}):
                    queries.append(query)
                    
                return render_template('admindashboard.html', msg = res, queries = queries)
            else:
                return render_template('dashboard.html', msg = res)
        else:
            return render_template('login.html', msg = res)

    return render_template('login.html')

@app.route('/listUsers', methods=['GET'])
@login_required
def listUsers():
    usersList = []
    
    collection = db['users']
    for user in collection.find({}):
        usersList.append(user)

    return render_template('listusers.html', res = usersList)

@app.route('/signout')
def signout():
    return User().signout()

@app.route('/deleteAccount', methods=['DELETE'])
def deleteAccount():
    return User().deleteAccount()

@app.route('/add_query', methods=['POST'])
def addQuery():
    res = User().addQuery()
    return render_template('dashboard.html', msg = res)


@app.route('/answer_query/<email>/<query_title>', methods=['GET', 'POST'])
def answerQuery(email, query_title):
    if request.method == 'POST':
        answer = request.form.get('answer')
        collection = db['query_table']

        queryRecord = collection.find_one({ "email" : email, "query_title" : query_title })
        is_ans = queryRecord['is_answered']

        ans = queryRecord['answer']
        if not is_ans:
            collection.find_one_and_update({ "email" : email, "query_title" : query_title } ,{ "$set" : { "email" : email, "query_title" : query_title, "answer" : answer, "is_answered" : True }}, upsert=True)
            msg = "Your answer has been saved :)"
        else:
            msg = "It has already been answered :("
            
        return render_template('answered.html', msg=msg, answer=ans)

    return '<h1>It has not updated!</h1>'


@app.route('/topQueries')
def topQueries():
    collection = db['query_table']

    queries = []
    for query in collection.find({}):
        queries.append(query)

    return render_template('topqueries.html', queries=queries)


@app.route('/myqueries/<id>')
@login_required
def myqueries(id):
    collection = db['query_table']

    myqueries = []
    for query in collection.find({ "email" : id }):
        myqueries.append(query)

    return render_template('myqueries.html', myqueries=myqueries)