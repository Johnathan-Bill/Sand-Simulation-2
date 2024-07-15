from typing import Tuple,Type,List
from Directions import GLOBAL_DIRECTIONS
class Particle:
    COLOR : Tuple
    NAME : str
    x : int
    y : int
    canFall : bool
    density : int
    last_update : int
    canRise : bool
    canMultiply : bool
    canDissipate : bool
    canGenerateParticle : bool
    generatesLeftover : bool
    DIRECTIONS: List[List[int]]
    change_rate : int
    special_interaction : bool
    def __init__(self, color: Tuple, name : str, x : int, y : int, density : int = -1, canFall : bool = False, dir : List[List[int]] = [], 
                 canRise: bool = False, canMultiply : bool = False, change_rate : int = -1, special_interaction : bool = False, 
                 canDissipate : bool = False, canGenerateParticle : bool = False, generatesLeftover : bool = False)  -> None:
        self.COLOR = color
        self.NAME = name
        self.x = x
        self.y = y
        self.canFall = canFall
        self.canRise = canRise
        self.canMultiply = canMultiply
        self.DIRECTIONS = dir
        self.density = density
        self.last_update = 0
        self.change_rate = change_rate
        self.special_interaction= special_interaction
        self.canDissipate = canDissipate
        self.canGenerateParticle = canGenerateParticle;
        self.generatesLeftover = generatesLeftover;
CONSUMABLE_BY_MOSS = ["Stone","Wood"]
CONSUMABLE_BY_FIRE= ["Moss","Wood"]
LAVA_INTERACTION = {"Water" : "Obsidian", "Wood": "Void", "Moss" : "Void"}
WATER_INTERACTION = {"Lava" : "Stone", "Fire": "Void"}
PARTICLE_GENERATIONS = {"Fire" : ["Smoke",2]}
PARTICLE_LEFTOVERS = {"Fire" : ["Ash",100], "Steam" : ["Water", 30]}
ParticleTypes: List[Type[Particle]] = []
def add_to_particle_list(particle : Type[Particle]) -> Type[Particle]:
    ParticleTypes.append(particle)
    print(f"Added {particle.NAME}")
    return particle

@add_to_particle_list
class Void(Particle):
    NAME = "Void"
    def __init__(self, x: int, y: int) -> None:
        super().__init__((0,0,0), self.NAME, x, y,-1)
@add_to_particle_list
class Sand(Particle):
    NAME = "Sand"
    
    def __init__(self, x: int, y: int) -> None:
        super().__init__((194, 178, 128), self.NAME, x, y,7,True,
                         (GLOBAL_DIRECTIONS["Down"],GLOBAL_DIRECTIONS["Down_Left"],GLOBAL_DIRECTIONS["Down_Right"]))
@add_to_particle_list
class Ash(Particle):
    NAME = "Ash"
    
    def __init__(self, x: int, y: int) -> None:
        super().__init__((106,108,109), self.NAME, x, y,7,True,
                         (GLOBAL_DIRECTIONS["Down"],GLOBAL_DIRECTIONS["Down_Left"],GLOBAL_DIRECTIONS["Down_Right"]))
@add_to_particle_list
class Stone(Particle):
    NAME = "Stone"
    def __init__(self, x: int, y: int) -> None:
        super().__init__((136, 140, 141), self.NAME, x, y,999, change_rate=45)
@add_to_particle_list
class Wood(Particle):
    NAME = "Wood"
    def __init__(self, x: int, y: int) -> None:
        super().__init__((161, 102, 47), self.NAME, x, y,999, change_rate=30)
        
@add_to_particle_list
class Obsidian(Particle):
    NAME = "Obsidian"
    def __init__(self, x: int, y: int) -> None:
        super().__init__((113,98,122), self.NAME, x, y,999, change_rate=30)
        
@add_to_particle_list
class Water(Particle):
    NAME = "Water"
    def __init__(self, x: int, y: int) -> None:
        super().__init__((28,163,236), self.NAME, x, y,5,True,
                         (GLOBAL_DIRECTIONS["Left"],GLOBAL_DIRECTIONS["Right"],GLOBAL_DIRECTIONS["Down"],GLOBAL_DIRECTIONS["Down_Left"],GLOBAL_DIRECTIONS["Down_Right"]),
                         special_interaction=True)
@add_to_particle_list
class Lava(Particle):
    NAME = "Lava"
    def __init__(self, x: int, y: int) -> None:
        super().__init__((255,37,0), self.NAME, x, y,4,True,
                         (GLOBAL_DIRECTIONS["Left"],GLOBAL_DIRECTIONS["Right"],GLOBAL_DIRECTIONS["Down"],GLOBAL_DIRECTIONS["Down_Left"],GLOBAL_DIRECTIONS["Down_Right"]),
                         special_interaction=True)
@add_to_particle_list
class Oil(Particle):
    NAME = "Oil"
    def __init__(self, x: int, y: int) -> None:
        super().__init__((219,207,92), self.NAME, x, y,3,True,
                         (GLOBAL_DIRECTIONS["Left"],GLOBAL_DIRECTIONS["Right"],GLOBAL_DIRECTIONS["Down"],GLOBAL_DIRECTIONS["Down_Left"],GLOBAL_DIRECTIONS["Down_Right"]))
@add_to_particle_list
class Smoke(Particle):
    NAME = "Smoke"
    def __init__(self, x: int, y: int) -> None:
        super().__init__((115, 130, 118), self.NAME, x, y,2, canFall= False,canRise = True, 
                         dir=(GLOBAL_DIRECTIONS["Left"],GLOBAL_DIRECTIONS["Right"],GLOBAL_DIRECTIONS["Up"],GLOBAL_DIRECTIONS["Up_Left"],GLOBAL_DIRECTIONS["Up_Right"]),canDissipate=True,change_rate=240)
@add_to_particle_list
class Steam(Particle):
    NAME = "Steam"
    def __init__(self, x: int, y: int) -> None:
        super().__init__((163, 221, 248), self.NAME, x, y,3, canFall= False,canRise = True, dir=(GLOBAL_DIRECTIONS["Left"],GLOBAL_DIRECTIONS["Right"],GLOBAL_DIRECTIONS["Up"],GLOBAL_DIRECTIONS["Up_Left"],GLOBAL_DIRECTIONS["Up_Right"]),
                         canDissipate=True, change_rate=180, generatesLeftover=True)
              
@add_to_particle_list
class Gas(Particle):
    NAME = "Gas"
    def __init__(self, x: int, y: int) -> None:
        super().__init__((131, 143, 51), self.NAME, x, y,4, canFall= False,canRise = True, dir=(GLOBAL_DIRECTIONS["Left"],GLOBAL_DIRECTIONS["Right"],GLOBAL_DIRECTIONS["Up"],GLOBAL_DIRECTIONS["Up_Left"],GLOBAL_DIRECTIONS["Up_Right"]),
                         canDissipate=True, change_rate=120)

@add_to_particle_list
class Moss(Particle):
    NAME = "Moss"
    def __init__(self, x: int, y: int) -> None:
        super().__init__((56,118,29), self.NAME, x, y,999,canMultiply=True,change_rate=60)
@add_to_particle_list
class Fire(Particle):
    NAME = "Fire"
    def __init__(self, x: int, y: int) -> None:
        super().__init__((170, 66, 3), self.NAME, x, y,999,canMultiply=True,special_interaction=True, change_rate=90, canDissipate=True, canGenerateParticle=True, generatesLeftover= False)