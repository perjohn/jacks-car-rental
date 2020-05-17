from rental_location import RentalLocation
from state import state_iterator, State


def test_state_iterator():
    states = []
    for state in state_iterator(max_capacity=1):
        states.append(state)

    assert len(states) == 4
    assert states[0].rental_location_1.available == 0
    assert states[0].rental_location_2.available == 0
    assert states[1].rental_location_1.available == 0
    assert states[1].rental_location_2.available == 1


def test_equals():
    rental_location_1 = RentalLocation(max_capacity=10, available=5)
    rental_location_2 = RentalLocation(max_capacity=10, available=5)
    state_1 = State(rental_location_1, rental_location_2)
    assert state_1 == state_1

    state_2 = State(rental_location_1, rental_location_2)
    assert state_1 == state_2

    rental_location_3 = RentalLocation(max_capacity=10, available=6)
    state_3 = State(rental_location_1, rental_location_3)
    assert state_1 != state_3

    rental_location_4 = RentalLocation(max_capacity=11, available=5)
    state_4 = State(rental_location_1, rental_location_4)
    assert state_1 != state_4
