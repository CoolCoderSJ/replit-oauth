from flask import *
from app import *
import requests
from urllib.parse import unquote

@app.route("/login", methods=['GET', 'POST'])
def login():
	if request.method == "GET":
		if "sid" in session.keys():
			return redirect(f"/")

		if "goto" in request.args:
			flags = {
				"goto": flask.request.url.split("goto=")[-1]
			}

		else:
			flags = {
				"goto": "/"
			}
		
		return render_template("login.html", **flags)

	else:
		username = request.form['username']
		password = request.form['password']
		hct = request.form['captchaToken']
		sid = request.form['sid']
		goto = request.form['goto']

		if sid:
			session['sid'] = sid
			return redirect(unquote(goto))

		r = requests.get('https://replit.com/~', allow_redirects=False)
		sid = r.cookies.get_dict()['connect.sid']
		r = requests.post("https://replit.com/login",
			data={
				"username": username,
				"password": password,
				"hCaptchaResponse": hct,
					"hCaptchaSiteKey": "473079ba-e99f-4e25-a635-e9b661c7dd3e",
				"teacher": False
			},
			headers={
				"User-Agent": "Mozilla/5.0",
				'X-Requested-With': "Replit CLI",
					"referrer": "https://replit.com"
			},
			cookies={
				"connect.sid": sid
			}
		)

		if r.status_code is not 200:
			return abort(400)

		session['sid'] = sid
		return redirect(unquote(goto))