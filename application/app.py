from flask import Flask
import socket

app = Flask(__name__)

@app.route('/')
def sayHello():
    return f"Name: {socket.gethostname()}"
    # return "Hello world!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)