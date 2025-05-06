from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
	return "Hello to the whole world!"
