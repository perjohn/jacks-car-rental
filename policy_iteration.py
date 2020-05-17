import matplotlib.pyplot as plt
import numpy as np

from poisson import calculate_poisson

MAX_CARS_AT_LOCATION = 20
MAX_CARS_MOVED = 5
GAMMA = 0.9
TARGET = 0.25

state = {
    'nr_of_cars_location_1': 0,
    'nr_of_cars_location_2': 0
}

values = np.zeros((MAX_CARS_AT_LOCATION + 1, MAX_CARS_AT_LOCATION + 1), dtype=int)
policy = np.zeros((MAX_CARS_AT_LOCATION + 1, MAX_CARS_AT_LOCATION + 1), dtype=int)


# values = np.arange(0, 441).reshape((21, 21))


class JacksCarRentalSolver:
    def __init__(self, max_cars=MAX_CARS_AT_LOCATION):
        self.max_cars = max_cars
        self.transition_probabilities = self.calculate_transition_probabilities()

    def calculate_transition_probabilities(self):
        prob_requests_1 = calculate_poisson(lambda_param=3, max_cars=self.max_cars + 1)
        prob_returns_1 = calculate_poisson(lambda_param=3, max_cars=self.max_cars + 1)
        prob_requests_2 = calculate_poisson(lambda_param=4, max_cars=self.max_cars + 1)
        prob_returns_2 = calculate_poisson(lambda_param=2, max_cars=self.max_cars + 1)
        prob_1 = np.outer(prob_requests_1, prob_returns_1)
        prob_2 = np.outer(prob_requests_2, prob_returns_2)
        return np.multiply.outer(prob_1, prob_2)

    def get_transition_probability(self, requests_1, returns_1, requests_2, returns_2):
        return self.transition_probabilities[requests_1, returns_1, requests_2, returns_2]

    def iterate_policy(self):
        while True:
            max_delta = 0
            for nr_cars_1 in range(self.max_cars + 1):
                for nr_cars_2 in range(self.max_cars + 1):
                    for nr_requests_1 in range(self.max_cars + 1):
                        current_value = values[nr_cars_1, nr_cars_2]
                        nr_requests_1, nr_requests_2, nr_returns_1, nr_returns_2 = get_random_car_requests_returns()
                        cars_to_be_moved = policy[nr_cars_1, nr_cars_2]
    
                        new_value = calculate_new_value(cars_to_be_moved, nr_cars_1, nr_cars_2, nr_requests_1,
                                                        nr_requests_2,
                                                        nr_returns_1, nr_returns_2)
                        values[nr_cars_1, nr_cars_2] = new_value
                        max_delta = max(max_delta,
                                        abs(current_value - new_value) / new_value) if new_value > 0 else new_value
            # draw_figure()
            if max_delta < TARGET:
                print(f'Max delta is {max_delta}')
                break
        pass


def calculate_new_value(cars_to_be_moved, nr_cars_1, nr_cars_2, nr_requests_1, nr_requests_2, nr_returns_1,
                        nr_returns_2):
    reward = -2 * cars_to_be_moved
    nr_cars_1_new_state = nr_cars_1 + nr_returns_1
    nr_cars_2_new_state = nr_cars_2 + nr_returns_2
    if cars_to_be_moved > 0:
        nr_cars_1_new_state += cars_to_be_moved
        nr_cars_2_new_state -= cars_to_be_moved
    else:
        nr_cars_1_new_state -= cars_to_be_moved
        nr_cars_2_new_state += cars_to_be_moved

    nr_cars_1_new_state = 20 if nr_cars_1_new_state > 20 else nr_cars_1_new_state
    nr_cars_2_new_state = 20 if nr_cars_2_new_state > 20 else nr_cars_2_new_state

    value_new_state = values[nr_cars_1_new_state, nr_cars_2_new_state]
    reward += min(nr_requests_1, nr_cars_1_new_state) * 10
    reward += min(nr_requests_2, nr_cars_2_new_state) * 10
    return reward + GAMMA * value_new_state


def get_random_car_requests_returns():
    return np.random.poisson(lam=(3, 4, 3, 2), size=(4,))


def draw_figure():
    fig, ax = plt.subplots()

    min_val, max_val = 0, MAX_CARS_AT_LOCATION + 1
    ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    ax.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)
    for i in range(max_val):
        for j in range(max_val):
            c = values[j, i]
            ax.text(i + 0.5, j + 0.5, str(c), va='center', ha='center')
    # ax.matshow(values, cmap=plt.cm.Blues)

    ax.set_xlim(min_val, max_val)
    ax.set_ylim(min_val, max_val)
    ax.set_xticks(np.arange(max_val))
    ax.set_yticks(np.arange(max_val))
    ax.grid()
    plt.show()
