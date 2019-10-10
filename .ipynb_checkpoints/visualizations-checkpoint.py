import scipy.stats as stats
import pandas as pd
import numpy as np
from statsmodels.stats.proportion import proportions_ztest
import matplotlib.pyplot as plt


def plot_power(min_diff, prob_b, size_a, size_b, significance = 0.05):
    """illustrating power through a two-tailed hypothesis test
       obtains the z-score for the minimum detectable difference using proportion_ztest distribution for the null hypothesis, h0            and alternative hypothesis, h1
       points that are greater than the zscore for the specified significance level
       power is the area after the threshold, i.e. 1 - the cumulative distribution function of that point"""
 
    prob_a = prob_b + min_diff
    count_a = size_a * prob_a
    count_b = size_b * prob_b
    counts = np.array([count_a, count_b])
    nobs = np.array([size_a, size_b])
    zscore, _ = proportions_ztest(counts, nobs, alternative = 'two-sided')

    h0 = stats.norm(loc = 0, scale = 1)
    h1 = stats.norm(loc = zscore, scale = 1)

    x = np.linspace(-5, 6, num = 100)
    threshold = h0.ppf(1 - significance/2)
    mask1 = (x > threshold)
    mask2 = (x < -threshold)
    

    power = np.round(1 - h1.cdf(threshold), 2)

    hypotheses = [h1, h0]
    labels = ['$H_1$ is true', '$H_0$ is true']
    for hypothesis, label in zip(hypotheses, labels):
        y = hypothesis.pdf(x)
        line = plt.plot(x, y, label = label)
        plt.fill_between(x = x[mask1], y1 = 0.0, y2 = y[mask1],
                         alpha = 0.2, color = line[0].get_color())
        plt.fill_between(x = x[mask2], y1 = 0.0, y2 = y[mask2],
                         alpha = 0.2, color = line[0].get_color())
    
    title = 'p1: {}, p2: {}, size1: {}, size2: {}, power: {}'
    plt.title(title.format(prob_a, prob_b, size_a, size_b, power), fontdict={'fontsize' : 15})
    plt.ylabel('Probability')
    plt.xlabel('')
    plt.legend()
    plt.tight_layout()
    plt.show()




