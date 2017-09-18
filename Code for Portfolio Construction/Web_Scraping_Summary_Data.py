# coding: utf-8

import urllib.request
from bs4 import BeautifulSoup
import datetime
import pandas as pd


def get_summary_data():
    address = "http://www.etf.com/"

    inception_date = [0] * 24
    legal_structure = [0] * 24
    expense_ratio = [0] * 24
    assets_under_management = [0] * 24
    average_daily_volume = [0] * 24
    average_spread = [0] * 24

    ETF24 = ['VTI', 'ITOT', 'SCHB', 'VEA', 'IXUS', 'SCHF', 'VWO', 'IEMG', 'SCHE', 'VIG', 'DVY', 'SCHD', 'VGSH', 'IEF',
             'TLT', 'MUB', 'TFI', 'PZA', 'SCHP', 'TIP', 'IPE', 'XLE', 'DJP', 'VDE']

    for e in range(24):
        url = address + ETF24[e]
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read()
        bsObj = BeautifulSoup(html, "html.parser")

        inception_date[e] = bsObj.find("span", {"class": "field-r-inception-date"}).get_text()
        d = datetime.datetime.strptime(inception_date[e], '%m/%d/%y')
        inception_date[e] = d.strftime('%Y-%m-%d')

        legal_structure[e] = bsObj.find("span", {"class": "field-r-legal-structure"}).get_text()

        expense_ratio[e] = bsObj.find("span", {"class": "field-r-expense-ratio"}).get_text()
        # convert ['0.05%'] to [0.05]
        temp = expense_ratio[e]
        expense_ratio[e] = float(temp[:-1])

        assets_under_management[e] = bsObj.find("span", {"class": "field-r-assets-under-management"}).get_text()
        # start: every element is in format ['$75.04 B'] or ['$866.61 M']
        # end: every element is in format [75.04] in billion
        temp1 = assets_under_management[e].split(' ')
        temp2 = temp1[0]
        temp1[0] = float(temp2[1:])  # get rid of the first element '$'
        if temp1[1] == 'M':
            temp1[0] = temp1[0] / 1000  # convert million into billion
        assets_under_management[e] = temp1[0]

        average_daily_volume[e] = bsObj.find("span", {"class": "field-r-average-daily--volume"}).get_text()
        # start: every element is in format ['$274.26 M']
        # end: every element is in format [274.26]
        temp1 = average_daily_volume[e].split(' ')
        temp2 = temp1[0]
        temp1[0] = float(temp2[1:])  # get rid of the first element '$'
        if temp1[1] == 'B':
            temp1[0] = temp1[0] * 1000  # convert billion into million
        average_daily_volume[e] = temp1[0]

        average_spread[e] = bsObj.find("span", {"class": "field-r-average-spread-"}).get_text()
        # convert ['0.05%'] to [0.05]
        temp = average_spread[e]
        average_spread[e] = float(temp[:-1])

    SUMMARY_DATA = DataFrame({
        'inception_date': inception_date,
        'legal_structure': legal_structure,
        'expense_ratio%': expense_ratio,
        'assets_under_management_B': assets_under_management,
        'average_daily_volume_M': average_daily_volume,
        'average_spread%': average_spread

    }, index=ETF24)

    return SUMMARY_DATA

def main():
    summary_data = get_summary_data()
    capital_data = summary_data['assets_under_management_B']
    weight = pd.dataframe(capital_data / sum(capital_data).todataframe)
    weight.to_csv(r"C:\My Files\Study\17 Spring\800 - Special Problems in FE (MS)\Code\FE-800\csv\weight.csv")
    print(summary_data)



if __name__ == "__main__":
    main()

