import unittest

import numpy as np


def brownian_motion(T=1, N=100, mu=0.1, sigma=0.1, S0=20):
    dt = float(T) / N
    t = np.linspace(0, T, N)
    W = np.random.standard_normal(size=N)
    W = np.cumsum(W) * np.sqrt(dt)  ### standard brownian motion ###
    X = (mu - 0.5 * sigma**2) * t + sigma * W
    S = S0 * np.exp(X)  ### geometric brownian motion ###
    return S


class TestLearnDiffusion(unittest.TestCase):
    def test_brownian_motion_length(self):
        # Check if the returned time series has the right length
        self.assertEqual(len(brownian_motion(T=1, N=100)), 100)

    def test_brownian_motion_start_value(self):
        # Check if the time series starts with the right value
        self.assertEqual(brownian_motion(T=1, N=100, S0=20)[0], 20)


if __name__ == "__main__":
    unittest.main()
