from itertools import product

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

from rental_location import RentalLocation, NotEnoughCarsException
from transition_probabilities import TransitionProbabilities

MAX_CARS = 20
MAX_CARS_MOVED = 5
TRANSFER_COST = 2
RENTAL_CREDIT = 10
GAMMA = 0.9
VALUE_CHANGE_THRESHOLD = 5
BAD_MOVE_COST = -1000


class JacksCarRentalSolver:
    def __init__(self, max_cars=MAX_CARS):
        self.max_cars = max_cars
        self.values = np.zeros((MAX_CARS + 1, MAX_CARS + 1), dtype=int)
        self.policy = np.zeros((MAX_CARS + 1, MAX_CARS + 1), dtype=int)
        self.trans_prob_req_1 = TransitionProbabilities(lambda_value=3, max_cars=MAX_CARS)
        self.trans_prob_ret_1 = TransitionProbabilities(lambda_value=3, max_cars=MAX_CARS)
        self.trans_prob_req_2 = TransitionProbabilities(lambda_value=4, max_cars=MAX_CARS)
        self.trans_prob_ret_2 = TransitionProbabilities(lambda_value=2, max_cars=MAX_CARS)

    def get_transition_probability(self, requests_1, returns_1, requests_2, returns_2):
        return self.trans_prob_req_1[requests_1] * self.trans_prob_ret_1[returns_1] * self.trans_prob_req_2[
            requests_2] * self.trans_prob_ret_2[returns_2]

    def policy_evaluation(self):
        nr_of_iterations = 1
        values_stable = False
        while not values_stable:
            max_delta = 0

            progress_bar = tqdm(product(range(self.max_cars + 1), range(self.max_cars + 1)),
                                total=(self.max_cars + 1) ** 2)
            for nr_cars_1, nr_cars_2 in progress_bar:
                progress_bar.set_description(
                    f'Policy evaluation iteration {nr_of_iterations}, max delta is {max_delta:.2f}')
                current_value = self.values[nr_cars_1, nr_cars_2]
                location_1 = RentalLocation(MAX_CARS, nr_cars_1)
                location_2 = RentalLocation(MAX_CARS, nr_cars_2)

                new_value = self.calculate_state_value(location_1, location_2)
                self.values[nr_cars_1, nr_cars_2] = new_value
                max_delta = max(max_delta, abs(current_value - new_value))
            if max_delta < VALUE_CHANGE_THRESHOLD:
                print(f'Done! Max delta is {max_delta}')
                draw_figure(self.values)
                values_stable = True
            else:
                nr_of_iterations += 1
                print(f'Not done yet at iteration {nr_of_iterations}. Max delta is {max_delta}')

    def policy_improvement(self):
        policy_stable = True
        progress_bar = tqdm(product(range(self.max_cars + 1), range(self.max_cars + 1)), total=(self.max_cars + 1) ** 2)
        for nr_cars_1, nr_cars_2 in progress_bar:
            progress_bar.set_description(f'Policy improvement: ')
            old_action = self.policy[nr_cars_1, nr_cars_2]
            max_move_1_to_2 = min(nr_cars_1, 5)
            max_move_2_to_1 = -min(nr_cars_2, 5)

            max_action_value = float('-inf')
            new_action = None
            for action in range(max_move_2_to_1, max_move_1_to_2):
                location_1 = RentalLocation(MAX_CARS, nr_cars_1)
                location_2 = RentalLocation(MAX_CARS, nr_cars_2)
                action_value = self.calculate_action_value(action, location_1, location_2)
                if action_value > max_action_value:
                    max_action_value = action_value
                    new_action = action

            if new_action:
                self.policy[nr_cars_1, nr_cars_2] = new_action
            if old_action != new_action:
                policy_stable = False
        draw_figure(self.policy)
        return policy_stable

    def calculate_state_value(self, location_1: RentalLocation, location_2: RentalLocation):
        action = self.policy[location_1.available, location_2.available]
        return self.calculate_action_value(action, location_1, location_2)

    def calculate_action_value(self, action: int, location_1: RentalLocation, location_2: RentalLocation):
        result = -TRANSFER_COST * abs(action)
        try:
            location_1.transfer_cars(-action)
            location_2.transfer_cars(action)
        except NotEnoughCarsException:
            return BAD_MOVE_COST
        for requests_1 in range(self.trans_prob_req_1.start_index, self.trans_prob_req_1.end_index):
            for returns_1 in range(self.trans_prob_ret_1.start_index, self.trans_prob_ret_1.end_index):
                for requests_2 in range(self.trans_prob_req_2.start_index, self.trans_prob_req_2.end_index):
                    for returns_2 in range(self.trans_prob_ret_2.start_index, self.trans_prob_ret_2.end_index):
                        prob = self.get_transition_probability(requests_1, returns_1, requests_2, returns_2)
                        valid_requests_1 = min(location_1.available, requests_1)
                        valid_requests_2 = min(location_2.available, requests_2)
                        reward = (valid_requests_1 + valid_requests_2) * RENTAL_CREDIT
                        available_1 = max(min(location_1.available - valid_requests_1 + returns_1, MAX_CARS), 0)
                        available_2 = max(min(location_2.available - valid_requests_2 + returns_2, MAX_CARS), 0)
                        result += prob * (reward + GAMMA * self.values[available_1, available_2])
        return result


def draw_figure(values):
    fig, ax = plt.subplots()

    min_val, max_val = 0, MAX_CARS + 1
    ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    ax.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)
    for i in range(max_val):
        for j in range(max_val):
            c = values[j, i]
            ax.text(i + 0.5, j + 0.5, str(c), va='center', ha='center')

    ax.set_xlim(min_val, max_val)
    ax.set_ylim(min_val, max_val)
    ax.set_xticks(np.arange(max_val))
    ax.set_yticks(np.arange(max_val))
    ax.grid()
    plt.show()
