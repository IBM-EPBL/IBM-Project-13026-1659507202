import collections
import email
import json
from flask import request, jsonify, session, redirect, render_template
from Application.database import db
from passlib.hash import pbkdf2_sha256
import uuid

class User():

    def start_session(self, userCreds):
        del userCreds['password']
        session['logged_in'] = True
        session['user'] = userCreds

        return "Session Created!"

    def signup(self):
        
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "role": request.form.get('role'),
            "password": request.form.get('password'),
        }
        re_pass = request.form.get('retyped-password')

        if user['password'] == re_pass:

            user['password'] = pbkdf2_sha256.encrypt(user['password'])

            collection = db['users']
            if collection.find_one({ "email": user['email'] }):
                return "User already exists!"
            if collection.find_one({ "name": user['name'] }):
                return "UserName already taken, try different name!"
            if collection.insert_one(user):
                return "Successfully Registered! Login to go to Dashboard!"

            return "Error : Something went wrong"

        else:
            return "Password mismatch!"


    def login(self):
        mailentered = request.form.get('email')

        user = db['users'].find_one({ "email": mailentered })

        if user != None:
            userCreds = db['users'].find_one({ "email" : user['email'] })
            return self.start_session(userCreds)
        
        return "User Doesn't Exist"

    def signout(self):
        session.clear()

        return redirect('/login')

    def deleteAccount(self):
        credentials = request.json
        collection = db['users']

        if collection.find_one({ "email" : credentials['email'] }):
            collection.delete_one({ "email" : credentials['email'] })
            return "The Account has been deleted successfully!", 200

        return "Account not found!", 400

    def addQuery(self):
        collection = db['query_table']

        query = {
            "email" : request.form.get('email'),
            "query_title" : request.form.get('query_title'),
            "query_body" : request.form.get('query_body'),
            "answer" : "",
            "is_answered" : False
        }

        is_raised = collection.find_one({ "query_title" : query['query_title'] })
        if is_raised == None:
            if collection.insert_one(query):
                return "Successfully Raised your Query :)"
            else:
                return "Unable to raise your Query!"

        else:
            return "Query Already raised!"