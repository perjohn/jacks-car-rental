import numpy as np
from scipy.stats import poisson


def calculate_poisson(lambda_param: int, max_cars: int) -> np.ndarray:
    return poisson.pmf(np.arange(max_cars), lambda_param)
