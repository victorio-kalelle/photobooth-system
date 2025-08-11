from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def titlepage():
    return render_template('titlepage.html')

@app.route('/login')
def loginpage():
    return render_template('login.html')

@app.route('/signup')
def signuppage():
    return render_template('signup.html')

@app.route('/photobooth')
def photoboothpage():
    return render_template('photobooth.html')

if __name__ == '__main__':
    app.run(debug=True)