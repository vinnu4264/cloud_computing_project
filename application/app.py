from flask import Flask
import math, random
import yfinance as yf
import pandas as pd
from datetime import date, timedelta
from pandas_datareader import data as pdr

app = Flask(__name__)

def process_data(minhistory, shots):
    yf.pdr_override()
    today = date.today()
    decadeAgo = today - timedelta(days=3652)
    data = pdr.get_data_yahoo('AMZN', start=decadeAgo, end=today)
    data['Buy']=0
    data['Sell']=0
    for i in range(len(data)):
        realbody=math.fabs(data.Open[i]-data.Close[i])
        bodyprojection=0.1*math.fabs(data.Close[i]-data.Open[i])

        # Hammer
        if data.High[i] >= data.Close[i] and data.High[i]-bodyprojection<= data.Close[i] and data.Close[i] >data.Open[i] and data.Open[i] >data.Low[i] and data.Open[i]-data.Low[i] >realbody:
            data.at[data.index[i], 'Buy'] = 1 

        # Inverted Hammer
        if data.High[i] >data.Close[i] and data.High[i]-data.Close[i] >realbody and data.Close[i] >data.Open[i] and data.Open[i] >= data.Low[i] and data.Open[i] <= data.Low[i]+bodyprojection:
            data.at[data.index[i], 'Buy'] = 1

        # Hanging Man
        if data.High[i] >= data.Open[i] and data.High[i]-bodyprojection<= data.Open[i] and data.Open[i] >data.Close[i] and data.Close[i] >data.Low[i] and data.Close[i]-data.Low[i] >realbody:
            data.at[data.index[i], 'Sell'] = 1

        # Shooting Star
        if data.High[i] >data.Open[i] and data.High[i]-data.Open[i] >realbody and data.Open[i] >data.Close[i] and data.Close[i] >= data.Low[i] and data.Close[i] <= data.Low[i]+bodyprojection:
            data.at[data.index[i], 'Sell'] = 1

    stats_data = {
        "buy":[], 
        "sell":[]
    }
    bdate=[]; sdate=[]
    b9=[]; b5=[]
    s9=[]; s5=[]
    
    for i in range(minhistory, len(data)):
        if data.Buy[i]==1:
            mean=data.Close[i-minhistory:i].pct_change(1).mean()
            std=data.Close[i-minhistory:i].pct_change(1).std()
            simulated = [random.gauss(mean,std) for x in range(shots)]
            simulated.sort(reverse=True)
            b5.append(simulated[int(len(simulated)*0.95)])
            b9.append(simulated[int(len(simulated)*0.99)])
            bdate.append(str(data.index[i]).split(" ")[0])
        elif data.Sell[i]==1:
            mean=data.Close[i-minhistory:i].pct_change(1).mean()
            std=data.Close[i-minhistory:i].pct_change(1).std()
            simulated = [random.gauss(mean,std) for x in range(shots)]
            simulated.sort(reverse=True)
            s5.append(simulated[int(len(simulated)*0.95)])
            s9.append(simulated[int(len(simulated)*0.99)])
            sdate.append(str(data.index[i]).split(" ")[0])
    stats_data['buy'] = [bdate, b5, b9]
    stats_data['sell'] = [sdate, s5, s9]
    return stats_data

@app.route('/<history>/<shots>')
def tester(history, shots):
    # /101/80000
    stats_data = process_data(int(history), int(shots))
    return stats_data

@app.route("/")
def health_check():
    return "Hello World!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    # app.run(debug=True, port=4040)