from flask import *
from app import *
from random import choice
import time, json

applications = S1(os.environ['DB'])
tokens = S1(os.environ['DB2'])
authcodes = S1(os.environ['DB3'])

@app.route("/authorize", methods=['GET', 'POST'])
def authorize():
	if request.method == "GET":
		if "sid" not in session.keys():
			return redirect(f"/login?goto={flask.request.url}")
			
		scopes = [
			"user",
			"user:recentrepls",
			"user:notifications",
			"user:id",
			"user:username",
			"user:name",
			"user:bio",
			"user:isVerified",
			"user:timeCreated",
			"user:repls",
			"user:languages",
			"user:markNotificationsAsRead",
	
			"repl",
			"repl:update",
			"repl:delete",
			"repl:boost",
			"repl:unboost",
			"repl:create",
			"repl:publish",
			"repl:unpublish",
		]
	
		args = request.args
	
		if not 'response-type' in args:
			return "No response type provided"
		if args['response-type'] != "code":
			return "Invalid response type"
	
		if not 'scopes' in args:
			return "No scopes provided"
	
		if " " in args['scopes']:
			scopes = args['scopes'].split(" ")
		else:
			scopes = args['scopes'].split("+")
	
		if "redirect-uri" not in args:
			return "No redirect uri provided"
	
		redirectUri = args['redirect-uri']
		
		if "clientid" not in args:
			return "No client ID provided"
	
		clientId = args['clientid']

		if clientId not in applications.get_keys():
			return "Invalid client ID"

		if redirectUri not in applications.get(clientId)['redirectUris']:
			return "Invalid redirect URI"

		scopesSimplified = []
		scopeDict = {}
		
		for scope in scopes:
			if scope == "user":
				for i in ["user:recentrepls","user:notifications","user:id","user:username","user:name","user:bio","user:isVerified","user:timeCreated","user:repls","user:languages","user:markNotificationsAsRead"]:
					if i not in scopesSimplified:
						scopesSimplified.append(i)
	
			elif scope == "repl":
				for i in ["repl:update","repl:delete","repl:boost","repl:unboost","repl:create","repl:publish","repl:unpublish",]:
					if i not in scopesSimplified:
						scopesSimplified.append(i)
	
			else:
				if scope not in scopesSimplified:
					scopesSimplified.append(scope)
		
		for scope in scopesSimplified:
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
		
		flags = {
			"scopes": scopeDict,
			"redirectUri": redirectUri,
			"clientId": clientId,
			"name": applications.get(clientId)['name']
		}
		
		return render_template("authorize.html", **flags)
	else:
		clientId = request.form['clientId']
		redirectUri = request.form['redirectUri']
		scopes = request.form['scopes']
		
		chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

		if clientId not in applications.get_keys():
			return "Invalid client ID"

		if redirectUri not in applications.get(clientId)['redirectUris']:
			return "Invalid redirect URI"

		if not "sid" in session.keys():
			return abort(401)

		code = ""
		for i in range(100):
			code += choice(chars)

		while code in authcodes.get_keys():
			code = ""
			for i in range(100):
				code += choice(chars)

		print(scopes.replace("'", '"'))
		authcodes.set(code, {
			"clientId": int(clientId),
			"time": time.time(),
			"scopes": list(json.loads(scopes.replace("'", '"')).keys()),
			"sid": session['sid']
		})

		if "?" in redirectUri:
			end = "&code="+code
		else:
			end = "?code="+code
			
		return redirect(f"{redirectUri}{end}")