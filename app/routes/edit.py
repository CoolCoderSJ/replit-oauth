from flask import *
from app import *
from random import choice
import time, requests

applications = S1(os.environ['DB'])
tokens = S1(os.environ['DB2'])
authcodes = S1(os.environ['DB3'])


@app.route("/edit", methods=['POST'])
def edit():
	if request.method == "POST":
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

		if applications.get(form['clientid'])['id'] != id:
			return abort(403)

		applications.set(form['clientid'], {
			"name": form['name'],
			"redirectUris": form['redirectUris'].replace(" ", "").split(","),
			"clientSecret": form['secret'],
			"id": id
		})

		return redirect("https://replit-oauth.coolcodersj.repl.co/")