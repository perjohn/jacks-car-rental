import numpy as np

from poisson import calculate_poisson


class TransitionProbabilities:
    epsilon = 0.001
    start_index = 0
    end_index = 0

    def __init__(self, lambda_value: int, max_cars: int, epsilon=0.001):
        self.epsilon = epsilon
        self.potential_probabilities = calculate_poisson(lambda_value, max_cars)
        self.start_index = self._find_start_index()
        self.end_index = self._find_end_index()

    def __getitem__(self, item):
        assert item >= self.start_index
        assert item <= self.end_index
        return self.potential_probabilities[item]

    def _find_start_index(self):
        start_index = 0
        for value in np.nditer(self.potential_probabilities):
            if value > self.epsilon:
                break
            else:
                start_index += 1
        return start_index

    def _find_end_index(self):
        self.end_index = self.start_index
        if self.end_index < len(self.potential_probabilities):
            for value in np.nditer(self.potential_probabilities[self.start_index:]):
                if value < self.epsilon:
                    break
                else:
                    self.end_index += 1
        return self.end_index
