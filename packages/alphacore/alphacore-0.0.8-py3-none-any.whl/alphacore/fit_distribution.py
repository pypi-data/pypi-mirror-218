from alphacore.utils import (
    fitters_input_checking,
    LS_optimization,
    MLE_optimization,
    plotting_positions,
    anderson_darling,
    colorprint,
)
from alphacore.distributions import Weibull_Distribution, Normal_Distribution
from autograd.differential_operators import hessian
import scipy.stats as ss
import numpy as np
from numpy.linalg import LinAlgError
import autograd.numpy as anp
from autograd.scipy.special import erf


class Fit_Weibull_2P:
    """
    Fits a two parameter Weibull distribution (alpha,beta) to the data provided.

    Parameters
    ----------
    failures : array, list
        The failure data. Must have at least 2 elements if force_beta is not
        specified or at least 1 element if force_beta is specified.
    right_censored : array, list, optional
        The right censored data. Optional input. Default = None.
    method : str, optional
        The method used to fit the distribution. Must be either 'MLE' (maximum
        likelihood estimation), 'LS' (least squares estimation), 'RRX' (Rank
        regression on X), or 'RRY' (Rank regression on Y). LS will perform both
        RRX and RRY and return the better one. Default is 'MLE'.
    optimizer : str, optional
        The optimization algorithm used to find the solution. Must be either
        'TNC', 'L-BFGS-B', 'nelder-mead', or 'powell'. Specifying the optimizer
        will result in that optimizer being used. To use all of these specify
        'best' and the best result will be returned. The default behaviour is to
        try each optimizer in order ('TNC', 'L-BFGS-B', 'nelder-mead', and
        'powell') and stop once one of the optimizers finds a solution. If the
        optimizer fails, the initial guess will be returned.
        For more detail see the `documentation
        <https://reliability.readthedocs.io/en/latest/Optimizers.html>`_.
    CI : float, optional
        confidence interval for estimating confidence limits on parameters. Must
        be between 0 and 1. Default is 0.95 for 95% CI.
    CI_type : str, None, optional
        This is the confidence bounds on time or reliability shown on the plot.
        Use None to turn off the confidence intervals. Must be either 'time',
        'reliability', or None. Default is 'time'. Some flexibility in names is
        allowed (eg. 't', 'time', 'r', 'rel', 'reliability' are all valid).
    force_beta : float, int, optional
        Used to specify the beta value if you need to force beta to be a certain
        value. Used in ALT probability plotting. Optional input. If specified it
        must be > 0.

    Returns
    -------
    alpha : float
        the fitted Weibull_2P alpha parameter
    beta : float
        the fitted Weibull_2P beta parameter
    alpha_SE : float
        the standard error (sqrt(variance)) of the parameter
    beta_SE :float
        the standard error (sqrt(variance)) of the parameter
    Cov_alpha_beta : float
        the covariance between the parameters
    alpha_upper : float
        the upper CI estimate of the parameter
    alpha_lower : float
        the lower CI estimate of the parameter
    beta_upper : float
        the upper CI estimate of the parameter
    beta_lower : float
        the lower CI estimate of the parameter
    loglik : float
        Log Likelihood (as used in Minitab and Reliasoft)
    loglik2 : float
        LogLikelihood*-2 (as used in JMP Pro)
    AICc : float
        Akaike Information Criterion
    BIC : float
        Bayesian Information Criterion
    AD : float
        the Anderson Darling (corrected) statistic (as reported by Minitab)
    distribution : object
        a Weibull_Distribution object with the parameters of the fitted
        distribution

    Notes
    -----
    If the fitting process encounters a problem a warning will be printed. This
    may be caused by the chosen distribution being a very poor fit to the data
    or the data being heavily censored. If a warning is printed, consider trying
    a different optimizer.
    """

    def __init__(
        self,
        failures=None,
        right_censored=None,
        CI=0.95,
        quantiles=None,
        CI_type="time",
        method="MLE",
        optimizer=None,
        force_beta=None,
    ):

        inputs = fitters_input_checking(
            dist="Weibull_2P",
            failures=failures,
            right_censored=right_censored,
            method=method,
            optimizer=optimizer,
            CI=CI,
            quantiles=quantiles,
            force_beta=force_beta,
            CI_type=CI_type,
        )
        failures = inputs.failures
        right_censored = inputs.right_censored
        CI = inputs.CI
        method = inputs.method
        optimizer = inputs.optimizer
        force_beta = inputs.force_beta
        CI_type = inputs.CI_type
        self.gamma = 0

        # Obtain least squares estimates
        if method == "MLE":
            LS_method = "LS"
        else:
            LS_method = method
        LS_results = LS_optimization(
            func_name="Weibull_2P",
            LL_func=Fit_Weibull_2P.LL,
            failures=failures,
            right_censored=right_censored,
            method=LS_method,
            force_shape=force_beta,
            LL_func_force=Fit_Weibull_2P.LL_fb,
        )

        # least squares method
        if method in ["LS", "RRX", "RRY"]:
            self.alpha = LS_results.guess[0]
            self.beta = LS_results.guess[1]
            self.method = str("Least Squares Estimation (" + LS_results.method + ")")
            self.optimizer = None
        # maximum likelihood method
        elif method == "MLE":
            MLE_results = MLE_optimization(
                func_name="Weibull_2P",
                LL_func=Fit_Weibull_2P.LL,
                initial_guess=[LS_results.guess[0], LS_results.guess[1]],
                failures=failures,
                right_censored=right_censored,
                optimizer=optimizer,
                force_shape=force_beta,
                LL_func_force=Fit_Weibull_2P.LL_fb,
            )
            self.alpha = MLE_results.scale
            self.beta = MLE_results.shape
            self.method = "Maximum Likelihood Estimation (MLE)"
            self.optimizer = MLE_results.optimizer

        # confidence interval estimates of parameters. This uses the Fisher
        # Matrix so it can be applied to both MLE and LS estimates.
        Z = -ss.norm.ppf((1 - CI) / 2)
        params = [self.alpha, self.beta]
        if force_beta is None:
            hessian_matrix = hessian(Fit_Weibull_2P.LL)(
                np.array(tuple(params)),
                np.array(tuple(failures)),
                np.array(tuple(right_censored)),
            )
            try:
                covariance_matrix = np.linalg.inv(hessian_matrix)
                self.alpha_SE = abs(covariance_matrix[0][0]) ** 0.5
                self.beta_SE = abs(covariance_matrix[1][1]) ** 0.5
                self.Cov_alpha_beta = covariance_matrix[0][1]
                self.alpha_upper = self.alpha * (
                    np.exp(Z * (self.alpha_SE / self.alpha))
                )
                self.alpha_lower = self.alpha * (
                    np.exp(-Z * (self.alpha_SE / self.alpha))
                )
                self.beta_upper = self.beta * (np.exp(Z * (self.beta_SE / self.beta)))
                self.beta_lower = self.beta * (np.exp(-Z * (self.beta_SE / self.beta)))
            except LinAlgError:
                # this exception is rare but can occur with some optimizers
                colorprint(
                    str(
                        "WARNING: The hessian matrix obtained using the "
                        + self.optimizer
                        + " optimizer is non-invertable for the Weibull_2P model.\n"
                        "Confidence interval estimates of the parameters could not be obtained.\n"
                        "You may want to try fitting the model using a different optimizer."
                    ),
                    text_color="red",
                )
                self.alpha_SE = 0
                self.beta_SE = 0
                self.Cov_alpha_beta = 0
                self.alpha_upper = self.alpha
                self.alpha_lower = self.alpha
                self.beta_upper = self.beta
                self.beta_lower = self.beta

        else:  # this is for when force beta is specified
            hessian_matrix = hessian(Fit_Weibull_2P.LL_fb)(
                np.array(tuple([self.alpha])),
                np.array(tuple(failures)),
                np.array(tuple(right_censored)),
                np.array(tuple([force_beta])),
            )
            try:
                covariance_matrix = np.linalg.inv(hessian_matrix)
                self.alpha_SE = abs(covariance_matrix[0][0]) ** 0.5
                self.beta_SE = 0
                self.Cov_alpha_beta = 0
                self.alpha_upper = self.alpha * (
                    np.exp(Z * (self.alpha_SE / self.alpha))
                )
                self.alpha_lower = self.alpha * (
                    np.exp(-Z * (self.alpha_SE / self.alpha))
                )
                self.beta_upper = self.beta
                self.beta_lower = self.beta
            except LinAlgError:
                # this exception is rare but can occur with some optimizers
                colorprint(
                    str(
                        "WARNING: The hessian matrix obtained using the "
                        + self.optimizer
                        + " optimizer is non-invertable for the Weibull_2P model.\n"
                        "Confidence interval estimates of the parameters could not be obtained.\n"
                        "You may want to try fitting the model using a different optimizer."
                    ),
                    text_color="red",
                )
                self.alpha_SE = 0
                self.beta_SE = 0
                self.Cov_alpha_beta = 0
                self.alpha_upper = self.alpha
                self.alpha_lower = self.alpha
                self.beta_upper = self.beta
                self.beta_lower = self.beta

        self.distribution = Weibull_Distribution(
            alpha=self.alpha,
            beta=self.beta,
            alpha_SE=self.alpha_SE,
            beta_SE=self.beta_SE,
            Cov_alpha_beta=self.Cov_alpha_beta,
            CI=CI,
            CI_type=CI_type,
        )

        # goodness of fit measures
        n = len(failures) + len(right_censored)
        if force_beta is None:
            k = 2
            LL2 = 2 * Fit_Weibull_2P.LL(params, failures, right_censored)
        else:
            k = 1
            LL2 = 2 * Fit_Weibull_2P.LL_fb(params, failures, right_censored, force_beta)
        self.loglik2 = LL2
        self.loglik = LL2 * -0.5
        if n - k - 1 > 0:
            self.AICc = 2 * k + LL2 + (2 * k**2 + 2 * k) / (n - k - 1)
        else:
            self.AICc = "Insufficient data"
        self.BIC = np.log(n) * k + LL2

        x, y = plotting_positions(failures=failures, right_censored=right_censored)
        self.AD = anderson_darling(
            fitted_cdf=self.distribution.CDF(xvals=x, show_plot=False), empirical_cdf=y
        )

    @staticmethod
    def logf(t, a, b):  # Log PDF (2 parameter Weibull)
        return (b - 1) * anp.log(t / a) + anp.log(b / a) - (t / a) ** b

    @staticmethod
    def logR(t, a, b):  # Log SF (2 parameter Weibull)
        return -((t / a) ** b)

    @staticmethod
    def LL(params, T_f, T_rc):
        # log likelihood function (2 parameter weibull)
        LL_f = Fit_Weibull_2P.logf(T_f, params[0], params[1]).sum()
        LL_rc = Fit_Weibull_2P.logR(T_rc, params[0], params[1]).sum()
        return -(LL_f + LL_rc)

    @staticmethod
    def LL_fb(params, T_f, T_rc, force_beta):
        # log likelihood function (2 parameter weibull) FORCED BETA
        LL_f = Fit_Weibull_2P.logf(T_f, params[0], force_beta).sum()
        LL_rc = Fit_Weibull_2P.logR(T_rc, params[0], force_beta).sum()
        return -(LL_f + LL_rc)


class Fit_Normal_2P:
    """
    Fits a two parameter Normal distribution (mu,sigma) to the data provided.
    Note that it will return a fit that may be partially in the negative domain
    (x<0). If you need an entirely positive distribution that is similar to
    Normal then consider using Weibull.

    Parameters
    ----------
    failures : array, list
        The failure data. Must have at least 2 elements if force_sigma is not
        specified or at least 1 element if force_sigma is specified.
    right_censored : array, list, optional
        The right censored data. Optional input. Default = None.
    method : str, optional
        The method used to fit the distribution. Must be either 'MLE' (maximum
        likelihood estimation), 'LS' (least squares estimation), 'RRX' (Rank
        regression on X), or 'RRY' (Rank regression on Y). LS will perform both
        RRX and RRY and return the better one. Default is 'MLE'.
    optimizer : str, optional
        The optimization algorithm used to find the solution. Must be either
        'TNC', 'L-BFGS-B', 'nelder-mead', or 'powell'. Specifying the optimizer
        will result in that optimizer being used. To use all of these specify
        'best' and the best result will be returned. The default behaviour is to
        try each optimizer in order ('TNC', 'L-BFGS-B', 'nelder-mead', and
        'powell') and stop once one of the optimizers finds a solution. If the
        optimizer fails, the initial guess will be returned.
        For more detail see the `documentation
        <https://reliability.readthedocs.io/en/latest/Optimizers.html>`_.
    CI : float, optional
        confidence interval for estimating confidence limits on parameters. Must
        be between 0 and 1. Default is 0.95 for 95% CI.
    CI_type : str, None, optional
        This is the confidence bounds on time or reliability shown on the plot.
        Use None to turn off the confidence intervals. Must be either 'time',
        'reliability', or None. Default is 'time'. Some flexibility in names is
        allowed (eg. 't', 'time', 'r', 'rel', 'reliability' are all valid).
    force_sigma : float, int, optional
        Used to specify the beta value if you need to force sigma to be a
        certain value. Used in ALT probability plotting. Optional input. If
        specified it must be > 0.
    quantiles : bool, str, list, array, None, optional
        quantiles (y-values) to produce a table of quantiles failed with
        lower, point, and upper estimates. Default is None which results in no
        output. To use default array [0.01, 0.05, 0.1,..., 0.95, 0.99] set
        quantiles as either 'auto', True, 'default', 'on'.
        If an array or list is specified then it will be used instead of the
        default array. Any array or list specified must contain values between
        0 and 1.

    Returns
    -------
    mu : float
        the fitted Normal_2P mu parameter
    sigma : float
        the fitted Normal_2P sigma parameter
    mu_SE : float
        the standard error (sqrt(variance)) of the parameter
    sigma_SE :float
        the standard error (sqrt(variance)) of the parameter
    Cov_mu_sigma : float
        the covariance between the parameters
    mu_upper : float
        the upper CI estimate of the parameter
    mu_lower : float
        the lower CI estimate of the parameter
    sigma_upper : float
        the upper CI estimate of the parameter
    sigma_lower : float
        the lower CI estimate of the parameter
    loglik : float
        Log Likelihood (as used in Minitab and Reliasoft)
    loglik2 : float
        LogLikelihood*-2 (as used in JMP Pro)
    AICc : float
        Akaike Information Criterion
    BIC : float
        Bayesian Information Criterion
    AD : float
        the Anderson Darling (corrected) statistic (as reported by Minitab)
    distribution : object
        a Normal_Distribution object with the parameters of the fitted
        distribution
    results : dataframe
        a pandas dataframe of the results (point estimate, standard error,
        lower CI and upper CI for each parameter)
    goodness_of_fit : dataframe
        a pandas dataframe of the goodness of fit values (Log-likelihood, AICc,
        BIC, AD).
    quantiles : dataframe
        a pandas dataframe of the quantiles with bounds on time. This is only
        produced if quantiles is not None. Since quantiles defaults to None,
        this output is not normally produced.
    probability_plot : object
        the axes handle for the probability plot. This is only returned if
        show_probability_plot = True

    Notes
    -----
    If the fitting process encounters a problem a warning will be printed. This
    may be caused by the chosen distribution being a very poor fit to the data
    or the data being heavily censored. If a warning is printed, consider trying
    a different optimizer.
    """

    def __init__(
        self,
        failures=None,
        right_censored=None,
        CI=0.95,
        quantiles=None,
        optimizer=None,
        CI_type="time",
        method="MLE",
        force_sigma=None,
    ):

        inputs = fitters_input_checking(
            dist="Normal_2P",
            failures=failures,
            right_censored=right_censored,
            method=method,
            optimizer=optimizer,
            CI=CI,
            quantiles=quantiles,
            force_sigma=force_sigma,
            CI_type=CI_type,
        )
        failures = inputs.failures
        right_censored = inputs.right_censored
        CI = inputs.CI
        method = inputs.method
        optimizer = inputs.optimizer
        force_sigma = inputs.force_sigma
        CI_type = inputs.CI_type

        # Obtain least squares estimates
        if method == "MLE":
            LS_method = "LS"
        else:
            LS_method = method
        LS_results = LS_optimization(
            func_name="Normal_2P",
            LL_func=Fit_Normal_2P.LL,
            failures=failures,
            right_censored=right_censored,
            method=LS_method,
            force_shape=force_sigma,
            LL_func_force=Fit_Normal_2P.LL_fs,
        )

        # least squares method
        if method in ["LS", "RRX", "RRY"]:
            self.mu = LS_results.guess[0]
            self.sigma = LS_results.guess[1]
            self.method = str("Least Squares Estimation (" + LS_results.method + ")")
            self.optimizer = None
        # maximum likelihood method
        elif method == "MLE":
            MLE_results = MLE_optimization(
                func_name="Normal_2P",
                LL_func=Fit_Normal_2P.LL,
                initial_guess=[LS_results.guess[0], LS_results.guess[1]],
                failures=failures,
                right_censored=right_censored,
                optimizer=optimizer,
                force_shape=force_sigma,
                LL_func_force=Fit_Normal_2P.LL_fs,
            )
            self.mu = MLE_results.scale
            self.sigma = MLE_results.shape
            self.method = "Maximum Likelihood Estimation (MLE)"
            self.optimizer = MLE_results.optimizer

        # confidence interval estimates of parameters
        Z = -ss.norm.ppf((1 - CI) / 2)
        params = [self.mu, self.sigma]
        if force_sigma is None:
            hessian_matrix = hessian(Fit_Normal_2P.LL)(
                np.array(tuple(params)),
                np.array(tuple(failures)),
                np.array(tuple(right_censored)),
            )
            try:
                covariance_matrix = np.linalg.inv(hessian_matrix)
                self.mu_SE = abs(covariance_matrix[0][0]) ** 0.5
                self.sigma_SE = abs(covariance_matrix[1][1]) ** 0.5
                self.Cov_mu_sigma = covariance_matrix[0][1]
                self.mu_upper = self.mu + (
                    Z * self.mu_SE
                )  # these are unique to normal and lognormal mu params
                self.mu_lower = self.mu + (-Z * self.mu_SE)
                self.sigma_upper = self.sigma * (
                    np.exp(Z * (self.sigma_SE / self.sigma))
                )
                self.sigma_lower = self.sigma * (
                    np.exp(-Z * (self.sigma_SE / self.sigma))
                )
            except LinAlgError:
                # this exception is rare but can occur with some optimizers
                colorprint(
                    str(
                        "WARNING: The hessian matrix obtained using the "
                        + self.optimizer
                        + " optimizer is non-invertable for the Normal_2P model.\n"
                        "Confidence interval estimates of the parameters could not be obtained.\n"
                        "You may want to try fitting the model using a different optimizer."
                    ),
                    text_color="red",
                )
                self.mu_SE = 0
                self.sigma_SE = 0
                self.Cov_mu_sigma = 0
                self.mu_upper = self.mu
                self.mu_lower = self.mu
                self.sigma_upper = self.sigma
                self.sigma_lower = self.sigma

        else:
            hessian_matrix = hessian(Fit_Normal_2P.LL_fs)(
                np.array(tuple([self.mu])),
                np.array(tuple(failures)),
                np.array(tuple(right_censored)),
                np.array(tuple([force_sigma])),
            )
            try:
                covariance_matrix = np.linalg.inv(hessian_matrix)
                self.mu_SE = abs(covariance_matrix[0][0]) ** 0.5
                self.sigma_SE = 0
                self.Cov_mu_sigma = 0
                self.mu_upper = self.mu + (
                    Z * self.mu_SE
                )  # these are unique to normal and lognormal mu params
                self.mu_lower = self.mu + (-Z * self.mu_SE)
                self.sigma_upper = self.sigma
                self.sigma_lower = self.sigma
            except LinAlgError:
                # this exception is rare but can occur with some optimizers
                colorprint(
                    str(
                        "WARNING: The hessian matrix obtained using the "
                        + self.optimizer
                        + " optimizer is non-invertable for the Normal_2P model.\n"
                        "Confidence interval estimates of the parameters could not be obtained.\n"
                        "You may want to try fitting the model using a different optimizer."
                    ),
                    text_color="red",
                )
                self.mu_SE = 0
                self.sigma_SE = 0
                self.Cov_mu_sigma = 0
                self.mu_upper = self.mu
                self.mu_lower = self.mu
                self.sigma_upper = self.sigma
                self.sigma_lower = self.sigma

        self.distribution = Normal_Distribution(
            mu=self.mu,
            sigma=self.sigma,
            mu_SE=self.mu_SE,
            sigma_SE=self.sigma_SE,
            Cov_mu_sigma=self.Cov_mu_sigma,
            CI=CI,
            CI_type=CI_type,
        )

        # goodness of fit measures
        n = len(failures) + len(right_censored)
        if force_sigma is None:
            k = 2
            LL2 = 2 * Fit_Normal_2P.LL(params, failures, right_censored)
        else:
            k = 1
            LL2 = 2 * Fit_Normal_2P.LL_fs(
                [self.mu], failures, right_censored, force_sigma
            )
        self.loglik2 = LL2
        self.loglik = LL2 * -0.5
        if n - k - 1 > 0:
            self.AICc = 2 * k + LL2 + (2 * k ** 2 + 2 * k) / (n - k - 1)
        else:
            self.AICc = "Insufficient data"
        self.BIC = np.log(n) * k + LL2

        x, y = plotting_positions(failures=failures, right_censored=right_censored)
        self.AD = anderson_darling(
            fitted_cdf=self.distribution.CDF(xvals=x, show_plot=False), empirical_cdf=y
        )

    @staticmethod
    def logf(t, mu, sigma):  # Log PDF (Normal)
        return anp.log(anp.exp(-0.5 * (((t - mu) / sigma) ** 2))) - anp.log(
            (sigma * (2 * anp.pi) ** 0.5)
        )

    @staticmethod
    def logR(t, mu, sigma):  # Log SF (Normal)
        return anp.log((1 + erf(((mu - t) / sigma) / 2 ** 0.5)) / 2)

    @staticmethod
    def LL(params, T_f, T_rc):  # log likelihood function (2 parameter Normal)
        LL_f = Fit_Normal_2P.logf(T_f, params[0], params[1]).sum()
        LL_rc = Fit_Normal_2P.logR(T_rc, params[0], params[1]).sum()
        return -(LL_f + LL_rc)

    @staticmethod
    def LL_fs(params, T_f, T_rc, force_sigma):
        # log likelihood function (2 parameter Normal) FORCED SIGMA
        LL_f = Fit_Normal_2P.logf(T_f, params[0], force_sigma).sum()
        LL_rc = Fit_Normal_2P.logR(T_rc, params[0], force_sigma).sum()
        return -(LL_f + LL_rc)
