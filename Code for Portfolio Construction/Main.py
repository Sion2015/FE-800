from Portfolio import *
from Black_Litterman import *

def main():
    ETF_tickers = ['VTI', 'VEA', 'VWO', 'VIG', 'XLE', 'SCHP', 'MUB', 'VGSH']
    # ETF_tickers = ['VTI', 'SCHB', 'VEA', 'IXUS', 'IEMG', 'DVY', 'SCHD', 'VGSH',
    #                'IEF', 'MUB', 'TFI', 'PZA', 'SCHP', 'DJP', 'VDE']

    build_start_date = "2013-01-01"
    build_end_date = "2016-01-04"

    # initial_data = Data(ETF_tickers, start_date=build_start_date, end_date=build_end_date, host="localhost:27017")
    # # Q_ARIMA = np.matrix([-0.004413366667244781, -0.004424015834531522, -0.005690773822704929, -0.005734796756841397, -0.005472827242047887, -0.0052321808471597914, -0.004364895249574041, -0.007686644049192283, -0.007867415841404813, -0.007274183151079553, -0.007435270639293345, -0.0074720911273814155, -0.007135610440594298, -0.007085256344163254, -0.009426469934431069]).transpose()
    # # Q_affiliate = np.matrix([0.000449417,0.000449417,0.00342539500,0.00342539500,0.004385759898,0.000309345023,0.000309345023,0.000167661891,-0.000442237962,0.002160696, 0.0021606969, 0.0021606969, 0.0006686066, 0.0011797109, 0.0011797109]).transpose()
    # initial_blacklitterman = BlackLitterman(initial_data, 1)#.add_arima(0.5)
    # initial_portfolio = Portfolio(initial_data, initial_blacklitterman, risk_tolerance=0.5, host=initial_data.host)
    # initial_benchmark = Portfolio(initial_data, initial_blacklitterman, risk_tolerance=0.7, host=initial_data.host, if_benchmark=True)
    # print(initial_portfolio.back_testing_result)
    # print(initial_benchmark.back_testing_result)

    return_list = []
    vol_list = []
    for tau in np.arange(0.0, 3.0, 0.05):
        initial_data = Data(ETF_tickers, start_date=build_start_date, end_date=build_end_date, host="localhost:27017")
        initial_blacklitterman = BlackLitterman(initial_data, 0.8)  # parameter  confidence level of affiliate. same as input
        initial_portfolio = Portfolio(initial_data, initial_blacklitterman, risk_tolerance=tau, host=initial_data.host,if_backtesting=False)


        return_list.append(initial_portfolio.annual_return)
        vol_list.append(initial_portfolio.annual_vol)

    print(return_list)
    print(vol_list)


    # for i in np.arange(1.5, 3.0, 0.05):
    #     initial_data = Data(ETF_tickers, start_date=build_start_date, end_date=build_end_date, host="localhost:27017")
    #     initial_blacklitterman = BlackLitterman(initial_data, 0.8)#.add_arima(0.5)
    #     initial_portfolio = Portfolio(initial_data, initial_blacklitterman, risk_tolerance=i, host=initial_data.host)
    #
    #     portfolio_return = np.matrix(initial_portfolio.annual_return)
    #     portfolio_vol = np.matrix(initial_portfolio.annual_vol)
    #     portfolio_sharpe_ratio = np.matrix(initial_portfolio.sharpe_ratio)
    #     rebalance_time = np.matrix(initial_portfolio.rebalance_times)
    #
    #     portfolio_VaR = np.matrix(calculate_VaR(portfolio_vol/np.sqrt(252)))
    #     portfolio_performance= initial_portfolio.porfolio_porformance
    #     temp_result = np.concatenate((initial_portfolio.target_weights,portfolio_return,portfolio_vol,portfolio_sharpe_ratio,rebalance_time),axis = 0)
    #     result = np.concatenate((result, temp_result), axis=1)
    #
    # np.savetxt(r"csv\result0.82.csv", result, delimiter=",")
    # print(result)









    #
    # backtesting_data = Data(ETF_tickers, start_date="2013-01-01", end_date="2017-01-01")  # 4 years data
    # for i in range(0,len(backtesting_data.price.index),21):  # monthly calculate
    #     price_matrix = backtesting_data.price[0+i:252+i,]
    #
    #
    # for i in range(1,12):
    #     temp_data = Data(ETF_tickers, start_date = "2013-{:02}-01".format(i), end_date = "2016-{:02}-01".format(i))
    #     temp_blacklitterman = BlackLitterman(temp_data, P_matrix, Q_affiliate, 0.8)
    #     temp_portfolio = Portfolio(temp_data, temp_blacklitterman, risk_tolerance=5)
    #     weights = np.concatenate((weights,temp_portfolio.weights), axis=-1)
    #
    # print(weights)
    #
    # pd.DataFrame(weights).to_csv("weights test1.csv")
    #
    # print_data = Data(ETF_tickers, start_date="2013-01-01", end_date="2017-01-01").price
    # print_data.to_csv("price test.csv")
    #
    # #
    # # for i in range(30):
    # #     initial_portfolio = Portfolio(initial_data, initial_blacklitterman, risk_tolerance=i)
    # #     print(initial_portfolio.weights)

if __name__ == "__main__":
    main()

