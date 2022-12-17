# import yfinance as yf
import datetime
import os
from numpy import nan
import pandas as pd
import math
import dateutil.relativedelta


def getStockPrices(symbol, start,end):
  stock = pd.read_csv(os.path.join("StockPrices",f"{symbol}.csv"), index_col=0)
  stock = stock.loc[start:end,:]
  return stock


def getOpenClosePrice(symbol, month, year ):
    
    end = datetime.date(year,month,1)
    start = end - dateutil.relativedelta.relativedelta(years=1)

    try:
        if not os.path.exists(os.path.join(os.getcwd(), "StockPrices", f"{symbol}.csv")):
          raise Exception
        stock = stock = getStockPrices(symbol, str(start), str(end))
        open = stock["Close"][0]
        close = stock["Close"][-1]
        dates = list(stock.index)
        openDate = dates[0]
        closeDate = dates[-1]
    except:
        open = nan
        close = nan
        openDate = nan
        closeDate = nan

    return open, close, openDate, closeDate


open, close, openDate, closeDate =  getOpenClosePrice("IOC.NS", 2, 2017 )
print(open, close, openDate, closeDate )
#
# month = 4
# year = 2020
# end = datetime.datetime(year,month,1)
# start = end - datetime.timedelta(days=366)

# stock = yf.download("NESTLEIND.NS",start=start, end=end, progress=False)
# print(stock)
# -------------------------FULL OUTER JOIN------------------

# technologies = {
#     'Courses':["Spark","PySpark","Python","pandas"],
#     'Fee1' :[20000,25000,22000,30000],
#     'Duration':['30days','40days','35days','50days'],
#               }
# index_labels=['r1','r2','r3','r4']
# df1 = pd.DataFrame(technologies,index=index_labels)

# technologies2 = {
#     'Courses':["Spark","Java","Python","Go"],
#     'Discount':[2000,2300,1200,2000],
#     'Fee2':[2000,25000,1200,2000]
#               }
# index_labels2=['r1','r6','r3','r5']
# df2 = pd.DataFrame(technologies2,index=index_labels2)

# print(df1)
# print(df2)


# df2=pd.merge(df1,df2, how='outer')
# print(df2)

# for col in df2.columns:
#     print(col)

# sum=0
# for val in df2["Fee2"]:
#     if val > 0:
#         sum+=val

# print(sum)
# Using replace
# df2["Discount"] = df2["Discount"].replace(np.nan, 0)


# print("\n",df2)
# i=2
# print(df2[f"Fee{i}"][1])


# -------------------- Iterate over df-----------

# technologies = {
#     'Courses':["Spark","PySpark","Python","pandas"],
#     'Fee' :[20000,25000,22000,30000],
#     'Duration':['30days','40days','35days','50days'],
#               }

# df1 = pd.DataFrame(technologies)

# selected=[]
# count = 0
# for i in range(len(df1.index)):

#     if(i<2):
#         selected.append(math.trunc(1.5373))
#     else:
#         selected.append(0)


# df1.insert(len(df1.columns), "Selected", selected, True)

# print(type(df1["Selected"][0]))


#---------------------get previous month----------------
# d = datetime.datetime.strptime("2020-02-29", "%Y-%m-%d")
# d2 = d - dateutil.relativedelta.relativedelta(months=1)
# print(d2)


# --------------------Iteration through date----------
# startMonth = 4
# startYear = 2020
# endMonth = 4
# endYear = 2021

# date = datetime.datetime.strptime(f"{startMonth}-{startYear}", "%m-%Y")
# print("start date = ", date.strftime("%m-%Y"))
# endDate = datetime.datetime.strptime(f"{endMonth}-{endYear}", "%m-%Y") + dateutil.relativedelta.relativedelta(months=1)
# endDate = endDate.strftime("%m-%Y")
# print("end date =", endDate)

# while(date.strftime("%m-%Y") != endDate ):
#     print(date.strftime("%m-%Y"))

#     date = date + dateutil.relativedelta.relativedelta(months=1)

#-----------nifty return------------

# data = yf.download("^NSEI", start = "2012-1-01", end = "2021-12-07", interval = '1mo')
# symbol = "NSE"
# # data.to_csv(f"{symbol}.csv")
# # print('.......done.......')
# # data = data.loc[:,["Close"]]
# # print(data)
# # print(type(data))
# for date in list(data.columns):
#     print(date)
