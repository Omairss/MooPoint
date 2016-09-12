import sys
import urllib
import traceback
import pandas as pd
from bs4 import BeautifulSoup
from StringIO import StringIO

def get_ticker_historical(ticker):

	if ticker['BSE_Scrip_Id'] != 'NM':

		csv 		= urllib.urlopen("http://ichart.yahoo.com/table.csv?s=" + ticker['BSE_Scrip_Id'] + ".BO&a=%7Bdate.addMonths(-2).format('MM')%7D&b=%7B" +
					"date.today.format('dd')%7D&c=%7Bdate.today.format('yyyy')%7D&d=%7Bdate.addMonths(-1).format('MM')%7D&e=%7B" + 
					"date.today.format('dd')%7D&f=%7Bdate.today.format('yyyy')%7D&g=d&ignore=.csv").read()
	
	elif ticker['NSE_ID'] != 'NM':	

		csv 		= urllib.urlopen("http://ichart.yahoo.com/table.csv?s=" + ticker['NSE_ID'] + ".NO&a=%7Bdate.addMonths(-2).format('MM')%7D&b=%7B" +
					"date.today.format('dd')%7D&c=%7Bdate.today.format('yyyy')%7D&d=%7Bdate.addMonths(-1).format('MM')%7D&e=%7B" + 
					"date.today.format('dd')%7D&f=%7Bdate.today.format('yyyy')%7D&g=d&ignore=.csv").read()


	ticker_df 	= pd.read_csv(StringIO(csv))

	ticker_df.to_csv(DATA_PATH + 'stocks/daily/' + ticker['BSE_Scrip_Id'] + '.csv')	

	return True


def main():

	global DATA_PATH

	DATA_PATH				= '../data/'

	ticker_list 			= pd.read_csv(DATA_PATH + 'tickers.csv')

	for index, ticker in ticker_list.iterrows():

		print ticker

		try: 		

			get_ticker_historical(ticker.to_dict())
		
		except:  	
			
			traceback.print_exc(file=sys.stdout)
			continue

	print 'Done'
		

main()