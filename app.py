from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello/<name>')
def hello(name):
    return render_template('hello.html', name1=name)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error404.html'), 404