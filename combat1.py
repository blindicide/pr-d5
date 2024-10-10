import random
import string

class Weapon:
    def __init__(self, name, damage, damage_type, cooldown, range):
        self.name = name
        self.damage = damage
        self.damage_type = damage_type
        self.cooldown = cooldown
        self.current_cooldown = 0
        self.range = range

    def is_ready(self):
        return self.current_cooldown == 0

    def fire(self):
        self.current_cooldown = self.cooldown
        return random.randint(self.damage // 2, self.damage)

    def tick(self):
        if self.current_cooldown > 0:
            self.current_cooldown -= 1


class Spaceship:
    def __init__(self, name, hull, armor, shields, weapons, shield_regen):
        self.name = name
        self.hull = hull
        self.armor = armor
        self.shields = shields
        self.weapons = weapons
        self.shield_regen = shield_regen
        self.em_resistance = random.uniform(0, 0.5)
        self.explosive_resistance = random.uniform(0, 0.5)
        self.hardened = False
        self.base_em_resistance = self.em_resistance
        self.base_explosive_resistance = self.explosive_resistance

    def is_alive(self):
        return self.hull > 0

    def take_damage(self, damage, damage_type):
        if damage_type == "EM":
            damage *= (1 - self.em_resistance)
        elif damage_type == "Explosive":
            damage *= (1 - self.explosive_resistance)

        damage = int(damage)

        if self.shields > 0:
            self.shields -= damage
            if self.shields < 0:
                damage = -self.shields
                self.shields = 0
                if self.armor > 0:
                    self.armor -= damage
                    if self.armor < 0:
                        self.hull += self.armor
                        self.armor = 0
                else:
                    self.hull -= damage
        elif self.armor > 0:
            self.armor -= damage
            if self.armor < 0:
                self.hull += self.armor
                self.armor = 0
        else:
            self.hull -= damage

        return damage

    def regenerate_shields(self):
        self.shields += self.shield_regen

    def attack_target(self, target, weapon, distance):
        damage = weapon.fire()
        if distance > weapon.range:
            print(f"{self.name} fired {weapon.name}, but it was out of range!")
            return
        damage_taken = target.take_damage(damage, weapon.damage_type)
        print(f"{self.name} attacks {target.name} with {weapon.name} for {damage_taken} damage!")

    def enemy_attack(self, target, distance):
        available_weapons = [weapon for weapon in self.weapons if weapon.is_ready() and distance <= weapon.range]
        if available_weapons:
            weapon = random.choice(available_weapons)
            damage = weapon.fire()
            damage_taken = target.take_damage(damage, weapon.damage_type)
            print(f"{self.name} attacks {target.name} with {weapon.name} for {damage_taken} damage!")


    def harden_shields(self):
        self.em_resistance *= 0.5
        self.explosive_resistance *= 0.5
        if self.em_resistance > 1:
            self.em_resistance = 1
        if self.explosive_resistance > 1:
            self.explosive_resistance = 1
        self.hardened = True
        print(f"{self.name} hardened their shields!")

    def unharden_shields(self):
        self.em_resistance = self.base_em_resistance
        self.explosive_resistance = self.base_explosive_resistance
        self.hardened = False

    def tick_weapons(self):
        for weapon in self.weapons:
            weapon.tick()


def generate_ship_name():
    return ''.join(random.choices(string.ascii_uppercase, k=3)) + '-' + str(random.randint(100, 999))


def combat(player_ship, enemy_ship):
    distance = 20 # Starting distance
    while player_ship.is_alive() and enemy_ship.is_alive():

        print(f"\nDistance: {distance} km")
        print(f"{player_ship.name} (Hull: {int(player_ship.hull)}, Armor: {int(player_ship.armor)}, Shields: {int(player_ship.shields)}, EM Resistance: {player_ship.em_resistance:.0%}, Explosive Resistance: {player_ship.explosive_resistance:.0%})")
        print(f"{enemy_ship.name} (Hull: {int(enemy_ship.hull)}, Armor: {int(enemy_ship.armor)}, Shields: {int(enemy_ship.shields)})")

        available_weapons = [weapon for weapon in player_ship.weapons if weapon.is_ready()]
        actions = ["Harden Shields", "Approach (1 km)", "Retreat (1 km)"]
        if available_weapons:
            for i, weapon in enumerate(available_weapons):
                print(f"{i + 1}. {weapon.name}")
            for i, action in enumerate(actions):
                print(f"{len(available_weapons) + i + 1}. {action}")

            while True:
                try:
                    action_choice = int(input("Choose action: "))
                    if 1 <= action_choice <= len(available_weapons):
                        selected_weapon = available_weapons[action_choice - 1]
                        player_ship.attack_target(enemy_ship, selected_weapon, distance)
                        break
                    elif action_choice == len(available_weapons) + 1:
                        player_ship.harden_shields()
                        print(f"{player_ship.name} (Hull: {int(player_ship.hull)}, Armor: {int(player_ship.armor)}, Shields: {int(player_ship.shields)}, EM Resistance: {player_ship.em_resistance:.0%}, Explosive Resistance: {player_ship.explosive_resistance:.0%})")
                        break
                    elif action_choice == len(available_weapons) + 2:
                        distance -= 1
                        print(f"{player_ship.name} approached. New distance: {distance} km")
                        break
                    elif action_choice == len(available_weapons) + 3:
                        distance += 1
                        print(f"{player_ship.name} retreated. New distance: {distance} km")
                        break

                    else:
                        print("Invalid action choice.")
                except ValueError:
                    print("Invalid input.")

        else:
            print("No weapons available this turn.")

        player_ship.regenerate_shields()
        enemy_ship.regenerate_shields()
        player_ship.tick_weapons()

        if enemy_ship.is_alive():
            # Basic AI
            if enemy_ship.shields < 100 and not enemy_ship.hardened:
                enemy_ship.harden_shields()
            elif any(weapon.is_ready() for weapon in enemy_ship.weapons if weapon.damage_type == "Explosive" and distance <= weapon.range) and random.random() < 0.5:
                enemy_ship.enemy_attack(player_ship, distance)
            elif all(weapon.range < distance for weapon in enemy_ship.weapons if weapon.is_ready()) and distance > 0:
                distance -= 1
                print(f"{enemy_ship.name} approached. New distance: {distance} km")
            elif any(weapon.is_ready() for weapon in enemy_ship.weapons if weapon.damage_type == "EM" and distance <= weapon.range):
                enemy_ship.enemy_attack(player_ship, distance)

            else:
                available_weapons = [weapon for weapon in enemy_ship.weapons if weapon.is_ready() and distance <= weapon.range]
                if available_weapons:
                    enemy_ship.enemy_attack(player_ship, distance)
            enemy_ship.tick_weapons()

        if player_ship.hardened:
            player_ship.unharden_shields()
        if enemy_ship.hardened:
            enemy_ship.unharden_shields()


    if player_ship.is_alive():
        print(f"\n{player_ship.name} wins!")
    else:
        print(f"\n{enemy_ship.name} wins!")


if __name__ == "__main__":
    player_weapons = [Weapon("Laser Cannon", 100, "EM", 0, 10), Weapon("Missile Launcher", 300, "Explosive", 3, 50)]
    enemy_weapons = [Weapon("Laser Cannon", 80, "EM", 0, 10), Weapon("Missile Launcher", 250, "Explosive", 4, 50)]
    player_ship = Spaceship(generate_ship_name(), 1000, 300, 500, player_weapons, 50)
    enemy_ship = Spaceship(generate_ship_name(), 800, 200, 300, enemy_weapons, 30)
    combat(player_ship, enemy_ship)
