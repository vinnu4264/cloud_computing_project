#!/usr/bin/env python3
import math
import random
import yfinance as yf
import pandas as pd
from datetime import date, timedelta
from pandas_datareader import data as pdr
# override yfinance with pandas – seems to be a common step
yf.pdr_override()

class collect_data:

    def __init__(self):
        today = date.today()
        decadeAgo = today - timedelta(days=3652)
        self.data = pdr.get_data_yahoo('AMZN', start=decadeAgo, end=today)
        self.data['Buy']=0
        self.data['Sell']=0

    def pre_processing(self, i):
        realbody=math.fabs(self.data.Open[i]-self.data.Close[i])
        bodyprojection=0.3*math.fabs(self.data.Close[i]-self.data.Open[i])
        return realbody, bodyprojection

    def hammer(self):
        for i in range(len(self.data)):
            realbody, bodyprojection = self.pre_processing(i)
            if self.data.High[i] >= self.data.Close[i] and self.data.High[i]-bodyprojection <= self.data.Close[i] and self.data.Close[i] > self.data.Open[i] and self.data.Open[i] > self.data.Low[i] and self.data.Open[i]-self.data.Low[i] > realbody:
                self.data.at[self.data.index[i], 'Buy'] = 1
            # Inverted Hammer
            if self.data.High[i] > self.data.Close[i] and self.data.High[i]-self.data.Close[i] > realbody and self.data.Close[i] > self.data.Open[i] and self.data.Open[i] >= self.data.Low[i] and self.data.Open[i] <= self.data.Low[i]+bodyprojection:
                self.data.at[self.data.index[i], 'Buy'] = 1
                #print("I", data.Open[i], data.High[i], data.Low[i], data.Close[i])
            # Hanging Man
            if self.data.High[i] >= self.data.Open[i] and self.data.High[i]-bodyprojection <= self.data.Open[i] and self.data.Open[i] > self.data.Close[i] and self.data.Close[i] > self.data.Low[i] and self.data.Close[i]-self.data.Low[i] > realbody:
                self.data.at[self.data.index[i], 'Sell'] = 1
                #print("M", data.Open[i], data.High[i], data.Low[i], data.Close[i])
            # Shooting Star
            if self.data.High[i] > self.data.Open[i] and self.data.High[i]-self.data.Open[i] > realbody and self.data.Open[i] > self.data.Close[i] and self.data.Close[i] >= self.data.Low[i] and self.data.Close[i] <= self.data.Low[i]+bodyprojection:
                self.data.at[self.data.index[i], 'Sell'] = 1
                #print("S", data.Open[i], data.High[i], data.Low[i], data.Close[i])

        minhistory = 101
        shots = 80000
        stats_data = {
            "buy":[], 
            "sell":[]
        }
        bdate=[]; sdate=[]
        b9=[]; b5=[]
        s9=[]; s5=[]
        
        for i in range(minhistory, len(self.data)):
            if self.data.Buy[i]==1:
                mean=self.data.Close[i-minhistory:i].pct_change(1).mean()
                std=self.data.Close[i-minhistory:i].pct_change(1).std()
                simulated = [random.gauss(mean,std) for x in range(shots)]
                simulated.sort(reverse=True)
                b5.append(simulated[int(len(simulated)*0.95)])
                b9.append(simulated[int(len(simulated)*0.99)])
                bdate.append(str(self.data.index[i]).split(" ")[0])
            elif self.data.Sell[i]==1:
                mean=self.data.Close[i-minhistory:i].pct_change(1).mean()
                std=self.data.Close[i-minhistory:i].pct_change(1).std()
                simulated = [random.gauss(mean,std) for x in range(shots)]
                simulated.sort(reverse=True)
                s5.append(simulated[int(len(simulated)*0.95)])
                s9.append(simulated[int(len(simulated)*0.99)])
                sdate.append(str(self.data.index[i]).split(" ")[0])
        stats_data['buy'] = [bdate, b5, b9]
        stats_data['sell'] = [sdate, s5, s9]
        return stats_data
        

