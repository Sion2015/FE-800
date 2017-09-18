import numpy as np
from data_preprocessing import *


class Data:
    # def __init__(self, tickers, from_data, to_data, database = ):
    def __init__(self, tickers, start_date, end_date, host):
        self.tickers = tickers
        #self.assetclass = get_asset_class(host=,tickers = )
        self.host = host
        self.price = get_daily_price(self.host, tickers, start_date, end_date)
        self.num = len(tickers)
        self.risk_free_rate = 0.0075/360
        self.returns = self.get_stock_return(self.price)
        self.affiliate_return = self.get_affliate_return_from_database(tickers)
        self.capital_weights = get_mktcap_weight(tickers, host=self.host)

    # def get_daily_price(self, ETF=None, startdate=None, enddate=None):
    #     # ETF selection
    #     if ETF == None:
    #         price = get_hist_data_close_for_many(host=self.host)
    #     else:
    #         price = get_hist_data_close_for_many(ETF=ETF, host=self.host)
    #
    #     # Time period selection
    #     if startdate == None:
    #         if enddate == None:
    #             price = price[:][:]
    #         else:
    #             price = price[:enddate][:]
    #     else:
    #         if enddate == 0:
    #             price = price[startdate:][:]
    #         else:
    #             price = price[startdate:enddate][:]
    #     return price

    def get_all_price_from_database(self, tickers):
        # price_dataframe = pd.read_csv(r"C:\My Files\Study\17 Spring\800 - Special Problems in FE (MS)\Code\FE-800\csv\test.csv",index_col="Date")
        price_dataframe = get_hist_data_close_for_many(tickers)
        price_dataframe = price_dataframe.dropna()
        return price_dataframe

    def get_covariance_matrix(self, if_print=False):
        # self.stock_return = get_stock_return(self.stock_price)
        covariance_matrix = np.cov(self.returns, rowvar=False)
        if if_print:
            print("Covariance Matrix is \n", covariance_matrix)
        return covariance_matrix

    def set_risk_free_rate(self, risk_free_rate):
        self.risk_free_rate = risk_free_rate

    def get_stock_return(self, price_data,if_print=False):
        # stock_returns = self.price.shift(1) / self.price - 1
        stock_returns = self.price / self.price.shift(1) - 1  # date under ascending order
        # self.stock_return = self.stock_price.apply(get_stock_return)
        stock_returns = stock_returns.dropna()
        if if_print:
            print("Return Matrix is \n", stock_returns)
        return stock_returns

    def get_equal_weighted_return(self, if_print=False):
        equal_weighted_return = self.returns.stack().mean(axis = 1)
        if if_print:
            print("Equal weighted portfolio return (benchmark): ", equal_weighted_return)
        return equal_weighted_return

    def get_equal_weighted_std(self, if_print=False):
        equal_weighted_std = np.std(self.returns.mean(axis = 1))
        if if_print:
            print("Equal weighted portfolio std (benchmark): ",equal_weighted_std)
        return equal_weighted_std

    def get_equal_weighted_daily_return(self):
        # todo: daily return
        pass

    def get_affliate_return_from_database(self,tickers):
        Q_affiliate_list = get_RA_views(tickers,host='localhost:27017')
        return Q_affiliate_list

    def get_risk_aversion_coefficient(self, if_print=False):
        risk_aversion = (self.get_equal_weighted_return() - self.risk_free_rate) / (self.get_equal_weighted_std() ** 2)
        if if_print:
            print("risk aversion coefficient is ", risk_aversion)
        return risk_aversion


def main():
    # csv_file_path = r"C:\My Files\Study\17 Spring\800 - Special Problems in FE (MS)\Code\FE-800\csv\test.csv"
    # import_price_data = pd.read_csv(filepath_or_buffer=csv_file_path, index_col=0).dropna()
    # data=Data(import_price_data)
    # print(data.returns.columns)
    ETF_tickers = ['VTI', 'ITOT', 'SCHB', 'VEA', 'IXUS', 'SCHF', 'VWO', 'IEMG', 'SCHE', 'VIG', 'DVY', 'SCHD', 'VGSH',
                   'IEF', 'TLT', 'MUB', 'TFI', 'PZA', 'SCHP', 'TIP', 'IPE', 'XLE', 'DJP', 'VDE']
    data = Data(ETF_tickers)
    path = r"C:\My Files\Study\17 Spring\800 - Special Problems in FE (MS)\Code\FE-800"
    print(data.capital_weights)

if __name__ == "__main__":
    main()
