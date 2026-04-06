from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")



@app.route('/hola')
def hola():
    return '<h1>HOLA!</h1>'