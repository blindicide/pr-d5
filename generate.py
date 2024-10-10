import random
import string
import pickle

def generate_systems(num_systems):
    systems = []
    for _ in range(num_systems):
        system_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4)) + '-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        num_planets = random.randint(1, 10)
        planets = []
        stations = [] # Initialize stations list for the system
        for i in range(num_planets):
            planet_name = system_name + ' ' + to_roman(i + 1)
            num_moons = random.randint(0, 5)
            moons = []
            for j in range(num_moons):
                moon_name = planet_name + chr(ord('a') + j)
                moon_size = round(random.uniform(1000, 5000), 1)
                moon = {
                    'name': moon_name,
                    'size': moon_size
                }
                moons.append(moon)
                # Add at most one station per moon
                if random.choice([True, False]): # 50% chance of a station
                    station_name = moon_name + " Station"
                    stations.append(station_name)


            planet_size = round(random.uniform(5000, 50000), 1)
            planet = {
                'name': planet_name,
                'size': planet_size,
                'habitable': random.choice([True, False]),
                'moons': moons
            }
            planets.append(planet)

        # Ensure at least one station and at most five stations per system
        num_additional_stations = random.randint(1,5) - len(stations) # Number of stations needed
        for k in range(num_additional_stations):
            if len(stations) < 5: # Only add if there's space
                station_name = system_name + f" Station {k+1}"
                stations.append(station_name)

        system = {
            'name': system_name,
            'planets': planets,
            'stations': stations, # Add stations to system data
            'routes': [],
            'coords': generate_coordinates(systems)
        }
        systems.append(system)
    return systems


def generate_coordinates(systems):
    while True:
        x = random.uniform(0, 250)
        y = random.uniform(0, 250)
        z = random.uniform(0, 250)

        valid_coords = True
        for system in systems:
            try:
                if distance((x, y, z), system['coords']) < 5:
                    valid_coords = False
                    break
            except KeyError:
                pass


        if valid_coords:
            return (x, y, z)


def distance(coords1, coords2):
    return ((coords1[0] - coords2[0])**2 + (coords1[1] - coords2[1])**2 + (coords1[2] - coords2[2])**2)**0.5



def connect_systems(systems):
    num_systems = len(systems)
    for i in range(num_systems):
        for j in range(i + 1, num_systems):
            if distance(systems[i]['coords'], systems[j]['coords']) < 50:
                systems[i]['routes'].append(systems[j]['name'])
                systems[j]['routes'].append(systems[i]['name'])


def print_unconnected_systems(systems):
    unconnected = [system['name'] for system in systems if not system['routes']]
    if unconnected:
        print("Unconnected systems:", ', '.join(unconnected))
    else:
        print("All systems are connected.")



def to_roman(num):
    roman_map = { 1: 'I', 4: 'IV', 5: 'V', 9: 'IX', 10: 'X', 40: 'XL', 50: 'L', 90: 'XC', 100: 'C', 400: 'XD', 500: 'D', 900: 'CM', 1000: 'M'}

    result = ""
    for value, numeral in sorted(roman_map.items(), reverse=True):
        while num >= value:
            result += numeral
            num -= value
    return result


if __name__ == "__main__":
    num_systems_to_generate = 150  # Example: Generate 5 systems
    generated_systems = generate_systems(num_systems_to_generate)
    connect_systems(generated_systems)
    print_unconnected_systems(generated_systems)

    with open('database.pk', 'wb') as f:
        pickle.dump(generated_systems, f)
