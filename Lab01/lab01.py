
class Weapon:
    def __init__(self, name: str, damage: int):
        self.name = name
        self.damage = damage
        self.description = f"{self.name} (Damage: {self.damage})"
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "damage": self.damage,
            "description": self.description
        }
        

class Armor:
    def __init__(self, name: str, defense: int):
        self.name = name
        self.defense = defense
        self.description = f"{self.name} (Defense: {self.defense})"
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "defense": self.defense,
            "description": self.description
        }


class Player:
    def __init__(self, name: str, health: int, level: int, guild: str, weapon: Weapon, armor: Armor, job: str, id: int):
        self.name = name
        self.health = health
        self.weapon = weapon
        self.armor = armor
        self.guild = guild
        self.job = job
        self.id = id
        self.level = level
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "health": self.health,
            "level": self.level,
            "weapon": self.weapon,
            "armor": self.armor,
            "guild": self.guild,
            "job": self.job
        }
    
    def attack(self):
        pass

class Guild:
    def __init__(self, name: str, members: list[Player], leader: Player):
        self.name = name
        self.leader = leader
        self.members = members
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "leader": self.leader,
            "members": self.members
        }

class GameSystem:
    def __init__(self) -> None:
        self.players: list[Player] = []
        self.guilds: list[Guild] = []
        self.weapons: list[Weapon] = []
        self.armors: list[Armor] = []
    
    def get_player_by_name(self, name: str):
        for player in self.players:
            if player.name == name:
                return player
        return None
    def get_guild_by_name(self, name: str):
        for guild in self.guilds:
            if guild.name == name:
                return guild
        return None

game = GameSystem()

sword = Weapon("Sword", 10)
bow = Weapon("Bow", 15)
axe = Weapon("Axe", 20)

leather_armor = Armor("Leather Armor", 10)
iron_armor = Armor("Iron Armor", 20)
titanium_armor = Armor("Titanium Armor", 30)

player1 = Player("Alexander", 100, 1, "Fallen Angels", sword, leather_armor, "Warrior", 1)
player2 = Player("Striker", 100, 3, "Fallen Angels", bow, iron_armor, "Archer", 2)
player3 = Player("Butcher", 100, 4,  "The Destroyer", axe, titanium_armor, "Berserker", 3)
player4 = Player("Throne", 100, 6, "The Destroyer", sword, leather_armor, "Warrior" ,4)

guild1 = Guild("Fallen Angels", [player1, player2], player1)
guild2 = Guild("The Destroyer", [player3, player4], player3)

game.players.extend([player1, player2, player3, player4])
game.guilds.extend([guild1, guild2])
game.weapons.extend([sword, bow, axe])
game.armors.extend([leather_armor, iron_armor, titanium_armor])

def print_player(game: GameSystem):
    for player in game.players:
        print(f"=== Player {player.id} ===")
        print(f"Name: {player.name}")
        print(f"Level: {player.level}")
        print(f"Health: {player.health}")
        print(f"Guild: {player.guild}")
        print(f"Job: {player.job}")   
        print(f"Weapon: {player.weapon.description}")
        print(f"Armor: {player.armor.description}")
        print("")
        
def print_guild(game: GameSystem):
    for i in game.guilds:
        print(f"=== Guild : {i.name} ===")
        print(f"Leader: {i.leader.name}")
        print("Members:")
        for j in i.members:
            print(f"  - {j.name}")
        print("")
        
def main():
    print("=============================================\n")
    print_player(game)
    print("=============================================\n")
    print_guild(game)

if __name__ == "__main__":
    main()
    