from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def titlepage():
    return render_template('titlepage.html')

@app.route('/layout')
def layout_selection():
    return render_template('layout.html')

@app.route('/frame')
def frame_selection():
    return render_template('frame.html')

@app.route('/photobooth')
def photobooth_page():
    return render_template('photobooth.html')

if __name__ == '__main__':
    app.run(debug=True)