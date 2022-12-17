
import os
import re
import math
import datetime  
import pandas as pd
from io import BytesIO
from numpy import nan
import dateutil.relativedelta

extra = []
profit = []

def getStockPrices(symbol, start,end):
  stock = pd.read_csv(os.path.join("StockPrices",f"{symbol}.csv"), index_col=0)
  stock = stock.loc[start:end,:]
  return stock

def getIndexStockList(month, year):
    
    filename = datetime.datetime.strptime(f"{month}-{year}", "%m-%Y").strftime("%b%y").lower() + ".csv"
    nifty50df = pd.read_csv(os.path.join("CSVs",filename), delimiter = ',', skiprows=2, nrows=50, engine='python', encoding='unicode_escape')
    return nifty50df

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


def getAnnualreturns(indexListDf, month, year):
   
    openList = []
    openDateList = []
    closeList = []
    closeDateList = []
    annualReturnList = []
    for symbol in indexListDf["Security Symbol"].to_list():
        open, close, openDate, closeDate = getOpenClosePrice(symbol+".NS", month, year)

        annualReturn = (close-open)/open

        openList.append(open)
        openDateList.append(openDate)
        closeDateList.append(closeDate)
        closeList.append(close)
        annualReturnList.append(annualReturn)
      
    # print(2)

    indexListDf.insert(len(indexListDf.columns), f"open ({month}-{year-1})", openList, True)
    indexListDf.insert(len(indexListDf.columns), f"openDate ({month}-{year-1})", openDateList, True)
    indexListDf.insert(len(indexListDf.columns), f"close ({month}-{year})", closeList, True)
    indexListDf.insert(len(indexListDf.columns), f"closeDate ({month}-{year})", closeDateList, True)
    indexListDf.insert(len(indexListDf.columns), f"annualReturn ({month}-{year})", annualReturnList, True)

    # print(3)

    return indexListDf


def markSelected(indexListDf, numOfStocks, month, year):
    selected=[]
    for i in range(len(indexListDf.index)):

        if(i<numOfStocks):
            selected.append(1)
        else:
            selected.append(0)


    indexListDf.insert(len(indexListDf.columns), f"selected ({month}-{year})", selected, True)

    return indexListDf


def trade(indexListDf, month, year, capital, numOfStocks):
    global profit
    global extra
    investmentAmount = capital/numOfStocks
    quantity = []
    value = []
    buy = 0
    sell = 0 

    lastMonthDate = datetime.datetime(year,month,1) - dateutil.relativedelta.relativedelta(months=1)
    
    for i in range(len(indexListDf.index)):
        if indexListDf.loc[i,f"action ({month}-{year})"] == "BUY":

            qty = math.trunc(investmentAmount/indexListDf.loc[i,f"close ({month}-{year})"])
            quantity.append(qty)

            val = qty*indexListDf.loc[i,f"close ({month}-{year})"]
            value.append(val)
            buy+=val


        elif indexListDf.loc[i,f"action ({month}-{year})"] == "HOLD":


            qty = indexListDf.loc[i,f"quantity ({lastMonthDate.month}-{lastMonthDate.year})"]
            quantity.append(qty)

            val = qty*indexListDf.loc[i,f"close ({month}-{year})"]
            value.append(val)           

        elif indexListDf.loc[i,f"action ({month}-{year})"] == "SELL":
            

            qty = (-1)*indexListDf.loc[i,f"quantity ({lastMonthDate.month}-{lastMonthDate.year})"]
            quantity.append(qty)

            val = qty*indexListDf.loc[i,f"close ({month}-{year})"]
            value.append(val)
            sell+=val    

        else:

            qty = 0
            quantity.append(qty)

            val = 0
            value.append(val)

    # print(indexListDf[f"action ({month}-{year})"])
    # print(quantity)
    # print(value)
    if buy > (-1)*sell:
      extra.append(buy-((-1)*sell))
      profit.append(0)
    
    else:
      profit.append(((-1)*sell)-buy)
      extra.append(0)

    indexListDf.insert(len(indexListDf.columns), f"quantity ({month}-{year})", quantity, True)
    indexListDf.insert(len(indexListDf.columns), f"value ({month}-{year})", value, True)
    
    return indexListDf

def takeAction(indexListDf, month, year):

    action = []
    lastMonthDate = datetime.datetime(year,month,1) - dateutil.relativedelta.relativedelta(months=1)

    for i in range(len(indexListDf.index)):

        if indexListDf.loc[i,f"selected ({month}-{year})"] == 1 and indexListDf.loc[i,f"selected ({lastMonthDate.month}-{lastMonthDate.year})"] == 0:
            action.append("BUY")

        elif indexListDf.loc[i,f"selected ({month}-{year})"] == 0 and indexListDf.loc[i,f"selected ({lastMonthDate.month}-{lastMonthDate.year})"] == 1:
            action.append("SELL")
        
        elif indexListDf.loc[i,f"selected ({month}-{year})"] == 1 and indexListDf.loc[i,f"selected ({lastMonthDate.month}-{lastMonthDate.year})"] == 1:    
            action.append("HOLD")
        
        else:
            action.append("NO ACTION")
        
    # print(action)
    indexListDf.insert(len(indexListDf.columns), f"action ({month}-{year})", action, True)

    return indexListDf



def getPortfolioValue(portfolioDf, month, year):
    portfolioValue = 0 
    for val in portfolioDf[f"value ({month}-{year})"]:
        if val>0:
            portfolioValue+=val

    return portfolioValue

def compareIndexVsPortfolio(portfolioDf, startMonth, startYear, endMonth, endYear):

    global profit
    global extra

    end = datetime.date(endYear,endMonth,1)
    start = datetime.date(startYear,startMonth,1)


    indexOpenCloseData = getStockPrices("^NSEI", str(start), str(end) )
    comparisonDf = indexOpenCloseData.loc[:,["Close"]]


    indexCummulativeReturn = [0]
    indexMonthlyReturn = [0]
    portfolioValue = []
    totalValue = []
    totalCummulativeReturn = [0]
    totalMonthlyReturn = [0]
    dates = list(comparisonDf.index)

    
    for i in range(1,len(dates)):

        firstVal = comparisonDf.loc[dates[0],"Close"]
        currVal = comparisonDf.loc[dates[i],"Close"]
        prevVal = comparisonDf.loc[dates[i-1],"Close"]

        indexCummulativeReturnValue = ((currVal - firstVal))/firstVal
        indexCummulativeReturn.append(indexCummulativeReturnValue)

        indexMonthlyReturnValue = ((currVal - prevVal))/prevVal
        indexMonthlyReturn.append(indexMonthlyReturnValue)


    for ind, date in enumerate(dates):
        date =  datetime.datetime.strptime(date, "%Y-%m-%d")
        portfolioMonthlyValue = getPortfolioValue(portfolioDf, date.month, date.year) 
        portfolioValue.append(portfolioMonthlyValue)

        sum = 0
        for i in range(0,ind+1):
            sum+=(profit[i]-extra[i])

        totalMonthlyValue = portfolioMonthlyValue + sum
        totalValue.append(totalMonthlyValue)
        

    for i in range(1,len(totalValue)):
        firstVal = totalValue[0]
        currVal = totalValue[i]
        prevVal = totalValue[i-1]

        totalCummulativeReturnValue = ((currVal-firstVal))/firstVal
        totalCummulativeReturn.append(totalCummulativeReturnValue)

        totalMonthlyReturnValue = (currVal-prevVal)/prevVal
        totalMonthlyReturn.append(totalMonthlyReturnValue)


    comparisonDf.insert(len(comparisonDf.columns), "indexCummulativeReturn", indexCummulativeReturn, True)
    comparisonDf.insert(len(comparisonDf.columns), "indexMonthlyReturn", indexMonthlyReturn, True)
    comparisonDf.insert(len(comparisonDf.columns), "portfolioValue", portfolioValue, True)
    comparisonDf.insert(len(comparisonDf.columns), "profit", profit, True)
    comparisonDf.insert(len(comparisonDf.columns), "extraAmount", extra, True)
    comparisonDf.insert(len(comparisonDf.columns), "totalValue", totalValue, True)
    comparisonDf.insert(len(comparisonDf.columns), "totalCummulativeReturn", totalCummulativeReturn, True)
    comparisonDf.insert(len(comparisonDf.columns), "totalMonthlyReturn", totalMonthlyReturn, True)
    comparisonDf.columns = comparisonDf.columns.str.replace('Close', 'indexClose')


    return comparisonDf

def toExcel(portfolioDf, comparisonDf):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')

    comparisonDf.to_excel(writer, sheet_name='Comparison')
    portfolioDf.to_excel(writer, sheet_name='Proof')

    workbook  = writer.book
    worksheet1 = writer.sheets['Comparison']
    worksheet2 = writer.sheets['Proof']

    openCol = []

    for ind, colName in enumerate(portfolioDf.columns):
        
        if re.match(r"^open[\s\(0-9-]*\)$",colName,re.IGNORECASE):
            openCol.append(ind)



    format1 = workbook.add_format({'num_format': '₹ 0.00'})
    format2 = workbook.add_format({'num_format': '0.00 %'})


    for i in range(len(openCol)):
        col = openCol[i]+1

        worksheet2.set_column(col, col, None, format1)
        worksheet2.set_column(col+2, col+2, None, format1)
        worksheet2.set_column(col+8, col+8, None, format1)
        worksheet2.set_column(col+4, col+4, None, format2)
        

    writer.save()
    processed_data = output.getvalue()
    return processed_data


def filterMonth(portfolioDf, month, year):

    monthlyDf = portfolioDf.loc[:,["Security Symbol", f"open ({month}-{year-1})", f"openDate ({month}-{year-1})",
    	f"close ({month}-{year})", f"closeDate ({month}-{year})", f"annualReturn ({month}-{year})", f"selected ({month}-{year})", f"action ({month}-{year})",
        f"quantity ({month}-{year})", f"value ({month}-{year})"]]

    monthlyDf = monthlyDf.loc[(monthlyDf[f"action ({month}-{year})"] != "NO ACTION")]
    monthlyDf = monthlyDf.dropna(subset=[f"action ({month}-{year})"])
    

    monthlyDf.set_index("Security Symbol", inplace=True)
    return monthlyDf


def momentumStrategyMain(startMonth, startYear, endMonth, endYear, numOfStocks, capital ):
    global profit
    global extra

    indexListDf = getIndexStockList(startMonth, startYear)
    indexListDf = indexListDf.loc[:,["Security Symbol"]]
    indexListDf = getAnnualreturns(indexListDf, startMonth, startYear)
    indexListDf = indexListDf.sort_values(by=[f"annualReturn ({startMonth}-{startYear})"], ascending=False, ignore_index=True)
    indexListDf = markSelected(indexListDf, numOfStocks, startMonth, startYear)

    action =[]
    for val in indexListDf[f"selected ({startMonth}-{startYear})"]:
        if val == 1:
            action.append("BUY")
        else:
            action.append("NO ACTION")

    indexListDf.insert(len(indexListDf.columns), f"action ({startMonth}-{startYear})", action, True)

    indexListDf = trade(indexListDf, startMonth, startYear, capital, numOfStocks)

    date = datetime.datetime.strptime(f"{startMonth}-{startYear}", "%m-%Y") + dateutil.relativedelta.relativedelta(months=1)
    endDate = datetime.datetime.strptime(f"{endMonth}-{endYear}", "%m-%Y") + dateutil.relativedelta.relativedelta(months=1)
    endDate = endDate.strftime("%m-%Y")

    portfolioDf = indexListDf
    extra = [0]
    profit = [0]

    while(date.strftime("%m-%Y") != endDate ):
        indexListDf = None
        month = date.month
        year = date.year 
        print(month, year)

        indexListDf = getIndexStockList(month, year)
        indexListDf = indexListDf.loc[:,["Security Symbol"]]
        indexListDf = getAnnualreturns(indexListDf, month, year)
        indexListDf = indexListDf.sort_values(by=[f"annualReturn ({month}-{year})"], ascending=False, ignore_index=True)
        indexListDf = markSelected(indexListDf, numOfStocks, month, year)

        indexListDf = pd.merge(portfolioDf, indexListDf, how='outer')
        lastMonthDate = datetime.datetime(year,month,1) - dateutil.relativedelta.relativedelta(months=1)

        indexListDf[f"selected ({lastMonthDate.month}-{lastMonthDate.year})"] = indexListDf[f"selected ({lastMonthDate.month}-{lastMonthDate.year})"].replace(nan, 0)

        indexListDf = takeAction(indexListDf, month, year)

        indexListDf = trade(indexListDf, month, year, capital, numOfStocks)

        portfolioDf = indexListDf
        date = date + dateutil.relativedelta.relativedelta(months=1)

    comparisonDf = compareIndexVsPortfolio(portfolioDf,startMonth, startYear, endMonth, endYear)

    return comparisonDf, portfolioDf
