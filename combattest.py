import random
import string

class Weapon:
    def __init__(self, name, damage, cooldown):
        self.name = name
        self.damage = damage
        self.cooldown = cooldown
        self.current_cooldown = 0

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

    def is_alive(self):
        return self.hull > 0

    def take_damage(self, damage):
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

    def regenerate_shields(self):
        self.shields += self.shield_regen

    def attack_target(self, target, weapon):
        damage = weapon.fire()
        target.take_damage(damage)
        print(f"{self.name} attacks {target.name} with {weapon.name} for {damage} damage!")

    def enemy_attack(self, target):
        available_weapons = [weapon for weapon in self.weapons if weapon.is_ready()]
        if available_weapons:
            weapon = random.choice(available_weapons)
            damage = weapon.fire()
            target.take_damage(damage)
            print(f"{self.name} attacks {target.name} for {damage} damage!")

    def tick_weapons(self):
        for weapon in self.weapons:
            weapon.tick()


def generate_ship_name():
    return ''.join(random.choices(string.ascii_uppercase, k=3)) + '-' + str(random.randint(100, 999))


def combat(player_ship, enemy_ship):
    while player_ship.is_alive() and enemy_ship.is_alive():
        print(f"\n{player_ship.name} (Hull: {player_ship.hull}, Armor: {player_ship.armor}, Shields: {player_ship.shields})")
        print(f"{enemy_ship.name} (Hull: {enemy_ship.hull}, Armor: {enemy_ship.armor}, Shields: {enemy_ship.shields})")

        available_weapons = [weapon for weapon in player_ship.weapons if weapon.is_ready()]
        if available_weapons:
            for i, weapon in enumerate(available_weapons):
                print(f"{i + 1}. {weapon.name}")

            while True:
                try:
                    weapon_choice = int(input("Choose your weapon: "))
                    if 1 <= weapon_choice <= len(available_weapons):
                        selected_weapon = available_weapons[weapon_choice - 1]
                        break
                    else:
                        print("Invalid weapon choice.")
                except ValueError:
                    print("Invalid input.")

            player_ship.attack_target(enemy_ship, selected_weapon)
        else:
            print("No weapons available this turn.")


        player_ship.regenerate_shields()
        enemy_ship.regenerate_shields()
        player_ship.tick_weapons()

        if enemy_ship.is_alive():
            enemy_ship.enemy_attack(player_ship)
            enemy_ship.tick_weapons()


    if player_ship.is_alive():
        print(f"\n{player_ship.name} wins!")
    else:
        print(f"\n{enemy_ship.name} wins!")


if __name__ == "__main__":
    player_weapons = [Weapon("Laser Cannon", 10, 0), Weapon("Missile Launcher", 30, 3)]  # Laser can fire every turn, missile every 3 turns
    enemy_weapons = [Weapon("Laser Cannon", 8, 0), Weapon("Missile Launcher", 25, 4)]
    player_ship = Spaceship(generate_ship_name(), 100, 30, 50, player_weapons, 5)
    enemy_ship = Spaceship(generate_ship_name(), 80, 20, 30, enemy_weapons, 3)
    combat(player_ship, enemy_ship)
