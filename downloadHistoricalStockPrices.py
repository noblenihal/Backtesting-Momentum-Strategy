import yfinance as yf
import pandas as pd
import os
import datetime
import requests
import traceback
import shutil
import dateutil.relativedelta



def getNifty50StockList(month, year):
    
    filename = datetime.datetime.strptime(f"{month}-{year}", "%m-%Y").strftime("%b%y").lower() + ".csv"
    nifty50df = pd.read_csv(os.path.join("CSVs",filename), delimiter = ',', skiprows=2, skipfooter=17, engine='python')
    return nifty50df


def saveHistoricalStockPrices(symbol):

    if os.path.exists(os.path.join(os.getcwd(), "StockPrices", f"{symbol}.csv")):
        return 

    try:
        start = datetime.datetime(2008,1,1)  #yyyymmdd
        end = datetime.datetime(2022,11,30)
        stockPrices = yf.download(symbol,start=start, end=end, progress=False, interval='1mo')

        stockPrices.to_csv(os.path.join(os.getcwd(), "StockPrices", f"{symbol}.csv"))
    except:
        print(f"{symbol}not found !")


startMonth = 1
startYear = 2008
endMonth = 11
endYear = 2022


date = datetime.datetime.strptime(f"{startMonth}-{startYear}", "%m-%Y") + dateutil.relativedelta.relativedelta(months=1)
endDate = datetime.datetime.strptime(f"{endMonth}-{endYear}", "%m-%Y") + dateutil.relativedelta.relativedelta(months=1)
endDate = endDate.strftime("%m-%Y")


while(date.strftime("%m-%Y") != endDate ):

    month = date.month
    year = date.year 
    print(month, year)


    nifty50listDf = getNifty50StockList(month, year)
    nifty50listDf = nifty50listDf.loc[:,["Security Symbol"]]
    for symbol in nifty50listDf["Security Symbol"].to_list():
        saveHistoricalStockPrices(symbol+".NS")
