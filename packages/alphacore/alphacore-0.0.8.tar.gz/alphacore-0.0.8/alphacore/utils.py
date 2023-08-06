import numpy as np
import json
from scipy.optimize import curve_fit, minimize
from numpy.linalg import LinAlgError
import scipy.stats as ss
from scipy.special import gammainc, betainc, erf
from autograd import value_and_grad
import autograd.numpy as anp
from autograd import jacobian as jac
from autograd_gamma import gammainccinv as agammainccinv
from autograd_gamma import gammaincc as agammaincc


def generate_X_array(dist, xvals=None, xmin=None, xmax=None):
    """
    Generates the array of X values for each of the PDf, CDF, SF, HF, CHF
    functions within reliability.Distributions

    This is done with a variety of cases in order to ensure that for regions of
    high gradient (particularly asymptotes to inf) the points are more
    concentrated. This ensures that the line always looks as smooth as possible
    using only 200 data points.

    Parameters
    ----------
    dist : object
        The distribution object
    xvals : array, list, optional
        The xvals for the plot if specified
    xmin : array, list, optional
        The xmin for the plot if specified
    xmax : array, list, optional
        The xmax for the plot if specified

    Returns
    -------
    X : array
        The X array that was generated.
    """

    # obtain the xvals array
    points = 200  # the number of points to use when generating the X array
    points_right = 25  # the number of points given to the area above QU. The total points is still equal to 'points' so the area below QU receives 'points - points_right'
    QL = dist.quantile(0.0001)  # quantile lower
    QU = dist.quantile(0.99)  # quantile upper
    if xvals is not None:
        X = xvals
        if type(X) in [float, int, np.float64]:
            if X < 0 and dist.name not in ["Normal", "Gumbel"]:
                raise ValueError("the value given for xvals is less than 0")
            if X > 1 and dist.name == "Beta":
                raise ValueError(
                    "the value given for xvals is greater than 1. The beta distribution is bounded between 0 and 1."
                )
            X = np.array([X])
        elif type(X) is list:
            X = np.array(X)
        elif type(X) is np.ndarray:
            pass
        else:
            raise ValueError(
                "unexpected type in xvals. Must be int, float, list, or array"
            )
        if (
            type(X) is np.ndarray
            and min(X) < 0
            and dist.name not in ["Normal", "Gumbel"]
        ):
            raise ValueError("xvals was found to contain values below 0")
        if type(X) is np.ndarray and max(X) > 1 and dist.name == "Beta":
            raise ValueError(
                "xvals was found to contain values above 1. The beta distribution is bounded between 0 and 1."
            )
    else:
        if dist.name in ["Weibull", "Lognormal", "Loglogistic", "Exponential", "Gamma"]:
            if xmin is None:
                xmin = 0
            if xmin < 0:
                raise ValueError(
                    "xmin must be greater than or equal to 0 for all distributions except the Normal and Gumbel distributions"
                )
            if xmax is None:
                xmax = dist.quantile(0.9999)
            if xmin > xmax:
                xmin, xmax = (
                    xmax,
                    xmin,
                )  # switch them if they are given in the wrong order
            if (
                (xmin < QL and xmax < QL)
                or (xmin >= QL and xmax <= QU)
                or (xmin > QU and xmax > QU)
            ):
                X = np.linspace(xmin, xmax, points)
            elif xmin < QL and xmax > QL and xmax < QU:
                if dist.gamma == 0:
                    if dist._pdf0 == 0:
                        X = np.hstack([xmin, np.linspace(QL, xmax, points - 1)])
                    else:  # pdf is asymptotic to inf at x=0
                        X = np.hstack([xmin, np.geomspace(QL, xmax, points - 1)])
                else:  # gamma > 0
                    if dist._pdf0 == 0:
                        X = np.hstack(
                            [xmin, dist.gamma - 1e-8, np.linspace(QL, xmax, points - 2)]
                        )
                    else:  # pdf is asymptotic to inf at x=0
                        detail = (
                            np.geomspace(QL - dist.gamma, xmax - dist.gamma, points - 2)
                            + dist.gamma
                        )
                        X = np.hstack([xmin, dist.gamma - 1e-8, detail])
            elif xmin > QL and xmin < QU and xmax > QU:
                if dist._pdf0 == 0:
                    X = np.hstack(
                        [
                            np.linspace(xmin, QU, points - points_right),
                            np.linspace(QU, xmax, points_right),
                        ]
                    )
                else:  # pdf is asymptotic to inf at x=0
                    try:
                        detail = (
                            np.geomspace(
                                xmin - dist.gamma,
                                QU - dist.gamma,
                                points - points_right,
                            )
                            + dist.gamma
                        )
                        right = (
                            np.geomspace(
                                QU - dist.gamma, xmax - dist.gamma, points_right
                            )
                            + dist.gamma
                        )
                    except ValueError:  # occurs for very low shape params causing QL-gamma to be zero
                        detail = np.linspace(xmin, QU, points - points_right)
                        right = np.linspace(QU, xmax, points_right)
                    X = np.hstack([detail, right])
            else:  # xmin < QL and xmax > QU
                if dist.gamma == 0:
                    if dist._pdf0 == 0:
                        X = np.hstack(
                            [
                                xmin,
                                np.linspace(QL, QU, points - (points_right + 1)),
                                np.geomspace(QU, xmax, points_right),
                            ]
                        )
                    else:  # pdf is asymptotic to inf at x=0
                        try:
                            X = np.hstack(
                                [
                                    xmin,
                                    np.geomspace(QL, QU, points - (points_right + 1)),
                                    np.geomspace(QU, xmax, points_right),
                                ]
                            )
                        except ValueError:  # occurs for very low shape params causing QL to be zero
                            X = np.hstack(
                                [
                                    xmin,
                                    np.linspace(QL, QU, points - (points_right + 1)),
                                    np.geomspace(QU, xmax, points_right),
                                ]
                            )
                else:  # gamma > 0
                    if dist._pdf0 == 0:
                        X = np.hstack(
                            [
                                xmin,
                                dist.gamma - 1e-8,
                                np.linspace(QL, QU, points - (points_right + 2)),
                                np.geomspace(
                                    QU - dist.gamma, xmax - dist.gamma, points_right
                                )
                                + dist.gamma,
                            ]
                        )
                    else:  # pdf is asymptotic to inf at x=0
                        try:
                            detail = (
                                np.geomspace(
                                    QL - dist.gamma,
                                    QU - dist.gamma,
                                    points - (points_right + 2),
                                )
                                + dist.gamma
                            )
                            right = (
                                np.geomspace(
                                    QU - dist.gamma, xmax - dist.gamma, points_right
                                )
                                + dist.gamma
                            )
                        except ValueError:  # occurs for very low shape params causing QL-gamma to be zero
                            detail = np.linspace(QL, QU, points - (points_right + 2))
                            right = np.linspace(QU, xmax, points_right)
                        X = np.hstack([xmin, dist.gamma - 1e-8, detail, right])
        elif dist.name in ["Normal", "Gumbel"]:
            if xmin is None:
                xmin = dist.quantile(0.0001)
            if xmax is None:
                xmax = dist.quantile(0.9999)
            if xmin > xmax:
                xmin, xmax = (
                    xmax,
                    xmin,
                )  # switch them if they are given in the wrong order
            if xmin <= 0 or xmin > dist.quantile(0.0001):
                X = np.linspace(xmin, xmax, points)
            else:
                X = np.hstack(
                    [0, np.linspace(xmin, xmax, points - 1)]
                )  # this ensures that the distribution is at least plotted from 0 if its xmin is above 0
        elif dist.name == "Beta":
            if xmin is None:
                xmin = 0
            if xmax is None:
                xmax = 1
            if xmax > 1:
                raise ValueError(
                    "xmax must be less than or equal to 1 for the beta distribution"
                )
            if xmin > xmax:
                xmin, xmax = (
                    xmax,
                    xmin,
                )  # switch them if they are given in the wrong order
            X = np.linspace(xmin, xmax, points)
        else:
            raise ValueError("Unrecognised distribution name")
    return X


def distributions_input_checking(
    self,
    func,
    xvals,
    xmin,
    xmax,
    show_plot=None,
    plot_CI=None,
    CI_type=None,
    CI=None,
    CI_y=None,
    CI_x=None,
):
    """
    Performs checks and sets default values for the inputs to distributions
    sub function (PDF, CDF, SF, HF, CHF)

    Parameters
    ----------
    self : object
        Distribution object created by reliability.Distributions
    func : str
        Must be either 'PDF','CDF', 'SF', 'HF', 'CHF'
    xvals : array, list
        x-values for plotting.
    xmin : int, float
        minimum x-value for plotting.
    xmax : int, float
        maximum x-value for plotting.
    show_plot : bool
        Whether the plot is to be shown.
    plot_CI : bool, optional
        Whether the confidence intervals are to be shown on the plot. Default is
        None.
    CI_type : str, optional
        If specified, it must be "time" or "reliability". Default is None
    CI : float, optional
        The confidence intervals. If specified, it must be between 0 and 1.
        Default is None.
    CI_y : list, array, optional
        The confidence interval y-values to trace. Default is None.
    CI_x : list, array, optional
        The confidence interval x-values to trace. Default is None.

    Returns
    -------
    X : array
        An array of the x-values for the plot. Created using generate_X_array
    xvals : array, list
        x-values for plotting.
    xmin : int, float
        minimum x-value for plotting.
    xmax : int, float
        maximum x-value for plotting.
    show_plot : bool
        Whether the plot is to be shown. Default is True. Only returned if func
        is 'PDF','CDF', 'SF', 'HF, or 'CHF'
    plot_CI : bool
        Whether the confidence intervals are to be shown on the plot. Default is
        True. Only returned if func is 'CDF', 'SF', or 'CHF' and self.name
        !='Beta'.
    CI_type : str
        The type of confidence interval. Will be either "time" or "reliability".
        Default is "time". Only returned if func is 'CDF', 'SF', or 'CHF' and
        self.name !='Beta'. If self.name=='Exponential' it will return None. If
        self.CI_type is specified and CI_type is None then self.CI_type will be
        used for CI_type.
    CI : float
        The confidence intervals between 0 and 1. Default is 0.95. Only returned
        if func is 'CDF', 'SF', or 'CHF' and self.name !='Beta'. If self.CI is
        specified and CI is None then self.CI will be used for CI.
    CI_y : list, array, float, int
        The confidence interval y-values to trace. Default is None. Only
        returned if func is 'CDF', 'SF', or 'CHF' and self.name !='Beta'.
    CI_x : list, array, float, int
        The confidence interval x-values to trace. Default is None. Only
        returned if func is 'CDF', 'SF', or 'CHF' and self.name !='Beta'.
    """
    if func not in ["PDF", "CDF", "SF", "HF", "CHF", "ALL"]:
        raise ValueError("func must be either 'PDF','CDF', 'SF', 'HF', 'CHF', 'ALL'")

    # type checking
    if type(xvals) not in [type(None), list, np.ndarray, int, float]:
        raise ValueError("xvals must be an int, float, list, or array. Default is None")
    if type(xmin) not in [type(None), int, float]:
        raise ValueError("xmin must be an int or float. Default is None")
    if type(xmax) not in [type(None), int, float]:
        raise ValueError("xmax must be an int or float. Default is None")
    if type(show_plot) not in [type(None), bool]:
        raise ValueError("show_plot must be True or False. Default is True")
    if type(plot_CI) not in [type(None), bool]:
        raise ValueError(
            "plot_CI must be True or False. Default is True. Only used if the distribution object was created by Fitters."
        )
    if type(CI_type) not in [type(None), str]:
        raise ValueError(
            'CI_type must be "time" or "reliability". Default is "time". Only used if the distribution object was created by Fitters.'
        )
    if CI is True:
        CI = 0.95
    if CI is False:
        CI = 0.95
        plot_CI = False
    if type(CI) not in [type(None), float]:
        raise ValueError(
            "CI must be between 0 and 1. Default is 0.95 for 95% confidence interval. Only used if the distribution object was created by Fitters."
        )
    if type(CI_y) not in [type(None), list, np.ndarray, float, int]:
        raise ValueError(
            'CI_y must be a list, array, float, or int. Default is None. Only used if the distribution object was created by Fitters anc CI_type="time".'
        )
    if type(CI_x) not in [type(None), list, np.ndarray, float, int]:
        raise ValueError(
            'CI_x must be a list, array, float, or int. Default is None. Only used if the distribution object was created by Fitters anc CI_type="reliability".'
        )

    # default values
    if (
        xmin is None
        and xmax is None
        and type(xvals) not in [list, np.ndarray, type(None)]
    ):
        X = xvals
        show_plot = False
    else:
        X = generate_X_array(dist=self, xvals=xvals, xmin=xmin, xmax=xmax)

    if CI is None and self.Z is None:
        CI = 0.95
    elif CI is not None:  # CI takes precedence over Z
        if CI <= 0 or CI >= 1:
            raise ValueError("CI must be between 0 and 1")
    else:  # CI is None and Z is not None
        CI = 1 - ss.norm.cdf(-self.Z) * 2  # converts Z to CI

    if show_plot is None:
        show_plot = True

    if plot_CI is None:
        plot_CI = True

    if self.name == "Exponential":
        if CI_type is not None:
            colorprint(
                "WARNING: CI_type is not required for the Exponential distribution since the confidence intervals of time and reliability are identical",
                text_color="red",
            )
            CI_type = None
    elif self.name == "Beta":
        if CI_type is not None:
            colorprint(
                "WARNING: CI_type is not used for the Beta distribution since the confidence intervals are not implemented",
                text_color="red",
            )
            CI_type = None
    else:
        if CI_type is None and self.CI_type is None:
            CI_type = "time"
        elif CI_type is None and self.CI_type is not None:
            CI_type = self.CI_type
        else:  # CI_type is not None
            if CI_type.upper() in ["T", "TIME"]:
                CI_type = "time"
            elif CI_type.upper() in ["R", "REL", "RELIABILITY"]:
                CI_type = "reliability"

    if CI_x is not None and CI_y is not None:
        if CI_type == "reliability":
            colorprint(
                "WARNING: CI_x and CI_y can not be specified at the same time. CI_y has been reset to None and the results for CI_x will be provided.",
                text_color="red",
            )
            CI_y = None
        else:
            colorprint(
                "WARNING: CI_x and CI_y can not be specified at the same time. CI_x has been reset to None and the results for CI_y will be provided.",
                text_color="red",
            )
            CI_x = None

    if CI_x is not None:
        if type(CI_x) in [float, int]:
            if CI_x <= 0 and self.name not in ["Normal", "Gumbel"]:
                raise ValueError("CI_x must be greater than 0")
            CI_x = np.array([CI_x])  # package as array. Will be unpacked later
        else:
            CI_x = np.asarray(CI_x)
            if min(CI_x) <= 0 and self.name not in ["Normal", "Gumbel"]:
                raise ValueError("CI_x values must all be greater than 0")

    if CI_y is not None:
        if type(CI_y) in [float, int]:
            if CI_y <= 0:
                raise ValueError("CI_y must be greater than 0")
            if CI_y >= 1 and func in ["CDF", "SF"]:
                raise ValueError("CI_y must be less than 1")
            CI_y = np.array([CI_y])  # package as array. Will be unpacked later
        else:
            CI_y = np.asarray(CI_y)
            if min(CI_y) <= 0:
                raise ValueError("CI_y values must all be above 0")
            if max(CI_y) >= 1 and func in ["CDF", "SF"]:
                raise ValueError("CI_y values must all be below 1")

    if self.name == "Beta":
        if func in ["PDF", "CDF", "SF", "HF", "CHF"]:
            return X, xvals, xmin, xmax, show_plot
        else:  # func ='ALL' which is used for the .plot() method
            return X, xvals, xmin, xmax
    else:  # everything except the Beta distribution
        if func in ["PDF", "HF"]:
            return X, xvals, xmin, xmax, show_plot
        elif func in ["CDF", "SF", "CHF"]:
            return X, xvals, xmin, xmax, show_plot, plot_CI, CI_type, CI, CI_y, CI_x
        else:  # func ='ALL' which is used for the .plot() method
            return X, xvals, xmin, xmax


# noinspection PyUnboundLocalVariable
def round_to_decimals(number, decimals=5, integer_floats_to_ints=True):
    """
    This function is used to round a number to a specified number of decimals.
    It is used heavily in the formatting of the parameter titles within
    reliability.Distributions

    It is not the same as rounding to a number of significant figures as it
    keeps preceeding zeros for numbers less than 1.

    Parameters
    ----------
    number : float
        The number to be rounded
    decimals : int
        The number of decimals (not including preceeding zeros) that are to be
        in the output
    integer_floats_to_ints : bool, optional
        Default is True. Removes trailing zeros from floats if there are no
        significant decimals (eg. 12.0 becomes 12).

    Returns
    -------
    number_rounded : float, int
        The number rounded. If the number has no trailing zeros and
        integer_floats_to_int is True then the output will be an int.

    Notes
    -----
    Examples (with decimals = 5):

    - 1234567.1234567 ==> 1234567.12345
    - 0.0001234567 ==> 0.00012345
    - 1234567 ==> 1234567
    - 0.00 ==> 0
    """

    if np.isfinite(number):  # check the input is not NaN
        if number < 0:
            sign = -1
            num = number * -1
            skip_to_end = False
        elif number > 0:
            sign = 1
            num = number
            skip_to_end = False
        else:  # number == 0
            if integer_floats_to_ints is True:
                out = int(number)
            else:
                out = number
            sign = 0
            skip_to_end = True
        if skip_to_end is False:
            if num > 1:
                decimal = num % 1
                whole = num - decimal
                if decimal == 0:
                    if integer_floats_to_ints is True:
                        out = int(whole)
                    else:
                        out = whole
                else:
                    out = np.round(num, decimals)
            else:  # num<1
                out = np.round(num, decimals - int(np.floor(np.log10(abs(num)))) - 1)
        output = out * sign
    else:
        output = number
    return output


def zeroise_below_gamma(X, Y, gamma):
    """
    This will make all Y values 0 for the corresponding X values being below
    gamma (the threshold parameter for Weibull, Exponential, Gamma, Loglogistic,
    and Lognormal).

    Used by HF and CHF which need to be zeroized if the gamma shifted form of
    the equation is used.

    Parameters
    ----------
    X : array, list
        The x values of the distribution. These areused to determine whis Y
        values to zeroize.
    Y : array, list
        The y-values of the distribution
    gamma : float, int
        The gamma parameter. This is the point at which Y values corresponding
        to X values below gamma will be zeroized.

    Returns
    -------
    Y : array
        The zeroized Y array
    """
    if gamma > 0:
        if len(np.where(X > gamma)[0]) == 0:
            Y[0::] = 0  # zeroize everything if there is no X values above gamma
        else:
            Y[0 : (np.where(X > gamma)[0][0])] = 0  # zeroize below X=gamma
    return Y


def unpack_single_arrays(array):
    """
    Unpacks arrays with a single element to return just that element

    Parameters
    ----------
    array : float, int, list, array
        The value for unpacking

    Returns
    -------
    output : float, list, int, array
        If the input was a single length numpy array then the output will be the
        item from the array. If the input was anything else then the output will
        match the input
    """
    if type(array) == np.ndarray:
        if len(array) == 1:
            out = array[0]
        else:
            out = array
    else:
        out = array
    return out


def plotting_positions(failures=None, right_censored=None, a=None):
    """
    Calculates the plotting positions for plotting on probability paper.
    This differs from the plotting_positions in reliability as it does
    not restore the original order of the points (they remain sorted)
    and it does not require pandas to work.

    Parameters
    ----------
    failures : array, list
        The failure data. Must have at least 1 element.
    right_censored : array, list, optional
        The right censored failure data. Optional input. Default = None.
    a : float, int, optional
        The heuristic constant for plotting positions of the form
        (k-a)/(n+1-2a) where k is the rank and n is the number of points.
        Optional input. Default is a = 0.3 which is the median rank method
        (same as the default in Minitab and Reliasoft). Must be in the range 0
        to 1. For more heuristics, see:
        https://en.wikipedia.org/wiki/Q%E2%80%93Q_plot#Heuristics

    Returns
    -------
    (array(x),array(y)) : tuple
        a tuple of two arrays. The arrays provide the x and y plotting
        positions. The x array will match the events parameter while the y
        array will be the empirical estimate of the CDF at each of the events.

    Notes
    -----
    This function is primarily used by the probability plotting functions. The
    order of the input data is preserved (not sorted).
    """

    # error checking the input
    if type(failures) in [list, np.ndarray]:
        f = np.asarray(failures)
    else:
        raise ValueError("events must be specified as an array or list")

    if type(right_censored) == type(None):
        rc = np.array([])
    elif type(right_censored) in [np.ndarray, list]:
        rc = np.asarray(right_censored)
    else:
        raise ValueError("if specified, suspensions must be an array or list")

    if a is None:
        a = 0.3
    elif a < 0 or a > 1:
        raise ValueError(
            "a must be in the range 0 to 1. Default is 0.3 which gives the median rank. For more information see https://en.wikipedia.org/wiki/Q%E2%80%93Q_plot#Heuristics"
        )

    # construct the dataframe for the rank adjustment method
    f_codes = np.ones_like(f)
    rc_codes = np.zeros_like(rc)
    cens_codes = list(np.hstack([f_codes, rc_codes]))
    all_data = list(np.hstack([f, rc]))
    n = len(all_data)

    df = np.array([all_data, cens_codes]).transpose()
    df_sorted = df[df[:, 0].argsort()]
    times = df_sorted[:, 0]
    censcodes = df_sorted[:, 1]
    reverse_i_all = np.arange(1, n + 1)[::-1]
    leading_cens = np.where(censcodes == 1)[0][0]
    failure_indices = np.where(censcodes == 1)[0]
    failure_rows = times[failure_indices]
    reverse_i = reverse_i_all[failure_indices]
    len_reverse_i = len(reverse_i)

    if leading_cens > 0:  # there are censored items before the first failure
        k = np.arange(1, len_reverse_i + 1)
        adjusted_rank2 = [0]
        rank_increment = [leading_cens / (n - 1)]
        for j in k:
            rank_increment.append((n + 1 - adjusted_rank2[-1]) / (1 + reverse_i[j - 1]))
            adjusted_rank2.append(adjusted_rank2[-1] + rank_increment[-1])
        adjusted_rank = adjusted_rank2[1:]
    else:  # the first item is a failure
        k = np.arange(1, len_reverse_i)
        adjusted_rank = [1]
        rank_increment = [1]
        for j in k:
            if j > 0:
                rank_increment.append((n + 1 - adjusted_rank[-1]) / (1 + reverse_i[j]))
                adjusted_rank.append(adjusted_rank[-1] + rank_increment[-1])
    F = []
    for i in adjusted_rank:
        F.append((i - a) / (n + 1 - 2 * a))

    return failure_rows, F


def linear_regression(
    x,
    y,
    slope=None,
    x_intercept=None,
    y_intercept=None,
    RRX_or_RRY="RRX",
    show_plot=False,
    **kwargs
):
    """
    This function provides the linear algebra solution to find line of best fit
    passing through points (x,y). Options to specify slope or intercept enable
    these parameters to be forced.

    Rank regression can be on X (RRX) or Y (RRY). Default is RRX.
    Note that slope depends on RRX_or_RRY. If you use RRY then slope is dy/dx
    but if you use RRX then slope is dx/dy.

    Parameters
    ----------
    x : array, list
        The x values
    y : array, list
        The y values
    slope : float, int, optional
        Used to force the slope. Default is None.
    x_intercept : float, int, optional
        Used to force the x-intercept. Default is None. Only used for RRY.
    y_intercept : float, int, optional
        Used to force the y-intercept. Default is None. Only used for RRX.
    RRX_or_RRY : str, optional
        Must be "RRY" or "RRX". Default is "RRY".
    show_plot : bool, optional
        If True, a plot of the line and points will be generated. Use plt.show()
        to show it.
    kwargs
        Keyword arguments for the plot that are passed to matplotlib for the
        line.

    Returns
    -------
    slope : float
        The slope of the line.
    intercept : float
        The intercept (x or y depending on RRX_or_RRY) of the line.

    Notes
    -----
    The equation of a line used here is Y = slope * X + intercept. This is the
    RRY form. For RRX it can be rearranged to X = (Y - intercept)/slope

    For more information on linear regression, see the `documentation <https://reliability.readthedocs.io/en/latest/How%20does%20Least%20Squares%20Estimation%20work.html>`_.
    """
    x = np.asarray(x)
    y = np.asarray(y)
    if len(x) != len(y):
        raise ValueError("x and y are different lengths")
    if RRX_or_RRY not in ["RRX", "RRY"]:
        raise ValueError('RRX_or_RRY must be either "RRX" or "RRY". Default is "RRY".')
    if x_intercept is not None and RRX_or_RRY == "RRY":
        raise ValueError("RRY must use y_intercept not x_intercept")
    if y_intercept is not None and RRX_or_RRY == "RRX":
        raise ValueError("RRX must use x_intercept not y_intercept")
    if slope is not None and (x_intercept is not None or y_intercept is not None):
        raise ValueError("You can not specify both slope and intercept")

    if RRX_or_RRY == "RRY":
        if y_intercept is not None:  # only the slope must be found
            min_pts = 1
            xx = np.array([x]).T
            yy = (y - y_intercept).T
        elif slope is not None:  # only the intercept must be found
            min_pts = 1
            xx = np.array([np.ones_like(x)]).T
            yy = (y - slope * x).T
        else:  # both slope and intercept must be found
            min_pts = 2
            xx = np.array([x, np.ones_like(x)]).T
            yy = y.T
    else:  # RRX
        if x_intercept is not None:  # only the slope must be found
            min_pts = 1
            yy = np.array([y]).T
            xx = (x - x_intercept).T
        elif slope is not None:  # only the intercept must be found
            min_pts = 1
            yy = np.array([np.ones_like(y)]).T
            xx = (x - slope * y).T
        else:  # both slope and intercept must be found
            min_pts = 2
            yy = np.array([y, np.ones_like(y)]).T
            xx = x.T

    if len(x) < min_pts:
        if slope is not None:
            err_str = str(
                "A minimum of 1 point is required to fit the line when the slope is specified."
            )
        elif x_intercept is not None and y_intercept is not None:
            err_str = str(
                "A minimum of 1 point is required to fit the line when the intercept is specified."
            )
        else:
            err_str = str(
                "A minimum of 2 points are required to fit the line when slope or intercept are not specified."
            )
        raise ValueError(err_str)

    if RRX_or_RRY == "RRY":
        try:
            solution = (
                np.linalg.inv(xx.T.dot(xx)).dot(xx.T).dot(yy)
            )  # linear regression formula for RRY
        except LinAlgError:
            raise RuntimeError(
                "An error has occurred when attempting to find the initial guess using least squares estimation.\nThis error is caused by a non-invertable matrix.\nThis can occur when there are only two very similar failure times like 10 and 10.000001.\nThere is no solution to this error, other than to use failure times that are more unique."
            )
        if y_intercept is not None:
            m = solution[0]
            c = y_intercept
        elif slope is not None:
            m = slope
            c = solution[0]
        else:
            m = solution[0]
            c = solution[1]
    else:  # RRX
        try:
            solution = (
                np.linalg.inv(yy.T.dot(yy)).dot(yy.T).dot(xx)
            )  # linear regression formula for RRX
        except LinAlgError:
            raise RuntimeError(
                "An error has occurred when attempting to find the initial guess using least squares estimation.\nThis error is caused by a non-invertable matrix.\nThis can occur when there are only two very similar failure times like 10 and 10.000001.\nThere is no solution to this error, other than to use failure times that are more unique."
            )
        if x_intercept is not None:
            m_x = solution[0]
            m = 1 / m_x
            c = -x_intercept / m_x
        elif slope is not None:
            m = 1 / slope
            c_x = solution[0]
            c = -c_x / slope
        else:
            m_x = solution[0]
            c_x = solution[1]
            m = 1 / m_x
            c = -c_x / m_x
    return m, c


def least_squares(dist, failures, right_censored, method="RRX", force_shape=None):
    """
    Uses least squares or non-linear least squares estimation to fit the
    parameters of the distribution to the plotting positions.

    Plotting positions are based on failures and right_censored so while least
    squares estimation does not consider the right_censored data in the same way
    as MLE, the plotting positions do. This means that right censored data are
    not ignored by least squares estimation, but the way the values are treated
    differs between least squares and MLE.

    The output of this method may be used as the initial guess for the MLE
    method.

    Parameters
    ----------
    dist : object
        Thew distribution object
    failures : array, list
        The failure data
    right_censored : array, list
        The right censored data. If there is no data then this should be an
        empty list.
    method : str, optional
        Must be "RRX" or "RRY". Default is RRX.
    force_shape : float, int, optional
        Used to force the shape (beta or sigma) parameter. Default is None which
        will not force the slope.

    Returns
    -------
    model_parameters : list
        The model's parameters in a list. eg. for "Weibull_2P" it will return
        [alpha,beta]. For "Weibull_3P" it will return [alpha,beta,gamma].

    Notes
    -----
    For more information on least squares estimation, see the `documentation <https://reliability.readthedocs.io/en/latest/How%20does%20Least%20Squares%20Estimation%20work.html>`_.

    For cases where the CDF is not linearizable (eg. Weibull_3P), this function
    uses non-linear least squares (NLLS) which uses scipy's curve_fit to find
    the parameters. This may sometimes fail as curve_fit is an optimization
    routine that needs an initial guess provided by this function.
    """

    if min(failures) <= 0 and dist not in ["Normal_2P", "Gumbel_2P"]:
        raise ValueError(
            "failures contains zeros or negative values which are only suitable when dist is Normal_2P or Gumbel_2P"
        )
    if max(failures) >= 1 and dist == "Beta_2P":
        raise ValueError(
            "failures contains values greater than or equal to one which is not allowed when dist is Beta_2P"
        )
    if force_shape is not None and dist not in [
        "Weibull_2P",
        "Normal_2P",
        "Lognormal_2P",
    ]:
        raise ValueError(
            "force_shape can only be applied to Weibull_2P, Normal_2P, and Lognormal_2P"
        )
    if method not in ["RRX", "RRY"]:
        raise ValueError('method must be either "RRX" or "RRY". Default is RRX.')

    from reliability.Probability_plotting import (
        plotting_positions,
    )  # this import needs to be here to prevent circular import if it is in the main module

    x, y = plotting_positions(failures=failures, right_censored=right_censored)
    x = np.array(x)
    y = np.array(y)
    gamma0 = (
        min(np.hstack([failures, right_censored])) - 0.001
    )  # initial guess for gamma when it is required for the 3P fitters
    if gamma0 < 0:
        gamma0 = 0

    if dist == "Weibull_2P":
        xlin = np.log(x)
        ylin = np.log(-np.log(1 - y))
        slope, intercept = linear_regression(
            xlin, ylin, slope=force_shape, RRX_or_RRY=method
        )
        LS_beta = slope
        LS_alpha = np.exp(-intercept / LS_beta)
        guess = [LS_alpha, LS_beta]

    elif dist == "Weibull_3P":
        # Weibull_2P estimate to create the guess for Weibull_3P
        xlin = np.log(x - gamma0)
        ylin = np.log(-np.log(1 - y))
        slope, intercept = linear_regression(xlin, ylin, RRX_or_RRY=method)
        LS_beta = slope
        LS_alpha = np.exp(-intercept / LS_beta)

        # NLLS for Weibull_3P
        def __weibull_3P_CDF(t, alpha, beta, gamma):
            return 1 - np.exp(-(((t - gamma) / alpha) ** beta))

        try:
            curve_fit_bounds = (
                [0, 0, 0],
                [1e20, 1000, gamma0],
            )  # ([alpha_lower,beta_lower,gamma_lower],[alpha_upper,beta_upper,gamma_upper])
            popt, _ = curve_fit(
                __weibull_3P_CDF,
                x,
                y,
                p0=[LS_alpha, LS_beta, gamma0],
                bounds=curve_fit_bounds,
                jac="3-point",
                method="trf",
                max_nfev=300 * len(failures),
            )  # This is the non-linear least squares method. p0 is the initial guess for [alpha,beta,gamma]
            NLLS_alpha = popt[0]
            NLLS_beta = popt[1]
            NLLS_gamma = popt[2]
            guess = [NLLS_alpha, NLLS_beta, NLLS_gamma]
        except (ValueError, LinAlgError, RuntimeError):
            colorprint(
                "WARNING: Non-linear least squares for Weibull_3P failed. The result returned is an estimate that is likely to be incorrect.",
                text_color="red",
            )
            guess = [LS_alpha, LS_beta, gamma0]

    elif dist == "Exponential_1P":
        if method == "RRY":
            x_intercept = None
            y_intercept = 0
        elif method == "RRX":
            y_intercept = None
            x_intercept = 0

        ylin = -np.log(1 - y)
        slope, _ = linear_regression(
            x, ylin, x_intercept=x_intercept, y_intercept=y_intercept, RRX_or_RRY=method
        )  # equivalent to y = m.x
        LS_Lambda = slope
        guess = [LS_Lambda]

    elif dist == "Exponential_2P":
        # Exponential_1P estimate to create the guess for Exponential_2P
        # while it is mathematically possible to use ordinary least squares (y=mx+c) for this, the LS method does not allow bounds on gamma. This can result in gamma > min(data) which should be impossible and will cause other errors.
        xlin = x - gamma0
        ylin = -np.log(1 - y)
        slope, _ = linear_regression(xlin, ylin, x_intercept=0, RRX_or_RRY="RRX")
        LS_Lambda = slope
        # NLLS for Exponential_2P
        def __exponential_2P_CDF(t, Lambda, gamma):
            return 1 - np.exp(-Lambda * (t - gamma))

        try:
            curve_fit_bounds = (
                [0, 0],
                [1e20, gamma0],
            )  # ([Lambda_lower,gamma_lower],[Lambda_upper,gamma_upper])
            popt, _ = curve_fit(
                __exponential_2P_CDF,
                x,
                y,
                p0=[LS_Lambda, gamma0],
                bounds=curve_fit_bounds,
                jac="3-point",
                method="trf",
                max_nfev=300 * len(failures),
            )
            NLLS_Lambda = popt[0]
            NLLS_gamma = popt[1]
            guess = [NLLS_Lambda, NLLS_gamma]
        except (ValueError, LinAlgError, RuntimeError):
            colorprint(
                "WARNING: Non-linear least squares for Exponential_2P failed. The result returned is an estimate that is likely to be incorrect.",
                text_color="red",
            )
            guess = [LS_Lambda, gamma0]

    elif dist == "Normal_2P":
        ylin = ss.norm.ppf(y)
        if force_shape is not None and method == "RRY":
            force_shape = 1 / force_shape  # only needs to be inverted for RRY not RRX
        slope, intercept = linear_regression(
            x, ylin, slope=force_shape, RRX_or_RRY=method
        )
        LS_sigma = 1 / slope
        LS_mu = -intercept * LS_sigma
        guess = [LS_mu, LS_sigma]

    elif dist == "Gumbel_2P":
        ylin = np.log(-np.log(1 - y))
        slope, intercept = linear_regression(x, ylin, RRX_or_RRY=method)
        LS_sigma = 1 / slope
        LS_mu = -intercept * LS_sigma
        guess = [LS_mu, LS_sigma]

    elif dist == "Lognormal_2P":
        xlin = np.log(x)
        ylin = ss.norm.ppf(y)
        if force_shape is not None and method == "RRY":
            force_shape = 1 / force_shape  # only needs to be inverted for RRY not RRX
        slope, intercept = linear_regression(
            xlin, ylin, slope=force_shape, RRX_or_RRY=method
        )
        LS_sigma = 1 / slope
        LS_mu = -intercept * LS_sigma
        guess = [LS_mu, LS_sigma]

    elif dist == "Lognormal_3P":
        # uses least squares to fit a normal distribution to the log of the data and minimizes the correlation coefficient (1 - R^2)
        def __gamma_optimizer(gamma_guess, x, y):
            xlin = np.log(x - gamma_guess)
            ylin = ss.norm.ppf(y)
            _, _, r, _, _ = ss.linregress(xlin, ylin)
            return 1 - (r**2)

        # NLLS for Normal_2P which is used by Lognormal_3P by taking the log of the data. This is more accurate than doing it with Lognormal_3P.
        def __normal_2P_CDF(t, mu, sigma):
            return (1 + erf(((t - mu) / sigma) / 2**0.5)) / 2

        res = minimize(
            __gamma_optimizer, gamma0, args=(x, y), method="TNC", bounds=[([0, gamma0])]
        )  # this obtains gamma
        gamma = res.x[0]

        try:
            curve_fit_bounds = (
                [-1e20, 0],
                [1e20, 1000],
            )  # ([mu_lower,sigma_lower],[mu_upper,sigma_upper])
            popt, _ = curve_fit(
                __normal_2P_CDF,
                np.log(x - gamma),
                y,
                p0=[np.mean(np.log(x - gamma)), np.std(np.log(x - gamma))],
                bounds=curve_fit_bounds,
                jac="3-point",
                method="trf",
                max_nfev=300 * len(failures),
            )  # This is the non-linear least squares method. p0 is the initial guess for [mu,sigma].
            NLLS_mu = popt[0]
            NLLS_sigma = popt[1]
            guess = [NLLS_mu, NLLS_sigma, gamma]
        except (ValueError, LinAlgError, RuntimeError):
            colorprint(
                "WARNING: Non-linear least squares for Lognormal_3P failed. The result returned is an estimate that is likely to be incorrect.",
                text_color="red",
            )
            guess = [np.mean(np.log(x - gamma)), np.std(np.log(x - gamma)), gamma]

    elif dist == "Loglogistic_2P":
        xlin = np.log(x)
        ylin = np.log(1 / y - 1)
        slope, intercept = linear_regression(xlin, ylin, RRX_or_RRY=method)
        LS_beta = -slope
        LS_alpha = np.exp(intercept / LS_beta)
        guess = [LS_alpha, LS_beta]

    elif dist == "Loglogistic_3P":

        def __loglogistic_3P_CDF(t, alpha, beta, gamma):
            return 1 / (1 + ((t - gamma) / alpha) ** -beta)

        # Loglogistic_2P estimate to create the guess for Loglogistic_3P
        xlin = np.log(x - gamma0)
        ylin = np.log(1 / y - 1)
        slope, intercept = linear_regression(xlin, ylin, RRX_or_RRY=method)
        LS_beta = -slope
        LS_alpha = np.exp(intercept / LS_beta)

        try:
            # Loglogistic_3P estimate
            curve_fit_bounds = (
                [0, 0, 0],
                [1e20, 1000, gamma0],
            )  # ([alpha_lower,beta_lower,gamma_lower],[alpha_upper,beta_upper,gamma_upper])
            popt, _ = curve_fit(
                __loglogistic_3P_CDF,
                x,
                y,
                p0=[LS_alpha, LS_beta, gamma0],
                bounds=curve_fit_bounds,
                jac="3-point",
                method="trf",
                max_nfev=300 * len(failures),
            )  # This is the non-linear least squares method. p0 is the initial guess for [alpha,beta,gamma].
            NLLS_alpha = popt[0]
            NLLS_beta = popt[1]
            NLLS_gamma = popt[2]
            guess = [NLLS_alpha, NLLS_beta, NLLS_gamma]
        except (ValueError, LinAlgError, RuntimeError):
            colorprint(
                "WARNING: Non-linear least squares for Loglogistic_3P failed. The result returned is an estimate that is likely to be incorrect.",
                text_color="red",
            )
            guess = [LS_alpha, LS_beta, gamma0]

    elif dist == "Gamma_2P":

        def __gamma_2P_CDF(t, alpha, beta):
            return gammainc(beta, t / alpha)

        # Weibull_2P estimate which is converted to a Gamma_2P initial guess
        xlin = np.log(x)
        ylin = np.log(-np.log(1 - y))
        slope, intercept = linear_regression(xlin, ylin, RRX_or_RRY=method)
        LS_beta = slope
        LS_alpha = np.exp(-intercept / LS_beta)

        # conversion of weibull parameters to gamma parameters. These values were found empirically and the relationship is only an approximate model
        beta_guess = abs(0.6932 * LS_beta**2 - 0.0908 * LS_beta + 0.2804)
        alpha_guess = abs(LS_alpha / (-0.00095 * beta_guess**2 + 1.1119 * beta_guess))

        def __perform_curve_fit():  # separated out for repeated use
            curve_fit_bounds = (
                [0, 0],
                [1e20, 1000],
            )  # ([alpha_lower,beta_lower],[alpha_upper,beta_upper])
            popt, _ = curve_fit(
                __gamma_2P_CDF,
                x,
                y,
                p0=[alpha_guess, beta_guess],
                bounds=curve_fit_bounds,
                jac="3-point",
                method="trf",
                max_nfev=300 * len(failures),
            )  # This is the non-linear least squares method. p0 is the initial guess for [alpha,beta]
            return [popt[0], popt[1]]

        try:
            # Gamma_2P estimate
            guess = __perform_curve_fit()
        except (ValueError, LinAlgError, RuntimeError):
            try:
                guess = __perform_curve_fit()
                # We repeat the same attempt at a curve_fit because of a very strange event.
                # When Fit_Gamma_2P is run twice in a row, the second attempt fails if there was a probability plot generated for the first attempt.
                # This was unable to debugged since the curve_fit has identical inputs each run and the curve_fit should not interact with the probability plot in any way.
                # One possible cause of this error may relate to memory usage though this is not confirmed.
                # By simply repeating the attempted curve_fit one more time, it often will work perfectly on the second try.
                # If it fails the second try then we report the failure and return the initial guess.
            except (ValueError, LinAlgError, RuntimeError):
                colorprint(
                    "WARNING: Non-linear least squares for Gamma_2P failed. The result returned is an estimate that is likely to be incorrect.",
                    text_color="red",
                )
                guess = [alpha_guess, beta_guess]

    elif dist == "Gamma_3P":

        def __gamma_2P_CDF(t, alpha, beta):
            return gammainc(beta, t / alpha)

        def __gamma_3P_CDF(t, alpha, beta, gamma):
            return gammainc(beta, (t - gamma) / alpha)

        # Weibull_2P estimate which is converted to a Gamma_2P initial guess
        xlin = np.log(x - gamma0 * 0.98)
        ylin = np.log(-np.log(1 - y))
        slope, intercept = linear_regression(xlin, ylin, RRX_or_RRY=method)
        LS_beta = slope
        LS_alpha = np.exp(-intercept / LS_beta)

        # conversion of weibull parameters to gamma parameters. These values were found empirically and the relationship is only an approximate model
        beta_guess = abs(0.6932 * LS_beta**2 - 0.0908 * LS_beta + 0.2804)
        alpha_guess = abs(LS_alpha / (-0.00095 * beta_guess**2 + 1.1119 * beta_guess))

        def __perform_curve_fit_gamma_2P():  # separated out for repeated use
            curve_fit_bounds = (
                [0, 0],
                [1e20, 1000],
            )  # ([alpha_lower,beta_lower],[alpha_upper,beta_upper])
            popt, _ = curve_fit(
                __gamma_2P_CDF,
                x - gamma0 * 0.98,
                y,
                p0=[alpha_guess, beta_guess],
                bounds=curve_fit_bounds,
                jac="3-point",
                method="trf",
                max_nfev=300 * len(failures),
            )  # This is the non-linear least squares method. p0 is the initial guess for [alpha,beta]
            return [popt[0], popt[1]]

        def __perform_curve_fit_gamma_3P():  # separated out for repeated use
            curve_fit_bounds_3P = (
                [0, 0, 0],
                [1e20, 1000, gamma0],
            )  # ([alpha_lower,beta_lower,gamma_lower],[alpha_upper,beta_upper,gamma_upper])
            popt, _ = curve_fit(
                __gamma_3P_CDF,
                x,
                y,
                p0=[NLLS_alpha_2P, NLLS_beta_2P, gamma0 * 0.98],
                bounds=curve_fit_bounds_3P,
                jac="3-point",
                method="trf",
                max_nfev=300 * len(failures),
            )  # This is the non-linear least squares method. p0 is the initial guess for [alpha,beta,gamma]
            return [popt[0], popt[1], popt[2]]

        try:
            # Gamma_2P estimate to create the guess for Gamma_3P
            guess_2P = __perform_curve_fit_gamma_2P()
            NLLS_alpha_2P, NLLS_beta_2P = guess_2P[0], guess_2P[1]
            try:
                # Gamma_3P estimate
                guess = __perform_curve_fit_gamma_3P()
            except (ValueError, LinAlgError, RuntimeError):
                try:
                    # try gamma_3P a second time
                    guess = __perform_curve_fit_gamma_3P()
                except (ValueError, LinAlgError, RuntimeError):
                    colorprint(
                        "WARNING: Non-linear least squares for Gamma_3P failed during Gamma_3P optimization. The result returned is an estimate that is likely to be incorrect.",
                        text_color="red",
                    )
                    guess = [NLLS_alpha_2P, NLLS_beta_2P, gamma0 * 0.98]
        except (ValueError, LinAlgError, RuntimeError):
            # We repeat the same attempt at a curve_fit because of a very strange event.
            # When Fit_Gamma_3P is run twice in a row, the second attempt fails if there was a probability plot generated for the first attempt.
            # This was unable to debugged since the curve_fit has identical inputs each run and the curve_fit should not interact with the probability plot in any way.
            # One possible cause of this error may relate to memory usage though this is not confirmed.
            # By simply repeating the attempted curve_fit one more time, it often will work perfectly on the second try.
            # If it fails the second try then we report the failure and return the initial guess.
            try:
                guess_2P = __perform_curve_fit_gamma_2P()
                NLLS_alpha_2P, NLLS_beta_2P = guess_2P[0], guess_2P[1]
                try:
                    # Gamma_3P estimate
                    guess = __perform_curve_fit_gamma_3P()
                except (ValueError, LinAlgError, RuntimeError):
                    try:
                        # try gamma_3P for a second time
                        guess = __perform_curve_fit_gamma_3P()
                    except (ValueError, LinAlgError, RuntimeError):
                        colorprint(
                            "WARNING: Non-linear least squares for Gamma_3P failed during Gamma_3P optimization. The result returned is an estimate that is likely to be incorrect.",
                            text_color="red",
                        )
                        guess = [NLLS_alpha_2P, NLLS_beta_2P, gamma0 * 0.98]
            except (ValueError, LinAlgError, RuntimeError):
                colorprint(
                    "WARNING: Non-linear least squares for Gamma_3P failed during Gamma_2P optimization. The result returned is an estimate that is likely to be incorrect.",
                    text_color="red",
                )
                guess = [alpha_guess, beta_guess, gamma0 * 0.98]

    elif dist == "Beta_2P":

        def __beta_2P_CDF(t, alpha, beta):
            return betainc(alpha, beta, t)

        try:
            curve_fit_bounds = (
                [0, 0],
                [100, 100],
            )  # ([alpha_lower,beta_lower],[alpha_upper,beta_upper])
            popt, _ = curve_fit(
                __beta_2P_CDF,
                x,
                y,
                p0=[2, 1],
                bounds=curve_fit_bounds,
                jac="3-point",
                method="trf",
                max_nfev=300 * len(failures),
            )  # This is the non-linear least squares method. p0 is the initial guess for [alpha,beta]
            NLLS_alpha = popt[0]
            NLLS_beta = popt[1]
            guess = [NLLS_alpha, NLLS_beta]
        except (ValueError, LinAlgError, RuntimeError):
            colorprint(
                "WARNING: Non-linear least squares for Beta_2P failed. The result returned is an estimate that is likely to be incorrect.",
                text_color="red",
            )
            guess = [2, 1]
    else:
        raise ValueError('Unknown dist. Use the correct name. eg. "Weibull_2P"')
    return guess


class LS_optimization:
    """
    This function is a control function for least squares regression and it is
    used by each of the Fitters. There is no actual "optimization" done here,
    with the exception of checking which method (RRX or RRY) gives the better
    solution.

    Parameters
    ----------
    func_name : str
        The function to be fitted. Eg. "Weibull_2P".
    LL_func : function
        The log-likelihood function from the fitter
    failures : list, array
        The failure data
    right_censored : list, array
        The right censored data. If there is no right censored data then this
        should be an empty array.
    method : str, optional
        Must be either "RRX", "RRY", "LS", or "NLLS". Default is "LS".
    force_shape : float, int, optional
        The shape parameter to be forced. Default is None which results in no
        forcing of the shape parameter.
    LL_func_force : function
        The log-likelihood function for when the shape parameter is forced. Only
        required if force_shape is not None.

    Returns
    -------
    guess : list
        The guess of the models parameters. The length of this list depends on
        the number of parameters in the model. The guess is obtained using
        Utils.least_squares
    method : str
        The method used. This will be either "RRX", "RRY" or "NLLS".

    Notes
    -----
    If method="LS" then both "RRX" and "RRY" will be tried and the best one will
    be returned.
    """

    def __init__(
        self,
        func_name,
        LL_func,
        failures,
        right_censored,
        method="LS",
        force_shape=None,
        LL_func_force=None,
    ):
        if method not in ["RRX", "RRY", "LS", "NLLS"]:
            raise ValueError(
                "method must be either RRX, RRY, LS, or NLLS. Default is LS"
            )
        if func_name in [
            "Weibull_3P",
            "Gamma_2P",
            "Gamma_3P",
            "Beta_2P",
            "Lognormal_3P",
            "Loglogistic_3P",
            "Exponential_2P",
        ]:
            guess = least_squares(
                dist=func_name, failures=failures, right_censored=right_censored
            )
            LS_method = "NLLS"
        elif method in ["RRX", "RRY"]:
            guess = least_squares(
                dist=func_name,
                failures=failures,
                right_censored=right_censored,
                method=method,
                force_shape=force_shape,
            )
            LS_method = method
        else:  # LS
            # RRX
            guess_RRX = least_squares(
                dist=func_name,
                failures=failures,
                right_censored=right_censored,
                method="RRX",
                force_shape=force_shape,
            )
            if force_shape is not None:
                loglik_RRX = -LL_func_force(
                    guess_RRX, failures, right_censored, force_shape
                )
            else:
                loglik_RRX = -LL_func(guess_RRX, failures, right_censored)
            # RRY
            guess_RRY = least_squares(
                dist=func_name,
                failures=failures,
                right_censored=right_censored,
                method="RRY",
                force_shape=force_shape,
            )
            if force_shape is not None:
                loglik_RRY = -LL_func_force(
                    guess_RRY, failures, right_censored, force_shape
                )
            else:
                loglik_RRY = -LL_func(guess_RRY, failures, right_censored)
            # take the best one
            if abs(loglik_RRX) < abs(loglik_RRY):  # RRX is best
                LS_method = "RRX"
                guess = guess_RRX
            else:  # RRY is best
                LS_method = "RRY"
                guess = guess_RRY
        self.guess = guess
        self.method = LS_method


class MLE_optimization:
    """
    This function performs Maximum Likelihood Estimation (MLE) to find the
    optimal parameters of the probability distribution. This functions is used
    by each of the fitters.

    Parameters
    ----------
    func_name : str
        The function to be fitted. Eg. "Weibull_2P".
    LL_func : function
        The log-likelihood function from the fitter
    initial_guess : list, array
        The initial guess of the model parameters that is used by the optimizer.
    failures : list, array
        The failure data
    right_censored : list, array
        The right censored data. If there is no right censored data then this
        should be an empty array.
    optimizer : str, None
        This must be either "TNC", "L-BFGS-B", "nelder-mead", "powell", "best",
        "all" or None. Fot detail on how these optimizers are used, please see
        the `documentation <https://reliability.readthedocs.io/en/latest/Optimizers.html>`_.
    force_shape : float, int, optional
        The shape parameter to be forced. Default is None which results in no
        forcing of the shape parameter.
    LL_func_force : function
        The log-likelihood function for when the shape parameter is forced. Only
        required if force_shape is not None.

    Returns
    -------
    scale : float
        Only returned for Weibull_2P, Weibull_3P, Lognormal_2P, Lognormal_3P,
        Gamma_2P, Gamma_3P, Loglogistic_2P, Loglogistic_3P, Exponential_1P,
        Exponential_2P, Normal_2P, Beta_2P, and Gumbel_2P
    shape : float
        Only returned for Weibull_2P, Weibull_3P, Lognormal_2P, Lognormal_3P,
        Gamma_2P, Gamma_3P, Loglogistic_2P, Loglogistic_3P, Normal_2P, Beta_2P,
        and Gumbel_2P
    alpha : float
        Only returned for Weibull_DS, Weibull_ZI and Weibull_DSZI
    beta : float
        Only returned for Weibull_DS, Weibull_ZI and Weibull_DSZI
    gamma : float
        Only returned for Weibull_3P, Exponential_2P, Gamma_3P, Lognormal_3P,
        and Loglogistic_3P.
    DS : float
        Only returned for Weibull_DS and Weibull_DSZI
    ZI : float
        Only returned for Weibull_ZI and Weibull_DSZI
    alpha_1 : float
        Only returned for Weibull_mixture and Weibull_CR
    beta_1 : float
        Only returned for Weibull_mixture and Weibull_CR
    alpha_2 : float
        Only returned for Weibull_mixture and Weibull_CR
    beta_2 : float
        Only returned for Weibull_mixture and Weibull_CR
    proportion_1 : float
        Only returned for Weibull_mixture
    proportion_2 : float
        Only returned for Weibull_mixture
    success : bool
        Whether at least one optimizer succeeded. If False then the least
        squares result will be returned in place of the MLE result.
    optimizer : str, None
        The optimizer used. If MLE failed then None is returned as the
        optimizer.

    Notes
    -----
    Not all of the above returns are always returned. It depends on which model
    is being used.

    If the MLE method fails then the initial guess (from least squares) will be
    returned with a printed warning.
    """

    def __init__(
        self,
        func_name,
        LL_func,
        initial_guess,
        failures,
        right_censored,
        optimizer,
        force_shape=None,
        LL_func_force=None,
    ):
        # this sub-function does the actual optimization. It is called each time a new optimizer is tried
        def loglik_optimizer(
            LL_func,
            guess,
            failures,
            right_censored,
            bounds,
            optimizer,
            force_shape,
            LL_func_force,
            func_name,
        ):
            """
            This sub-function does the actual optimization. It is called each
            time a new optimizer is tried.

            Parameters
            ----------
            LL_func : function
                The log-likelihood function from the fitter
            guess : list, array
                The initial guess of the model parameters that is used by the optimizer.
            failures : list, array
                The failure data
            right_censored : list, array
                The right censored data. If there is no right censored data then this
                should be an empty array.
            bounds : list
                The bounds on the solution
            optimizer : str, None
                This must be either "TNC", "L-BFGS-B", "nelder-mead", or
                "powell".
            force_shape : float, int, optional
                The shape parameter to be forced. Default is None which results in no
                forcing of the shape parameter.
            LL_func_force : function
                The log-likelihood function for when the shape parameter is forced. Only
                required if force_shape is not None.
            func_name : str
                The function name. eg. "Weibull_2P"

            Returns
            -------
            success : bool
                Whether the optimizer was successful
            log_likelihood : float
                The log-likelihood of the solution
            model_parameters : array
                The model parameters of the solution

            Notes
            -----
            The returns are provided in a tuple of success, log_likelihood,
            model_parameters.
            """
            delta_LL = 1
            LL_array = [1000000]
            runs = 0

            if func_name in ["Weibull_ZI", "Weibull_DSZI"]:
                ZI = True
            else:
                ZI = False

            if ZI is True:  # Zero Inflated distribution (applies to ZI and DSZI)
                args = (failures[failures == 0], failures[failures > 0], right_censored)
            else:
                args = (failures, right_censored)

            if force_shape is None:
                while delta_LL > 0.001 and runs < 5:
                    # exits after LL convergence or 5 iterations
                    runs += 1
                    result = minimize(
                        value_and_grad(LL_func),
                        guess,
                        args=args,
                        jac=True,
                        method=optimizer,
                        bounds=bounds,
                    )
                    guess = result.x  # update the guess each iteration
                    if ZI is True:
                        LL2 = 2 * LL_func(
                            guess,
                            failures[failures == 0],
                            failures[failures > 0],
                            right_censored,
                        )
                    else:
                        LL2 = 2 * LL_func(guess, failures, right_censored)
                    LL_array.append(np.abs(LL2))
                    delta_LL = abs(LL_array[-1] - LL_array[-2])
            else:  # this will only be run for Weibull_2P, Normal_2P, and Lognormal_2P so the guess is structured with this in mind
                bounds = [bounds[0]]
                guess = [guess[0]]
                while (
                    delta_LL > 0.001 and runs < 5
                ):  # exits after LL convergence or 5 iterations
                    runs += 1
                    result = minimize(
                        value_and_grad(LL_func_force),
                        guess,
                        args=(failures, right_censored, force_shape),
                        jac=True,
                        method=optimizer,
                        bounds=bounds,
                    )
                    guess = result.x
                    LL2 = 2 * LL_func_force(
                        guess, failures, right_censored, force_shape
                    )
                    LL_array.append(np.abs(LL2))
                    delta_LL = abs(LL_array[-1] - LL_array[-2])
                    guess = result.x  # update the guess each iteration
            return result.success, LL_array[-1], result.x

        # generate the bounds on the solution
        gamma0 = max(0, min(np.hstack([failures, right_censored])) - 0.0001)
        if func_name in ["Weibull_2P", "Gamma_2P", "Beta_2P", "Loglogistic_2P"]:
            bounds = [(0, None), (0, None)]
        elif func_name in ["Weibull_3P", "Gamma_3P", "Loglogistic_3P"]:
            bounds = [(0, None), (0, None), (0, gamma0)]
        elif func_name in ["Normal_2P", "Gumbel_2P", "Lognormal_2P"]:
            bounds = [(None, None), (0, None)]
        elif func_name == "Lognormal_3P":
            bounds = [(None, None), (0, None), (0, gamma0)]
        elif func_name == "Exponential_1P":
            bounds = [(0, None)]
        elif func_name == "Exponential_2P":
            bounds = [(0, None), (0, gamma0)]
        elif func_name == "Weibull_mixture":
            bounds = [
                (0.0001, None),
                (0.0001, None),
                (0.0001, None),
                (0.0001, None),
                (0.0001, 0.9999),
            ]
        elif func_name == "Weibull_CR":
            bounds = [(0.0001, None), (0.0001, None), (0.0001, None), (0.0001, None)]
        elif func_name == "Weibull_DSZI":
            bounds = [(0.0001, None), (0.0001, None), (0.00001, 1), (0, 0.99999)]
        elif func_name == "Weibull_DS":
            bounds = [(0.0001, None), (0.0001, None), (0.00001, 1)]
        elif func_name == "Weibull_ZI":
            bounds = [(0.0001, None), (0.0001, None), (0, 0.99999)]
        else:
            raise ValueError(
                'func_name is not recognised. Use the correct name e.g. "Weibull_2P"'
            )

        # determine which optimizers to use
        stop_after_success = False
        if (
            optimizer is None
        ):  # default is to try in this order but stop after one succeeds
            optimizers_to_try = ["TNC", "L-BFGS-B", "nelder-mead", "powell"]
            stop_after_success = True
        else:
            if optimizer in [
                "best",
                "BEST",
                "all",
                "ALL",
            ]:  # try all of the bounded optimizers
                optimizers_to_try = ["TNC", "L-BFGS-B", "nelder-mead", "powell"]
            elif optimizer.upper() == "TNC":
                optimizers_to_try = ["TNC"]
            elif optimizer.upper() in ["L-BFGS-B", "LBFGSB"]:
                optimizers_to_try = ["L-BFGS-B"]
            elif optimizer.upper() == "POWELL":
                optimizers_to_try = ["powell"]
            elif optimizer.upper() in ["NELDER-MEAD", "NELDERMEAD"]:
                optimizers_to_try = ["nelder-mead"]
            else:
                raise ValueError(
                    str(
                        str(optimizer)
                        + ' is not a valid optimizer. Please specify either "TNC", "L-BFGS-B", "nelder-mead", "powell" or "best".'
                    )
                )

        # use each of the optimizers specified
        ALL_successes = []
        ALL_loglik = []
        ALL_results = []
        ALL_opt_names = []
        optimizers_tried_str = "Optimizers tried:"
        for opt in optimizers_to_try:
            optim_results = loglik_optimizer(
                LL_func,
                initial_guess,
                failures,
                right_censored,
                bounds,
                opt,
                force_shape,
                LL_func_force,
                func_name,
            )
            ALL_successes.append(optim_results[0])
            ALL_loglik.append(optim_results[1])
            ALL_results.append(optim_results[2])
            ALL_opt_names.append(opt)
            optimizers_tried_str = optimizers_tried_str + " " + opt + ","
            if optim_results[0] is True and stop_after_success is True:
                break  # stops after it finds one that works
        optimizers_tried_str = optimizers_tried_str[0:-1]  # remove the last comma
        # extract the results
        if True not in ALL_successes:
            # everything failed, need to return the initial guess
            self.success = False
            self.optimizer = None
            if func_name == "Weibull_mixture":
                colorprint(
                    "WARNING: MLE estimates failed for Weibull_mixture. The initial estimates have been returned. These results may not be as accurate as MLE. "
                    + optimizers_tried_str,
                    text_color="red",
                )
                self.alpha_1 = initial_guess[0]
                self.beta_1 = initial_guess[1]
                self.alpha_2 = initial_guess[2]
                self.beta_2 = initial_guess[3]
                self.proportion_1 = initial_guess[4]
                self.proportion_2 = 1 - initial_guess[4]
            elif func_name == "Weibull_CR":
                colorprint(
                    "WARNING: MLE estimates failed for Weibull_CR. The initial estimates have been returned. These results may not be as accurate as MLE. "
                    + optimizers_tried_str,
                    text_color="red",
                )
                self.alpha_1 = initial_guess[0]
                self.beta_1 = initial_guess[1]
                self.alpha_2 = initial_guess[2]
                self.beta_2 = initial_guess[3]
            elif func_name == "Weibull_DSZI":
                colorprint(
                    "WARNING: MLE estimates failed for Weibull_DSZI. The initial estimates have been returned. These results may not be as accurate as MLE. "
                    + optimizers_tried_str,
                    text_color="red",
                )
                self.alpha = initial_guess[0]
                self.beta = initial_guess[1]
                self.DS = initial_guess[2]
                self.ZI = initial_guess[3]
            elif func_name == "Weibull_DS":
                colorprint(
                    "WARNING: MLE estimates failed for Weibull_DS. The initial estimates have been returned. These results may not be as accurate as MLE. "
                    + optimizers_tried_str,
                    text_color="red",
                )
                self.alpha = initial_guess[0]
                self.beta = initial_guess[1]
                self.DS = initial_guess[2]
            elif func_name == "Weibull_ZI":
                colorprint(
                    "WARNING: MLE estimates failed for Weibull_ZI. The initial estimates have been returned. These results may not be as accurate as MLE. "
                    + optimizers_tried_str,
                    text_color="red",
                )
                self.alpha = initial_guess[0]
                self.beta = initial_guess[1]
                self.ZI = initial_guess[2]
            else:
                colorprint(
                    str(
                        "WARNING: MLE estimates failed for "
                        + func_name
                        + ". The least squares estimates have been returned. These results may not be as accurate as MLE. "
                        + optimizers_tried_str
                    ),
                    text_color="red",
                )
                if force_shape is None:
                    self.scale = initial_guess[0]  # alpha, mu, Lambda
                    if func_name not in ["Exponential_1P", "Exponential_2P"]:
                        self.shape = initial_guess[1]  # beta, sigma
                    else:
                        if func_name == "Exponential_2P":
                            self.gamma = initial_guess[1]  # gamma for Exponential_2P
                    if func_name in [
                        "Weibull_3P",
                        "Gamma_3P",
                        "Loglogistic_3P",
                        "Lognormal_3P",
                    ]:
                        # gamma for Weibull_3P, Gamma_3P, Loglogistic_3P, Lognormal_3P
                        self.gamma = initial_guess[2]
                # this will only be reached for Weibull_2P, Normal_2P and Lognormal_2P so the scale and shape extraction is fine for these
                else:
                    self.scale = initial_guess[0]
                    self.shape = force_shape
        else:
            # at least one optimizer succeeded. Need to drop the failed ones then get the best of the successes
            items = np.arange(0, len(ALL_successes))[::-1]

            for i in items:
                if ALL_successes[i] is not True:
                    ALL_successes.pop(i)
                    ALL_loglik.pop(i)
                    ALL_results.pop(i)
                    ALL_opt_names.pop(i)
            idx_best = ALL_loglik.index(min(ALL_loglik))
            params = ALL_results[idx_best]
            self.optimizer = ALL_opt_names[idx_best]
            self.success = True

            if func_name == "Weibull_mixture":
                self.alpha_1 = params[0]
                self.beta_1 = params[1]
                self.alpha_2 = params[2]
                self.beta_2 = params[3]
                self.proportion_1 = params[4]
                self.proportion_2 = 1 - params[4]
            elif func_name == "Weibull_CR":
                self.alpha_1 = params[0]
                self.beta_1 = params[1]
                self.alpha_2 = params[2]
                self.beta_2 = params[3]
            elif func_name == "Weibull_DSZI":
                self.alpha = params[0]
                self.beta = params[1]
                self.DS = params[2]
                self.ZI = params[3]
            elif func_name == "Weibull_DS":
                self.alpha = params[0]
                self.beta = params[1]
                self.DS = params[2]
            elif func_name == "Weibull_ZI":
                self.alpha = params[0]
                self.beta = params[1]
                self.ZI = params[2]
            else:
                if force_shape is None:
                    self.scale = params[0]  # alpha, mu, Lambda
                    if func_name not in ["Exponential_1P", "Exponential_2P"]:
                        self.shape = params[1]  # beta, sigma
                    else:
                        if func_name == "Exponential_2P":
                            self.gamma = params[1]  # gamma for Exponential_2P
                    if func_name in [
                        "Weibull_3P",
                        "Gamma_3P",
                        "Loglogistic_3P",
                        "Lognormal_3P",
                    ]:
                        self.gamma = params[
                            2
                        ]  # gamma for Weibull_3P, Gamma_3P, Loglogistic_3P, Lognormal_3P
                else:  # this will only be reached for Weibull_2P, Normal_2P and Lognormal_2P so the scale and shape extraction is fine for these
                    self.scale = params[0]
                    self.shape = force_shape


class fitters_input_checking:
    """
    This function performs error checking and some basic default operations for
    all the inputs given to each of the fitters.

    Parameters
    ----------
    dist : str
        Must be one of "Everything", "Weibull_2P", "Weibull_3P", "Gamma_2P",
        "Gamma_3P", "Exponential_1P", "Exponential_2P", "Gumbel_2P",
        "Normal_2P", "Lognormal_2P", "Lognormal_3P", "Loglogistic_2P",
        "Loglogistic_3P", "Beta_2P", "Weibull_Mixture", "Weibull_CR",
        "Weibull_DSZI", "Weibull_DS", "Weibull_ZI".
    failures : array, list
        The failure data
    right_censored : array, list, optional
        The right censored data
    method : str, optional
        Must be either "MLE","LS","RRX", or "RRY". Some flexibility in input is
        tolerated. eg "LS", "LEAST SQUARES", "LSQ", "NLRR", "NLLS" will all be
        recogsised as "LS". Default is MLE
    optimizer : str, optional
        Must be one of "TNC", "L-BFGS-B", "nelder-mead", "powell", "best".
        Default is None which will result in each being tried until one
        succeeds. For more detail see the `documentation <https://reliability.readthedocs.io/en/latest/Optimizers.html>`_.
    CI : float, optional
        Confidence interval. Must be between 0 and 1. Default is 0.95 for 95%
        confidence interval (2 sided).
    quantiles : array, list, bool, optional
        An array or list of the quantiles to calculate. If True then the
        default array will be used. Default array is [0.01, 0.05, 0.1, 0.2, 0.25,
        0.5, 0.75, 0.8, 0.9, 0.95, 0.99].
        If False then no quantiles will be calculated. Default is False.
    force_beta : float, int, optional
        Used to force beta for the Weibull_2P distribution. Default is None
        which will not force beta.
    force_sigma : float, int, optional
        Used to force sigma for the Normal_2P and Lognormal_2P distributions.
        Default is None which will not force sigma.
    CI_type : str, optional
        Must be either "time" or "reliability". Default is None which results in
        "time" being used (controlled in Fitters). Some flexibility is strings
        is allowed. eg. "r", "R", "rel", "REL", "reliability", "RELIABILITY"
        will all be recognized as "reliability".

    Returns
    -------
    failures : array
        The failure times
    right_censored : array
        The right censored times. This will be an empty array if the input was
        None.
    CI : float
        The confidence interval (between 0 and 1)
    method : str, None
        This will return "MLE", "LS", "RRX", "RRY" or None.
    optimizer : str, None
        This will return "TNC", "L-BFGS-B", "nelder-mead", "powell", "best", or
        None.
    quantiles : array, None
        The quantiles or None.
    force_beta : float, None
        The beta parameter to be forced in Weibull_2P
    force_sigma : float, None
            The sigma parameter to be forced in Normal_2P, or Lognormal_2P
    CI_type : str, None
        "time", "reliability", or None

    Notes
    -----
    For full detail on what is checked and the errors produced, you should read
    the source code.

    Some returns are None if the input is None. How None affects the behavior
    is governed by other functions such as the individual fitters and other
    Utils.
    """

    def __init__(
        self,
        dist,
        failures,
        right_censored=None,
        method=None,
        optimizer=None,
        CI=0.95,
        quantiles=False,
        force_beta=None,
        force_sigma=None,
        CI_type=None,
    ):

        if dist not in [
            "Everything",
            "Weibull_2P",
            "Weibull_3P",
            "Gamma_2P",
            "Gamma_3P",
            "Exponential_1P",
            "Exponential_2P",
            "Gumbel_2P",
            "Normal_2P",
            "Lognormal_2P",
            "Lognormal_3P",
            "Loglogistic_2P",
            "Loglogistic_3P",
            "Beta_2P",
            "Weibull_Mixture",
            "Weibull_CR",
            "Weibull_DSZI",
            "Weibull_DS",
            "Weibull_ZI",
        ]:
            raise ValueError(
                "incorrect dist specified. Use the correct name. eg. Weibull_2P"
            )

        # fill right_censored with empty list if not specified
        if right_censored is None:
            right_censored = []

        # type checking and converting to arrays for failures and right_censored
        if type(failures) not in [list, np.ndarray]:
            raise ValueError("failures must be a list or array of failure data")
        if type(right_censored) not in [list, np.ndarray]:
            raise ValueError(
                "right_censored must be a list or array of right censored failure data"
            )
        failures = np.asarray(failures).astype(float)
        right_censored = np.asarray(right_censored).astype(float)

        # check failures and right_censored are in the right range for the distribution
        if dist not in ["Normal_2P", "Gumbel_2P"]:
            # raise an error for values below zero
            all_data = np.hstack([failures, right_censored])
            if dist == "Beta_2P" and (min(all_data) < 0 or max(all_data) > 1):
                raise ValueError(
                    "All failure and censoring times for the beta distribution must be between 0 and 1."
                )
            elif min(all_data) < 0:
                raise ValueError(
                    "All failure and censoring times must be greater than zero."
                )
            # remove zeros and issue a warning. These are impossible since the pdf should be 0 at t=0. Leaving them in causes an error.
            rc0 = right_censored
            f0 = failures
            right_censored = rc0[rc0 != 0]
            failures = f0[f0 != 0]
            if len(failures) != len(f0):
                if dist == "Everything":
                    colorprint(
                        "WARNING: failures contained zeros. These have been removed to enable fitting of all distributions. Consider using Fit_Weibull_ZI or Fit_Weibull_DSZI if you need to include the zero inflation in the models.",
                        text_color="red",
                    )
                else:
                    colorprint(
                        str(
                            "WARNING: failures contained zeros. These have been removed to enable fitting of the "
                            + dist
                            + " distribution. Consider using Fit_Weibull_ZI or Fit_Weibull_DSZI if you need to include the zero inflation in the model."
                        ),
                        text_color="red",
                    )

            if len(right_censored) != len(rc0):
                if dist == "Everything":
                    colorprint(
                        "WARNING: right_censored contained zeros. These have been removed to enable fitting of all distributions.",
                        text_color="red",
                    )
                else:
                    colorprint(
                        str(
                            "WARNING: right_censored contained zeros. These have been removed to enable fitting of the "
                            + dist
                            + " distribution."
                        ),
                        text_color="red",
                    )
            if dist == "Beta_2P":
                rc1 = right_censored
                f1 = failures
                right_censored = rc1[rc1 != 1]
                failures = f1[f1 != 1]
                if len(failures) != len(f1):
                    colorprint(
                        "WARNING: failures contained ones. These have been removed to enable fitting of the Beta_2P distribution.",
                        text_color="red",
                    )
                if len(right_censored) != len(rc1):
                    colorprint(
                        "WARNING: right_censored contained ones. These have been removed to enable fitting of the Beta_2P distribution.",
                        text_color="red",
                    )

        # type and value checking for CI
        if type(CI) not in [float, np.float64]:
            raise ValueError(
                "CI must be between 0 and 1. Default is 0.95 for 95% Confidence interval."
            )
        if CI <= 0 or CI >= 1:
            raise ValueError(
                "CI must be between 0 and 1. Default is 0.95 for 95% Confidence interval."
            )

        # error checking for optimizer
        if optimizer is not None:
            if type(optimizer) is not str:
                raise ValueError(
                    'optimizer must be either "TNC", "L-BFGS-B", "nelder-mead", "powell", "best" or None. For more detail see the documentation: https://reliability.readthedocs.io/en/latest/Optimizers.html'
                )
            if optimizer.upper() == "TNC":
                optimizer = "TNC"
            elif optimizer.upper() == "POWELL":
                optimizer = "powell"
            elif optimizer.upper() in ["L-BFGS-B", "LBFGSB"]:
                optimizer = "L-BFGS-B"
            elif optimizer.upper() in ["NELDER-MEAD", "NELDERMEAD", "NM"]:
                optimizer = "nelder-mead"
            elif optimizer.upper() in ["ALL", "BEST"]:
                optimizer = "best"
            else:
                raise ValueError(
                    'optimizer must be either "TNC", "L-BFGS-B", "nelder-mead", "powell", "best" or None. For more detail see the documentation: https://reliability.readthedocs.io/en/latest/Optimizers.html'
                )

        # error checking for method
        if method is not None:
            if type(method) is not str:
                raise ValueError(
                    'method must be either "MLE" (maximum likelihood estimation), "LS" (least squares), "RRX" (rank regression on X), or "RRY" (rank regression on Y).'
                )
            if method.upper() == "RRX":
                method = "RRX"
            elif method.upper() == "RRY":
                method = "RRY"
            elif method.upper() in ["LS", "LEAST SQUARES", "LSQ", "NLRR", "NLLS"]:
                method = "LS"
            elif method.upper() in [
                "MLE",
                "ML",
                "MAXIMUM LIKELIHOOD ESTIMATION",
                "MAXIMUM LIKELIHOOD",
                "MAX LIKELIHOOD",
            ]:
                method = "MLE"
            else:
                raise ValueError(
                    'method must be either "MLE" (maximum likelihood estimation), "LS" (least squares), "RRX" (rank regression on X), or "RRY" (rank regression on Y).'
                )

        # quantiles error checking
        if type(quantiles) in [str, bool]:
            if quantiles in ["auto", True, "default", "on"]:
                # quantiles to be used as the defaults in the table of quantiles #
                quantiles = np.array(
                    [0.01, 0.05, 0.1, 0.2, 0.25, 0.5, 0.75, 0.8, 0.9, 0.95, 0.99]
                )
        elif quantiles is not None:
            if type(quantiles) not in [list, np.ndarray]:
                raise ValueError("quantiles must be a list or array")
            quantiles = np.asarray(quantiles)
            if max(quantiles) >= 1 or min(quantiles) <= 0:
                raise ValueError("quantiles must be between 0 and 1")

        # force_beta and force_sigma error checking
        if force_beta is not None:
            if force_beta <= 0:
                raise ValueError("force_beta must be greater than 0.")
            if type(force_beta) == int:
                force_beta = float(
                    force_beta
                )  # autograd needs floats. crashes with ints
        if force_sigma is not None:
            if force_sigma <= 0:
                raise ValueError("force_sigma must be greater than 0.")
            if type(force_sigma) == int:
                force_sigma = float(
                    force_sigma
                )  # autograd needs floats. crashes with ints

        # minimum number of failures checking
        if dist in ["Weibull_3P", "Gamma_3P", "Lognormal_3P", "Loglogistic_3P"]:
            min_failures = 3
        elif dist in [
            "Weibull_2P",
            "Gamma_2P",
            "Normal_2P",
            "Lognormal_2P",
            "Gumbel_2P",
            "Loglogistic_2P",
            "Beta_2P",
            "Exponential_2P",
            "Everything",
            "Weibull_ZI",
            "Weibull_DS",
            "Weibull_DSZI",
        ]:
            if force_sigma is None and force_beta is None:
                min_failures = 2
            else:
                min_failures = 1
        elif dist == "Exponential_1P":
            min_failures = 1
        elif dist in ["Weibull_Mixture", "Weibull_CR"]:
            min_failures = 4

        number_of_unique_failures = len(
            np.unique(failures)
        )  # failures need to be unique. ie. [4,4] counts as 1 distinct failure
        if number_of_unique_failures < min_failures:
            if force_beta is not None:
                raise ValueError(
                    str(
                        "The minimum number of distinct failures required for a "
                        + dist
                        + " distribution with force_beta specified is "
                        + str(min_failures)
                        + "."
                    )
                )
            elif force_sigma is not None:
                raise ValueError(
                    str(
                        "The minimum number of distinct failures required for a "
                        + dist
                        + " distribution with force_sigma specified is "
                        + str(min_failures)
                        + "."
                    )
                )
            elif dist == "Everything":
                raise ValueError(
                    "The minimum number of distinct failures required to fit everything is "
                    + str(min_failures)
                    + "."
                )
            else:
                raise ValueError(
                    str(
                        "The minimum number of distinct failures required for a "
                        + dist
                        + " distribution is "
                        + str(min_failures)
                        + "."
                    )
                )

        # error checking for CI_type
        if CI_type is not None:
            if CI_type in ["t", "time", "T", "TIME"]:
                CI_type = "time"
            elif CI_type in ["r", "R", "rel", "REL", "reliability", "RELIABILITY"]:
                CI_type = "reliability"
            else:
                raise ValueError('CI_type must be "time" or "reliability"')

        # return everything
        self.failures = failures
        self.right_censored = right_censored
        self.CI = CI
        self.method = method
        self.optimizer = optimizer
        self.quantiles = quantiles
        self.force_beta = force_beta
        self.force_sigma = force_sigma
        self.CI_type = CI_type


def anderson_darling(fitted_cdf, empirical_cdf):
    """
    Calculates the Anderson-Darling goodness of fit statistic.
    These formulas are based on the method used in MINITAB which gives an
    adjusted form of the original AD statistic described on Wikipedia.

    Parameters
    ----------
    fitted_cdf : list, array
        The fitted CDF values at the data points
    empirical_cdf  : list, array
        The empirical (rank adjustment) CDF values at the data points

    Returns
    -------
    AD : float
        The anderson darling (adjusted) test statistic.
    """
    if type(fitted_cdf) != np.ndarray:
        fitted_cdf = [fitted_cdf]  # required when there is only 1 failure
    Z = np.sort(np.asarray(fitted_cdf))
    Zi = np.hstack([Z, 1 - 1e-12])
    Zi_1 = (np.hstack([0, Zi]))[0:-1]  # Z_i-1
    FnZi = np.sort(np.asarray(empirical_cdf))
    FnZi_1 = np.hstack([0, FnZi])  # Fn(Z_i-1)
    lnZi = np.log(Zi)
    lnZi_1 = np.hstack([0, lnZi])[0:-1]

    A = -Zi - np.log(1 - Zi) + Zi_1 + np.log(1 - Zi_1)
    B = 2 * np.log(1 - Zi) * FnZi_1 - 2 * np.log(1 - Zi_1) * FnZi_1
    C = (
        lnZi * FnZi_1**2
        - np.log(1 - Zi) * FnZi_1**2
        - lnZi_1 * FnZi_1**2
        + np.log(1 - Zi_1) * FnZi_1**2
    )
    n = len(fitted_cdf)
    AD = n * ((A + B + C).sum())
    return AD


def colorprint(
    string,
    text_color=None,
    background_color=None,
    bold=False,
    underline=False,
    italic=False,
):
    """
    Provides easy access to color printing in the console.

    This function is used to print warnings in red text, but it can also do a
    lot more.

    Parameters
    ----------
    string
    text_color : str, None, optional
        Must be either grey, red, green, yellow, blue, pink, or turquoise. Use
        None to leave the color as white. Default is None.
    background_color : str, None, optional
        Must be either grey, red, green, yellow, blue, pink, or turquoise. Use
        None to leave the color as the transparent. Default is None.
    bold : bool, optional
        Default is False.
    underline : bool, optional
        Default is False.
    italic : bool, optional
        Default is False.

    Returns
    -------
    None
        The output is printed to the console.

    Notes
    -----
    Some flexibility in color names is allowed. eg. red and r will both give red.

    As there is only one string argument, if you have multiple strings to print,
    you must first combine them using str(string_1,string_2,...).
    """
    text_colors = {
        "grey": "\033[90m",
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "pink": "\033[95m",
        "turquoise": "\033[96m",
        None: "\033[39m",
    }

    background_colors = {
        "grey": "\033[100m",
        "red": "\033[101m",
        "green": "\033[102m",
        "yellow": "\033[103m",
        "blue": "\033[104m",
        "pink": "\033[105m",
        "turquoise": "\033[106m",
        None: "\033[49m",
    }

    if bold is True:
        BOLD = "\033[1m"
    else:
        BOLD = "\033[21m"

    if underline is True:
        UNDERLINE = "\033[4m"
    else:
        UNDERLINE = "\033[24m"

    if italic is True:
        ITALIC = "\033[3m"
    else:
        ITALIC = "\033[23m"

    if type(text_color) not in [str, np.str_, type(None)]:
        raise ValueError("text_color must be a string")
    elif text_color is None:
        pass
    elif text_color.upper() in ["GREY", "GRAY", "GR"]:
        text_color = "grey"
    elif text_color.upper() in ["RED", "R"]:
        text_color = "red"
    elif text_color.upper() in ["GREEN", "G"]:
        text_color = "green"
    elif text_color.upper() in ["YELLOW", "Y"]:
        text_color = "yellow"
    elif text_color.upper() in ["BLUE", "B", "DARKBLUE", "DARK BLUE"]:
        text_color = "blue"
    elif text_color.upper() in ["PINK", "P", "PURPLE"]:
        text_color = "pink"
    elif text_color.upper() in [
        "TURQUOISE",
        "TURQ",
        "T",
        "CYAN",
        "C",
        "LIGHTBLUE",
        "LIGHT BLUE",
        "LB",
    ]:
        text_color = "turquoise"
    else:
        raise ValueError(
            "Unknown text_color. Options are grey, red, green, yellow, blue, pink, turquoise."
        )

    if type(background_color) not in [str, np.str_, type(None)]:
        raise ValueError("background_color must be a string")
    if background_color is None:
        pass
    elif background_color.upper() in ["GREY", "GRAY", "GR"]:
        background_color = "grey"
    elif background_color.upper() in ["RED", "R"]:
        background_color = "red"
    elif background_color.upper() in ["GREEN", "G"]:
        background_color = "green"
    elif background_color.upper() in ["YELLOW", "Y"]:
        background_color = "yellow"
    elif background_color.upper() in ["BLUE", "B", "DARKBLUE", "DARK BLUE"]:
        background_color = "blue"
    elif background_color.upper() in ["PINK", "P", "PURPLE"]:
        background_color = "pink"
    elif background_color.upper() in [
        "TURQUOISE",
        "TURQ",
        "T",
        "CYAN",
        "C",
        "LIGHTBLUE",
        "LIGHT BLUE",
        "LB",
    ]:
        background_color = "turquoise"
    else:
        raise ValueError(
            "Unknown text_color. Options are grey, red, green, yellow, blue, pink, turquoise."
        )

    print(
        BOLD
        + ITALIC
        + UNDERLINE
        + background_colors[background_color]
        + text_colors[text_color]
        + string
        + "\033[0m"
    )


def clean_CI_arrays(xlower, xupper, ylower, yupper, plot_type="CDF", x=None, q=None):
    """
    This function cleans the CI arrays of nans and numbers <= 0 and also removes
    numbers >= 1 if plot_type is CDF or SF.

    Parameters
    ----------
    xlower : list, array
        The lower x array for the confidence interval
    xupper : list, array
        The upper x array for the confidence interval
    ylower : list, array
        The lower y array for the confidence interval
    yupper : list, array
        The upper y array for the confidence interval
    plot_type : str, optional
        Must be "CDF", "SF", "CHF". Default is "CDF"
    x : array, optional
        The x array for CI extraction
    q : array, optional
        The q array for CI extraction

    Returns
    -------
    xlower : array
        The "cleaned" lower x array for the confidence interval
    xupper : array
        The "cleaned" upper x array for the confidence interval
    ylower : array
        The "cleaned" lower y array for the confidence interval
    ylower : array
        The "cleaned" upper y array for the confidence interval

    Notes
    -----
    The returned arrays will all be the same length

    The cleaning is done by deleting values. If the cleaned arrays are < 2 items
    in length then an error will be triggered.
    """
    # format the input as arrays
    xlower = np.asarray(xlower)
    xupper = np.asarray(xupper)
    ylower = np.asarray(ylower)
    yupper = np.asarray(yupper)

    # create empty arrays to fill with cleaned values
    xlower_out = np.array([])
    xupper_out = np.array([])
    ylower_out = np.array([])
    yupper_out = np.array([])

    xlower_out2 = np.array([])
    xupper_out2 = np.array([])
    ylower_out2 = np.array([])
    yupper_out2 = np.array([])

    xlower_out3 = np.array([])
    xupper_out3 = np.array([])
    ylower_out3 = np.array([])
    yupper_out3 = np.array([])

    # remove nans in all arrays
    for i in np.arange(len(xlower)):
        if (
            np.isfinite(xlower[i])
            and np.isfinite(xupper[i])
            and np.isfinite(ylower[i])
            and np.isfinite(yupper[i])
        ):
            xlower_out = np.append(xlower_out, xlower[i])
            xupper_out = np.append(xupper_out, xupper[i])
            ylower_out = np.append(ylower_out, ylower[i])
            yupper_out = np.append(yupper_out, yupper[i])

    # remove values >= 1 for CDF and SF
    if plot_type.upper() in ["CDF", "SF"]:
        for i in np.arange(len(xlower_out)):
            if ylower_out[i] < 1 and yupper_out[i] < 1:
                xlower_out2 = np.append(xlower_out2, xlower_out[i])
                xupper_out2 = np.append(xupper_out2, xupper_out[i])
                ylower_out2 = np.append(ylower_out2, ylower_out[i])
                yupper_out2 = np.append(yupper_out2, yupper_out[i])
    else:  # do nothing
        xlower_out2 = xlower_out
        xupper_out2 = xupper_out
        ylower_out2 = ylower_out
        yupper_out2 = yupper_out

    # remove values <=0 for all cases
    tol = 1e-50  # tolerance for equivalent to zero. Accounts for precision error
    for i in np.arange(len(xlower_out2)):
        if ylower_out2[i] > tol and yupper_out2[i] > tol:
            xlower_out3 = np.append(xlower_out3, xlower_out2[i])
            xupper_out3 = np.append(xupper_out3, xupper_out2[i])
            ylower_out3 = np.append(ylower_out3, ylower_out2[i])
            yupper_out3 = np.append(yupper_out3, yupper_out2[i])

    # checks whether CI_x or CI_y was specified and resulted in values being deleted due to being illegal values. Raises a more detailed error for the user.
    if len(xlower_out3) != len(xlower) and x is not None:
        raise ValueError(
            "The confidence intervals for CI_x cannot be returned because they are NaN. This may occur when the SF=0. Try specifying CI_x values closer to the mean of the distribution."
        )
    if len(ylower_out3) != len(ylower) and q is not None:
        raise ValueError(
            "The confidence intervals for CI_y cannot be returned because they are NaN. This may occur when the CI_y is near 0 or 1. Try specifying CI_y values closer to 0.5."
        )

    # final error check for lengths matching and there still being at least 2 elements remaining
    if (
        len(xlower_out3) != len(xupper_out3)
        or len(xlower_out3) != len(yupper_out3)
        or len(xlower_out3) != len(ylower_out3)
        or len(xlower_out3) < 1
    ):
        colorprint(
            "ERROR in clean_CI_arrays: Confidence intervals could not be plotted due to the presence of too many NaNs in the arrays.",
            text_color="red",
        )

    return xlower_out3, xupper_out3, ylower_out3, yupper_out3


def no_reverse(x, CI_type, plot_type):
    """
    This is used to convert an array that decreases and then increases into an
    array that decreases then is constant at its minimum.

    The always decreasing rule will apply unless CI_type = 'time' and
    plot_type = 'CHF'

    This function is used to provide a correction to the confidence intervals
    which mathematically are correct but practically should never decrease.

    Parameters
    ----------
    x : array, list
        The array or list to which the no_reverse correction is applied
    CI_type : str
        Must be either 'time' or 'reliability'
    plot_type : str
        Must be either 'CDF', 'SF', or 'CHF'

    Returns
    -------
    x : array
        A corrected form of the input x that obeys the always decreasing rule
        (or the always increasing rule in the case of CI_type = 'time' and
        plot_type = 'CHF').
    """
    if type(x) not in [np.ndarray, list]:
        raise ValueError("x must be a list or array")
    if len(x) < 2:
        raise ValueError("x must be a list or array with length greater than 1")
    if CI_type == "time" and plot_type == "CHF":
        decreasing = False
    else:
        decreasing = True

    x = np.copy(np.asarray(x))
    if all(np.isfinite(x)):
        # it will not work if there are any nans
        if decreasing is True:
            idxmin = np.where(x == min(x))[0][0]
            if idxmin < len(x) - 1:
                x[idxmin::] = min(x)
        elif decreasing is False:
            idxmax = np.where(x == max(x))[0][0]
            if idxmax < len(x) - 1:
                x[idxmax::] = max(x)
        else:
            return ValueError("The parameter 'decreasing' must be True or False")
    return x


def validate_CI_params(*args):
    """
    Returns False if any of the args is None or Nan, else returns True.
    This function is different to using all() because it performs the checks
    using np.isfinite(arg).

    Parameters
    ----------
    *args : bool
        Any number of boolean arguments

    Returns
    -------
    is_valid : bool
        False if any of the args is None or Nan else returns True.
    """
    is_valid = True
    for arg in args:
        if arg is None or np.isfinite(arg) is np.False_:
            is_valid = False
    return is_valid


def transform_spaced(
    transform,
    y_lower=1e-8,
    y_upper=1 - 1e-8,
    num=1000,
    alpha=None,
    beta=None,
):
    """
    Creates linearly spaced array based on a specified transform.

    This is similar to np.linspace or np.logspace but is designed for weibull
    space, exponential space, normal space, gamma space, loglogistic space,
    gumbel space and beta space.

    It is useful if the points generated are going to be plotted on axes that
    are scaled using the same transform and need to look equally spaced in the
    transform space.

    Parameters
    ----------
    transform : str
        The transform name. Must be either weibull, exponential, normal, gamma,
        gumbel, loglogistic, or beta.
    y_upper : float, optional
        The lower bound (must be within the bounds 0 to 1). Default is 1e-8
    y_lower : float, optional
        The upper bound (must be within the bounds 0 to 1). Default is 1-1e-8
    num : int, optional
        The number of values in the array. Default is 1000.
    alpha : int, float, optional
        The alpha value of the beta distribution. Only used if the transform is
        beta
    beta : int, float, optional
        The beta value of the beta or gamma distribution. Only used if the
        transform is beta or gamma

    Returns
    -------
    transformed_array : array
        transform spaced array. This appears linearly spaced when plotted in
        transform space.

    Notes
    -----
    Note that lognormal is the same as normal, since the x-axis is what is
    transformed in lognormal, not the y-axis.
    """
    np.seterr("ignore")  # this is required due to an error in scipy.stats
    if y_lower > y_upper:
        y_lower, y_upper = y_upper, y_lower
    if y_lower <= 0 or y_upper >= 1:
        raise ValueError("y_lower and y_upper must be within the range 0 to 1")
    if num <= 2:
        raise ValueError("num must be greater than 2")
    if transform in ["normal", "Normal", "norm", "Norm"]:
        fwd = lambda x: ss.norm.ppf(x)
        inv = lambda x: ss.norm.cdf(x)
    elif transform in ["gumbel", "Gumbel", "gbl", "gum", "Gum", "Gbl"]:
        fwd = lambda x: ss.gumbel_l.ppf(x)
        inv = lambda x: ss.gumbel_l.cdf(x)
    elif transform in ["weibull", "Weibull", "weib", "Weib", "wbl"]:
        fwd = lambda x: np.log(-np.log(1 - x))
        inv = lambda x: 1 - np.exp(-np.exp(x))
    elif transform in ["loglogistic", "Loglogistic", "LL", "ll", "loglog"]:
        fwd = lambda x: np.log(1 / x - 1)
        inv = lambda x: 1 / (np.exp(x) + 1)
    elif transform in ["exponential", "Exponential", "expon", "Expon", "exp", "Exp"]:
        fwd = lambda x: ss.expon.ppf(x)
        inv = lambda x: ss.expon.cdf(x)
    elif transform in ["gamma", "Gamma", "gam", "Gam"]:
        if beta is None:
            raise ValueError("beta must be specified to use the gamma transform")
        else:
            fwd = lambda x: ss.gamma.ppf(x, a=beta)
            inv = lambda x: ss.gamma.cdf(x, a=beta)
    elif transform in ["beta", "Beta"]:
        if alpha is None or beta is None:
            raise ValueError(
                "alpha and beta must be specified to use the beta transform"
            )
        else:
            fwd = lambda x: ss.beta.ppf(x, a=beta, b=alpha)
            inv = lambda x: ss.beta.cdf(x, a=beta, b=alpha)
    elif transform in [
        "lognormal",
        "Lognormal",
        "LN",
        "ln",
        "lognorm",
        "Lognorm",
    ]:  # the transform is the same, it's just the xscale that is ln for lognormal
        raise ValueError(
            "the Lognormal transform is the same as the normal transform. Specify normal and try again"
        )
    else:
        raise ValueError(
            "transform must be either exponential, normal, weibull, loglogistic, gamma, or beta"
        )

    # find the value of the bounds in tranform space
    upper = fwd(y_upper)
    lower = fwd(y_lower)
    # generate the array in transform space
    arr = np.linspace(lower, upper, num)
    # convert the array back from transform space
    transform_array = inv(arr)
    return transform_array


class distribution_confidence_intervals:
    """
    This class contains several subfunctions that provide all the confidence
    intervals for CDF, SF, CHF for each distribution for which it is
    implemented.

    The class has no parameters or returns as it is used primarily to create the
    confidence interval object which is used by the subfunctions.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """

    @staticmethod
    def exponential_CI(
        self,
        func="CDF",
        plot_CI=None,
        CI=None,
        text_title="",
        color=None,
        q=None,
        x=None,
    ):
        """
        Generates the confidence intervals for CDF, SF, and CHF of the
        Exponential distribution.

        Parameters
        ----------
        self : object
            The distribution object
        func : str
            Must be either "CDF", "SF" or "CHF". Default is "CDF"
        plot_CI : bool, None
            The confidence intervals will only be plotted if plot_CI is True.
        CI : float
            The confidence interval. Must be between 0 and 1
        text_title : str
            The existing CDF/SF/CHF text title to which the confidence interval
            string will be added.
        color : str
            The color to be used to fill the confidence intervals.
        q : array, list, optional
            The quantiles to be calculated. Default is None.
        x : array, list, optional
            The x-values to be calculated. Default is None.

        Returns
        -------
        t_lower : array
            The lower bounds on time. Only returned if q is not None.
        t_upper :array
            The upper bounds on time. Only returned if q is not None.
        R_lower : array
            The lower bounds on reliability. Only returned if x is not None.
        R_upper :array
            The upper bounds on reliability. Only returned if x is not None.

        Notes
        -----
        self must contain particular values for this function to work. These
        include self.Lambda_SE and self.Z.

        As a Utils function, there is very limited error checking done, as this
        function is not intended for users to access directly.

        For the Exponential distribution, the bounds on time and reliability are
        the same.

        For an explaination of how the confidence inervals are calculated,
        please see the `documentation <https://reliability.readthedocs.io/en/latest/How%20are%20the%20confidence%20intervals%20calculated.html>`_.

        """
        points = 200

        # this section plots the confidence interval
        if (
            self.Lambda_SE is not None
            and self.Z is not None
            and (plot_CI is True or q is not None or x is not None)
        ):

            if func not in ["CDF", "SF", "CHF"]:
                raise ValueError("func must be either CDF, SF, or CHF")
            if type(q) not in [list, np.ndarray, type(None)]:
                raise ValueError(
                    "q must be a list or array of quantiles. Default is None"
                )
            if type(x) not in [list, np.ndarray, type(None)]:
                raise ValueError(
                    "x must be a list or array of x-values. Default is None"
                )
            if q is not None:
                q = np.asarray(q)
            if x is not None:
                x = np.asarray(x)

            Z = -ss.norm.ppf((1 - CI) / 2)  # converts CI to Z

            Lambda_upper = self.Lambda * (np.exp(Z * (self.Lambda_SE / self.Lambda)))
            Lambda_lower = self.Lambda * (np.exp(-Z * (self.Lambda_SE / self.Lambda)))

            if x is not None:
                t = x - self.gamma
            else:
                t0 = self.quantile(0.00001) - self.gamma
                if t0 <= 0:
                    t0 = 0.0001
                t = np.geomspace(
                    t0,
                    self.quantile(0.99999) - self.gamma,
                    points,
                )

            # calculate the CIs using the formula for SF
            Y_lower = np.exp(-Lambda_lower * t)
            Y_upper = np.exp(-Lambda_upper * t)

            # clean the arrays of illegal values (<=0, nans, >=1 (if CDF or SF))
            t, t, Y_lower, Y_upper = clean_CI_arrays(
                xlower=t,
                xupper=t,
                ylower=Y_lower,
                yupper=Y_upper,
                plot_type=func,
                q=q,
                x=x,
            )
            # artificially correct for any reversals
            if (x is None or q is None) and len(Y_lower) > 2 and len(Y_upper) > 2:
                Y_lower = no_reverse(Y_lower, CI_type=None, plot_type=func)
                Y_upper = no_reverse(Y_upper, CI_type=None, plot_type=func)

            if func == "CDF":
                yy_upper = 1 - Y_upper
                yy_lower = 1 - Y_lower
            elif func == "SF":
                yy_upper = Y_upper
                yy_lower = Y_lower
            elif func == "CHF":
                yy_upper = -np.log(Y_upper)  # same as -np.log(SF)
                yy_lower = -np.log(Y_lower)

            if q is not None:
                t_lower = -np.log(q) / Lambda_upper + self.gamma
                t_upper = -np.log(q) / Lambda_lower + self.gamma
                return t_lower, t_upper
            elif x is not None:
                return Y_lower, Y_upper

    @staticmethod
    def weibull_CI(
        self,
        func="CDF",
        plot_CI=None,
        CI_type=None,
        CI=None,
        text_title="",
        color=None,
        q=None,
        x=None,
    ):
        """
        Generates the confidence intervals for CDF, SF, and CHF of the
        Weibull distribution.

        Parameters
        ----------
        self : object
            The distribution object
        func : str
            Must be either "CDF", "SF" or "CHF". Default is "CDF"
        plot_CI : bool, None
            The confidence intervals will only be plotted if plot_CI is True.
        CI_type : str
            Must be either "time" or "reliability"
        CI : float
            The confidence interval. Must be between 0 and 1
        text_title : str
            The existing CDF/SF/CHF text title to which the confidence interval
            string will be added.
        color : str
            The color to be used to fill the confidence intervals.
        q : array, list, optional
            The quantiles to be calculated. Default is None. Only used if
            CI_type='time'.
        x : array, list, optional
            The x-values to be calculated. Default is None. Only used if
            CI_type='reliability'.

        Returns
        -------
        t_lower : array
            The lower bounds on time. Only returned if CI_type is "time" and q
            is not None.
        t_upper :array
            The upper bounds on time. Only returned if CI_type is "time" and q
            is not None.
        R_lower : array
            The lower bounds on reliability. Only returned if CI_type is
            "reliability" and x is not None.
        R_upper :array
            The upper bounds on reliability. Only returned if CI_type is
            "reliability" and x is not None.

        Notes
        -----
        self must contain particular values for this function to work. These
        include self.alpha_SE, self.beta_SE, self.Cov_alpha_beta, self.Z.

        As a Utils function, there is very limited error checking done, as this
        function is not intended for users to access directly.

        For an explaination of how the confidence inervals are calculated,
        please see the `documentation <https://reliability.readthedocs.io/en/latest/How%20are%20the%20confidence%20intervals%20calculated.html>`_.
        """
        points = 200  # the number of data points in each confidence interval (upper and lower) line

        # this determines if the user has specified for the CI bounds to be shown or hidden.
        if (
            validate_CI_params(self.alpha_SE, self.beta_SE, self.Cov_alpha_beta, self.Z)
            is True
            and (plot_CI is True or q is not None or x is not None)
            and CI_type is not None
        ):
            if CI_type in ["time", "t", "T", "TIME", "Time"]:
                CI_type = "time"
            elif CI_type in [
                "reliability",
                "r",
                "R",
                "RELIABILITY",
                "rel",
                "REL",
                "Reliability",
            ]:
                CI_type = "reliability"
            if func not in ["CDF", "SF", "CHF"]:
                raise ValueError("func must be either CDF, SF, or CHF")
            if type(q) not in [list, np.ndarray, type(None)]:
                raise ValueError(
                    "q must be a list or array of quantiles. Default is None"
                )
            if type(x) not in [list, np.ndarray, type(None)]:
                raise ValueError(
                    "x must be a list or array of x-values. Default is None"
                )
            if q is not None:
                q = np.asarray(q)
            if x is not None:
                x = np.asarray(x)

            Z = -ss.norm.ppf((1 - CI) / 2)  # converts CI to Z

            def u(t, alpha, beta):  # u = ln(-ln(R))
                return beta * (anp.log(t) - anp.log(alpha))  # weibull SF linearized

            def v(R, alpha, beta):  # v = ln(t)
                return (1 / beta) * anp.log(-anp.log(R)) + anp.log(
                    alpha
                )  # weibull SF rearranged for t

            du_da = jac(u, 1)  # derivative wrt alpha (bounds on reliability)
            du_db = jac(u, 2)  # derivative wrt beta (bounds on reliability)
            dv_da = jac(v, 1)  # derivative wrt alpha (bounds on time)
            dv_db = jac(v, 2)  # derivative wrt beta (bounds on time)

            def var_u(self, v):  # v is time
                return (
                    du_da(v, self.alpha, self.beta) ** 2 * self.alpha_SE**2
                    + du_db(v, self.alpha, self.beta) ** 2 * self.beta_SE**2
                    + 2
                    * du_da(v, self.alpha, self.beta)
                    * du_db(v, self.alpha, self.beta)
                    * self.Cov_alpha_beta
                )

            def var_v(self, u):  # u is reliability
                return (
                    dv_da(u, self.alpha, self.beta) ** 2 * self.alpha_SE**2
                    + dv_db(u, self.alpha, self.beta) ** 2 * self.beta_SE**2
                    + 2
                    * dv_da(u, self.alpha, self.beta)
                    * dv_db(u, self.alpha, self.beta)
                    * self.Cov_alpha_beta
                )

            # Confidence bounds on time (in terms of reliability)
            if CI_type == "time":
                # Y is reliability (R)
                if func == "CHF":
                    chf_array = np.geomspace(1e-8, self._chf[-1] * 1.5, points)
                    Y = np.exp(-chf_array)
                else:  # CDF and SF
                    if q is not None:
                        Y = q
                    else:
                        Y = transform_spaced(
                            "weibull", y_lower=1e-8, y_upper=1 - 1e-8, num=points
                        )

                # v is ln(t)
                v_lower = v(Y, self.alpha, self.beta) - Z * (var_v(self, Y) ** 0.5)
                v_upper = v(Y, self.alpha, self.beta) + Z * (var_v(self, Y) ** 0.5)

                t_lower = np.exp(v_lower) + self.gamma  # transform back from ln(t)
                t_upper = np.exp(v_upper) + self.gamma

                # clean the arrays of illegal values (<=0, nans, >=1 (if CDF or SF))
                t_lower, t_upper, Y, Y = clean_CI_arrays(
                    xlower=t_lower,
                    xupper=t_upper,
                    ylower=Y,
                    yupper=Y,
                    plot_type=func,
                    q=q,
                )
                # artificially correct for any reversals
                if q is None and len(t_lower) > 2 and len(t_upper) > 2:
                    t_lower = no_reverse(t_lower, CI_type=CI_type, plot_type=func)
                    t_upper = no_reverse(t_upper, CI_type=CI_type, plot_type=func)

                if func == "CDF":
                    yy = 1 - Y
                elif func == "SF":
                    yy = Y
                elif func == "CHF":
                    yy = -np.log(Y)

                if q is not None:
                    return t_lower, t_upper

            # Confidence bounds on Reliability (in terms of time)
            elif CI_type == "reliability":
                if x is not None:
                    t = x - self.gamma
                else:
                    t0 = self.quantile(0.00001) - self.gamma
                    if t0 <= 0:
                        t0 = 0.0001
                    t = np.geomspace(
                        t0,
                        self.quantile(0.99999) - self.gamma,
                        points,
                    )

                # u is reliability ln(-ln(R))
                u_lower = (
                    u(t, self.alpha, self.beta) + Z * var_u(self, t) ** 0.5
                )  # note that gamma is incorporated into u but not in var_u. This is the same as just shifting a Weibull_2P across
                u_upper = u(t, self.alpha, self.beta) - Z * var_u(self, t) ** 0.5

                Y_lower = np.exp(-np.exp(u_lower))  # transform back from ln(-ln(R))
                Y_upper = np.exp(-np.exp(u_upper))

                # clean the arrays of illegal values (<=0, nans, >=1 (if CDF or SF))
                t, t, Y_lower, Y_upper = clean_CI_arrays(
                    xlower=t,
                    xupper=t,
                    ylower=Y_lower,
                    yupper=Y_upper,
                    plot_type=func,
                    x=x,
                )
                # artificially correct for any reversals
                if x is None and len(Y_lower) > 2 and len(Y_upper) > 2:
                    Y_lower = no_reverse(Y_lower, CI_type=CI_type, plot_type=func)
                    Y_upper = no_reverse(Y_upper, CI_type=CI_type, plot_type=func)

                if func == "CDF":
                    yy_lower = 1 - Y_lower
                    yy_upper = 1 - Y_upper
                elif func == "SF":
                    yy_lower = Y_lower
                    yy_upper = Y_upper
                elif func == "CHF":
                    yy_lower = -np.log(Y_lower)
                    yy_upper = -np.log(Y_upper)

                if x is not None:
                    return Y_lower, Y_upper

    @staticmethod
    def gamma_CI(
        self,
        func="CDF",
        plot_CI=None,
        CI_type=None,
        CI=None,
        text_title="",
        color=None,
        q=None,
        x=None,
    ):
        """
        Generates the confidence intervals for CDF, SF, and CHF of the
        Gamma distribution.

        Parameters
        ----------
        self : object
            The distribution object
        func : str
            Must be either "CDF", "SF" or "CHF". Default is "CDF".
        plot_CI : bool, None
            The confidence intervals will only be plotted if plot_CI is True.
        CI_type : str
            Must be either "time" or "reliability"
        CI : float
            The confidence interval. Must be between 0 and 1
        text_title : str
            The existing CDF/SF/CHF text title to which the confidence interval
            string will be added.
        color : str
            The color to be used to fill the confidence intervals.
        q : array, list, optional
            The quantiles to be calculated. Default is None. Only used if CI_type='time'.
        x : array, list, optional
            The x-values to be calculated. Default is None. Only used if CI_type='reliability'.

        Returns
        -------
        t_lower : array
            The lower bounds on time. Only returned if CI_type is "time" and q
            is not None.
        t_upper :array
            The upper bounds on time. Only returned if CI_type is "time" and q
            is not None.
        R_lower : array
            The lower bounds on reliability. Only returned if CI_type is
            "reliability" and x is not None.
        R_upper :array
            The upper bounds on reliability. Only returned if CI_type is
            "reliability" and x is not None.

        Notes
        -----
        self must contain particular values for this function to work. These
        include self.mu_SE, self.beta_SE, self.Cov_mu_beta, self.Z.

        As a Utils function, there is very limited error checking done, as this
        function is not intended for users to access directly.

        For an explaination of how the confidence inervals are calculated,
        please see the `documentation <https://reliability.readthedocs.io/en/latest/How%20are%20the%20confidence%20intervals%20calculated.html>`_.
        """
        points = 200  # the number of data points in each confidence interval (upper and lower) line

        # this determines if the user has specified for the CI bounds to be shown or hidden.

        if (
            validate_CI_params(self.mu_SE, self.beta_SE, self.Cov_mu_beta, self.Z)
            is True
            and (plot_CI is True or q is not None or x is not None)
            and CI_type is not None
        ):
            if CI_type in ["time", "t", "T", "TIME", "Time"]:
                CI_type = "time"
            elif CI_type in [
                "reliability",
                "r",
                "R",
                "RELIABILITY",
                "rel",
                "REL",
                "Reliability",
            ]:
                CI_type = "reliability"
            if func not in ["CDF", "SF", "CHF"]:
                raise ValueError("func must be either CDF, SF, or CHF")
            if type(q) not in [list, np.ndarray, type(None)]:
                raise ValueError(
                    "q must be a list or array of quantiles. Default is None"
                )
            if type(x) not in [list, np.ndarray, type(None)]:
                raise ValueError(
                    "x must be a list or array of x-values. Default is None"
                )
            if q is not None:
                q = np.asarray(q)
            if x is not None:
                x = np.asarray(x)

            Z = -ss.norm.ppf((1 - CI) / 2)  # converts CI to Z

            def u(t, mu, beta):  # u = R
                return agammaincc(beta, t / anp.exp(mu))

            def v(R, mu, beta):  # v = ln(t)
                return anp.log(agammainccinv(beta, R)) + mu

            du_dm = jac(u, 1)  # derivative wrt mu (bounds on reliability)
            du_db = jac(u, 2)  # derivative wrt beta (bounds on reliability)
            dv_dm = jac(v, 1)  # derivative wrt mu (bounds on time)
            dv_db = jac(v, 2)  # derivative wrt beta (bounds on time)

            def var_u(self, v):  # v is time
                return (
                    du_dm(v, self.mu, self.beta) ** 2 * self.mu_SE**2
                    + du_db(v, self.mu, self.beta) ** 2 * self.beta_SE**2
                    + 2
                    * du_dm(v, self.mu, self.beta)
                    * du_db(v, self.mu, self.beta)
                    * self.Cov_mu_beta
                )

            def var_v(self, u):  # u is reliability
                return (
                    dv_dm(u, self.mu, self.beta) ** 2 * self.mu_SE**2
                    + dv_db(u, self.mu, self.beta) ** 2 * self.beta_SE**2
                    + 2
                    * dv_dm(u, self.mu, self.beta)
                    * dv_db(u, self.mu, self.beta)
                    * self.Cov_mu_beta
                )

            # Confidence bounds on time (in terms of reliability)
            if CI_type == "time":
                # Y is reliability (R)
                if func == "CHF":
                    chf_array = np.geomspace(1e-8, self._chf[-1] * 1.5, points)
                    Y = np.exp(-chf_array)
                else:  # CDF and SF
                    if q is not None:
                        Y = q
                    else:
                        if self.beta > 3:
                            Y = transform_spaced(
                                "gamma",
                                y_lower=1e-8,
                                y_upper=1 - 1e-8,
                                beta=self.beta,
                                num=points,
                            )
                        else:
                            Y = np.linspace(1e-8, 1 - 1e-8, points)

                # v is ln(t)
                v_lower = v(Y, self.mu, self.beta) - Z * (var_v(self, Y) ** 0.5)
                v_upper = v(Y, self.mu, self.beta) + Z * (var_v(self, Y) ** 0.5)

                t_lower = np.exp(v_lower) + self.gamma
                t_upper = np.exp(v_upper) + self.gamma

                # clean the arrays of illegal values (<=0, nans, >=1 (if CDF or SF))
                t_lower, t_upper, Y, Y = clean_CI_arrays(
                    xlower=t_lower,
                    xupper=t_upper,
                    ylower=Y,
                    yupper=Y,
                    plot_type=func,
                    q=q,
                )
                # artificially correct for any reversals
                if q is None and len(t_lower) > 2 and len(t_upper) > 2:
                    t_lower = no_reverse(t_lower, CI_type=CI_type, plot_type=func)
                    t_upper = no_reverse(t_upper, CI_type=CI_type, plot_type=func)

                if func == "CDF":
                    yy = 1 - Y
                elif func == "SF":
                    yy = Y
                elif func == "CHF":
                    yy = -np.log(Y)

                if q is not None:
                    return t_lower, t_upper

            # Confidence bounds on Reliability (in terms of time)
            elif CI_type == "reliability":
                if x is not None:
                    t = x - self.gamma
                else:
                    if self.gamma == 0:
                        t0 = 0.0001
                    else:
                        t0 = self.quantile(0.0000001)
                    t = np.linspace(
                        t0 - self.gamma,
                        self.quantile(0.99999) - self.gamma,
                        points,
                    )

                # u is reliability
                # note that gamma is incorporated into u but not in var_u. This is the same as just shifting a Gamma_2P across
                R = u(t, self.mu, self.beta)
                varR = var_u(self, t)
                R_lower = R / (R + (1 - R) * np.exp((Z * varR**0.5) / (R * (1 - R))))
                R_upper = R / (R + (1 - R) * np.exp((-Z * varR**0.5) / (R * (1 - R))))

                # transform back from u = R
                Y_lower = R_lower
                Y_upper = R_upper

                # clean the arrays of illegal values (<=0, nans, >=1 (if CDF or SF))
                t, t, Y_lower, Y_upper = clean_CI_arrays(
                    xlower=t,
                    xupper=t,
                    ylower=Y_lower,
                    yupper=Y_upper,
                    plot_type=func,
                    x=x,
                )
                # artificially correct for any reversals
                if x is None and len(Y_lower) > 2 and len(Y_upper) > 2:
                    Y_lower = no_reverse(Y_lower, CI_type=CI_type, plot_type=func)
                    Y_upper = no_reverse(Y_upper, CI_type=CI_type, plot_type=func)

                if func == "CDF":
                    yy_lower = 1 - Y_lower
                    yy_upper = 1 - Y_upper
                elif func == "SF":
                    yy_lower = Y_lower
                    yy_upper = Y_upper
                elif func == "CHF":
                    yy_lower = -np.log(Y_lower)
                    yy_upper = -np.log(Y_upper)

                if x is not None:
                    return Y_lower, Y_upper

    @staticmethod
    def normal_CI(
        self,
        func="CDF",
        plot_CI=None,
        CI_type=None,
        CI=None,
        text_title="",
        color=None,
        q=None,
        x=None,
    ):
        """
        Generates the confidence intervals for CDF, SF, and CHF of the
        Normal distribution.

        Parameters
        ----------
        self : object
            The distribution object
        func : str
            Must be either "CDF", "SF" or "CHF". Default is "CDF".
        plot_CI : bool, None
            The confidence intervals will only be plotted if plot_CI is True.
        CI_type : str
            Must be either "time" or "reliability"
        CI : float
            The confidence interval. Must be between 0 and 1
        text_title : str
            The existing CDF/SF/CHF text title to which the confidence interval
            string will be added.
        color : str
            The color to be used to fill the confidence intervals.
        q : array, list, optional
            The quantiles to be calculated. Default is None. Only used if CI_type='time'.
        x : array, list, optional
            The x-values to be calculated. Default is None. Only used if CI_type='reliability'.

        Returns
        -------
        t_lower : array
            The lower bounds on time. Only returned if CI_type is "time" and q
            is not None.
        t_upper :array
            The upper bounds on time. Only returned if CI_type is "time" and q
            is not None.
        R_lower : array
            The lower bounds on reliability. Only returned if CI_type is
            "reliability" and x is not None.
        R_upper :array
            The upper bounds on reliability. Only returned if CI_type is
            "reliability" and x is not None.

        Notes
        -----
        self must contain particular values for this function to work. These
        include self.mu_SE, self.sigma_SE, self.Cov_mu_sigma, self.Z.

        As a Utils function, there is very limited error checking done, as this
        function is not intended for users to access directly.

        For an explaination of how the confidence inervals are calculated,
        please see the `documentation <https://reliability.readthedocs.io/en/latest/How%20are%20the%20confidence%20intervals%20calculated.html>`_.
        """
        points = 200  # the number of data points in each confidence interval (upper and lower) line

        # this determines if the user has specified for the CI bounds to be shown or hidden.
        if (
            validate_CI_params(self.mu_SE, self.sigma_SE, self.Cov_mu_sigma, self.Z)
            is True
            and (plot_CI is True or q is not None or x is not None)
            and CI_type is not None
        ):
            if CI_type in ["time", "t", "T", "TIME", "Time"]:
                CI_type = "time"
            elif CI_type in [
                "reliability",
                "r",
                "R",
                "RELIABILITY",
                "rel",
                "REL",
                "Reliability",
            ]:
                CI_type = "reliability"
            if func not in ["CDF", "SF", "CHF"]:
                raise ValueError("func must be either CDF, SF, or CHF")
            if type(q) not in [list, np.ndarray, type(None)]:
                raise ValueError(
                    "q must be a list or array of quantiles. Default is None"
                )
            if type(x) not in [list, np.ndarray, type(None)]:
                raise ValueError(
                    "x must be a list or array of x-values. Default is None"
                )
            if q is not None:
                q = np.asarray(q)
            if x is not None:
                x = np.asarray(x)

            Z = -ss.norm.ppf((1 - CI) / 2)  # converts CI to Z

            def u(t, mu, sigma):  # u = phiinv(R)
                return (mu - t) / sigma  # normal SF linearlized

            def v(R, mu, sigma):  # v = t
                return mu - sigma * ss.norm.ppf(R)

            # for consistency with other distributions, the derivatives are da for d_sigma and db for d_mu. Just think of a is first parameter and b is second parameter.
            du_da = jac(u, 1)  # derivative wrt mu (bounds on reliability)
            du_db = jac(u, 2)  # derivative wrt sigma (bounds on reliability)
            dv_da = jac(v, 1)  # derivative wrt mu (bounds on time)
            dv_db = jac(v, 2)  # derivative wrt sigma (bounds on time)

            def var_u(self, v):  # v is time
                return (
                    du_da(v, self.mu, self.sigma) ** 2 * self.mu_SE**2
                    + du_db(v, self.mu, self.sigma) ** 2 * self.sigma_SE**2
                    + 2
                    * du_da(v, self.mu, self.sigma)
                    * du_db(v, self.mu, self.sigma)
                    * self.Cov_mu_sigma
                )

            def var_v(self, u):  # u is reliability
                return (
                    dv_da(u, self.mu, self.sigma) ** 2 * self.mu_SE**2
                    + dv_db(u, self.mu, self.sigma) ** 2 * self.sigma_SE**2
                    + 2
                    * dv_da(u, self.mu, self.sigma)
                    * dv_db(u, self.mu, self.sigma)
                    * self.Cov_mu_sigma
                )

            # Confidence bounds on time (in terms of reliability)
            if CI_type == "time":
                # Y is reliability (R)
                if func == "CHF":
                    chf_array = np.geomspace(1e-8, self._chf[-1] * 1.5, points)
                    Y = np.exp(-chf_array)
                else:  # CDF and SF
                    if q is not None:
                        Y = q
                    else:
                        Y = transform_spaced(
                            "normal", y_lower=1e-8, y_upper=1 - 1e-8, num=points
                        )

                # v is t
                t_lower = v(Y, self.mu, self.sigma) - Z * (var_v(self, Y) ** 0.5)
                t_upper = v(Y, self.mu, self.sigma) + Z * (var_v(self, Y) ** 0.5)

                # clean the arrays of illegal values (<=0, nans, >=1 (if CDF or SF))
                t_lower, t_upper, Y, Y = clean_CI_arrays(
                    xlower=t_lower,
                    xupper=t_upper,
                    ylower=Y,
                    yupper=Y,
                    plot_type=func,
                    q=q,
                )
                # artificially correct for any reversals
                if q is None and len(t_lower) > 2 and len(t_upper) > 2:
                    t_lower = no_reverse(t_lower, CI_type=CI_type, plot_type=func)
                    t_upper = no_reverse(t_upper, CI_type=CI_type, plot_type=func)

                if func == "CDF":
                    yy = 1 - Y
                elif func == "SF":
                    yy = Y
                elif func == "CHF":
                    yy = -np.log(Y)

                if q is not None:
                    return t_lower, t_upper

            # Confidence bounds on Reliability (in terms of time)
            elif CI_type == "reliability":
                if x is not None:
                    t = x
                else:
                    t = np.linspace(
                        self.quantile(0.00001), self.quantile(0.99999), points
                    )

                # u is reliability u = phiinv(R)
                u_lower = u(t, self.mu, self.sigma) + Z * var_u(self, t) ** 0.5
                u_upper = u(t, self.mu, self.sigma) - Z * var_u(self, t) ** 0.5

                Y_lower = ss.norm.cdf(u_lower)  # transform back from u = phiinv(R)
                Y_upper = ss.norm.cdf(u_upper)

                # clean the arrays of illegal values (<=0, nans, >=1 (if CDF or SF))
                t, t, Y_lower, Y_upper = clean_CI_arrays(
                    xlower=t,
                    xupper=t,
                    ylower=Y_lower,
                    yupper=Y_upper,
                    plot_type=func,
                    x=x,
                )
                # artificially correct for any reversals
                if x is None and len(Y_lower) > 2 and len(Y_upper) > 2:
                    Y_lower = no_reverse(Y_lower, CI_type=CI_type, plot_type=func)
                    Y_upper = no_reverse(Y_upper, CI_type=CI_type, plot_type=func)

                if func == "CDF":
                    yy_lower = 1 - Y_lower
                    yy_upper = 1 - Y_upper
                elif func == "SF":
                    yy_lower = Y_lower
                    yy_upper = Y_upper
                elif func == "CHF":
                    yy_lower = -np.log(Y_lower)
                    yy_upper = -np.log(Y_upper)

                if x is not None:
                    return Y_lower, Y_upper

    @staticmethod
    def lognormal_CI(
        self,
        func="CDF",
        plot_CI=None,
        CI_type=None,
        CI=None,
        text_title="",
        color=None,
        q=None,
        x=None,
    ):
        """
        Generates the confidence intervals for CDF, SF, and CHF of the
        Lognormal distribution.

        Parameters
        ----------
        self : object
            The distribution object
        func : str
            Must be either "CDF", "SF" or "CHF". Default is "CDF".
        plot_CI : bool, None
            The confidence intervals will only be plotted if plot_CI is True.
        CI_type : str
            Must be either "time" or "reliability"
        CI : float
            The confidence interval. Must be between 0 and 1
        text_title : str
            The existing CDF/SF/CHF text title to which the confidence interval
            string will be added.
        color : str
            The color to be used to fill the confidence intervals.
        q : array, list, optional
            The quantiles to be calculated. Default is None. Only used if CI_type='time'.
        x : array, list, optional
            The x-values to be calculated. Default is None. Only used if CI_type='reliability'.

        Returns
        -------
        t_lower : array
            The lower bounds on time. Only returned if CI_type is "time" and q
            is not None.
        t_upper :array
            The upper bounds on time. Only returned if CI_type is "time" and q
            is not None.
        R_lower : array
            The lower bounds on reliability. Only returned if CI_type is
            "reliability" and x is not None.
        R_upper :array
            The upper bounds on reliability. Only returned if CI_type is
            "reliability" and x is not None.

        Notes
        -----
        self must contain particular values for this function to work. These
        include self.mu_SE, self.sigma_SE, self.Cov_mu_sigma, self.Z.

        As a Utils function, there is very limited error checking done, as this
        function is not intended for users to access directly.

        For an explaination of how the confidence inervals are calculated,
        please see the `documentation <https://reliability.readthedocs.io/en/latest/How%20are%20the%20confidence%20intervals%20calculated.html>`_.
        """
        points = 200  # the number of data points in each confidence interval (upper and lower) line

        # this determines if the user has specified for the CI bounds to be shown or hidden.
        if (
            validate_CI_params(self.mu_SE, self.sigma_SE, self.Cov_mu_sigma, self.Z)
            is True
            and (plot_CI is True or q is not None or x is not None)
            and CI_type is not None
        ):
            if CI_type in ["time", "t", "T", "TIME", "Time"]:
                CI_type = "time"
            elif CI_type in [
                "reliability",
                "r",
                "R",
                "RELIABILITY",
                "rel",
                "REL",
                "Reliability",
            ]:
                CI_type = "reliability"
            if func not in ["CDF", "SF", "CHF"]:
                raise ValueError("func must be either CDF, SF, or CHF")
            if type(q) not in [list, np.ndarray, type(None)]:
                raise ValueError(
                    "q must be a list or array of quantiles. Default is None"
                )
            if type(x) not in [list, np.ndarray, type(None)]:
                raise ValueError(
                    "x must be a list or array of x-values. Default is None"
                )

            if q is not None:
                q = np.asarray(q)
            if x is not None:
                x = np.asarray(x)

            Z = -ss.norm.ppf((1 - CI) / 2)  # converts CI to Z

            def u(t, mu, sigma):  # u = phiinv(R)
                return (mu - np.log(t)) / sigma  # lognormal SF linearlized

            def v(R, mu, sigma):  # v = ln(t)
                return mu - sigma * ss.norm.ppf(R)

            # for consistency with other distributions, the derivatives are da for d_sigma and db for d_mu. Just think of a is first parameter and b is second parameter.
            du_da = jac(u, 1)  # derivative wrt mu (bounds on reliability)
            du_db = jac(u, 2)  # derivative wrt sigma (bounds on reliability)
            dv_da = jac(v, 1)  # derivative wrt mu (bounds on time)
            dv_db = jac(v, 2)  # derivative wrt sigma (bounds on time)

            def var_u(self, v):  # v is time
                return (
                    du_da(v, self.mu, self.sigma) ** 2 * self.mu_SE**2
                    + du_db(v, self.mu, self.sigma) ** 2 * self.sigma_SE**2
                    + 2
                    * du_da(v, self.mu, self.sigma)
                    * du_db(v, self.mu, self.sigma)
                    * self.Cov_mu_sigma
                )

            def var_v(self, u):  # u is reliability
                return (
                    dv_da(u, self.mu, self.sigma) ** 2 * self.mu_SE**2
                    + dv_db(u, self.mu, self.sigma) ** 2 * self.sigma_SE**2
                    + 2
                    * dv_da(u, self.mu, self.sigma)
                    * dv_db(u, self.mu, self.sigma)
                    * self.Cov_mu_sigma
                )

            if CI_type == "time":
                # Confidence bounds on time (in terms of reliability)
                # Y is reliability (R)
                if func == "CHF":
                    chf_array = np.geomspace(1e-8, self._chf[-1] * 1.5, points)
                    Y = np.exp(-chf_array)
                else:  # CDF and SF
                    if q is not None:
                        Y = q
                    else:
                        Y = transform_spaced(
                            "normal", y_lower=1e-8, y_upper=1 - 1e-8, num=points
                        )

                # v is ln(t)
                v_lower = v(Y, self.mu, self.sigma) - Z * (var_v(self, Y) ** 0.5)
                v_upper = v(Y, self.mu, self.sigma) + Z * (var_v(self, Y) ** 0.5)

                t_lower = np.exp(v_lower) + self.gamma
                t_upper = np.exp(v_upper) + self.gamma

                # clean the arrays of illegal values (<=0, nans, >=1 (if CDF or SF))
                t_lower, t_upper, Y, Y = clean_CI_arrays(
                    xlower=t_lower,
                    xupper=t_upper,
                    ylower=Y,
                    yupper=Y,
                    plot_type=func,
                    q=q,
                )
                # artificially correct for any reversals
                if q is None and len(t_lower) > 2 and len(t_upper) > 2:
                    t_lower = no_reverse(t_lower, CI_type=CI_type, plot_type=func)
                    t_upper = no_reverse(t_upper, CI_type=CI_type, plot_type=func)

                if func == "CDF":
                    yy = 1 - Y
                elif func == "SF":
                    yy = Y
                elif func == "CHF":
                    yy = -np.log(Y)

                if q is not None:
                    return t_lower, t_upper

            elif CI_type == "reliability":
                # Confidence bounds on Reliability (in terms of time)
                if x is not None:
                    t = x - self.gamma
                else:
                    t0 = self.quantile(0.00001) - self.gamma
                    if t0 <= 0:
                        t0 = 0.0001
                    t = np.geomspace(
                        t0,
                        self.quantile(0.99999) - self.gamma,
                        points,
                    )

                # u is reliability u = phiinv(R)
                u_lower = u(t, self.mu, self.sigma) + Z * var_u(self, t) ** 0.5
                u_upper = u(t, self.mu, self.sigma) - Z * var_u(self, t) ** 0.5

                Y_lower = ss.norm.cdf(u_lower)  # transform back from u = phiinv(R)
                Y_upper = ss.norm.cdf(u_upper)

                # clean the arrays of illegal values (<=0, nans, >=1 (if CDF or SF))
                t, t, Y_lower, Y_upper = clean_CI_arrays(
                    xlower=t,
                    xupper=t,
                    ylower=Y_lower,
                    yupper=Y_upper,
                    plot_type=func,
                    x=x,
                )
                # artificially correct for any reversals
                if x is None and len(Y_lower) > 2 and len(Y_upper) > 2:
                    Y_lower = no_reverse(Y_lower, CI_type=CI_type, plot_type=func)
                    Y_upper = no_reverse(Y_upper, CI_type=CI_type, plot_type=func)

                if func == "CDF":
                    yy_lower = 1 - Y_lower
                    yy_upper = 1 - Y_upper
                elif func == "SF":
                    yy_lower = Y_lower
                    yy_upper = Y_upper
                elif func == "CHF":
                    yy_lower = -np.log(Y_lower)
                    yy_upper = -np.log(Y_upper)

                if x is not None:
                    return Y_lower, Y_upper

    @staticmethod
    def loglogistic_CI(
        self,
        func="CDF",
        plot_CI=None,
        CI_type=None,
        CI=None,
        text_title="",
        color=None,
        q=None,
        x=None,
    ):
        """
        Generates the confidence intervals for CDF, SF, and CHF of the
        Loglogistic distribution.

        Parameters
        ----------
        self : object
            The distribution object
        func : str
            Must be either "CDF", "SF" or "CHF". Default is "CDF".
        plot_CI : bool, None
            The confidence intervals will only be plotted if plot_CI is True.
        CI_type : str
            Must be either "time" or "reliability"
        CI : float
            The confidence interval. Must be between 0 and 1
        text_title : str
            The existing CDF/SF/CHF text title to which the confidence interval
            string will be added.
        color : str
            The color to be used to fill the confidence intervals.
        q : array, list, optional
            The quantiles to be calculated. Default is None. Only used if CI_type='time'.
        x : array, list, optional
            The x-values to be calculated. Default is None. Only used if CI_type='reliability'.

        Returns
        -------
        t_lower : array
            The lower bounds on time. Only returned if CI_type is "time" and q
            is not None.
        t_upper :array
            The upper bounds on time. Only returned if CI_type is "time" and q
            is not None.
        R_lower : array
            The lower bounds on reliability. Only returned if CI_type is
            "reliability" and x is not None.
        R_upper :array
            The upper bounds on reliability. Only returned if CI_type is
            "reliability" and x is not None.

        Notes
        -----
        self must contain particular values for this function to work. These
        include self.alpha_SE, self.beta_SE, self.Cov_alpha_beta, self.Z.

        As a Utils function, there is very limited error checking done, as this
        function is not intended for users to access directly.

        For an explaination of how the confidence inervals are calculated,
        please see the `documentation <https://reliability.readthedocs.io/en/latest/How%20are%20the%20confidence%20intervals%20calculated.html>`_.
        """
        points = 200  # the number of data points in each confidence interval (upper and lower) line

        # this determines if the user has specified for the CI bounds to be shown or hidden.
        if (
            validate_CI_params(self.alpha_SE, self.beta_SE, self.Cov_alpha_beta, self.Z)
            is True
            and (plot_CI is True or q is not None or x is not None)
            and CI_type is not None
        ):
            if CI_type in ["time", "t", "T", "TIME", "Time"]:
                CI_type = "time"
            elif CI_type in [
                "reliability",
                "r",
                "R",
                "RELIABILITY",
                "rel",
                "REL",
                "Reliability",
            ]:
                CI_type = "reliability"
            if func not in ["CDF", "SF", "CHF"]:
                raise ValueError("func must be either CDF, SF, or CHF")
            if type(q) not in [list, np.ndarray, type(None)]:
                raise ValueError(
                    "q must be a list or array of quantiles. Default is None"
                )
            if type(x) not in [list, np.ndarray, type(None)]:
                raise ValueError(
                    "x must be a list or array of x-values. Default is None"
                )
            if q is not None:
                q = np.asarray(q)
            if x is not None:
                x = np.asarray(x)

            Z = -ss.norm.ppf((1 - CI) / 2)  # converts CI to Z

            def u(t, alpha, beta):  # u = ln(1/R - 1)
                return beta * (anp.log(t) - anp.log(alpha))  # loglogistic SF linearized

            def v(R, alpha, beta):  # v = ln(t)
                return (1 / beta) * anp.log(1 / R - 1) + anp.log(
                    alpha
                )  # loglogistic SF rearranged for t

            du_da = jac(u, 1)  # derivative wrt alpha (bounds on reliability)
            du_db = jac(u, 2)  # derivative wrt beta (bounds on reliability)
            dv_da = jac(v, 1)  # derivative wrt alpha (bounds on time)
            dv_db = jac(v, 2)  # derivative wrt beta (bounds on time)

            def var_u(self, v):  # v is time
                return (
                    du_da(v, self.alpha, self.beta) ** 2 * self.alpha_SE**2
                    + du_db(v, self.alpha, self.beta) ** 2 * self.beta_SE**2
                    + 2
                    * du_da(v, self.alpha, self.beta)
                    * du_db(v, self.alpha, self.beta)
                    * self.Cov_alpha_beta
                )

            def var_v(self, u):  # u is reliability
                return (
                    dv_da(u, self.alpha, self.beta) ** 2 * self.alpha_SE**2
                    + dv_db(u, self.alpha, self.beta) ** 2 * self.beta_SE**2
                    + 2
                    * dv_da(u, self.alpha, self.beta)
                    * dv_db(u, self.alpha, self.beta)
                    * self.Cov_alpha_beta
                )

            if CI_type == "time":  # Confidence bounds on time (in terms of reliability)
                # Y is reliability (R)
                if func == "CHF":
                    chf_array = np.geomspace(1e-8, self._chf[-1] * 1.5, points)
                    Y = np.exp(-chf_array)
                else:  # CDF and SF
                    if q is not None:
                        Y = q
                    else:
                        Y = transform_spaced(
                            "loglogistic", y_lower=1e-8, y_upper=1 - 1e-8, num=points
                        )

                # v is ln(t)
                v_lower = v(Y, self.alpha, self.beta) - Z * (var_v(self, Y) ** 0.5)
                v_upper = v(Y, self.alpha, self.beta) + Z * (var_v(self, Y) ** 0.5)

                t_lower = np.exp(v_lower) + self.gamma  # transform back from ln(t)
                t_upper = np.exp(v_upper) + self.gamma

                # clean the arrays of illegal values (<=0, nans, >=1 (if CDF or SF))
                t_lower, t_upper, Y, Y = clean_CI_arrays(
                    xlower=t_lower,
                    xupper=t_upper,
                    ylower=Y,
                    yupper=Y,
                    plot_type=func,
                    q=q,
                )
                # artificially correct for any reversals
                if q is None and len(t_lower) > 2 and len(t_upper) > 2:
                    t_lower = no_reverse(t_lower, CI_type=CI_type, plot_type=func)
                    t_upper = no_reverse(t_upper, CI_type=CI_type, plot_type=func)

                if func == "CDF":
                    yy = 1 - Y
                elif func == "SF":
                    yy = Y
                elif func == "CHF":
                    yy = -np.log(Y)

                if q is not None:
                    return t_lower, t_upper

            elif (
                CI_type == "reliability"
            ):  # Confidence bounds on Reliability (in terms of time)
                if x is not None:
                    t = x - self.gamma
                else:
                    t0 = self.quantile(0.00001) - self.gamma
                    if t0 <= 0:
                        t0 = 0.0001
                    t = np.geomspace(
                        t0,
                        self.quantile(0.99999) - self.gamma,
                        points,
                    )

                # u is reliability ln(1/R - 1)
                u_lower = (
                    u(t, self.alpha, self.beta) + Z * var_u(self, t) ** 0.5
                )  # note that gamma is incorporated into u but not in var_u. This is the same as just shifting a Weibull_2P across
                u_upper = u(t, self.alpha, self.beta) - Z * var_u(self, t) ** 0.5

                Y_lower = 1 / (np.exp(u_lower) + 1)  # transform back from ln(1/R - 1)
                Y_upper = 1 / (np.exp(u_upper) + 1)

                # clean the arrays of illegal values (<=0, nans, >=1 (if CDF or SF))
                t, t, Y_lower, Y_upper = clean_CI_arrays(
                    xlower=t,
                    xupper=t,
                    ylower=Y_lower,
                    yupper=Y_upper,
                    plot_type=func,
                    x=x,
                )
                # artificially correct for any reversals
                if x is None and len(Y_lower) > 2 and len(Y_upper) > 2:
                    Y_lower = no_reverse(Y_lower, CI_type=CI_type, plot_type=func)
                    Y_upper = no_reverse(Y_upper, CI_type=CI_type, plot_type=func)

                if func == "CDF":
                    yy_lower = 1 - Y_lower
                    yy_upper = 1 - Y_upper
                elif func == "SF":
                    yy_lower = Y_lower
                    yy_upper = Y_upper
                elif func == "CHF":
                    yy_lower = -np.log(Y_lower)
                    yy_upper = -np.log(Y_upper)

                if x is not None:
                    return Y_lower, Y_upper

    @staticmethod
    def gumbel_CI(
        self,
        func="CDF",
        plot_CI=None,
        CI_type=None,
        CI=None,
        text_title="",
        color=None,
        q=None,
        x=None,
    ):
        """
        Generates the confidence intervals for CDF, SF, and CHF of the
        Gumbel distribution.

        Parameters
        ----------
        self : object
            The distribution object
        func : str
            Must be either "CDF", "SF" or "CHF". Default is "CDF".
        plot_CI : bool, None
            The confidence intervals will only be plotted if plot_CI is True.
        CI_type : str
            Must be either "time" or "reliability"
        CI : float
            The confidence interval. Must be between 0 and 1
        text_title : str
            The existing CDF/SF/CHF text title to which the confidence interval
            string will be added.
        color : str
            The color to be used to fill the confidence intervals.
        q : array, list, optional
            The quantiles to be calculated. Default is None. Only used if CI_type='time'.
        x : array, list, optional
            The x-values to be calculated. Default is None. Only used if CI_type='reliability'.

        Returns
        -------
        t_lower : array
            The lower bounds on time. Only returned if CI_type is "time" and q
            is not None.
        t_upper :array
            The upper bounds on time. Only returned if CI_type is "time" and q
            is not None.
        R_lower : array
            The lower bounds on reliability. Only returned if CI_type is
            "reliability" and x is not None.
        R_upper :array
            The upper bounds on reliability. Only returned if CI_type is
            "reliability" and x is not None.

        Notes
        -----
        self must contain particular values for this function to work. These
        include self.mu_SE, self.sigma_SE, self.Cov_mu_sigma, self.Z.

        As a Utils function, there is very limited error checking done, as this
        function is not intended for users to access directly.

        For an explaination of how the confidence inervals are calculated,
        please see the `documentation <https://reliability.readthedocs.io/en/latest/How%20are%20the%20confidence%20intervals%20calculated.html>`_.
        """
        points = 200  # the number of data points in each confidence interval (upper and lower) line

        # this determines if the user has specified for the CI bounds to be shown or hidden.
        if (
            validate_CI_params(self.mu_SE, self.sigma_SE, self.Cov_mu_sigma, self.Z)
            is True
            and (plot_CI is True or q is not None or x is not None)
            and CI_type is not None
        ):
            if CI_type in ["time", "t", "T", "TIME", "Time"]:
                CI_type = "time"
            elif CI_type in [
                "reliability",
                "r",
                "R",
                "RELIABILITY",
                "rel",
                "REL",
                "Reliability",
            ]:
                CI_type = "reliability"
            if func not in ["CDF", "SF", "CHF"]:
                raise ValueError("func must be either CDF, SF, or CHF")
            if type(q) not in [list, np.ndarray, type(None)]:
                raise ValueError(
                    "q must be a list or array of quantiles. Default is None"
                )
            if type(x) not in [list, np.ndarray, type(None)]:
                raise ValueError(
                    "x must be a list or array of x-values. Default is None"
                )
            if q is not None:
                q = np.asarray(q)
            if x is not None:
                x = np.asarray(x)

            Z = -ss.norm.ppf((1 - CI) / 2)  # converts CI to Z

            def u(t, mu, sigma):  # u = ln(-ln(R))
                return (t - mu) / sigma  # gumbel SF linearlized

            def v(R, mu, sigma):  # v = t
                return mu + sigma * anp.log(-anp.log(R))  # Gumbel SF rearranged for t

            # for consistency with other distributions, the derivatives are da for d_sigma and db for d_mu. Just think of a is first parameter and b is second parameter.
            du_da = jac(u, 1)  # derivative wrt mu (bounds on reliability)
            du_db = jac(u, 2)  # derivative wrt sigma (bounds on reliability)
            dv_da = jac(v, 1)  # derivative wrt mu (bounds on time)
            dv_db = jac(v, 2)  # derivative wrt sigma (bounds on time)

            def var_u(self, v):  # v is time
                return (
                    du_da(v, self.mu, self.sigma) ** 2 * self.mu_SE**2
                    + du_db(v, self.mu, self.sigma) ** 2 * self.sigma_SE**2
                    + 2
                    * du_da(v, self.mu, self.sigma)
                    * du_db(v, self.mu, self.sigma)
                    * self.Cov_mu_sigma
                )

            def var_v(self, u):  # u is reliability
                return (
                    dv_da(u, self.mu, self.sigma) ** 2 * self.mu_SE**2
                    + dv_db(u, self.mu, self.sigma) ** 2 * self.sigma_SE**2
                    + 2
                    * dv_da(u, self.mu, self.sigma)
                    * dv_db(u, self.mu, self.sigma)
                    * self.Cov_mu_sigma
                )

            if CI_type == "time":  # Confidence bounds on time (in terms of reliability)
                # Y is reliability (R)
                if func == "CHF":
                    chf_array = np.geomspace(1e-8, self._chf[-1] * 1.5, points)
                    Y = np.exp(-chf_array)
                else:  # CDF and SF
                    if q is not None:
                        Y = q
                    else:
                        Y = transform_spaced(
                            "gumbel", y_lower=1e-8, y_upper=1 - 1e-8, num=points
                        )

                # v is t
                t_lower = v(Y, self.mu, self.sigma) - Z * (var_v(self, Y) ** 0.5)
                t_upper = v(Y, self.mu, self.sigma) + Z * (var_v(self, Y) ** 0.5)

                # clean the arrays of illegal values (<=0, nans, >=1 (if CDF or SF))
                t_lower, t_upper, Y, Y = clean_CI_arrays(
                    xlower=t_lower,
                    xupper=t_upper,
                    ylower=Y,
                    yupper=Y,
                    plot_type=func,
                    q=q,
                )
                # artificially correct for any reversals
                if q is None and len(t_lower) > 2 and len(t_upper) > 2:
                    t_lower = no_reverse(t_lower, CI_type=CI_type, plot_type=func)
                    t_upper = no_reverse(t_upper, CI_type=CI_type, plot_type=func)

                if func == "CDF":
                    yy = 1 - Y
                elif func == "SF":
                    yy = Y
                elif func == "CHF":
                    yy = -np.log(Y)

                if q is not None:
                    return t_lower, t_upper

            elif (
                CI_type == "reliability"
            ):  # Confidence bounds on Reliability (in terms of time)
                if x is not None:
                    t = x
                else:
                    t = np.linspace(
                        self.quantile(0.00001), self.quantile(0.99999), points
                    )

                # u is reliability u = ln(-ln(R))
                u_lower = u(t, self.mu, self.sigma) + Z * var_u(self, t) ** 0.5
                u_upper = u(t, self.mu, self.sigma) - Z * var_u(self, t) ** 0.5

                Y_lower = np.exp(-np.exp(u_lower))  # transform back from ln(-ln(R))
                Y_upper = np.exp(-np.exp(u_upper))

                # clean the arrays of illegal values (<=0, nans, >=1 (if CDF or SF))
                t, t, Y_lower, Y_upper = clean_CI_arrays(
                    xlower=t,
                    xupper=t,
                    ylower=Y_lower,
                    yupper=Y_upper,
                    plot_type=func,
                    x=x,
                )
                # artificially correct for any reversals
                if x is None and len(Y_lower) > 2 and len(Y_upper) > 2:
                    Y_lower = no_reverse(Y_lower, CI_type=CI_type, plot_type=func)
                    Y_upper = no_reverse(Y_upper, CI_type=CI_type, plot_type=func)

                if func == "CDF":
                    yy_lower = 1 - Y_lower
                    yy_upper = 1 - Y_upper
                elif func == "SF":
                    yy_lower = Y_lower
                    yy_upper = Y_upper
                elif func == "CHF":
                    yy_lower = -np.log(Y_lower)
                    yy_upper = -np.log(Y_upper)

                if x is not None:
                    return Y_lower, Y_upper


def extract_CI(dist, func="CDF", CI_type="time", CI=0.95, CI_y=None, CI_x=None):
    """
    Extracts the confidence bounds at CI_x or CI_y.

    Parameters
    ----------
    dist : object
        Distribution object from reliability.Distributions
    func : str
        Must be either 'CDF', 'SF', 'CHF'
    CI_type : str
        Must be either 'time' or 'reliability'
    CI : float
        The confidence interval. Must be between 0 and 1.
    CI_y : list, array
        The y-values from which to extract the confidence interval (x-values)
        for bounds on time.
    CI_x : list, array
        The x-values from which to extract the confidence interval (y-values)
        for bounds on reliability.

    Returns
    -------
    lower : array
        An array of the lower confidence bounds at CI_x or CI_y
    upper : array
        An array of the upper confidence bounds at CI_x or CI_y

    Notes
    -----
    If CI_type="time" then CI_y must be specified in order to extract the
    confidence bounds on time.

    If CI_type="reliability" then CI_x must be specified in order to extract the
    confidence bounds on reliability.
    """

    if dist.name == "Exponential":
        if CI_y is not None and CI_x is not None:
            raise ValueError(
                "Both CI_x and CI_y have been provided. Please provide only one."
            )
        if CI_y is not None:
            if func == "SF":
                q = np.asarray(CI_y)
            elif func == "CDF":
                q = 1 - np.asarray(CI_y)
            elif func == "CHF":
                q = np.exp(-np.asarray(CI_y))
            else:
                raise ValueError("func must be CDF, SF, or CHF")
            SF_time = distribution_confidence_intervals.exponential_CI(
                self=dist, CI=CI, q=q
            )
            lower, upper = SF_time[0], SF_time[1]
        elif CI_x is not None:
            SF_rel = distribution_confidence_intervals.exponential_CI(
                self=dist, CI=CI, x=CI_x
            )
            if func == "SF":
                lower, upper = SF_rel[1], SF_rel[0]
            elif func == "CDF":
                lower, upper = 1 - SF_rel[0], 1 - SF_rel[1]
            elif func == "CHF":
                lower, upper = -np.log(SF_rel[0]), -np.log(SF_rel[1])
            else:
                raise ValueError("func must be CDF, SF, or CHF")
        else:
            lower, upper = None, None
    else:
        if CI_y is not None and CI_x is not None:
            raise ValueError(
                "Both CI_x and CI_y have been provided. Please provide only one."
            )
        if CI_x is not None and CI_y is None and CI_type == "time":
            colorprint(
                'WARNING: If CI_type="time" then CI_y must be specified in order to extract the confidence bounds on time.',
                text_color="red",
            )
            lower, upper = None, None
        elif CI_y is not None and CI_x is None and CI_type == "reliability":
            colorprint(
                'WARNING: If CI_type="reliability" then CI_x must be specified in order to extract the confidence bounds on reliability.',
                text_color="red",
            )
            lower, upper = None, None
        elif (CI_y is not None and CI_type == "time") or (
            CI_x is not None and CI_type == "reliability"
        ):
            if CI_type == "time":
                if func == "SF":
                    q = np.asarray(CI_y)
                elif func == "CDF":
                    q = 1 - np.asarray(CI_y)
                elif func == "CHF":
                    q = np.exp(-np.asarray(CI_y))
                else:
                    raise ValueError("func must be CDF, SF, or CHF")
            if dist.name == "Weibull":
                if CI_type == "time":
                    SF_time = distribution_confidence_intervals.weibull_CI(
                        self=dist, CI_type="time", CI=CI, q=q
                    )
                    lower, upper = SF_time[0], SF_time[1]
                elif CI_type == "reliability":
                    SF_rel = distribution_confidence_intervals.weibull_CI(
                        self=dist, CI_type="reliability", CI=CI, x=CI_x
                    )
                    if func == "SF":
                        lower, upper = SF_rel[0], SF_rel[1]
                    elif func == "CDF":
                        lower, upper = 1 - SF_rel[1], 1 - SF_rel[0]
                    elif func == "CHF":
                        lower, upper = -np.log(SF_rel[1]), -np.log(SF_rel[0])
            elif dist.name == "Normal":
                if CI_type == "time":
                    SF_time = distribution_confidence_intervals.normal_CI(
                        self=dist, CI_type="time", CI=CI, q=q
                    )
                    lower, upper = SF_time[0], SF_time[1]
                elif CI_type == "reliability":
                    SF_rel = distribution_confidence_intervals.normal_CI(
                        self=dist, CI_type="reliability", CI=CI, x=CI_x
                    )
                    if func == "SF":
                        lower, upper = SF_rel[1], SF_rel[0]
                    elif func == "CDF":
                        lower, upper = 1 - SF_rel[0], 1 - SF_rel[1]
                    elif func == "CHF":
                        lower, upper = -np.log(SF_rel[0]), -np.log(SF_rel[1])
            elif dist.name == "Lognormal":
                if CI_type == "time":
                    SF_time = distribution_confidence_intervals.lognormal_CI(
                        self=dist, CI_type="time", CI=CI, q=q
                    )
                    lower, upper = SF_time[0], SF_time[1]
                elif CI_type == "reliability":
                    SF_rel = distribution_confidence_intervals.lognormal_CI(
                        self=dist, CI_type="reliability", CI=CI, x=CI_x
                    )
                    if func == "SF":
                        lower, upper = SF_rel[1], SF_rel[0]
                    elif func == "CDF":
                        lower, upper = 1 - SF_rel[0], 1 - SF_rel[1]
                    elif func == "CHF":
                        lower, upper = -np.log(SF_rel[0]), -np.log(SF_rel[1])
            elif dist.name == "Gamma":
                if CI_type == "time":
                    SF_time = distribution_confidence_intervals.gamma_CI(
                        self=dist, CI_type="time", CI=CI, q=q
                    )
                    lower, upper = SF_time[0], SF_time[1]
                elif CI_type == "reliability":
                    SF_rel = distribution_confidence_intervals.gamma_CI(
                        self=dist, CI_type="reliability", CI=CI, x=CI_x
                    )
                    if func == "SF":
                        lower, upper = SF_rel[0], SF_rel[1]
                    elif func == "CDF":
                        lower, upper = 1 - SF_rel[1], 1 - SF_rel[0]
                    elif func == "CHF":
                        lower, upper = -np.log(SF_rel[1]), -np.log(SF_rel[0])
            elif dist.name == "Gumbel":
                if CI_type == "time":
                    SF_time = distribution_confidence_intervals.gumbel_CI(
                        self=dist, CI_type="time", CI=CI, q=q
                    )
                    lower, upper = SF_time[0], SF_time[1]
                elif CI_type == "reliability":
                    SF_rel = distribution_confidence_intervals.gumbel_CI(
                        self=dist, CI_type="reliability", CI=CI, x=CI_x
                    )
                    if func == "SF":
                        lower, upper = SF_rel[0], SF_rel[1]
                    elif func == "CDF":
                        lower, upper = 1 - SF_rel[1], 1 - SF_rel[0]
                    elif func == "CHF":
                        lower, upper = -np.log(SF_rel[1]), -np.log(SF_rel[0])
            elif dist.name == "Loglogistic":
                if CI_type == "time":
                    SF_time = distribution_confidence_intervals.loglogistic_CI(
                        self=dist, CI_type="time", CI=CI, q=q
                    )
                    lower, upper = SF_time[0], SF_time[1]
                elif CI_type == "reliability":
                    SF_rel = distribution_confidence_intervals.loglogistic_CI(
                        self=dist, CI_type="reliability", CI=CI, x=CI_x
                    )
                    if func == "SF":
                        lower, upper = SF_rel[0], SF_rel[1]
                    elif func == "CDF":
                        lower, upper = 1 - SF_rel[1], 1 - SF_rel[0]
                    elif func == "CHF":
                        lower, upper = -np.log(SF_rel[1]), -np.log(SF_rel[0])
            else:
                raise ValueError("Unknown distribution")
        else:
            lower, upper = None, None
    if type(lower) is not type(None):
        if len(lower) == 1:  # unpack arrays of length 1
            lower, upper = lower[0], upper[0]
    return lower, upper


def random_xy_data(
    model,
    parameters,
    x=None,
    xmin=None,
    xmax=None,
    size=None,
    sigma=None,
    logspace=False,
    x_positive_only=False,
    seed=None,
):
    """
    Generates random data for a scatterplot. Returns the data as x,y

    Parameters
    ----------
    model : object
        A model from utils.linear_models
    parameters : array, list
        The parameters for the model
    x : array, list
        The x data to be used. If not specified, it is generated using xmin, xmax, and size
    xmin : float, int
        The lower x value to use for generating the data. Only used if x is not specified.
    xmax : float, int
        The upper x value to use for generating the data. Only used if x is not specified.
    size : int
        The size of the random data array. If not specified defaults to 1.
    sigma : float, int
        The standard deviation of the normal distribution used for the random noise. If not specified defaults to 1/10th the range of the noiseless x_data and x_data respectively.
    logspace : bool
        If True will provide logspaced data. If False will provide linspaced data. Default is False.
    x_positive_only :
        If True will force all the x data to be positive using abs(x).

    Returns
    -------
    x, y : tuple
        A tuple of arrays of the x and y data.
    """

    if seed is not None:
        np.random.seed(seed)

    if x is None:
        if xmin is None:
            xmin = 0
        if xmax is None:
            xmax = 10
        if xmin > xmax:
            xmin, xmax = xmax, xmin
        if size is None:
            size = 1
        if logspace is True:
            x = np.geomspace(xmin, xmax, size)
        else:
            x = np.linspace(xmin, xmax, size)
    x_range = max(x) - min(x)
    if sigma is None:
        sigma_x = x_range / 10
    else:
        sigma_x = sigma
    x_noise = np.random.normal(loc=0, scale=sigma_x, size=len(x))
    x_data = x + x_noise
    if x_positive_only is True:
        x_data = abs(x_data)

    y_true = model(x_data, *parameters)
    y_range = max(y_true) - min(y_true)
    if sigma is None:
        sigma_y = y_range / 10
    else:
        sigma_y = sigma
    y_noise = np.random.normal(loc=0, scale=sigma_y, size=len(x))
    y_data = y_true + y_noise
    return x_data, y_data


class linear_models:
    """
    A collection of linear models
    """

    @staticmethod
    def linear(x, a, b):
        """
        Straight line
        y = a * x + b
        """
        return a * x + b

    @staticmethod
    def poly_2(x, a, b, c):
        """
        Quadratic
        y = a * x**2 + b * x + c
        """
        return a * x**2 + b * x + c

    @staticmethod
    def poly_3(x, a, b, c, d):
        """
        Cubic
        y = a * x**3 + b * x**2 + c * x + d
        """
        return a * x**3 + b * x**2 + c * x + d

    @staticmethod
    def poly_4(x, a, b, c, d, e):
        """
        Quartic
        y = a * x**4 + b * x**3 + c * x**2 + d * x + e
        """
        return a * x**4 + b * x**3 + c * x**2 + d * x + e

    @staticmethod
    def poly_5(x, a, b, c, d, e, f):
        """
        Quintic
        y = a * x**5 + b * x**4 + c * x**3 + d * x**2 + e * x + f
        """
        return a * x**5 + b * x**4 + c * x**3 + d * x**2 + e * x + f

    @staticmethod
    def poly_6(x, a, b, c, d, e, f, g):
        """
        Sextic
        y = a * x**6 + b * x**5 + c * x**4 + d * x**3 + e * x**2 + f * x + g
        """
        return (
            a * x**6 + b * x**5 + c * x**4 + d * x**3 + e * x**2 + f * x + g
        )

    @staticmethod
    def logarithmic(x, a, b, c):
        """
        Logarithmic
        y = a * np.log(b * x) + c
        """
        return a * np.log(b * x) + c

    @staticmethod
    def exponential(x, a, b, c):
        """
        Exponential
        y = a * np.exp(b * x) + c
        """
        return a * np.exp(b * x) + c

    @staticmethod
    def power(x, a, b):
        """
        Power
        y = a * x**b
        """
        return a * x**b


def removeNegativesInX(x, y=None):
    """
    Removes negatives from a list or array.

    Parameters
    ----------
    x : array, list
        The first array or list to be processed.
    y : array, list, optional
        The second array or list to be processed.

    Returns
    -------
    x_out : list, array
        A list or array of the same type as x input with the negatives removed.
    y_out : list, array
        A list or array of the same type as y input with the negatives removed.

    """

    if y is not None:
        if type(x) == list:
            x = np.asarray(x)
            y = np.asarray(y)
            arr_out = False
        else:
            arr_out = True
        x_out = x[x > 0]
        y_out = y[x > 0]
        if arr_out is False:
            x_out = x_out.tolist()
            y_out = y_out.tolist()
        return x_out, y_out
    else:
        if type(x) == list:
            x = np.asarray(x)
            arr_out = False
        else:
            arr_out = True
        x_out = x[x > 0]
        if arr_out is False:
            x_out = x_out.tolist()
        return x_out


def removeNaNs(x, y=None):
    """
    Removes NaNs and inf from a list or array.

    Parameters
    ----------
    x : array, list
        The first array or list to be processed.
    y : array, list, optional
        The second array or list to be processed.

    Returns
    -------
    x_out : list, array
        A list or array of the same type as x input with the NaNs removed.
    y_out : list, array
        A list or array of the same type as y input with the NaNs removed.


    Notes
    -----
    This is better than simply using "x = x[numpy.logical_not(numpy.isnan(x))]"
    as numpy crashes for str and bool.
    """
    if y is not None:
        if len(x) != len(y):
            raise ValueError("x and y must be the same length")
        if type(x) == np.ndarray:
            x = list(x)
            y = list(y)
            arr_out = True
        else:
            arr_out = False
        x_out = []
        y_out = []
        for i in range(len(x)):
            keep_x, keep_y = 0, 0
            xi = x[i]
            yi = y[i]
            if type(xi) in [str, bool, np.str_]:
                if xi not in ["nan", "inf"]:
                    keep_x = 1
            elif type(xi) in [
                int,
                float,
                np.int16,
                np.int32,
                np.float16,
                np.float32,
                np.float64,
            ]:
                if np.logical_not(np.isnan(xi)) and np.logical_not(
                    np.isinf(xi)
                ):  # this only works for numbers
                    keep_x = 1
            else:
                raise ValueError("Unexpected type in X: ", str(type(xi)))
            if type(yi) in [str, bool, np.str_]:
                if yi not in ["nan", "inf"]:
                    keep_y = 1
            elif type(yi) in [
                int,
                float,
                np.int16,
                np.int32,
                np.float16,
                np.float32,
                np.float64,
            ]:
                if np.logical_not(np.isnan(yi)) and np.logical_not(
                    np.isinf(yi)
                ):  # this only works for numbers
                    keep_y = 1
            else:
                raise ValueError("Unexpected type in X: ", str(type(xi)))

            keep = keep_x * keep_y
            if keep == 1:
                x_out.append(xi)
                y_out.append(yi)

        if arr_out is True:
            x_out = np.asarray(x_out)
            y_out = np.asarray(y_out)
        return x_out, y_out
    else:
        if type(x) == np.ndarray:
            x = list(x)
            arr_out = True
        else:
            arr_out = False
        out = []
        for i in x:
            if type(i) in [str, bool, np.str_]:
                if i not in ["nan", "inf"]:
                    out.append(i)
            elif np.logical_not(np.isnan(i)) and np.logical_not(
                np.isinf(i)
            ):  # this only works for numbers
                out.append(i)
        if arr_out is True:
            out = np.asarray(out)
        return out


def printObject(object):
    """
    This function provides a simplified way of extracting all the values from an
    object and printing them.
    """
    object_dict = object.__dict__
    keys = object_dict.keys()
    for item in keys:
        print(item, "=", object_dict[item])
    print("")


class objectConverters:
    """
    Converters for python objects. Includes:
    List to Dictionary
    List to Object
    Dictionary to Object
    """

    def list2dict(keys, values):
        """
        Generates a dictionary using keys and values
        """
        return dict(zip(keys, values))

    @staticmethod
    class list2object:
        """
        Generates an object using keys and values
        """

        def __init__(self, keys, values, object_to_use=None):
            if len(keys) == len(values):
                for i in range(len(keys)):
                    if object_to_use is None:
                        setattr(self, keys[i], values[i])
                    else:
                        setattr(object_to_use, keys[i], values[i])
            else:
                raise ValueError("number of keys does not match number of values")

    @staticmethod
    class dict2object:
        """
        Generates an object from a dictionary
        """

        def __init__(self, dictionary=None, object_to_use=None):
            if dictionary is not None:
                for key, value in dictionary.items():
                    if object_to_use is None:
                        setattr(self, key, value)
                    else:
                        setattr(object_to_use, key, value)

    @staticmethod
    def object2dict(object_to_use):
        """
        Generates a dictionary from an object
        """
        dict_out = object_to_use.__dict__
        return dict_out

    @staticmethod
    def object2json(object_to_use):
        """
        Generates json object from a python object
        """
        json_out = json.dumps(vars(object_to_use))
        return json_out
