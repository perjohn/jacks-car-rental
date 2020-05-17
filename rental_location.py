class RentalLocation:
    def __init__(self, max_capacity: int, available: int):
        self.max_capacity = max_capacity
        self.available = available

    def transfer_cars(self, nr_of_car_transfers):
        if nr_of_car_transfers < 0:
            if self.available + nr_of_car_transfers < 0:
                raise RuntimeError
            else:
                self.available += nr_of_car_transfers
        else:
            self.available = min(self.max_capacity, self.available + nr_of_car_transfers)

    def __repr__(self):
        return f'RentalLocation(available={self.available})'

    def __eq__(self, other):
        return self.max_capacity == other.max_capacity and self.available == other.available

    def __hash__(self):
        return hash((self.max_capacity, self.available))
