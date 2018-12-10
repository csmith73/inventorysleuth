from flask import Flask, render_template, request, redirect, jsonify, session, abort, flash
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('comingsoon.html')

if __name__ == "__main__":
    #app.run()
    app.run(host='0.0.0.0')
