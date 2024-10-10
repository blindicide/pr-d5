import pickle
from random import randint

def load_database(filename="database.pk"):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def display_system_info(system):
    print(f"System: {system['name']}")
    print("Planets:")
    for planet in system['planets']:
        print(f"  {planet['name']} (Size: {planet['size']:.1f}, Habitable: {planet['habitable']})")
        for moon in planet['moons']:
            print(f"    Moon: {moon['name']} (Size: {moon['size']:.1f})")
    print("Stations:")
    for station in system['stations']:
        print(f"  {station}")
    print("Connections:")
    for route in system['routes']:
        print(f"  {route}")

def main():
    database = load_database()
    mk = randint(10, 50)
    current_system = database[mk]  # Start in a random system
    print(f"Current system: {current_system['name']}") # Only display system name at launch

    while True:
        command = input("Enter command (travel/info/exit): ").lower()
        if command == "travel":
            destination = input("Enter destination system: ")
            if destination in current_system['routes']:
                current_system = next((s for s in database if s['name'] == destination), None)
                print(f"Current system: {current_system['name']}") # Display system name after travel
            else:
                print("Invalid destination. Not connected to current system.")
        elif command == "info":
            display_system_info(current_system) # Display detailed info on command
        elif command == "exit":
            break
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
