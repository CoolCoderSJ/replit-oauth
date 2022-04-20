from flask import *
from app import *
import requests
from random import choice

applications = S1(os.environ['DB'])
tokens = S1(os.environ['DB2'])
authcodes = S1(os.environ['DB3'])


@app.route("/", methods=['GET', 'POST'])
def index_route():
	if request.method == "GET":
		if "sid" not in session.keys():
			return redirect("/login")
			
		sid = session['sid']
	
		json_data = {
			'query': 'query current {currentUser {id}}',
		}
	
		headers = {
			'X-Requested-With':'replit',
			'Origin':'https://replit.com',
			'Accept':'application/json',
			'Referrer':'https://replit.com/jdog787',
			'Content-Type':'application/json',
			'Connection':'keep-alive',
			'Host': "replit.com",
			"x-requested-with": "XMLHttpRequest",
			"User-Agent": "Mozilla/5.0",
			"Cookie": f"connect.sid={sid};"
		}
	
		
		r = requests.post('https://replit.com/graphql', headers=headers, json=json_data)
		id = r.json()['data']['currentUser']['id']
	
		userApps = []
		for application in applications.get_keys():
			if applications.get(application)['id'] == id:
				app = applications.get(application)
				redirectUris = ""
				for uri in app['redirectUris']:
					redirectUris += uri+","
				app['redirectUris'] = redirectUris
				userApps.append([app, application])
	
		tokensUsed = []
	
		for token in tokens.get_keys():
			if tokens.get(token)['sid'] == sid:
				scopeDict = {}
				for scope in tokens.get(token)['scopes']:
					if scope == "user:recentrepls":
						scopeDict['user:recentrepls'] = "View all of your recent repls"
			
					if scope == "user:notifications":
						scopeDict['user:notifications'] = "View all of your notifications"
			
					if scope == "user:id":
						scopeDict['user:id'] = "Get your user id"
			
					if scope == "user:username":
						scopeDict['user:username'] = "Get your username"
			
					if scope == "user:name":
						scopeDict['user:name'] = "Get your full name"
			
					if scope == "user:bio":
						scopeDict['user:bio'] = "Get your user bio"
			
					if scope == "user:isVerified":
						scopeDict['user:isVerified'] = "Check if your email is verified"
		
					if scope == "user:timeCreated":
						scopeDict['user:timeCreated'] = "Check the time your account was created at"
			
					if scope == 'user:repls':
						scopeDict['user:repls'] = "Get all of your repls"
			
					if scope == "user:languages":
						scopeDict['user:languages'] = "Get all of your used langauges"
			
					if scope == "user:markNotificationsAsRead":
						scopeDict['user:markNotificationsAsRead'] = "Mark all of your notifications as read"
			
					if scope == "repl:update":
						scopeDict['repl:update'] = "Update a repl"
			
					if scope == "repl:delete":
						scopeDict['repl:delete'] = "Delete a repl"
			
					if scope == "repl:boost":
						scopeDict['repl:boost'] = "Boost a repl"
			
					if scope == "repl:unboost":
						scopeDict['repl:unboost'] = "Remove a boost from a repl"
			
					if scope == "repl:create":
						scopeDict['repl:create'] = "Create a repl on your account"
			
					if scope == "repl:publish":
						scopeDict['repl:publish'] = "Publish a repl"
			
					if scope == "repl:unpublish":
						scopeDict['repl:unpublish'] = "Unpublish a repl"
				
				tokensUsed.append([applications.get(str(tokens.get(token)['clientid'])), tokens.get(token), scopeDict, token])
	
		flags = {
			"apps": userApps,
			"tokens": tokensUsed
		}
		return render_template('index.html', **flags)
	else:
		form = request.form
		sid = session['sid']
	
		json_data = {
			'query': 'query current {currentUser {id}}',
		}
	
		headers = {
			'X-Requested-With':'replit',
			'Origin':'https://replit.com',
			'Accept':'application/json',
			'Referrer':'https://replit.com/jdog787',
			'Content-Type':'application/json',
			'Connection':'keep-alive',
			'Host': "replit.com",
			"x-requested-with": "XMLHttpRequest",
			"User-Agent": "Mozilla/5.0",
			"Cookie": f"connect.sid={sid};"
		}
	
		
		r = requests.post('https://replit.com/graphql', headers=headers, json=json_data)
		id = r.json()['data']['currentUser']['id']

		chars = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

		clientid = ""

		for i in range(15):
			clientid += str(choice(chars))

		chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

		clientSecret = ""

		for i in range(25):
			clientSecret += choice(chars)

		applications.set(clientid, {
			"name": form['name'],
			"redirectUris": form['redirectUris'].replace(" ", "").split(","),
			"clientSecret": clientSecret,
			"id": id
		})

		return redirect("https://replit-oauth.coolcodersj.repl.co/")