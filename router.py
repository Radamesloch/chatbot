from flask import Flask, render_template, request
from chat import get_Chat_response


app = Flask(__name__)

# FLASK ROUTES
@app.route("/")
def index():
    return render_template('chat.html')
@app.route("/get", methods=["GET", "POST"])
def chat():    
    input = request.form["msg"]
    return get_Chat_response(input)

"""INIT FLASK APPLICATION"""
if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5000')