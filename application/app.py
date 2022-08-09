from flask import Flask
import socket
from time import sleep
from random import randint

app = Flask(__name__)


def sleep_custom():
    sleep(randint(1, 9))

@app.route('/<test>')
def sayHello(test):
    if test=="t1":
        sleep_custom()
        return {
            "Name": f"{socket.gethostname()}",
            "Test": "Called t1"
        }
    elif test=="t2":
        sleep_custom()
        return {
            "Name": f"{socket.gethostname()}",
            "Test": "Called t2"
        }
    elif test=="t3":
        sleep_custom()
        return {
            "Name": f"{socket.gethostname()}",
            "Test": "Called t3"
        }
    else:
        sleep_custom()
        return {
            "Name": f"{socket.gethostname()}",
            "Test": "Called Other"
        }
    
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    # app.run(debug=True, port=3000)