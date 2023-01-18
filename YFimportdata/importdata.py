
import pandas as pd
import yfinance as yf
import datetime

start = datetime.datetime(2015,5,31)
end = datetime.datetime(2023,1,1)
ticker = ("ES=F")

def getdata(tickers,startdate,enddate):

    df = pd.DataFrame(yf.download([tickers],start=startdate,end=enddate))
    return df

def adjustdata(df):

    df.drop(['Adj Close'],axis=1,inplace=True)
    df.columns = ["open","high","low","close","volume"]
    df["dayofweek"] = df.index.dayofweek
    df["day"] = df.index.day
    df["month"] = df.index.month
    df["year"] = df.index.year
    df["dayofyear"] = df.index.dayofyear
    df["quarter"] = df.index.quarter

    return df

dataset = adjustdata(getdata(ticker,start,end))

