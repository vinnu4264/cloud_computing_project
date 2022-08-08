#!/usr/bin/env python3
import math
import random
import yfinance as yf
import pandas as pd
from datetime import date, timedelta
from pandas_datareader import data as pdr

class Data_Processor():

    def __init__(self):
        # override yfinance with pandas – seems to be a common step
        yf.pdr_override()
        # Get stock data from Yahoo Finance – here, asking for about 10 years of Gamestop
        # which had an interesting time in 2021: https://en.wikipedia.org/wiki/GameStop_short_squeeze
        today = date.today()
        decadeAgo = today - timedelta(days=3652)
        self.data = pdr.get_data_yahoo('AMZN', start=decadeAgo, end=today)
        # Other symbols: TSLA – Tesla, AMZN – Amazon, NFLX – Netflix, BP.L – BP
        # Add two columns to this to allow for Buy and Sell signals
        # fill with zero
        self.data['Buy']=0
        self.data['Sell']=0
        data = self.data

        # Find the 4 different types of signals – uncomment print statements
        # if you want to look at the data these pick out in some another way
        for i in range(len(data)):
            # Hammer
            realbody=math.fabs(data.Open[i]-data.Close[i])
            bodyprojection=0.3*math.fabs(data.Close[i]-data.Open[i])
        if data.High[i] >= data.Close[i] and data.High[i]-bodyprojection <= data.Close[i] and data.Close[i] > data.Open[i] and data.Open[i] > data.Low[i] and data.Open[i]-data.Low[i] > realbody:
                    data.at[data.index[i], 'Buy'] = 1
                    #print("H", data.Open[i], data.High[i], data.Low[i], data.Close[i])
        # Inverted Hammer
        if data.High[i] > data.Close[i] and data.High[i]-data.Close[i] > realbody and data.Close[i] > data.Open[i] and data.Open[i] >= data.Low[i] and data.Open[i] <= data.Low[i]+bodyprojection:
            data.at[data.index[i], 'Buy'] = 1
            #print("I", data.Open[i], data.High[i], data.Low[i], data.Close[i])
        # Hanging Man
        if data.High[i] >= data.Open[i] and data.High[i]-bodyprojection <= data.Open[i] and data.Open[i] > data.Close[i] and data.Close[i] > data.Low[i] and data.Close[i]-data.Low[i] > realbody:
            data.at[data.index[i], 'Sell'] = 1
            #print("M", data.Open[i], data.High[i], data.Low[i], data.Close[i])
        # Shooting Star
        if data.High[i] > data.Open[i] and data.High[i]-data.Open[i] > realbody and data.Open[i] > data.Close[i] and data.Close[i] >= data.Low[i] and data.Close[i] <= data.Low[i]+bodyprojection:
            data.at[data.index[i], 'Sell'] = 1
            #print("S", data.Open[i], data.High[i], data.Low[i], data.Close[i])

        