import numpy as np


class View:
    def __init__(self, Data, Q_matrix, P_matrix, confidence_level):
        self.data = Data
        self.num = len(Data.returns.columns)
        self.confidence_level = confidence_level
        self.P_matrix = P_matrix
        self.Q_matrix = Q_matrix
        self.base_level = 1/2
        self.omega = self.get_omega_array()
        self.Omega = self.get_Omega_matrix()

    def get_omega_array(self):
            # confidence level is determined by http://globalriskguard.com/resources/assetman/assetall_0004.pdf

        covariance_matrix = self.data.get_covariance_matrix()
        P_Sigma_inv_P = self.P_matrix.dot(covariance_matrix.dot(self.P_matrix.transpose())).sum()
        calibration_factor = P_Sigma_inv_P / (1 / self.base_level)
        print(calibration_factor)

        K = len(self.Q_matrix)
        var = []
        for i in range(K):
            var.append(calibration_factor * 1 / self.confidence_level)
        # Omega = np.diag(var)
        return var

    def get_Omega_matrix(self):
        Omega = np.diag(self.omega)
        return Omega

    def __call__(self, new_View):
        self.P_matrix = np.concatenate((self.P_matrix, new_View.P_matrix))
        self.Q_matrix = np.concatenate((self.Q_matrix, new_View.Q_matrix))
        self.omega = self.omega + new_View.omega
        self.Omega = self.get_Omega_matrix()
        return self

def main():
    for i in range(1,12):
        print("2013-{:02}-01".format(i))


if __name__ == "__main__":
    main()