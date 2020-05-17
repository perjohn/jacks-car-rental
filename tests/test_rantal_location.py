import pytest

from rental_location import RentalLocation


def test_rental_location():
    rental_location = RentalLocation(max_capacity=10, available=5)
    rental_location.transfer_cars(2)
    assert rental_location.available == 7


def test_rental_location_negative():
    rental_location = RentalLocation(max_capacity=10, available=5)
    rental_location.transfer_cars(-2)
    assert rental_location.available == 3


def test_rental_location_exceeding_max_capacity():
    rental_location = RentalLocation(max_capacity=10, available=5)
    rental_location.transfer_cars(7)
    assert rental_location.available == 10


def test_rental_location_less_than_zero():
    rental_location = RentalLocation(max_capacity=10, available=5)
    with pytest.raises(RuntimeError):
        rental_location.transfer_cars(-7)


def test_equals():
    rental_location_1 = RentalLocation(max_capacity=10, available=5)
    assert rental_location_1 == rental_location_1

    rental_location_2 = RentalLocation(max_capacity=10, available=5)
    assert rental_location_1 == rental_location_2

    rental_location_3 = RentalLocation(max_capacity=10, available=6)
    assert rental_location_1 != rental_location_3

    rental_location_4 = RentalLocation(max_capacity=11, available=5)
    assert rental_location_1 != rental_location_4
