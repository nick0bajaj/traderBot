import requests
import json
import math
import pandas as pd

td_consumer_key = 'HBLGFCFHJ11P6H4KZIA5CIR4RGVUJCAH'


#quote
def getStats(stock):
	endpoint = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/quotes?'
	full_url = endpoint.format(stock_ticker=stock)
	page = requests.get(url=full_url,
	                    params={'apikey' : td_consumer_key})
	content = json.loads(page.content)
	return content

#historical
def getHistory(stock):
	endpoint = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/pricehistory'
	full_url = endpoint.format(stock_ticker=stock)
	page = requests.get(url=full_url,
	                   params={'apikey' : td_consumer_key})
	content = json.loads(page.content)
	print(content)
	return content['candless']

def parseGetHistory(stock):
	history = {}
	ema = 0
	smoothing = 2
	oldhistory = getHistory(stock)
	days = len(oldhistory)
	for i in oldhistory:
		datetime = i["datetime"]
		avgPrice = (i['open'] + i['high'] + i['low'] + i['close'])/4
		ema = (avgPrice * (smoothing/(1+days))) + ema * (1 - (smoothing/(1 + days)))
		history[stock] = (ema, datetime, (i['close'] - ema))
	return history

def getReccomendations():
	totalEma = {}
	topFiveNames = [0,1,2,3,4]
	test = math.inf
	topFiveValues = [(0,test),(0,test),(0,test),(0,test),(0,test)]
	for stock in getSymbols():
		i = 0
		currEma = parseGetHistory(stock)[stock]
		totalEma[stock] = currEma
		while(i < 4):
			currVal = currEma[0]
			currDiff = currEma[1]
			if (currVal > topFiveValues[i][0]) and (currVal < topFiveValues[i][1]):
				topFiveNames[i] = stock
				topFiveValues[i] = (currVal, currDiff)
				i = 5
			else:
				i = i + 1
	return topFiveNames



def getSymbols():
	table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
	df = table[0]
	df.to_csv('S&P500-Info.csv')
	df.to_csv("S&P500-Symbols.csv", columns=['Symbol'])
	return df["Symbol"]


print(getReccomendations())

# def getOldFile():
# 	oldFile = open("stockData.txt","r+")
# 	oldData = {}
# 	for line in oldFile:
# 		symbol, ema, timestamp = line.split(" ")
# 		oldData[symbol] = (ema, timestamp)
# 	return oldFile, oldData

# def updateFile():
# 	symbols = getSymbols()
# 	oldFile, oldData = getOldFile()
# 	newData = oldData.copy()
# 	for symbol in symbols:
# 		timestamp = getStats(symbol)
# 		if(oldData(symbol)):
# 			if(oldData(symbol)[1] != timestamp):
# 				updateStock(newData, timestamp, symbol)
# 	oldFile.writelines(newData)

# def updateStock(newData, timestamp, symbol):
# 	getHistory(symbol)[[timestamp]:]
# 	emi = calculateEMI(valueLst)
# 	newData[symbol] = (emi, timestamp)
# 	return newData
