import math

import numpy as np
import pytest

from policy_iteration import JacksCarRentalSolver


def test_calculate_transition_probabilities():
    car_rental_solver = JacksCarRentalSolver(max_cars=1)
    transition_probs = car_rental_solver.transition_probabilities
    assert transition_probs.shape == (2, 2, 2, 2)
    assert transition_probs[0, 0, 0, 0] == pytest.approx(math.exp(-3) * math.exp(-3) * math.exp(-4) * math.exp(-2))
    assert transition_probs[1, 0, 0, 0] == pytest.approx(3 * math.exp(-3) * math.exp(-3) * math.exp(-4) * math.exp(-2))
    assert transition_probs[0, 1, 0, 0] == pytest.approx(math.exp(-3) * 3 * math.exp(-3) * math.exp(-4) * math.exp(-2))
    assert transition_probs[0, 0, 1, 0] == pytest.approx(math.exp(-3) * math.exp(-3) * 4 * math.exp(-4) * math.exp(-2))
    assert transition_probs[0, 0, 0, 1] == pytest.approx(math.exp(-3) * math.exp(-3) * math.exp(-4) * 2 * math.exp(-2))
    assert transition_probs[1, 1, 1, 1] == pytest.approx(
        3 * math.exp(-3) * 3 * math.exp(-3) * 4 * math.exp(-4) * 2 * math.exp(-2))


def test_get_transition_probability():
    car_rental_solver = JacksCarRentalSolver(max_cars=1)
    assert car_rental_solver.get_transition_probability(
        requests_1=0, returns_1=0, requests_2=0, returns_2=0) == pytest.approx(
        math.exp(-3) * math.exp(-3) * math.exp(-4) * math.exp(-2))
    assert car_rental_solver.get_transition_probability(
        requests_1=1, returns_1=0, requests_2=0, returns_2=0) == pytest.approx(
        3 * math.exp(-3) * math.exp(-3) * math.exp(-4) * math.exp(-2))
    assert car_rental_solver.get_transition_probability(
        requests_1=1, returns_1=0, requests_2=0, returns_2=1) == pytest.approx(
        3 * math.exp(-3) * math.exp(-3) * math.exp(-4) * 2 * math.exp(-2))


def test_calculate_transition_probabilities_sums_approx_to_one_for_large_number_of_max_cars():
    car_rental_solver = JacksCarRentalSolver(max_cars=20)
    assert car_rental_solver.transition_probabilities.shape == (21, 21, 21, 21)
    assert np.sum(car_rental_solver.transition_probabilities) == pytest.approx(1)
