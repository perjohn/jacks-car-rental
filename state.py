from rental_location import RentalLocation


class State:
    def __init__(self, rental_location_1: RentalLocation, rental_location_2: RentalLocation):
        self.rental_location_1 = rental_location_1
        self.rental_location_2 = rental_location_2

    def __eq__(self, other):
        return self.rental_location_1 == other.rental_location_1 and self.rental_location_2 == other.rental_location_2

    def __hash__(self):
        return hash((self.rental_location_1, self.rental_location_2))


def state_iterator(max_capacity: int):
    for nr_cars_1 in range(max_capacity + 1):
        rental_location_1 = RentalLocation(max_capacity=max_capacity, available=nr_cars_1)
        for nr_cars_2 in range(max_capacity + 1):
            rental_location_2 = RentalLocation(max_capacity=max_capacity, available=nr_cars_2)
            yield State(rental_location_1, rental_location_2)
