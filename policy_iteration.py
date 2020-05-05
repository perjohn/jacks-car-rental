import matplotlib.pyplot as plt
import numpy as np

MAX_CARS_AT_LOCATION = 20
MAX_CARS_MOVED = 5
GAMMA = 0.9

state = {
    'nr_of_cars_location_1': 0,
    'nr_of_cars_location_2': 0
}

values = np.zeros((MAX_CARS_AT_LOCATION + 1, MAX_CARS_AT_LOCATION + 1), dtype=int)
policy = np.zeros((MAX_CARS_AT_LOCATION + 1, MAX_CARS_AT_LOCATION + 1), dtype=int)


def iterate_policy():
    for nr_cars_1 in range(MAX_CARS_AT_LOCATION + 1):
        for nr_cars_2 in range(MAX_CARS_AT_LOCATION + 1):
            nr_requests_1, nr_requests_2, nr_returns_1, nr_returns_2 = get_random_car_requests_returns()
            cars_to_be_moved = policy[nr_cars_1, nr_cars_2]

            new_value = calculate_new_value(cars_to_be_moved, nr_cars_1, nr_cars_2, nr_requests_1, nr_requests_2,
                                            nr_returns_1, nr_returns_2)
            values[nr_cars_1, nr_cars_2] = new_value
    draw_figure()
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
            ax.text(i + 0.5, max_val - j - 0.5, str(c), va='center', ha='center')
    # ax.matshow(values, cmap=plt.cm.Blues)

    ax.set_xlim(min_val, max_val)
    ax.set_ylim(min_val, max_val)
    ax.set_xticks(np.arange(max_val))
    ax.set_yticks(np.arange(max_val))
    ax.grid()
    plt.show()
