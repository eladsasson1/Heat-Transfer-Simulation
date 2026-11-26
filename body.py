# Class representing a physical body capable of receiving or releasing heat
class Body:
    # Constructor to validate inputs and initialize instance variables
    def __init__(self, mass, specific_heat, temperature):
        if mass <= 0:
            raise ValueError("Mass must be greater than zero.")
        if specific_heat <= 0:
            raise ValueError("Specific heat must be greater than zero.")
        if temperature < 0:
            raise ValueError("Temperature must be greater than or equal to zero.")

        self.mass = mass
        self.specific_heat = specific_heat
        self.temperature = temperature

    # Method to add or release heat and update the body's temperature
    def add_heat(self, heat):
        delta_temperature = heat / (self.mass * self.specific_heat)
        new_temperature = self.temperature + delta_temperature
        self.temperature = new_temperature
        return self.temperature


# Test section that runs only when this file is executed directly
if __name__ == "__main__":
    # Create a Body object with mass 100 kg, specific heat 0.15 J/(kg·°C), and temperature 200°C
    body = Body(mass=100, specific_heat=0.15, temperature=200)

    # Add 20 Joules of heat and print the returned temperature
    temp_after_adding_heat = body.add_heat(20)
    print(temp_after_adding_heat)

    # Add -40 Joules of heat to the same object and print the returned temperature
    temp_after_removing_heat = body.add_heat(-40)
    print(temp_after_removing_heat)
