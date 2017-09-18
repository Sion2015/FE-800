# import cvxopt as opt
# from cvxopt import blas, solvers
from Views import *


class BlackLitterman:
    def __init__(self, Data, confidence_level):
        # original data
        self.data = Data
        self.stock_price = Data.price
        self.num = len(Data.returns.columns)
        self.stock_return = Data.returns
        self.covariance_matrix = self.get_covariance_matrix()


        # input for the Implied Excess Equilibrium Return
        self.risk_aversion_coefficient = 1

        # self.risk_aversion_coefficient = Data.get_risk_aversion_coefficient()
        self.capital_weights = Data.capital_weights
        self.equilibrium_expected_return = self.get_equilibrium_expected_return()

        # affiliate long-term expected return
        self.affiliate_return = Data.affiliate_return

        # input for the Combined Expected Return
        self.base_level = 1/2
        self.P_matrix = np.diag(np.ones(len(Data.tickers)))
        self.Q_matrix = np.matrix(self.affiliate_return).transpose()
        self.if_ARIMA = False
        self.view_count = 0
        self.omega = self.get_omega_array(self.P_matrix, self.Q_matrix, confidence_level)
        self.Omega = np.diag(self.omega)

        # result of Black-Litterman
        self.combined_return, self.combined_covariance_matrix = self.calc_blacklitterman()

    def get_covariance_matrix(self, if_print=False):
        # self.stock_return = get_stock_return(self.stock_price)
        covariance_matrix = np.cov(self.stock_return, rowvar=False)
        if if_print:
            print("Covariance Matrix is \n", covariance_matrix)
        return covariance_matrix

    def get_equilibrium_expected_return(self, if_print=False):
        equilibrium_expected_return = self.risk_aversion_coefficient * np.dot(self.covariance_matrix, self.capital_weights)
        if if_print:
            print("Equilibrium Expected Return is \n", equilibrium_expected_return)
        return equilibrium_expected_return

    def get_omega_array(self, P_matrix, Q_matrix, confidence_level):
        # confidence level is determined by http://globalriskguard.com/resources/assetman/assetall_0004.pdf
        covariance_matrix = self.covariance_matrix
        P_Sigma_inv_P = P_matrix.dot(covariance_matrix.dot(P_matrix.transpose())).sum()
        calibration_factor = P_Sigma_inv_P / (1 / self.base_level)

        K = len(Q_matrix)
        var = []
        for i in range(K):
            var.append(calibration_factor * 1 / confidence_level)
        return var

    def __call__(self, new_data: Data):
        self.stock_price = new_data.price
        self.stock_return = new_data.returns
        self.covariance_matrix = self.get_covariance_matrix()
        self.equilibrium_expected_return = self.get_equilibrium_expected_return()
        if self.if_ARIMA:
            Q_Arima_list = recalculate_ARIMA(new_data)
            self.Q_matrix = np.matrix(self.affiliate_return + Q_Arima_list).transpose()
        self.combined_return, self.combined_covariance_matrix = self.calc_blacklitterman()

        return self

    def add_arima(self, confidence_level):
        self.if_ARIMA = True
        new_P_matrix = np.diag(np.ones(len(self.data.tickers)))
        new_Q_matrix = get_Q_matrix(recalculate_ARIMA(self.data))
        self.P_matrix = np.concatenate((self.P_matrix, new_P_matrix))
        self.Q_matrix = np.concatenate((self.Q_matrix, new_Q_matrix))
        self.omega = self.omega + self.get_omega_array(new_P_matrix, new_Q_matrix, confidence_level)
        self.Omega = np.diag(self.omega)
        return self

    def add_views(self, new_P, new_Q, new_confidence_level):
        self.P_matrix = np.concatenate((self.P_matrix, new_P))
        self.Q_matrix = np.concatenate((self.Q_matrix, new_Q))
        self.omega = self.omega + self.get_omega_array(new_P, new_Q, new_confidence_level)
        self.Omega = np.diag(self.omega)
        self.view_count += 1
        return self

    def calc_blacklitterman(self):
        # Input:
            # tau: a scalar
            # Sigma: the covariance matrix of excess returns (N * N)
            # P: a matrix that identifies the assets involved in the views(K * N or 1 * N)
            # Omega: a diagonal covariance matrix of error terms from the expressed views
            #        representing the uncertainty in each view(K * K)
            # Pi: Implied Equilibrium Return(N * 1)
            # Q: view vector
        # todo: modify based on the view
        # todo: add confidence level

        # P = np.diag(np.ones(self.num))
        # K = len(self.views)  # need a function

        # base_level = 1/2
        # confidence_level = 0.6
        # P_Sigma_inv_P = P.dot(self.covariance_matrix.dot(P.transpose()))
        # calibration_factor = P_Sigma_inv_P / (1 / base_level)
        # var = []
        # for i in range(K):
        #     # var.append(1/960 * (P[i].dot(self.covariance_matrix.dot(P[i].transpose()))))
        #     var.append(calibration_factor * 1 / confidence_level)      # confidence level set to 60%
        # Omega = np.diag(var)
        # # Omega = np.diag((np.repeat([1],[self.num]))) # need a function

        P = self.P_matrix
        Omega = self.Omega

        tau_Sigma_inv = np.linalg.inv(self.risk_aversion_coefficient * self.covariance_matrix)
        P_Omega_inv_P = (P.transpose().dot(np.linalg.inv(Omega))).dot(P)
        tau_Sigma_inv_Pi = np.dot(tau_Sigma_inv,self.equilibrium_expected_return)
        P_Omega_inv_Q = (P.transpose().dot(np.linalg.inv(Omega))).dot(self.Q_matrix)

        combined_return = np.dot(np.linalg.inv(tau_Sigma_inv + P_Omega_inv_P), (tau_Sigma_inv_Pi + P_Omega_inv_Q))
        combined_covariance_matrix = self.covariance_matrix + np.linalg.inv(tau_Sigma_inv + P_Omega_inv_P)
        return combined_return, combined_covariance_matrix
    #
    # def optimal_portfolio(self,
    #                       expected_return= object(),
    #                       covariance_matrix= object()):
    #     n = self.num
    #     # returns = np.asmatrix(self.stock_return.transpose())
    #
    #     N = 100
    #     mus = [10 ** (5.0 * t / N - 1.0) for t in range(N)]
    #
    #     # Convert to cvxopt matrices
    #     # S = opt.matrix(np.cov(returns))
    #     # pbar = opt.matrix(np.mean(returns, axis=1))
    #     if expected_return is object():
    #         pbar = opt.matrix(self.combined_return)
    #     else:
    #         pbar = opt.matrix(expected_return)
    #
    #     if covariance_matrix is object():
    #         S = opt.matrix(self.combined_covariance_matrix)
    #     else:
    #         S = opt.matrix(covariance_matrix)
    #
    #     # Create constraint matrices
    #     G = -opt.matrix(np.eye(n))  # negative n x n identity matrix
    #     h = opt.matrix(0.0, (n, 1))
    #     A = opt.matrix(1.0, (1, n))
    #     b = opt.matrix(1.0)
    #
    #     # Calculate efficient frontier weights using quadratic programming
    #     portfolios = [solvers.qp(mu * S, -pbar, G, h, A, b)['x']
    #                   for mu in mus]
    #     # CALCULATE RISKS AND RETURNS FOR FRONTIER
    #     returns = [blas.dot(pbar, x) for x in portfolios]
    #     risks = [np.sqrt(blas.dot(x, S * x)) for x in portfolios]
    #     # CALCULATE THE 2ND DEGREE POLYNOMIAL OF THE FRONTIER CURVE
    #     m1 = np.polyfit(returns, risks, 2)
    #     x1 = np.sqrt(m1[2] / m1[0])
    #     # CALCULATE THE OPTIMAL PORTFOLIO
    #     wt = solvers.qp(opt.matrix(x1 * S), -pbar, G, h, A, b)['x']
    #     return np.asarray(wt), returns, risks


def main():
    pass

if __name__ == "__main__":
    main()
