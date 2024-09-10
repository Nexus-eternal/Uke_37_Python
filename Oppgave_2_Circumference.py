# Import block
from math import pi

# Variables
radius_of_earth = 6371000

# Define calculating function
def callculate_circumference(radius):
    result = 2*pi*radius                # Calculate circumference
    return int(result)                  # Return result of calculation

# Call print function to check if everything works
print(f"Circumferense of the Earth is ca. {callculate_circumference(radius_of_earth)}m.")