import quandl as qd
from pymongo import MongoClient
import pandas as pd


def get_db(host="localhost", port=27017):
    client = MongoClient(host, port)
    db_name = client.test_1
    return db_name


def get_collection(db):
    collection = db["robo_advisor"]
    print(collection)


def download_data():
    pass


def save_price_data(tickers, paths, host="localhost", port=27017, qd_apikey='6opTKxN_Q5d8aGDKKwxm'):
    db = get_db(host, port)
    db.ETF.delete_many({})  # empty the database
    qd.ApiConfig.api_key = qd_apikey

    # ETFs = ['VTI':"US STOCKS",'ITOT':"US STOCKS",'SCHB':"US STOCKS",'VEA':"FOREIGN \
    # DEVELOPED STOCKS",'IXUS':"FOREIGN DEVELOPED STOCKS",'SCHF':"FOREIGN DEVELOPED STOCKS",
    # 'VWO':"EMERGING MARKET STOCKS",'IEMG':"EMERGING MARKET STOCKS",'SCHE':"EMERGING MARKET\
    # STOCKS",'VIG':"DIVIDEND GROWTH STOCKS",'DVY':"DIVIDEND GROWTH STOCKS",'SCHD':"DIVIDEND\
    # GROWTH STOCKS",'IEF':"US GOVERNMENT BONDS",'TLT':"US\
    # GOVERNMENT BONDS"]

    # ETFs = {'VTI':"US STOCKS",'ITOT':"US STOCKS"}

    # Download Data
    data = pd.DataFrame()

    for k in tickers.keys():
        print("start download etf " + k)

        try:
            temp_data = qd.get("GOOG/NYSEARCA_" + k, start_data="2010-01-01", returns="pandas")
        except:
            temp_data = qd.get('GOOG/NASDAQ_' + k, start_date="2010-01-01", returns="pandas")
        else:
            pass

        temp_data_close = temp_data.loc[:, "Close"]
        data.insert(len(data.columns), k, temp_data_close)
        # data = pd.join(data,temp_data_close,how = "outer")

    data.to_csv(path_or_buf=paths)
    return data


def main():
    ETFs = {'VTI':"US STOCKS",'ITOT':"US STOCKS",'SCHB':"US STOCKS",'VEA':"FOREIGN \
    DEVELOPED STOCKS",'IXUS':"FOREIGN DEVELOPED STOCKS",'SCHF':"FOREIGN DEVELOPED STOCKS",
    'VWO':"EMERGING MARKET STOCKS",'IEMG':"EMERGING MARKET STOCKS",'SCHE':"EMERGING MARKET\
    STOCKS",'VIG':"DIVIDEND GROWTH STOCKS",'DVY':"DIVIDEND GROWTH STOCKS",'SCHD':"DIVIDEND\
    GROWTH STOCKS",'VGSH':"US GOVERNMENT BONDS",'IEF':"US GOVERNMENT BONDS",'TLT':"US\
    GOVERNMENT BONDS",'MUB':"MUNICIPAL BONDS",'TFI':"MUNICIPAL BONDS",'PZA':"MUNICIPAL \
    BONDS",'SCHP':"TREASURY INFLATION-PROTECTED SECURITIES (TIPS)",'TIP':"TREASURY \
    INFLATION-PROTECTED SECURITIES (TIPS)",'IPE':"TREASURY INFLATION-PROTECTED SECUR\
    ITIES (TIPS)",'XLE':"NATURAL RESOURCES",'DJP':"NATURAL RESOURCES",
    'VDE':"NATURAL RESOURCES"}

    csv_file_path = r"C:\My Files\Study\17 Spring\800 - Special Problems in FE (MS)\Code\FE-800\csv\test.csv"
    data = save_price_data(ETFs,csv_file_path)
    print(data)

if __name__ == "__main__":
    main()
    print("success!")

