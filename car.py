class Car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
        self.odometer_reading = 0

    def get_descriptive_name(self):
        long_name = f"{self.year} {self.make} {self.model}"
        return long_name.title()
    
    def read_odometer(self):
        print(f"Esse carro rodou {self.odometer_reading} mi.")

    def update_odometer(self, miles):
        self.odometer_reading = miles

    def increment_odometer(self, miles):
        self.odometer_reading += miles

    