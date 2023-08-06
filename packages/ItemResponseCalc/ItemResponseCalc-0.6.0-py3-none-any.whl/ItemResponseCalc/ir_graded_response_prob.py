"""This module implements core functions of the
IRT Graded Response Model (Samejima, 1997).

These functions are collected in a separate module to simplify
selecting either this model, or the similar
IRT Partial Credits Model.

*** Main Class: GradedResponse

*** References:
F. Samejima (1997). Graded response model.
In W. J. v. D. Linden and R. K. Hambleton, eds.,
*Handbook of Modern Item Response Theory*, p. 85–100. Springer, New York.

J.-P. Fox (2010). *Bayesian Item Response Modeling: Theory and Applications*.
Statistics for Social and Behavioral Sciences. Springer.

*** Version:
2020-06-14, first version with methods copied from item_respondents
    to replace functions previously defined there.
2020-06-15, cleanup, tested
"""
import numpy as np

from ItemResponseCalc.item_graded_response import GradedResponseItem
from ItemResponseCalc.safe_logistic import logistic

import logging
logger = logging.getLogger(__name__)


# --------------------------------------------------------------------------
class GradedResponse:
    """Implementing central methods to calculate
    log probability of observed responses, and corresponding gradients,
    given item and respondent parameters.
    No internal properties, only static methods and class methods
    """
    item_class = GradedResponseItem
    # ref to class implementing distribution of item parameters for this model

    @staticmethod
    def response_prob_by_theta(theta, tau, latent_scale=1.):
        """Conditional probability of ordinal responses, given trait value,
        averaged across tau samples
        :param theta: array of trait values
        :param tau: 2D array of threshold samples
            tau[m, l] = m-th sample of upper limit of l-th response interval,
            except extreme thresholds at -inf, +inf
        :param latent_scale: (optional) scale of latent-variable logistic distribution
        :return: pr = array of response probabilities
            pr[..., l] = P{response = l | theta[...], tau}
            = logistic.cdf(theta[...] - tau[l]) - logistic.cdf(theta[...] - tau[l-1])
            pr.shape == (*theta.shape, tau.shape[-1] + 1)
        """
        t = tau - theta[..., np.newaxis, np.newaxis]
        t /= latent_scale
        cdf = np.mean(logistic.cdf(t), axis=-2)  # average across tau samples
        p = np.concatenate((np.zeros((*cdf.shape[:-1], 1)),
                            cdf,
                            np.ones((*cdf.shape[:-1], 1))),
                            axis=-1)
        p = np.diff(p, axis=-1)
        return p

    @staticmethod
    def logprob_by_theta(theta, tau_i, w_i, r_i):
        """sum log prob of observed data
        for ONE item, for ALL subjects in ONE group,
        averaged across tau samples for that item
        :param theta: theta[n, s, t] = n-th sample of t-th trait by s-th subject
        :param tau_i: tau_i[m, l] = m-th sample of UPPER interval limit for l-th response
            tau_i.shape[-1] == L_i - 1
        :param w_i: 1D array with w_i[t] = i-th item weight for t-th trait
            len(w_i) == theta.shape[-1]
        :param r_i: r_i[s] = response index for s-th subject to i-th item
            len(r_i) == theta.shape[1]
        :return: lp = 1D array, with lp[n] = n-th sample
        """
        lp = response_logprob(theta, tau_i, r_i)
        # lp[n, m, t] = n-th theta sample, m-th tau sample, t-th trait
        lp = np.mean(lp, axis=-2)  # across tau samples
        # lp[n, t]
        lp = np.dot(lp, w_i)  # ***** let caller do this ???
        # lp[n]
        return lp

    @staticmethod
    def logprob_by_tau(theta, tau_i, w_i, r_i):
        """log prob of observed responses for ONE item and ALL respondents in ONE group
        summed across subjects, averaged across theta samples
        using current theta distribution.
        :param theta: theta[n, s, t] = n-th sample of t-th trait by s-th subject
        :param tau_i: tau_i[m, l] = m-th sample of UPPER interval limit for l-th response
            tau_i.shape[-1] == L_i - 1
        :param w_i: 1D array with w_i[t] = i-th item weight for t-th trait
        :param r_i: list with r_i[s] = response index for s-th subject to i-th item
        :return: lp = 2D array, with lp[m, t] = m-th sample for t-th trait
        """
        lp = response_logprob(theta, tau_i, r_i)
        lp = np.mean(lp, axis=0)  # across theta samples
        # lp[m, t] = m-th tau sample, for t-th trait
        if w_i is None:
            return lp
        else:
            return np.dot(lp, w_i)  # let caller do this ?

    @staticmethod
    def d_logprob_by_theta(theta, tau_i, w_i, r_i):
        """gradient of logprob_by_theta, w.r.t theta
        :param theta: theta[n, s, t] = n-th sample of t-th trait by s-th subject
        :param tau_i: tau_i[m, l] = m-th sample of UPPER interval limit for l-th response
            tau_i.shape[-1] == L_i - 1
        :param w_i: 1D array with w_i[t] = i-th item weight for t-th trait
        :param r_i: list with r_i[s] = response index for s-th subject to i-th item
        :return: dlp = 3D array, with
            dlp.shape == theta.shape
            dlp[n, s, t] = d logprob_by_theta(*)[n] / d theta[n, s, t]
        """
        (tau_low, tau_high) = response_interval(tau_i, r_i)
        # tau_low[m, s] and tau_high[m, s] are (low, high) interval limits
        th = theta[:, None, :, :]  # to allow broadcast
        # th[n, 0, s, t] = n-th sample of t-th trait for s-th subject
        dlp = d_log_prob_range_dm(tau_low[..., None] - th, tau_high[..., None] - th)
        # dlp[n, m, s, t] = n-th theta sample, m-th tau sample for s-th subject
        dlp = np.mean(dlp, axis=1)
        # dlp[n, s, t] = n-th sample of t-th trait for s-th subject
        return dlp * w_i  # ***** let caller do the weighting ???

    @staticmethod
    def d_logprob_by_tau(theta, tau_i, w_i, r_i):
        """Gradient of logprob_by_tau w.r.t. tau_i,
        summed across subjects, averaged across theta samples
        :param theta: theta[n, s, t] = n-th sample of t-th trait by s-th subject
        :param tau_i: tau_i[m, l] = m-th sample of UPPER interval limit for l-th response
            tau_i.shape[-1] == L_i - 1
        :param w_i: 1D array with w_i[t] = i-th item weight for t-th trait
        :param r_i: list with r_i[s] = response index for s-th subject to i-th item
        :return: dlp = 3D array, with
            dlp[m, l, t] = d logprob(tau_i[m, :] / d tau_i[m, l], given t-th trait
            dlp.shape == (*tau_i.shape, theta.shape[-1)
        """
        (tau_low, tau_high) = response_interval(tau_i, r_i)
        # tau_low[m, s] and tau_high[m, s] are (low, high) interval limits
        th = theta[:, None, :, :]  # to allow broadcast
        (da, db) = d_log_prob_range_dab(tau_low[..., None] - th,
                                        tau_high[..., None] - th)
        # da[n, m, s, t] = n-th theta sample, m-th tau sample for t-th trait of s-th subject
        # of derivative w.r.t. tau_low
        # db similar for tau_high
        da = np.dot(np.mean(da, axis=0), w_i)
        db = np.dot(np.mean(db, axis=0), w_i)
        # da[n, m, s] = n-th theta sample, m-th tau sample of s-th subject, same for db
        n_response_levels = tau_i.shape[-1] + 1
        r_bool = np.array([r_i == l
                           for l in range(n_response_levels)]).T
        dlp = np.dot(da, r_bool[:, 1:]) + np.dot(db, r_bool[:, :-1])
        # dlp[m, l] = derivative w.r.t tau_i[m, l], sum across all responses
        # when tau[m, l] is LOWER limit PLUS when it is UPPER limit
        return dlp


# -------------------------------- help functions for GradedResponse

def response_logprob(theta, tau_i, r_i):
    """log prob of observed data
    for ONE item, and ALL subjects in ONE group,
    summed across subjects
    :param theta: theta[n, s, t] = n-th sample of t-th trait by s-th subject
    :param tau_i: tau_i[m, l] = m-th sample of UPPER interval limit for l-th response
        tau_i.shape[-1] == L_i - 1
    :param r_i: r_i[s] = response index for s-th subject to i-th item
        len(r_i) == theta.shape[1]
    :return: lp = 1D array, with lp[n] = n-th sample
    """
    (tau_low, tau_high) = response_interval(tau_i, r_i)
    # tau_low[m, s] and tau_high[m, s] are (low, high) interval limits
    th = theta[:, None, :, :]  # to allow broadcast
    # th[n, 0, s, t] = n-th sample of t-th trait for s-th subject
    lp = log_prob_range(tau_low[..., None] - th, tau_high[..., None] - th)
    # lp[n, m, s, t] = n-th sample of t-th trait for s-th subject, with m-th tau sample
    return np.sum(lp, axis=-2)  # across subjects
    # lp[n, m, t]


def response_interval(tau_i, r_i):
    """Get response interval for given thresholds and responses for ONE item
    :param tau_i: 2D array with threshold samples, as
        tau_i[m, l] = m-th sample of UPPER limit of l-th response interval,
            EXCEPT extreme limits -infty, +infty
        tau_i.shape[-1] == L - 1, with L = highest response value
    :param r_i: 1D array of response indices, with missing response = -1
        r_i[s] = response index for s-th subject in range(L)
        except r_[s] = -1 in case of missing response
    :return: tuple (tau_low, tau_high) with
        tau_low[m, s] = m-th sample of lower interval limit for r_i[s]
        tau_high[m, s] = m-th sample of upper interval limit for r_i[s]
        tau_low.shape == tau_high.shape
    """
    r_i = np.asarray(r_i)
    max_l = tau_i.shape[-1] - 1
    # r_i may be -1 for missing response, or = max_l +1 for highest interval
    tau_low = tau_i[:, np.maximum(0, r_i - 1)]
    tau_low[:, r_i <= 0] = -np.inf  # lowest interval OR missing response value
    tau_high = tau_i[:, np.minimum(max_l, r_i)]
    tau_high[:, r_i > max_l] = np.inf  # highest interval
    tau_high[:, r_i < 0] = np.inf  # missing response value
    return tau_low, tau_high


def log_prob_range(a, b):
    """log prob{ a < R <= b },
    for standard logistic random variable R, i.e.,
    = log(logistic.cdf(b) - logistic.cdf(a))
    :param a: array of lower interval limits
    :param b: array of upper interval limits, such that
        a.shape == b.shape
        -inf <= a < b <= +inf
    :return: lP = array of logprob values
        lP.shape == a.shape
    """
    # Reformulated, numerically safer than use of cdf functions:
    return (np.log1p(-np.exp(a - b))
            - np.log1p(np.exp(-b))
            - np.log1p(np.exp(a))
            )


def d_log_prob_range_dm(am, bm):
    """Gradient d log_prob_range(am, bm) / dm, where
    am = a - m, and bm = b - m
    :param am: array with lower limits
    :param bm: array with upper limits
        am.shape == bm.shape
        -inf <= am  < bm <= +inf
    :return: d_dm = array of gradient elements
        d_dm.shape == am.shape == bm.shape

    Method:
    log_prob_range = log-prob( a < Z <= b),
    for a logistic-distributed Z with location = m and scale=1,
    = logprob(a-m < Y <= b-m) for standardized Y with location = 0.
    = ln(1 - e^(am-bm)) - ln(1 + e^(-bm)) - ln(1 + e^(am))
    am - bm = a - b is independent of m.
    Thus,
    d_dm = - e^{-bm) / (1+ e^{-bm} ) + e^am / (1 + e^am)
    """
    # *** reformulate and check for numerical problem here, too
    return logistic.cdf(am) - logistic.cdf(-bm)


def d_log_prob_range_dab(am, bm):
    """Gradient d log_prob_range(am, bm) w.r.t. interval limits (a, b), where
    am = a - m, and bm = b - m
    :param am: array with lower limits
    :param bm: array with upper limits
        am.shape == bm.shape
        -infty <= am  < bm <= +infty
    :return: tuple (d_da, d_db), where
        d_da = d logprob(am, bm) w.r.t lower limit a
        d_db = d logprob(am, bm) w.r.t upper limet b
        d_da.shape == d_db.shape == am.shape == bm.shape

    Method:
    log_prob_range = log-prob( a < Z <= b),
    for a logistic-distributed Z with location = m and scale=1,
    = logprob(a-m < Y <= b-m) for standardized Y with location = 0.
    = ln(1 - e^(am-bm)) - ln(1 + e^(-bm)) - ln(1 + e^(am))

    d_da = -1 / (e^{bm - am} - 1 ) - e^am / (1 + e^am)
    d_db = +1 / (e^{bm - am} - 1 ) + e^bm / (1 + e^bm)
    """

    c = 1 / np.expm1(bm - am)
    if np.any(np.logical_not(np.isfinite(c))):
        logger.warning('Invalid tau, zero interval width')
    return - c - logistic.cdf(am), c + logistic.cdf(-bm)


# -------------------------------------------------------- TEST:
if __name__ == '__main__':
    # Testing some module functions

    from scipy.optimize import check_grad, approx_fprime

    print('\n*** Check logprob_range gradients: ')
    a = np.array([5.])
    b = a + 2.

    def test_logprob_range_m(y):
        return log_prob_range(a - y, b - y)

    def test_d_logprob_range_dm(y):
        return d_log_prob_range_dm(a- y, b- y)

    # ------------------------------------
    def test_logprob_range_a(y):
        return log_prob_range(a + y, b)

    def test_d_logprob_range_da(y):
        return d_log_prob_range_dab(a + y, b)[0]

    # ----------------------------------------
    def test_logprob_range_b(y):
        return log_prob_range(a, b + y)

    def test_d_logprob_range_db(y):
        return d_log_prob_range_dab(a, b + y)[1]

    test_y = np.array([0.])
    print(f'test_logprob_range_m(test_y) = {test_logprob_range_m(test_y)}')

    err = check_grad(test_logprob_range_m, test_d_logprob_range_dm, test_y)
    print('d_logprob_range_dm =', test_d_logprob_range_dm(test_y))
    print('approx_grad = ', approx_fprime(test_y,
                                          test_logprob_range_m,
                                          epsilon=1e-6))
    print('check_grad err = ', err)

    print(f'test_logprob_range_a(test_y) = {test_logprob_range_a(test_y)}')
    err = check_grad(test_logprob_range_a, test_d_logprob_range_da, test_y)
    print('d_logprob_range_da =', test_d_logprob_range_da(test_y))
    print('approx_grad = ', approx_fprime(test_y,
                                          test_logprob_range_a,
                                          epsilon=1e-6))
    print('check_grad err = ', err)

    print(f'test_logprob_range_b(test_y) = {test_logprob_range_b(test_y)}')
    err = check_grad(test_logprob_range_b, test_d_logprob_range_db, test_y)
    print('d_logprob_range_db =', test_d_logprob_range_db(test_y))
    print('approx_grad = ', approx_fprime(test_y,
                                          test_logprob_range_b,
                                          epsilon=1e-6))
    print('check_grad err = ', err)

    # ---------------------------------------------------------
    # print('\nTesting logprob_by_tau\n')
    #
    # weight = np.eye(n_traits)  # ********** item_i <=> trait_i
    #
    # item_ind = 0
    # w_i = weight[item_ind]
    #
    # # ----------------------------------------
    # def test_logprob_mean_theta(y):
    #     tau = y[None, :]
    #     return g_ind.logprob_by_tau(tau, item_ind, w_i)[0]
    #
    # def test_d_logprob_mean_theta(y):
    #     tau = y[None, :]
    #     return g_ind.d_logprob_by_tau(tau, item_ind, w_i)[0]
    #
    # test_tau = np.array(tau)[0,0,:]  # must be vector for test
    # print('test_tau= ', test_tau)
    # print('test_logprob_mean_theta(test_tau, item_ind)= ', test_logprob_mean_theta(test_tau))
    #
    # err = check_grad(test_logprob_mean_theta, test_d_logprob_mean_theta, test_tau)
    # print('grad_test =', test_d_logprob_mean_theta(test_tau))
    # print('approx_grad = ', approx_fprime(test_tau,
    #                                       test_logprob_mean_theta,
    #                                       epsilon=1e-6))
    # print('check_grad err = ', err)
    #
    # test_tau = np.array(tau)[0, 0, :]  # must be vector for test
    # print('test_tau= ', test_tau)
    # print('test_logprob_mean_theta(test_tau, item_ind)= ', test_logprob_mean_theta(test_tau))
    #
    # err = check_grad(test_logprob_mean_theta, test_d_logprob_mean_theta, test_tau)
    # print('grad_test =', test_d_logprob_mean_theta(test_tau))
    # print('approx_grad = ', approx_fprime(test_tau,
    #                                       test_logprob_mean_theta,
    #                                       epsilon=1e-6))
    # print('check_grad err = ', err)
