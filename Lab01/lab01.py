class Weapon:
    def __init__(self, name: str, damage: int):
        self.__name = name
        self.__damage = damage

    @property
    def name(self):
        return self.__name

    @property
    def damage(self):
        return self.__damage

    def __str__(self):
        return f"{self.name} (Damage: {self.damage})"


class Armor:
    def __init__(self, name: str, defense: int):
        self.__name = name
        self.__defense = defense

    @property
    def name(self):
        return self.__name

    @property
    def defense(self):
        return self.__defense

    def __str__(self):
        return f"{self.name} (Defense: {self.defense})"


class Player:
    def __init__(self, name: str, health: int, level: int, guild: str, weapon: Weapon, armor: Armor, job: str, uid: int):
        self.__name = name
        self.__health = health
        self.__level = level
        self.__guild = guild
        self.__weapon = weapon
        self.__armor = armor
        self.__job = job
        self.__id = uid

    @property
    def name(self):
        return self.__name

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, value: int):
        self.__health = max(0, value)  # Ensure health is not negative.

    @property
    def weapon(self):
        return self.__weapon

    @weapon.setter
    def weapon(self, value: Weapon):
        self.__weapon = value

    @property
    def armor(self):
        return self.__armor

    @armor.setter
    def armor(self, value: Armor):
        self.__armor = value

    @property
    def guild(self):
        return self.__guild

    @guild.setter
    def guild(self, value: str):
        self.__guild = value

    @property
    def id(self):
        return self.__id

    @property
    def level(self):
        return self.__level

    def level_up(self, levels: int = 1):
        self.__level += levels

    def __str__(self):
        return (
            f"=== Player {self.id} ===\n"
            f"  Name: {self.name}\n"
            f"  Level: {self.level}\n"
            f"  Health: {self.health}\n"
            f"  Guild: {self.guild}\n"
            f"  Weapon: {self.weapon}\n"
            f"  Armor: {self.armor}"
        )


class Guild:
    def __init__(self, name: str, leader: Player):
        self.__name = name
        self.__leader = leader
        self.__members = [leader]

    def add_member(self, player: Player):
        if player not in self.__members:
            self.__members.append(player)

    def remove_member(self, player: Player):
        if player in self.__members:
            self.__members.remove(player)

    def set_leader(self, player: Player):
        if player in self.__members:
            self.__leader = player

    @property
    def name(self):
        return self.__name

    @property
    def leader(self):
        return self.__leader

    @property
    def members(self):
        return self.__members

    def __str__(self):
        members_list = "\n- ".join([member.name for member in self.__members])
        return ( f"=== {self.name} ===\n"
                 f"Leader: {self.leader.name} 👑\n"
                 f"Members:\n- {members_list}")


class GameSystem:
    def __init__(self):
        self.players = []
        self.guilds = []
        self.weapons = []
        self.armors = []

    def get_player_by_name(self, name: str):
        return next((player for player in self.players if player.name == name), None)

    def get_guild_by_name(self, name: str):
        return next((guild for guild in self.guilds if guild.name == name), None)

    def display_players(self):
        for player in self.players:
            print(player)
            print("-" * 20)

    def display_guilds(self):
        for guild in self.guilds:
            print(guild)
            print("=" * 30)


# Initialize game
game = GameSystem()

# Sample data
sword = Weapon("Sword", 10)
bow = Weapon("Bow", 15)
axe = Weapon("Axe", 20)

leather_armor = Armor("Leather Armor", 10)
iron_armor = Armor("Iron Armor", 20)
titanium_armor = Armor("Titanium Armor", 30)

player1 = Player("Alexander", 100, 1, "Fallen Angels", sword, leather_armor, "Warrior", 1)
player2 = Player("Striker", 100, 3, "Fallen Angels", bow, iron_armor, "Archer", 2)
player3 = Player("Butcher", 100, 4, "The Destroyer", axe, titanium_armor, "Berserker", 3)
player4 = Player("Throne", 100, 6, "The Destroyer", sword, leather_armor, "Warrior", 4)

guild1 = Guild("Fallen Angels", player1)
guild2 = Guild("The Destroyer", player3)

guild1.add_member(player2)
guild2.add_member(player4)

game.players.extend([player1, player2, player3, player4])
game.guilds.extend([guild1, guild2])
game.weapons.extend([sword, bow, axe])
game.armors.extend([leather_armor, iron_armor, titanium_armor])

# Main function
def main():
    print("Players:")
    game.display_players()
    print("\nGuilds:")
    game.display_guilds()


if __name__ == "__main__":
    main()
