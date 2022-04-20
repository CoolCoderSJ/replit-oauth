from flask import *
from app import *
from random import choice
import time

applications = S1(os.environ['DB'])
tokens = S1(os.environ['DB2'])
authcodes = S1(os.environ['DB3'])

@app.route("/token", methods=['POST'])
def token():
	if request.method == "POST":
		form = request.get_json(force=True)
		
		code = form['code']
		scopes = form['scopes']
		clientid = form['clientid']
		clientsecret = form['clientsecret']
		redirect_uri = form['redirect_uri']

		code = authcodes.get(code)

		if time.time() - code['time'] > 6000:
			authcodes.delete(form['code'])
			return Response("Code has expired.", status=400)

		if clientsecret != applications.get(str(clientid))['clientSecret']:
			return Response("Invalid secret", status=401)

		scopesSimplified = []

		if " " in scopes:
			scopes = scopes.split(" ")
		else:
			scopes = scopes.split("+")
			
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


		if scopesSimplified != code['scopes']:
			return Response("Scopes do not match.", status=400)

		if redirect_uri not in applications.get(str(clientid))['redirectUris']:
			return Response("Invalid redirect uri.", status=400)

		chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

		token = ""
		for i in range(100):
			token += choice(chars)

		while token in tokens.get_keys():
			token = ""
			for i in range(100):
				token += choice(chars)
		
		tokens.set(token, {
			"clientid": clientid,
			"scopes": scopesSimplified,
			"sid": code['sid']
		})

		print("all tokens", tokens.get_keys())

		authcodes.delete(form['code'])

		return token