from Black_Litterman import *
import scipy.optimize
from Views import *
import numpy as np
from pyfolio import timeseries


class Portfolio:
    def __init__(self, data:Data, strategy:BlackLitterman, risk_tolerance, host, account_deposit=100000,
                 if_backtesting=True, frequency="Monthly", if_benchmark=False):
        self.if_benchmark = if_benchmark
        self.num = data.num
        self.data = data
        self.risk_free_rate = data.risk_free_rate
        self.price_data = data.price
        self.return_data = data.returns
        self.host = host

        self.blacklitterman = strategy
        self.expected_return = np.matrix(strategy.combined_return)
        self.covariance_matrix = np.matrix(strategy.combined_covariance_matrix)

        self.risk_tolerance = risk_tolerance
        self.equal_weighted_weight = np.matrix(np.ones([self.num]) / self.num).transpose()
        if self.if_benchmark:
            self.target_weights = self.equal_weighted_weight
        else:
            self.target_weights = self.solve_weights(self.risk_tolerance)

        self.rebalance_times = 0

        if if_backtesting:
            self.drift_limit = 0.025
            self.initial_cash = account_deposit
            self.total_value = self.initial_cash
            self.day_count = 0

            self.shares = np.floor(self.total_value * self.target_weights.A1 / self.price_data.iloc[-1])
            self.residual_cash = self.total_value - self.calculate_stock_value(self.price_data.iloc[-1]).sum()

            self.back_testing_result = self.run_back_testing(frequency)

        else:
            self.annual_return = self.get_portfolio_return() * 252
            self.annual_vol = self.get_portfolio_std() * np.sqrt(252)
            print(self.annual_return)
            print(self.annual_vol)

            # self.test = self.mean_variance_optimization(self.risk_tolerance)
            # print(self.test)

        # self.weights = self.mean_variance_optimization(risk_tolerance)
        #self.result =         # todo: combine the result

        # self.shares = np.floor(self.initial_cash * self.weights / data[-1, :])


    def mean_variance_optimization(self, risk_aversion_p):
        mu = np.matrix(self.expected_return).transpose()
        Q = np.matrix(self.covariance_matrix)
        l = np.matrix(np.repeat([1], self.num))
        c = np.matrix([1])
        O = np.matrix([0])

        A = np.concatenate((Q, l), axis=0)
        B = np.concatenate((np.transpose(l), O), axis=0)
        C = np.column_stack((A, B))
        D = np.concatenate(((risk_aversion_p * np.transpose(mu)), c), axis=0)

        E = np.dot(np.linalg.inv(C), D)
        weights_result = np.delete(E, len(E) - 1, 0)
        return weights_result

    def get_boundary_constraint(self):
        b = []
        for e in range(self.num):
            if get_asset_class(self.host, self.data.tickers[e]) == 'TREASURY INFLATION-PROTECTED SECURITIES (TIPS)':
                b.append((0.00, 0.35))
                # b[e] = (0.00, 0.35)
            else:
                b.append((0.05, 0.35))
                # b[e] = (0.05, 0.35)
        return b

    def solve_weights(self, risk_aversion_p):
        def fitness(weights, return_array,
                    covariance_matrix, risk_free_rate, risk_aversion_p):
            # Method 1: Maximize sharpe ratio
            # mean = np.dot(return_array.transpose(), weights)
            # var = np.dot(np.dot(weights.transpose(), covariance_matrix), weights)
            # util = (mean - risk_free_rate) / np.sqrt(var)
            # return 1 / util

            # Method 2: maximize O_max = tau * mu_P - 1/2 * sigma_P ^ 2
            #           based on Levy and Markowitz[1979]
            util = 1/2 * np.dot(weights.transpose(), covariance_matrix).dot(weights) - risk_aversion_p * np.dot(return_array.transpose(), weights)
            return util
        initial_weights = self.equal_weighted_weight
        # b_ = [(0.05, 0.35) for i in range(self.num)]
        b_ = self.get_boundary_constraint()
        c_ = ({'type': 'eq', "fun": lambda x: np.sum(x) - 1.0})
        optimized = scipy.optimize.minimize(fitness,initial_weights,
                                            args=(self.expected_return,self.covariance_matrix,self.risk_free_rate, risk_aversion_p),
                                            method="SLSQP", constraints=c_, bounds=b_,
                                            options={"disp": False, "eps": 1e-11, "ftol": 1e-11})
        if not optimized.success:
            raise BaseException(optimized.message)
        weight = np.matrix(optimized.x).transpose()
        # print(1/2 * np.dot(weight.transpose(), self.covariance_matrix)).dot(weight)
        # print(1/2 * weight.transpose().dot(self.covariance_matrix).dot(weight))
        # print(np.dot(self.expected_return.transpose(), weight))
        return weight

    def calculate_stock_value(self,daily_price_matrix):
        stock_value_matrix = np.dot(daily_price_matrix, np.diag(self.shares))
        return stock_value_matrix

    def calculate_total_value(self,daily_price_matrix):
        self.total_value = self.calculate_stock_value(daily_price_matrix).sum() + self.residual_cash
        return self.total_value

    def calculate_drift(self,daily_price_matrix) :
        current_weights = self.calculate_stock_value(daily_price_matrix) / self.total_value
        drift = abs(self.target_weights.A1 - current_weights).sum() / 2
        return drift

    def rebalance(self, temp_data):
        self.shares = np.floor(self.total_value * self.target_weights.A1 / temp_data.price.iloc[-1])
        self.residual_cash = self.total_value - self.calculate_stock_value(temp_data.price.iloc[-1]).sum()
        self.rebalance_times += 1

    def recalculate_target_weight(self, temp_data):
        temp_blacklitterman = self.blacklitterman(temp_data)
        self.expected_return = np.matrix(temp_blacklitterman.combined_return)
        self.covariance_matrix = np.matrix(temp_blacklitterman.combined_covariance_matrix)
        if not self.if_benchmark:
            self.target_weights = self.solve_weights(self.risk_tolerance)

    def daily_update(self, daily_price, if_monthly = True, save_to_database = True):
        date = daily_price.name
        daily_shares = self.shares
        daily_target_weights = self.target_weights.A1.tolist()
        daily_total_value = self.calculate_total_value(daily_price)
        daily_residual_cash = self.residual_cash
        daily_drift = self.calculate_drift(daily_price)
        self.day_count += self.day_count

        if if_monthly:
            if self.day_count == 22:
                end_date = daily_price.name
                start_date = pd.date_range(end = end_date,periods = 4, freq = "365D").tolist()[0]
                temp_data = Data(tickers=self.data.tickers, start_date= start_date, end_date= end_date)
                self.recalculate_target_weight(temp_data)
                self.day_count = 0

        if daily_drift > self.drift_limit:
            end_date = daily_price.name
            start_date = pd.date_range(end = end_date,periods = 4, freq = "365D").tolist()[0]
            temp_data = Data(tickers=self.data.tickers, start_date= start_date, end_date= end_date, host=self.host)
            self.recalculate_target_weight(temp_data)
            self.rebalance(temp_data)

        # output
        if save_to_database:
            pass
        else:
            print(daily_shares)
            print(daily_total_value)
            print(daily_target_weights)
            print(daily_drift)
            print(daily_residual_cash)

        weights = pd.Series(daily_target_weights, index=self.data.tickers)
        analysis = pd.Series({"daily_total_value": daily_total_value,
                          "daily_residual_cash": daily_residual_cash,
                          "daily_drift": daily_drift})
        result = weights.append(analysis)
        return result

    def run_back_testing(self, frequency = "Monthly", if_plot = False, if_csv = False):
        price_data = Data(tickers=self.data.tickers, start_date="2016-01", end_date="2016-12", host=self.host).price
        # result = pd.DataFrame(self.daily_update(daily_price = price_data.iloc[0]),
        #                       columns=["date","daily_total_value", "daily_residual_cash", "daily_drift"]).set_index("date")

        result = price_data.apply(lambda row: self.daily_update(row), axis=1)

        self.portfolio_daily_return = calculate_daily_return(result["daily_total_value"])
        self.calculate_portfolio_performance()

        print(self.risk_tolerance)
        print("annual_return = %f, annual_vol = %f, sharpe_ratio = %f" % (self.annual_return, self.annual_vol, self.sharpe_ratio))


        if if_plot:
            # plot()
            pass
        if if_csv:
            # write to csv()
            pass
        return result

    def get_portfolio_std(self):
        portfolio_var = (np.transpose(self.target_weights).dot(self.covariance_matrix)).dot(self.target_weights)
        return np.sqrt(portfolio_var.item())

    def get_portfolio_return(self):
        portfolio_return = self.expected_return.transpose().dot(self.target_weights)
        return portfolio_return.item()

    def get_historical_return(self):
        historical_return_matrix = self.return_data.dot(self.target_weights.transpose())
        return historical_return_matrix

    def get_portfolio_performance(self):
        portfolio_return = self.get_portfolio_return()
        portfolio_std = self.get_portfolio_std()
        sharpe_ratio = (self.get_portfolio_return() - self.data.risk_free_rate) / self.get_portfolio_std()
        # todo: tracking_error = get.equal_weighted_return
        # todo: information_ratio
        return portfolio_return, portfolio_std, sharpe_ratio

    def get_portfolio_daily_return(self):
        daily_return = self.return_data.dot(self.target_weights)
        return daily_return

    def set_drift_limit(self, drift_limit):
        self.drift_limit = drift_limit

    def set_risk_tolerance(self, risk_tolerance):
        self.risk_tolerance = risk_tolerance

    def set_risk_free_rate(self, risk_free_rate):
        self.risk_free_rate = risk_free_rate

    def calculate_portfolio_performance(self):
        self.annual_return = calculate_annual_return(self.portfolio_daily_return)
        self.annual_vol = calculate_anual_vol(self.portfolio_daily_return)
        self.sharpe_ratio = calculate_sharpe_ratio(self.portfolio_daily_return)


        self.max_drawdown = timeseries.max_drawdown(self.portfolio_daily_return)
        self.VaR = calculate_VaR(self.annual_vol / np.sqrt(252))
        # daily, you can change the parameter in calculate_VaR()
        self.sortino_ratio = timeseries.sortino_ratio(self.portfolio_daily_return)


def main():
    pass

if __name__ == "__main__":
    main()
