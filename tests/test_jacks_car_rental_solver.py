import math

import numpy as np
import pytest

from policy_iteration import JacksCarRentalSolver


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
