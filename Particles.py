from typing import Tuple,Type,List
from Directions import GLOBAL_DIRECTIONS
class Particle:
    COLOR : Tuple
    NAME : str
    x : int
    y : int
    canFall : bool
    density : int
    updated : bool
    canRise : bool
    DIRECTIONS: List[List[int]]
    def __init__(self, color: Tuple, name : str, x : int, y : int, density : int = -1, canFall : bool = False, dir : List[List[int]] = [], canRise: bool = False) -> None:
        self.COLOR = color
        self.NAME = name
        self.x = x
        self.y = y
        self.canFall = canFall
        self.canRise = canRise
        self.DIRECTIONS = dir
        self.density = density
        self.updated = False

    
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
class Stone(Particle):
    NAME = "Stone"
    def __init__(self, x: int, y: int) -> None:
        super().__init__((136, 140, 141), self.NAME, x, y,999)
@add_to_particle_list
class Wood(Particle):
    NAME = "Wood"
    def __init__(self, x: int, y: int) -> None:
        super().__init__((161, 102, 47), self.NAME, x, y,999)
        
@add_to_particle_list
class Water(Particle):
    NAME = "Water"
    def __init__(self, x: int, y: int) -> None:
        super().__init__((28,163,236), self.NAME, x, y,5,True,
                         (GLOBAL_DIRECTIONS["Left"],GLOBAL_DIRECTIONS["Right"],GLOBAL_DIRECTIONS["Down"],GLOBAL_DIRECTIONS["Down_Left"],GLOBAL_DIRECTIONS["Down_Right"]))
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
                         dir=(GLOBAL_DIRECTIONS["Left"],GLOBAL_DIRECTIONS["Right"],GLOBAL_DIRECTIONS["Up"],GLOBAL_DIRECTIONS["Up_Left"],GLOBAL_DIRECTIONS["Up_Right"]))
@add_to_particle_list
class Smoke(Particle):
    NAME = "Steam"
    def __init__(self, x: int, y: int) -> None:
        super().__init__((163, 221, 248), self.NAME, x, y,3, canFall= False,canRise = True, dir=(GLOBAL_DIRECTIONS["Left"],GLOBAL_DIRECTIONS["Right"],GLOBAL_DIRECTIONS["Up"],GLOBAL_DIRECTIONS["Up_Left"],GLOBAL_DIRECTIONS["Up_Right"]))