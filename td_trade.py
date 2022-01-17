import requests
import pandas as pd
import time


def price_history(company, minutes):
    # define an endpoint with a stock of your choice, MUST BE UPPER
    endpoint = r"https://api.tdameritrade.com/v1/marketdata/{}/pricehistory".format(company)

    # define the payload
    payload = {'apikey':'',
               'periodType':'day',
               'frequencyType':'minute',
               'frequency':'{}'.format(minutes),
               'period':'2',
               'endDate':'{}'.format(round(round(time.time(), 3)*1000)),
               'startDate':'1641116407000',
               'needExtendedHoursData':'true'}

    # make a request
    content = requests.get(url = endpoint, params = payload)

    # convert it dictionary object
    data = content.json()
    return data



def index_instruments(company):
    # define an endpoint with a stock of your choice, MUST BE UPPER
    endpoint = r"https://api.tdameritrade.com/v1/instruments".format(company)

    # define the payload
    payload = {'apikey':'',
               'periodType':'day',
               'frequencyType':'minute',
               'frequency':'1',
               'period':'2',
               'endDate':'1642126509000',
               'startDate':'1642126508000',
               'needExtendedHoursData':'true'}

    # make a request
    content = requests.get(url = endpoint, params = payload)

    # convert it dictionary object
    data = content.json()
    return data





def current_prices(companies):
        #ex:'GOOG,MSFT,AAPL'
    # define an endpoint with a stock of your choice, MUST BE UPPER
    endpoint = r"https://api.tdameritrade.com/v1/marketdata/quotes"

    # define the payload
    payload = {'apikey':'',
               'symbol':companies}

    # make a request
    content = requests.get(url = endpoint, params = payload)

    # convert it dictionary object
    data = content.json()
    return data

def show_prices(stocks):

    while True:
        prices = current_prices(stocks)


        #print(a['GOOG']['bidPrice'], a['GOOG']['lastPrice'])


        print('SPY:', prices['SPY']['lastPrice'], 'TSLA:', prices['TSLA']['lastPrice'], 'GOOG:', prices['GOOG']['lastPrice'], end = "\r")

stocks = 'GOOG,SPY,TSLA'
#show_prices(stocks)

def options(company):
        #ex:'GOOG,MSFT,AAPL'
    # define an endpoint with a stock of your choice, MUST BE UPPER
    endpoint = r"https://api.tdameritrade.com/v1/marketdata/chains"

    # define the payload
    payload = {'apikey':'',
               'symbol':company}

    # make a request
    content = requests.get(url = endpoint, params = payload)

    # convert it dictionary object
    data = content.json()
    return data


def show_tree(json_file):
    import json
    json_formatted_str = json.dumps(json_file, indent=2)

    print(json_formatted_str)



#print(optionss["putExpDateMap"]["2022-01-07:1"]["200.0"][0]['theta'])
def filter_options():
    for date in optionss["putExpDateMap"]:
        for price in optionss["putExpDateMap"][str(date)]:
            option = optionss["putExpDateMap"][str(date)][str(price)]
            if float(option[0]['theta']) < -.01 and float(option[0]['delta']) > .09:
                print(option[0]['symbol'])

    for date in optionss["callExpDateMap"]:
        for price in optionss["callExpDateMap"][str(date)]:
            option = optionss["callExpDateMap"][str(date)][str(price)]
            if float(option[0]['theta']) < -.01 and float(option[0]['delta']) > .1:
                print(option[0]['symbol'])
