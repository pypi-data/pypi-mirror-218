import numpy as np
import scipy.stats as ss
from alphacore.utils import (
    round_to_decimals,
    distributions_input_checking,
    unpack_single_arrays,
    zeroise_below_gamma,
    extract_CI,
    colorprint,
)
from scipy import integrate

dec = 4  # number of decimals to use when rounding descriptive statistics and parameter titles
np.seterr(divide="ignore", invalid="ignore")  # ignore the divide by zero warnings


class Weibull_Distribution:
    """
    Weibull probability distribution. Creates a probability distribution object.

    Parameters
    ----------
    alpha : float, int
        Scale parameter. Must be > 0
    beta : float, int
        Shape parameter. Must be > 0
    gamma : float, int, optional
        threshold (offset) parameter. Must be >= 0. Default = 0

    Returns
    -------
    name : str
        'Weibull'
    name2 : 'str
        'Weibull_2P' or 'Weibull_3P' depending on the value of the gamma
        parameter
    param_title_long : str
        'Weibull Distribution (α=5,β=2)'
    param_title : str
        'α=5,β=2'
    parameters : list
        [alpha,beta,gamma]
    alpha : float
    beta : float
    gamma : float
    mean : float
    variance : float
    standard_deviation : float
    skewness : float
    kurtosis : float
    excess_kurtosis : float
    median : float
    mode : float
    b5 : float
    b95 : float

    Notes
    -----
    kwargs are used internally to generate the confidence intervals
    """

    def __init__(self, alpha=None, beta=None, gamma=0, **kwargs):
        self.name = "Weibull"
        if alpha is None or beta is None:
            raise ValueError(
                "Parameters alpha and beta must be specified. Eg. Weibull_Distribution(alpha=5,beta=2)"
            )
        self.alpha = float(alpha)
        self.beta = float(beta)
        self.gamma = float(gamma)
        self.parameters = np.array([self.alpha, self.beta, self.gamma])
        mean, var, skew, kurt = ss.weibull_min.stats(
            self.beta, scale=self.alpha, loc=self.gamma, moments="mvsk"
        )
        self.mean = float(mean)
        self.variance = float(var)
        self.standard_deviation = var**0.5
        self.skewness = float(skew)
        self.kurtosis = kurt + 3
        self.excess_kurtosis = float(kurt)
        self.median = ss.weibull_min.median(self.beta, scale=self.alpha, loc=self.gamma)
        if self.beta >= 1:
            self.mode = (
                self.alpha * ((self.beta - 1) / self.beta) ** (1 / self.beta)
                + self.gamma
            )
        else:
            self.mode = self.gamma
        if self.gamma != 0:
            self.param_title = str(
                "α="
                + str(round_to_decimals(self.alpha, dec))
                + ",β="
                + str(round_to_decimals(self.beta, dec))
                + ",γ="
                + str(round_to_decimals(self.gamma, dec))
            )
            self.param_title_long = str(
                "Weibull Distribution (α="
                + str(round_to_decimals(self.alpha, dec))
                + ",β="
                + str(round_to_decimals(self.beta, dec))
                + ",γ="
                + str(round_to_decimals(self.gamma, dec))
                + ")"
            )
            self.name2 = "Weibull_3P"
        else:
            self.param_title = str(
                "α="
                + str(round_to_decimals(self.alpha, dec))
                + ",β="
                + str(round_to_decimals(self.beta, dec))
            )
            self.param_title_long = str(
                "Weibull Distribution (α="
                + str(round_to_decimals(self.alpha, dec))
                + ",β="
                + str(round_to_decimals(self.beta, dec))
                + ")"
            )
            self.name2 = "Weibull_2P"
        self.b5 = ss.weibull_min.ppf(0.05, self.beta, scale=self.alpha, loc=self.gamma)
        self.b95 = ss.weibull_min.ppf(0.95, self.beta, scale=self.alpha, loc=self.gamma)

        # extracts values for confidence interval plotting
        if "alpha_SE" in kwargs:
            self.alpha_SE = kwargs.pop("alpha_SE")
        else:
            self.alpha_SE = None
        if "beta_SE" in kwargs:
            self.beta_SE = kwargs.pop("beta_SE")
        else:
            self.beta_SE = None
        if "Cov_alpha_beta" in kwargs:
            self.Cov_alpha_beta = kwargs.pop("Cov_alpha_beta")
        else:
            self.Cov_alpha_beta = None
        if "CI" in kwargs:
            CI = kwargs.pop("CI")
            self.Z = -ss.norm.ppf((1 - CI) / 2)
        else:
            self.Z = None
        if "CI_type" in kwargs:
            self.CI_type = kwargs.pop("CI_type")
        else:
            self.CI_type = "time"
        for item in kwargs.keys():
            colorprint(
                str(
                    "WARNING: "
                    + item
                    + " is not recognised as an appropriate entry in kwargs. Appropriate entries are alpha_SE, beta_SE, Cov_alpha_beta, CI, and CI_type."
                ),
                text_color="red",
            )
        self._pdf0 = ss.weibull_min.pdf(
            0, self.beta, scale=self.alpha, loc=0
        )  # the pdf at 0. Used by Utils.restore_axes_limits and Utils.generate_X_array
        self._hf0 = ss.weibull_min.pdf(
            0, self.beta, scale=self.alpha, loc=0
        ) / ss.weibull_min.sf(
            0, self.beta, scale=self.alpha, loc=0
        )  # the hf at 0. Used by Utils.restore_axes_limits and Utils.generate_X_array

    def PDF(self, xvals=None, xmin=None, xmax=None, show_plot=True):
        """
        Plots the PDF (probability density function)

        Parameters
        ----------
        show_plot : bool, optional
            True or False. Default = True
        xvals : array, list, optional
            x-values for plotting
        xmin : int, float, optional
            minimum x-value for plotting
        xmax : int, float, optional
            maximum x-value for plotting

        Returns
        -------
        yvals : array, float
            The y-values of the plot

        Notes
        -----
        The plot will be shown if show_plot is True (which it is by default).

        If xvals is specified, it will be used. If xvals is not specified but
        xmin and/or xmax are specified then an array with 200 elements will be
        created using these limits. If nothing is specified then the range will
        be based on the distribution's parameters.
        """
        X, xvals, xmin, xmax, show_plot = distributions_input_checking(
            self, "PDF", xvals, xmin, xmax, show_plot
        )

        pdf = ss.weibull_min.pdf(X, self.beta, scale=self.alpha, loc=self.gamma)
        pdf = unpack_single_arrays(pdf)
        return pdf

    def CDF(
        self,
        xvals=None,
        xmin=None,
        xmax=None,
        show_plot=True,
        plot_CI=True,
        CI_type=None,
        CI=None,
        CI_y=None,
        CI_x=None
    ):
        """
        Plots the CDF (cumulative distribution function)

        Parameters
        ----------
        xvals : array, list, optional
            x-values for plotting
        xmin : int, float, optional
            minimum x-value for plotting
        xmax : int, float, optional
            maximum x-value for plotting
        show_plot : bool, optional
            True or False. Default = True
        plot_CI : bool, optional
            True or False. Default = True. Only used if the distribution object
            was created by Fitters.
        CI_type : str, optional
            Must be either "time" or "reliability". Default is "time". Only used
            if the distribution object was created by Fitters.
        CI : float, optional
            The confidence interval between 0 and 1. Only used if the
            distribution object was created by Fitters.
        CI_y : list, array, optional
            The confidence interval y-values to trace. Only used if the
            distribution object was created by Fitters and CI_type='time'.
        CI_x : list, array, optional
            The confidence interval x-values to trace. Only used if the
            distribution object was created by Fitters and
            CI_type='reliability'.

        Returns
        -------
        yvals : array, float
            The y-values of the plot. Only returned if CI_x and CI_y are not
            specified.
        lower_estimate, point_estimate, upper_estimate : tuple
            A tuple of arrays or floats of the confidence interval estimates
            based on CI_x or CI_y. Only returned if CI_x or CI_y is specified
            and the confidence intervals are available. If CI_x is specified,
            the point estimate is the y-values from the distribution at CI_x. If
            CI_y is specified, the point estimate is the x-values from the
            distribution at CI_y.

        Notes
        -----
        The plot will be shown if show_plot is True (which it is by default).

        If xvals is specified, it will be used. If xvals is not specified but
        xmin and/or xmax are specified then an array with 200 elements will be
        created using these limits. If nothing is specified then the range will
        be based on the distribution's parameters.
        """

        (
            X,
            xvals,
            xmin,
            xmax,
            show_plot,
            plot_CI,
            CI_type,
            CI,
            CI_y,
            CI_x,
        ) = distributions_input_checking(
            self, "CDF", xvals, xmin, xmax, show_plot, plot_CI, CI_type, CI, CI_y, CI_x
        )

        cdf = ss.weibull_min.cdf(X, self.beta, scale=self.alpha, loc=self.gamma)
        cdf = unpack_single_arrays(cdf)

        lower_CI, upper_CI = extract_CI(
            dist=self, func="CDF", CI_type=CI_type, CI=CI, CI_y=CI_y, CI_x=CI_x
        )
        if lower_CI is not None and upper_CI is not None:
            if CI_type == "time":
                return lower_CI, self.quantile(CI_y), upper_CI
            elif CI_type == "reliability":
                cdf_point = ss.weibull_min.cdf(
                    CI_x, self.beta, scale=self.alpha, loc=self.gamma
                )
                return lower_CI, unpack_single_arrays(cdf_point), upper_CI
        else:
            return cdf

    def SF(
        self,
        xvals=None,
        xmin=None,
        xmax=None,
        show_plot=True,
        plot_CI=True,
        CI_type=None,
        CI=None,
        CI_y=None,
        CI_x=None
    ):
        """
        Plots the SF (survival function)

        Parameters
        ----------
        xvals : array, list, optional
            x-values for plotting
        xmin : int, float, optional
            minimum x-value for plotting
        xmax : int, float, optional
            maximum x-value for plotting
        show_plot : bool, optional
            True or False. Default = True
        plot_CI : bool, optional
            True or False. Default = True. Only used if the distribution object
            was created by Fitters.
        CI_type : str, optional
            Must be either "time" or "reliability". Default is "time". Only used
            if the distribution object was created by Fitters.
        CI : float, optional
            The confidence interval between 0 and 1. Only used if the
            distribution object was created by Fitters.
        CI_y : list, array, optional
            The confidence interval y-values to trace. Only used if the
            distribution object was created by Fitters and CI_type='time'.
        CI_x : list, array, optional
            The confidence interval x-values to trace. Only used if the
            distribution object was created by Fitters and
            CI_type='reliability'.

        Returns
        -------
        yvals : array, float
            The y-values of the plot. Only returned if CI_x and CI_y are not
            specified.
        lower_estimate, point_estimate, upper_estimate : tuple
            A tuple of arrays or floats of the confidence interval estimates
            based on CI_x or CI_y. Only returned if CI_x or CI_y is specified
            and the confidence intervals are available. If CI_x is specified,
            the point estimate is the y-values from the distribution at CI_x. If
            CI_y is specified, the point estimate is the x-values from the
            distribution at CI_y.

        Notes
        -----
        The plot will be shown if show_plot is True (which it is by default).

        If xvals is specified, it will be used. If xvals is not specified but
        xmin and/or xmax are specified then an array with 200 elements will be
        created using these limits. If nothing is specified then the range will
        be based on the distribution's parameters.
        """

        (
            X,
            xvals,
            xmin,
            xmax,
            show_plot,
            plot_CI,
            CI_type,
            CI,
            CI_y,
            CI_x,
        ) = distributions_input_checking(
            self, "SF", xvals, xmin, xmax, show_plot, plot_CI, CI_type, CI, CI_y, CI_x
        )

        sf = ss.weibull_min.sf(X, self.beta, scale=self.alpha, loc=self.gamma)
        sf = unpack_single_arrays(sf)

        lower_CI, upper_CI = extract_CI(
            dist=self, func="SF", CI_type=CI_type, CI=CI, CI_y=CI_y, CI_x=CI_x
        )
        if lower_CI is not None and upper_CI is not None:
            if CI_type == "time":
                return lower_CI, self.inverse_SF(CI_y), upper_CI
            elif CI_type == "reliability":
                sf_point = ss.weibull_min.sf(
                    CI_x, self.beta, scale=self.alpha, loc=self.gamma
                )
                return lower_CI, unpack_single_arrays(sf_point), upper_CI
        else:
            return sf

    def HF(self, xvals=None, xmin=None, xmax=None, show_plot=True):
        """
        Plots the HF (hazard function)

        Parameters
        ----------
        show_plot : bool, optional
            True or False. Default = True
        xvals : array, list, optional
            x-values for plotting
        xmin : int, float, optional
            minimum x-value for plotting
        xmax : int, float, optional
            maximum x-value for plotting

        Returns
        -------
        yvals : array, float
            The y-values of the plot

        Notes
        -----
        The plot will be shown if show_plot is True (which it is by default).

        If xvals is specified, it will be used. If xvals is not specified but
        xmin and/or xmax are specified then an array with 200 elements will be
        created using these limits. If nothing is specified then the range will
        be based on the distribution's parameters.
        """

        X, xvals, xmin, xmax, show_plot = distributions_input_checking(
            self, "HF", xvals, xmin, xmax, show_plot
        )  # lgtm [py/mismatched-multiple-assignment]

        hf = (self.beta / self.alpha) * ((X - self.gamma) / self.alpha) ** (
            self.beta - 1
        )
        hf = zeroise_below_gamma(X=X, Y=hf, gamma=self.gamma)
        hf = unpack_single_arrays(hf)
        self._hf = hf  # required by the CI plotting part
        self._X = X
        return hf

    def CHF(
        self,
        xvals=None,
        xmin=None,
        xmax=None,
        show_plot=True,
        plot_CI=True,
        CI_type=None,
        CI=None,
        CI_y=None,
        CI_x=None
    ):
        """
        Plots the CHF (cumulative hazard function)

        Parameters
        ----------
        xvals : array, list, optional
            x-values for plotting
        xmin : int, float, optional
            minimum x-value for plotting
        xmax : int, float, optional
            maximum x-value for plotting
        show_plot : bool, optional
            True or False. Default = True
        plot_CI : bool, optional
            True or False. Default = True. Only used if the distribution object
            was created by Fitters.
        CI_type : str, optional
            Must be either "time" or "reliability". Default is "time". Only used
            if the distribution object was created by Fitters.
        CI : float, optional
            The confidence interval between 0 and 1. Only used if the
            distribution object was created by Fitters.
        CI_y : list, array, optional
            The confidence interval y-values to trace. Only used if the
            distribution object was created by Fitters and CI_type='time'.
        CI_x : list, array, optional
            The confidence interval x-values to trace. Only used if the
            distribution object was created by Fitters and
            CI_type='reliability'.

        Returns
        -------
        yvals : array, float
            The y-values of the plot. Only returned if CI_x and CI_y are not
            specified.
        lower_estimate, point_estimate, upper_estimate : tuple
            A tuple of arrays or floats of the confidence interval estimates
            based on CI_x or CI_y. Only returned if CI_x or CI_y is specified
            and the confidence intervals are available. If CI_x is specified,
            the point estimate is the y-values from the distribution at CI_x. If
            CI_y is specified, the point estimate is the x-values from the
            distribution at CI_y.

        Notes
        -----
        The plot will be shown if show_plot is True (which it is by default).

        If xvals is specified, it will be used. If xvals is not specified but
        xmin and/or xmax are specified then an array with 200 elements will be
        created using these limits. If nothing is specified then the range will
        be based on the distribution's parameters.
        """

        (
            X,
            xvals,
            xmin,
            xmax,
            show_plot,
            plot_CI,
            CI_type,
            CI,
            CI_y,
            CI_x,
        ) = distributions_input_checking(
            self, "CHF", xvals, xmin, xmax, show_plot, plot_CI, CI_type, CI, CI_y, CI_x
        )

        chf = ((X - self.gamma) / self.alpha) ** self.beta
        chf = zeroise_below_gamma(X=X, Y=chf, gamma=self.gamma)
        chf = unpack_single_arrays(chf)
        self._chf = chf  # required by the CI plotting part
        self._X = X

        lower_CI, upper_CI = extract_CI(
            dist=self, func="CHF", CI_type=CI_type, CI=CI, CI_y=CI_y, CI_x=CI_x
        )
        if lower_CI is not None and upper_CI is not None:
            if CI_type == "time":
                return lower_CI, self.inverse_SF(np.exp(-CI_y)), upper_CI
            elif CI_type == "reliability":
                chf_point = zeroise_below_gamma(
                    X=CI_x,
                    Y=((CI_x - self.gamma) / self.alpha) ** self.beta,
                    gamma=self.gamma,
                )
                return lower_CI, unpack_single_arrays(chf_point), upper_CI
        else:
            return chf

    def quantile(self, q):
        """
        Quantile calculator

        Parameters
        ----------
        q : float, list, array
            Quantile to be calculated. Must be between 0 and 1.

        Returns
        -------
        x : float, array
            The inverse of the CDF at q. This is the probability that a random
            variable from the distribution is < q
        """
        if type(q) in [int, float, np.float64]:
            if q < 0 or q > 1:
                raise ValueError("Quantile must be between 0 and 1")
        elif type(q) in [list, np.ndarray]:
            if min(q) < 0 or max(q) > 1:
                raise ValueError("Quantile must be between 0 and 1")
        else:
            raise ValueError("Quantile must be of type float, list, array")
        ppf = ss.weibull_min.ppf(q, self.beta, scale=self.alpha, loc=self.gamma)
        return unpack_single_arrays(ppf)

    def inverse_SF(self, q):
        """
        Inverse survival function calculator

        Parameters
        ----------
        q : float, list, array
            Quantile to be calculated. Must be between 0 and 1.

        Returns
        -------
        x : float, array
            The inverse of the SF at q.
        """
        if type(q) in [int, float, np.float64]:
            if q < 0 or q > 1:
                raise ValueError("Quantile must be between 0 and 1")
        elif type(q) in [list, np.ndarray]:
            if min(q) < 0 or max(q) > 1:
                raise ValueError("Quantile must be between 0 and 1")
        else:
            raise ValueError("Quantile must be of type float, list, array")
        isf = ss.weibull_min.isf(q, self.beta, scale=self.alpha, loc=self.gamma)
        return unpack_single_arrays(isf)

    def mean_residual_life(self, t):
        """
        Mean Residual Life calculator

        Parameters
        ----------
        t : int, float
            Time (x-value) at which mean residual life is to be evaluated

        Returns
        -------
        MRL : float
            The mean residual life
        """
        R = lambda x: ss.weibull_min.sf(x, self.beta, scale=self.alpha, loc=self.gamma)
        integral_R, error = integrate.quad(R, t, np.inf)
        MRL = integral_R / R(t)
        return MRL

    def random_samples(self, number_of_samples, seed=None):
        """
        Draws random samples from the probability distribution

        Parameters
        ----------
        number_of_samples : int
            The number of samples to be drawn. Must be greater than 0.
        seed : int, optional
            The random seed passed to numpy. Default = None

        Returns
        -------
        samples : array
            The random samples

        Notes
        -----
        This is the same as rvs in scipy.stats
        """
        if type(number_of_samples) != int or number_of_samples < 1:
            raise ValueError("number_of_samples must be an integer greater than 0")
        if seed is not None:
            np.random.seed(seed)
        RVS = ss.weibull_min.rvs(
            self.beta, scale=self.alpha, loc=self.gamma, size=number_of_samples
        )
        return RVS


class Normal_Distribution:
    """
    Normal probability distribution. Creates a probability distribution object.

    Parameters
    ----------
    mu : float, int
        Location parameter
    sigma : float, int
        Scale parameter. Must be > 0

    Returns
    -------
    name : str
        'Normal'
    name2 : 'str
        'Normal_2P'
    param_title_long : str
        'Normal Distribution (μ=5,σ=2)'
    param_title : str
        'μ=5,σ=2'
    parameters : list
        [mu,sigma]
    mu : float
    sigma : float
    mean : float
    variance : float
    standard_deviation : float
    skewness : float
    kurtosis : float
    excess_kurtosis : float
    median : float
    mode : float
    b5 : float
    b95 : float

    Notes
    -----
    kwargs are used internally to generate the confidence intervals
    """

    def __init__(self, mu=None, sigma=None, **kwargs):
        self.name = "Normal"
        self.name2 = "Normal_2P"
        if mu is None or sigma is None:
            raise ValueError(
                "Parameters mu and sigma must be specified. Eg. Normal_Distribution(mu=5,sigma=2)"
            )
        self.mu = float(mu)
        self.sigma = float(sigma)
        self.parameters = np.array([self.mu, self.sigma])
        self.mean = mu
        self.variance = sigma ** 2
        self.standard_deviation = sigma
        self.skewness = 0
        self.kurtosis = 3
        self.excess_kurtosis = 0
        self.median = mu
        self.mode = mu
        self.param_title = str(
            "μ="
            + str(round_to_decimals(self.mu, dec))
            + ",σ="
            + str(round_to_decimals(self.sigma, dec))
        )
        self.param_title_long = str(
            "Normal Distribution (μ="
            + str(round_to_decimals(self.mu, dec))
            + ",σ="
            + str(round_to_decimals(self.sigma, dec))
            + ")"
        )
        self.b5 = ss.norm.ppf(0.05, loc=self.mu, scale=self.sigma)
        self.b95 = ss.norm.ppf(0.95, loc=self.mu, scale=self.sigma)

        # extracts values for confidence interval plotting
        if "mu_SE" in kwargs:
            self.mu_SE = kwargs.pop("mu_SE")
        else:
            self.mu_SE = None
        if "sigma_SE" in kwargs:
            self.sigma_SE = kwargs.pop("sigma_SE")
        else:
            self.sigma_SE = None
        if "Cov_mu_sigma" in kwargs:
            self.Cov_mu_sigma = kwargs.pop("Cov_mu_sigma")
        else:
            self.Cov_mu_sigma = None
        if "CI" in kwargs:
            CI = kwargs.pop("CI")
            self.Z = -ss.norm.ppf((1 - CI) / 2)
        else:
            self.Z = None
        if "CI_type" in kwargs:
            self.CI_type = kwargs.pop("CI_type")
        else:
            self.CI_type = "time"
        for item in kwargs.keys():
            colorprint(
                str(
                    "WARNING: "
                    + item
                    + "is not recognised as an appropriate entry in kwargs. Appropriate entries are mu_SE, sigma_SE, Cov_mu_sigma, CI, and CI_type."
                ),
                text_color="red",
            )

        self._pdf0 = 0  # the pdf at 0. Used by Utils.restore_axes_limits and Utils.generate_X_array
        self._hf0 = 0  # the hf at 0. Used by Utils.restore_axes_limits and Utils.generate_X_array

    def PDF(self, xvals=None, xmin=None, xmax=None):
        """
        Plots the PDF (probability density function)

        Parameters
        ----------
        xvals : array, list, optional
            x-values for plotting
        xmin : int, float, optional
            minimum x-value for plotting
        xmax : int, float, optional
            maximum x-value for plotting

        Returns
        -------
        yvals : array, float
            The y-values of the plot

        Notes
        -----
        The plot will be shown if show_plot is True (which it is by default).

        If xvals is specified, it will be used. If xvals is not specified but
        xmin and/or xmax are specified then an array with 200 elements will be
        created using these limits. If nothing is specified then the range will
        be based on the distribution's parameters.
        """
        X, xvals, xmin, xmax, show_plot = distributions_input_checking(
            self, "PDF", xvals, xmin, xmax
        )

        pdf = ss.norm.pdf(X, self.mu, self.sigma)
        pdf = unpack_single_arrays(pdf)
        return pdf

    def CDF(
        self,
        xvals=None,
        xmin=None,
        xmax=None,
        show_plot=True,
        plot_CI=True,
        CI_type=None,
        CI=None,
        CI_y=None,
        CI_x=None,
    ):
        """
        Plots the CDF (cumulative distribution function)

        Parameters
        ----------
        show_plot : bool, optional
            True or False. Default = True
        xvals : array, list, optional
            x-values for plotting
        xmin : int, float, optional
            minimum x-value for plotting
        xmax : int, float, optional
            maximum x-value for plotting
                plot_CI : bool, optional
            True or False. Default = True. Only used if the distribution object
            was created by Fitters.
        plot_CI : bool, optional
            True or False. Default = True. Only used if the distribution object
            was created by Fitters.
        CI_type : str, optional
            Must be either "time" or "reliability". Default is "time". Only used
            if the distribution object was created by Fitters.
        CI : float, optional
            The confidence interval between 0 and 1. Only used if the
            distribution object was created by Fitters.
        CI_y : list, array, optional
            The confidence interval y-values to trace. Only used if the
            distribution object was created by Fitters and CI_type='time'.
        CI_x : list, array, optional
            The confidence interval x-values to trace. Only used if the
            distribution object was created by Fitters and
            CI_type='reliability'.


        Returns
        -------
        yvals : array, float
            The y-values of the plot. Only returned if CI_x and CI_y are not
            specified.
        lower_estimate, point_estimate, upper_estimate : tuple
            A tuple of arrays or floats of the confidence interval estimates
            based on CI_x or CI_y. Only returned if CI_x or CI_y is specified
            and the confidence intervals are available. If CI_x is specified,
            the point estimate is the y-values from the distribution at CI_x. If
            CI_y is specified, the point estimate is the x-values from the
            distribution at CI_y.

        Notes
        -----
        The plot will be shown if show_plot is True (which it is by default).

        If xvals is specified, it will be used. If xvals is not specified but
        xmin and/or xmax are specified then an array with 200 elements will be
        created using these limits. If nothing is specified then the range will
        be based on the distribution's parameters.
        """
        (
            X,
            xvals,
            xmin,
            xmax,
            show_plot,
            plot_CI,
            CI_type,
            CI,
            CI_y,
            CI_x,
        ) = distributions_input_checking(
            self, "CDF", xvals, xmin, xmax, show_plot, plot_CI, CI_type, CI, CI_y, CI_x
        )

        cdf = ss.norm.cdf(X, self.mu, self.sigma)
        cdf = unpack_single_arrays(cdf)

        lower_CI, upper_CI = extract_CI(
            dist=self, func="CDF", CI_type=CI_type, CI=CI, CI_y=CI_y, CI_x=CI_x
        )
        if lower_CI is not None and upper_CI is not None:
            if CI_type == "time":
                return lower_CI, self.quantile(CI_y), upper_CI
            elif CI_type == "reliability":
                cdf_point = ss.norm.cdf(CI_x, self.mu, self.sigma)
                return lower_CI, unpack_single_arrays(cdf_point), upper_CI
        else:
            return cdf

    def SF(
        self,
        xvals=None,
        xmin=None,
        xmax=None,
        show_plot=True,
        plot_CI=True,
        CI_type=None,
        CI=None,
        CI_y=None,
        CI_x=None
    ):
        """
        Plots the SF (survival function)

        Parameters
        ----------
        show_plot : bool, optional
            True or False. Default = True
        xvals : array, list, optional
            x-values for plotting
        xmin : int, float, optional
            minimum x-value for plotting
        xmax : int, float, optional
            maximum x-value for plotting
                plot_CI : bool, optional
            True or False. Default = True. Only used if the distribution object
            was created by Fitters.
        plot_CI : bool, optional
            True or False. Default = True. Only used if the distribution object
            was created by Fitters.
        CI_type : str, optional
            Must be either "time" or "reliability". Default is "time". Only used
            if the distribution object was created by Fitters.
        CI : float, optional
            The confidence interval between 0 and 1. Only used if the
            distribution object was created by Fitters.
        CI_y : list, array, optional
            The confidence interval y-values to trace. Only used if the
            distribution object was created by Fitters and CI_type='time'.
        CI_x : list, array, optional
            The confidence interval x-values to trace. Only used if the
            distribution object was created by Fitters and
            CI_type='reliability'.


        Returns
        -------
        yvals : array, float
            The y-values of the plot. Only returned if CI_x and CI_y are not
            specified.
        lower_estimate, point_estimate, upper_estimate : tuple
            A tuple of arrays or floats of the confidence interval estimates
            based on CI_x or CI_y. Only returned if CI_x or CI_y is specified
            and the confidence intervals are available. If CI_x is specified,
            the point estimate is the y-values from the distribution at CI_x. If
            CI_y is specified, the point estimate is the x-values from the
            distribution at CI_y.

        Notes
        -----
        The plot will be shown if show_plot is True (which it is by default).

        If xvals is specified, it will be used. If xvals is not specified but
        xmin and/or xmax are specified then an array with 200 elements will be
        created using these limits. If nothing is specified then the range will
        be based on the distribution's parameters.
        """
        (
            X,
            xvals,
            xmin,
            xmax,
            show_plot,
            plot_CI,
            CI_type,
            CI,
            CI_y,
            CI_x,
        ) = distributions_input_checking(
            self, "SF", xvals, xmin, xmax, show_plot, plot_CI, CI_type, CI, CI_y, CI_x
        )

        sf = ss.norm.sf(X, self.mu, self.sigma)
        sf = unpack_single_arrays(sf)

        lower_CI, upper_CI = extract_CI(
            dist=self, func="SF", CI_type=CI_type, CI=CI, CI_y=CI_y, CI_x=CI_x
        )
        if lower_CI is not None and upper_CI is not None:
            if CI_type == "time":
                return lower_CI, self.inverse_SF(CI_y), upper_CI
            elif CI_type == "reliability":
                sf_point = ss.norm.sf(CI_x, self.mu, self.sigma)
                return lower_CI, unpack_single_arrays(sf_point), upper_CI
        else:
            return sf

    def HF(self, xvals=None, xmin=None, xmax=None, show_plot=True):
        """
        Plots the HF (hazard function)

        Parameters
        ----------
        show_plot : bool, optional
            True or False. Default = True
        xvals : array, list, optional
            x-values for plotting
        xmin : int, float, optional
            minimum x-value for plotting
        xmax : int, float, optional
            maximum x-value for plotting

        Returns
        -------
        yvals : array, float
            The y-values of the plot

        Notes
        -----
        The plot will be shown if show_plot is True (which it is by default).

        If xvals is specified, it will be used. If xvals is not specified but
        xmin and/or xmax are specified then an array with 200 elements will be
        created using these limits. If nothing is specified then the range will
        be based on the distribution's parameters.
        """
        X, xvals, xmin, xmax, show_plot = distributions_input_checking(
            self, "HF", xvals, xmin, xmax, show_plot
        )  # lgtm [py/mismatched-multiple-assignment]

        hf = ss.norm.pdf(X, self.mu, self.sigma) / ss.norm.sf(X, self.mu, self.sigma)
        hf = unpack_single_arrays(hf)
        return hf

    def CHF(
        self,
        xvals=None,
        xmin=None,
        xmax=None,
        show_plot=True,
        plot_CI=True,
        CI_type=None,
        CI=None,
        CI_y=None,
        CI_x=None
    ):
        """
        Plots the CHF (cumulative hazard function)

        Parameters
        ----------
        show_plot : bool, optional
            True or False. Default = True
        xvals : array, list, optional
            x-values for plotting
        xmin : int, float, optional
            minimum x-value for plotting
        xmax : int, float, optional
            maximum x-value for plotting
                plot_CI : bool, optional
            True or False. Default = True. Only used if the distribution object
            was created by Fitters.
        plot_CI : bool, optional
            True or False. Default = True. Only used if the distribution object
            was created by Fitters.
        CI_type : str, optional
            Must be either "time" or "reliability". Default is "time". Only used
            if the distribution object was created by Fitters.
        CI : float, optional
            The confidence interval between 0 and 1. Only used if the
            distribution object was created by Fitters.
        CI_y : list, array, optional
            The confidence interval y-values to trace. Only used if the
            distribution object was created by Fitters and CI_type='time'.
        CI_x : list, array, optional
            The confidence interval x-values to trace. Only used if the
            distribution object was created by Fitters and
            CI_type='reliability'.



        Returns
        -------
        yvals : array, float
            The y-values of the plot. Only returned if CI_x and CI_y are not
            specified.
        lower_estimate, point_estimate, upper_estimate : tuple
            A tuple of arrays or floats of the confidence interval estimates
            based on CI_x or CI_y. Only returned if CI_x or CI_y is specified
            and the confidence intervals are available. If CI_x is specified,
            the point estimate is the y-values from the distribution at CI_x. If
            CI_y is specified, the point estimate is the x-values from the
            distribution at CI_y.

        Notes
        -----
        The plot will be shown if show_plot is True (which it is by default).

        If xvals is specified, it will be used. If xvals is not specified but
        xmin and/or xmax are specified then an array with 200 elements will be
        created using these limits. If nothing is specified then the range will
        be based on the distribution's parameters.
        """
        (
            X,
            xvals,
            xmin,
            xmax,
            show_plot,
            plot_CI,
            CI_type,
            CI,
            CI_y,
            CI_x,
        ) = distributions_input_checking(
            self, "CHF", xvals, xmin, xmax, show_plot, plot_CI, CI_type, CI, CI_y, CI_x
        )

        chf = -np.log(ss.norm.sf(X, self.mu, self.sigma))
        chf = unpack_single_arrays(chf)
        self._chf = chf  # required by the CI plotting part
        self._X = X

        lower_CI, upper_CI = extract_CI(
            dist=self, func="CHF", CI_type=CI_type, CI=CI, CI_y=CI_y, CI_x=CI_x
        )
        if lower_CI is not None and upper_CI is not None:
            if CI_type == "time":
                return lower_CI, self.inverse_SF(np.exp(-CI_y)), upper_CI
            elif CI_type == "reliability":
                chf_point = -np.log(ss.norm.sf(CI_x, self.mu, self.sigma))
                return lower_CI, unpack_single_arrays(chf_point), upper_CI
        else:
            return chf

    def quantile(self, q):
        """
        Quantile calculator

        Parameters
        ----------
        q : float, list, array
            Quantile to be calculated. Must be between 0 and 1.

        Returns
        -------
        x : float
            The inverse of the CDF at q. This is the probability that a random
            variable from the distribution is < q
        """
        if type(q) in [int, float, np.float64]:
            if q < 0 or q > 1:
                raise ValueError("Quantile must be between 0 and 1")
        elif type(q) in [list, np.ndarray]:
            if min(q) < 0 or max(q) > 1:
                raise ValueError("Quantile must be between 0 and 1")
        else:
            raise ValueError("Quantile must be of type float, list, array")
        ppf = ss.norm.ppf(q, loc=self.mu, scale=self.sigma)
        return unpack_single_arrays(ppf)

    def inverse_SF(self, q):
        """
        Inverse survival function calculator

        Parameters
        ----------
        q : float, list, array
            Quantile to be calculated. Must be between 0 and 1.

        Returns
        -------
        x : float
            The inverse of the SF at q.
        """
        if type(q) in [int, float, np.float64]:
            if q < 0 or q > 1:
                raise ValueError("Quantile must be between 0 and 1")
        elif type(q) in [list, np.ndarray]:
            if min(q) < 0 or max(q) > 1:
                raise ValueError("Quantile must be between 0 and 1")
        else:
            raise ValueError("Quantile must be of type float, list, array")
        isf = ss.norm.isf(q, loc=self.mu, scale=self.sigma)
        return unpack_single_arrays(isf)

    def mean_residual_life(self, t):
        """
        Mean Residual Life calculator

        Parameters
        ----------
        t : int, float
            Time (x-value) at which mean residual life is to be evaluated

        Returns
        -------
        MRL : float
            The mean residual life
        """
        R = lambda x: ss.norm.sf(x, loc=self.mu, scale=self.sigma)
        integral_R, error = integrate.quad(R, t, np.inf)
        MRL = integral_R / R(t)
        return MRL

    def random_samples(self, number_of_samples, seed=None):
        """
        Draws random samples from the probability distribution

        Parameters
        ----------
        number_of_samples : int
            The number of samples to be drawn. Must be greater than 0.
        seed : int, optional
            The random seed passed to numpy. Default = None

        Returns
        -------
        samples : array
            The random samples

        Notes
        -----
        This is the same as rvs in scipy.stats
        """
        if type(number_of_samples) != int or number_of_samples < 1:
            raise ValueError("number_of_samples must be an integer greater than 0")
        if seed is not None:
            np.random.seed(seed)
        RVS = ss.norm.rvs(loc=self.mu, scale=self.sigma, size=number_of_samples)
        return RVS
