from flask import Flask
import socket
from time import sleep
from random import randint
from data_collector import collect_data

app = Flask(__name__)

@app.route('/')
def tester():
    d = collect_data()
    stats_data = d.hammer()
    return stats_data


@app.route('/custom/<test>')
def sayHello(test):
    d = collect_data()
    stats_data = d.hammer()
    return stats_data
    # if test=="t1":
        
    #     return {
    #         "Name": f"{socket.gethostname()}",
    #         "Test": "Called t1"
    #     }
    # elif test=="t2":
        
    #     return {
    #         "Name": f"{socket.gethostname()}",
    #         "Test": "Called t2"
    #     }
    # elif test=="t3":
        
    #     return {
    #         "Name": f"{socket.gethostname()}",
    #         "Test": "Called t3"
    #     }
    # else:
        
    #     return {
    #         "Name": f"{socket.gethostname()}",
    #         "Test": "Called Other"
    #     }
    
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    # app.run(debug=True, port=4040)