import os
import sys
import urllib
import time
import traceback
import pandas as pd
from os import listdir
from bs4 import BeautifulSoup
from StringIO import StringIO
from selenium import webdriver
from os.path import isfile, join


def scrape_screener(ticker):

	driver 					= webdriver.PhantomJS()	
	driver.set_window_size(1120, 550)

	reports_list = ['quarters', 'annuals', 'balancesheet', 'cashflow']
	analysis	 = ['charts', 'analysis', 'peers', 'reports']
	reports 	 = {}
 
	if ticker['BSE_Scrip_Code'] != 'NM': 	url 	= "https://www.screener.in/company/" + str(ticker['BSE_Scrip_Code']) + '/'

	elif ticker['NSE_ID'] != 'NM': 			url 	= "https://www.screener.in/company/" + str(ticker['NSE_ID']) + '/'
	
	driver.get(url)	
	
	#html 	= driver.find_element_by_xpath("//*[contains(text(), 'Export to Excel')]").click()
	
	for report in reports_list: 

		html = driver.find_element_by_id(report)
		
		print '\n'
		print report
		print '-' * 100
		
		table 		 	= html.text
		column_names 	= table.split('\n')[1].split(' ')
		column_names 	= ' '.join([a + '-' + b for a,b in zip(column_names[0::2], column_names[1::2])])	
		table		 	= table.split('\n')[2:len(table)]



		if report == 'annuals': 
			
			column_names 	= column_names + ' TTM'
			table 			= table[:12]
			

		
		table	 	 	= [column_names] + table
		table 		 	= ('\n').join(table)

		table 			= table.replace('Operating Profit', 'operating_profit').replace('Other Income', 'other_income')\
						.replace('Profit before tax', 'profit_before_tax').replace('Net Profit', 'net_profit')\
						.replace('Cash from Operating Activity', 'cash_from_operating_activity')\
						.replace('Cash from Investing Activity', 'cash_from_investing_activity')\
						.replace('Cash from Financing Activity', 'cash_from_financing_activity')\
						.replace('Net Cash Flow', 'net_cash_flow').replace('Total Liabilities', 'total_liabilites')\
						.replace('Share Capital', 'share_capital').replace('Other Liabilities', 'other_liabilities')\
						.replace('Fixed Assets', 'fixed_assets').replace('Other Assets', 'other_assets')\
						.replace('Total Assets', 'total_assets').replace('Dividend Payout', 'divident_payout')\
						.replace('EPS (unadj)', 'EPS_unadj')


		pd.read_csv(StringIO(table), delimiter = ' ').transpose().to_csv(DATA_PATH + 'stocks/quarterly/' + report + '/' + ticker['BSE_Scrip_Id'] + '.csv')

	driver.quit()

	#url 	= urllib.urlopen("https://www.screener.in" + btn.get_attribute("href"))

	#print pd.read_excel(url)

	return driver



def main():

	global DATA_PATH

	DATA_PATH				= '../data/'

	ticker_list 			= pd.read_csv(DATA_PATH + 'tickers.csv')
	files 					= [f.split('.csv')[0] for f in listdir(DATA_PATH + 'stocks/quarterly/annuals') if isfile(join(DATA_PATH + 'stocks/quarterly/annuals',f)) ]

	ticker_list				= ticker_list[~ticker_list['BSE_Scrip_Id'].isin(files)]

	for index, ticker in ticker_list.iterrows():

		print ticker

		try:

			driver = scrape_screener(ticker.to_dict())

		except:  	
			
			traceback.print_exc(file=sys.stdout)
			continue

		time.sleep(2)

	print 'Done'
	
	#driver.quit()
	#display.stop()

main()