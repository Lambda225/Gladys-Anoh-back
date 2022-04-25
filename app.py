from blueprints import app,user
from flask import redirect,url_for

@app.route('/')
def Acceuil():
    return redirect(url_for('user.home'))

if __name__ == '__main__':
    app.run(debug=True)
