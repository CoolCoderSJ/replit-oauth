from flask import *
from app import *
from random import choice
import time, requests

applications = S1(os.environ['DB'])
tokens = S1(os.environ['DB2'])
authcodes = S1(os.environ['DB3'])


@app.route("/revoke", methods=['POST'])
def revoke():
	if request.method == "POST":
		token = request.form['token']

		if tokens.get(token)['sid'] != session['sid']:
			return abort(403)

		tokens.delete(token)

		return redirect("https://replit-oauth.coolcodersj.repl.co/")