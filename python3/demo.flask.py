# from http://flask.pocoo.org/ tutorial
from flask import Flask, url_for
app = Flask(__name__)

@app.route("/") # take note of this decorator syntax, it's a common pattern
def index():
    return "Index Page"

@app.route("/hello")
def hello():
	return "Hello Flask!"

@app.route("/user/<username>")
def showuser(username):
	return "userid = %s" % str(username)

'''
following types are supported: int, float, path
'''
@app.route("/post/<int:post_id>")
def showpost(post_id):
	return "post = %d" % post_id

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request_method == 'POST':
		return 'login with POST method'
	else:
		return 'show login info with GET method'

# dump url's
with app.test_request_context():
	print (url_for('index'))
	print (url_for('hello'))
	print (url_for('showuser', username='username'))

if __name__ == "__main__":
	#app.debug = True # toggle debug mode, app.run(debug=True) will also do
    app.run() # listen on loop, 127.x.x.x
	#app.run(host='0.0.0.0') # listen on 0.0.0.0

'''
Deployment:
 * apache: mod_wsgi: apt install libapache2-mod-wsgi
   you need a file *.wsgi under e.g. /var/www/yourapp/

   ```python
   from yourapplication import app as application
   ```

   then configure apache2

   ```apache2
<VirtualHost *>
    ServerName example.com

    WSGIDaemonProcess yourapplication user=user1 group=group1 threads=5
    WSGIScriptAlias / /var/www/yourapplication/yourapplication.wsgi
    #WSGIScriptReloading On

    <Directory /var/www/yourapplication>
        WSGIProcessGroup yourapplication
        WSGIApplicationGroup %{GLOBAL}
        Order deny,allow
        Allow from all
    </Directory>
</VirtualHost>
   ```

'''
