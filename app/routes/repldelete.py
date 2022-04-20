from flask import *
from app import *
from random import choice
import time, requests

applications = S1(os.environ['DB'])
tokens = S1(os.environ['DB2'])
authcodes = S1(os.environ['DB3'])


@app.route("/api/v1/me/repldelete", methods=['POST'])
def deleteRepl():
	if request.method == "POST":
		headers = request.headers
		form = request.get_json(force=True)
		if "Authorization" not in headers:
			return abort(401)

		token = headers['Authorization']
		if "Bearer " not in token:
			return abort(401)

		token = token.replace("Bearer ", "")
		print(token)

		if token not in tokens.get_keys():
			return abort(403)

		scopes = tokens.get(token)['scopes']

		if "repl:delete" not in scopes:
			return abort(403)

		sid = tokens.get(token)['sid']

		json_data = {
		    'query': """mutation delRepl ($id: String!) {
 deleteRepl (id: $id) {
  id
}
}""",
		    'variables': {
		        'id': form['id'],
		    },
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
		return r.status_code