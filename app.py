import datetime
import dateutil.relativedelta
import streamlit as st
from backtestingMomentumStrategy import momentumStrategyMain, toExcel, filterMonth
import pandas as pd

st. set_page_config(layout="wide")

def getDataframes(startMonth, startYear, endMonth, endYear, numOfStocks, capital):
    comparisonDf, portfolioDf = momentumStrategyMain(startMonth, startYear, endMonth, endYear, numOfStocks, capital)
    
    return comparisonDf, portfolioDf 

def updateDateframe():

    st.session_state["startMonth"] = st.session_state.startDate.month
    st.session_state["startYear"] = st.session_state.startDate.year
    st.session_state["endMonth"] = st.session_state.endDate.month
    st.session_state["endYear"] = st.session_state.endDate.year


    comparisonDf, portfolioDf = getDataframes(st.session_state.startMonth, st.session_state.startYear, st.session_state.endMonth, st.session_state.endYear, st.session_state.numOfStocks, st.session_state.capital)
    excelSheet = toExcel(portfolioDf, comparisonDf)

    st.session_state["comparisonDf"] = comparisonDf
    st.session_state["portfolioDf"] = portfolioDf
    st.session_state["excelSheet"] = excelSheet
    


def updateMonthlyDf():
    selectedDate = datetime.datetime.strptime(st.session_state.choice,"%b %Y")
    monthlyDf = filterMonth(st.session_state.portfolioDf, selectedDate.month, selectedDate.year)
    st.session_state["monthlyDf"] = monthlyDf


st.title("Momentum Strategy Analysis")

# form = st.form("Input Form")
startDate = st.date_input("Start Date", value = datetime.datetime(2017,8,1) , min_value=datetime.datetime(2009,1,1), max_value=datetime.datetime(2022,11,30), key="startDate", on_change=updateDateframe)
endDate = st.date_input("End Date", value = datetime.datetime(2018,8,1), min_value=datetime.datetime(2009,1,1), max_value=datetime.datetime(2022,11,30), key="endDate", on_change=updateDateframe)
capital = st.number_input("Capital", min_value=500000, key="capital", on_change=updateDateframe)
numOfStocks = st.number_input("Number of Stocks", key="numOfStocks", value = 10, on_change=updateDateframe)

if "startMonth" not in st.session_state:

    st.session_state["startMonth"] = st.session_state.startDate.month
    st.session_state["startYear"] = st.session_state.startDate.year
    st.session_state["endMonth"] = st.session_state.endDate.month
    st.session_state["endYear"] = st.session_state.endDate.year


   
if "comparisonDf" not in st.session_state:

    # st.write(f"Selected Range : {startMonth}/{startYear} to {endMonth}/{endYear}")
    # st.write(f"Capital : {capital}")
    # st.write(f"Number of Stocks : {numOfStocks}")

    comparisonDf, portfolioDf = getDataframes(st.session_state.startMonth, st.session_state.startYear, st.session_state.endMonth, st.session_state.endYear, st.session_state.numOfStocks, st.session_state.capital)
    excelSheet = toExcel(portfolioDf, comparisonDf)

    st.session_state["comparisonDf"] = comparisonDf
    st.session_state["portfolioDf"] = portfolioDf
    st.session_state["excelSheet"] = excelSheet

    

st.download_button(label='📥 Download Excel', data=st.session_state.excelSheet ,file_name= f"Momentum {st.session_state.startMonth}/{st.session_state.startYear} to {st.session_state.endMonth}/{ st.session_state.endYear}.xlsx")

st.write(st.session_state.comparisonDf)

dates = [ datetime.datetime.strptime(date,"%Y-%m-%d").strftime("%b %Y") for date in list(st.session_state.comparisonDf.index)]

choice = st.selectbox("Choose Date: ", dates, key="choice", on_change=updateMonthlyDf)

selectedDate = datetime.datetime.strptime(st.session_state.choice,"%b %Y")

if "monthlyDf" not in st.session_state:
    monthlyDf = filterMonth(st.session_state.portfolioDf, selectedDate.month, selectedDate.year)
    st.session_state["monthlyDf"] = monthlyDf

st.dataframe(st.session_state.monthlyDf)



