from typing import Tuple,Type,List
from Directions import GLOBAL_DIRECTIONS
class Particle:
    COLOR : Tuple
    NAME : str
    x : int
    y : int
    canFall : bool
    DIRECTIONS: List[List[int]]
    def __init__(self, color: Tuple, name : str, x : int, y : int, canFall : bool = False, dir : List[List[int]] = [] ) -> None:
        self.COLOR = color
        self.NAME = name
        self.x = x
        self.y = y
        self.canFall = canFall
        self.DIRECTIONS = dir

    
ParticleTypes: List[Type[Particle]] = []
def add_to_particle_list(particle : Type[Particle]) -> Type[Particle]:
    ParticleTypes.append(particle)
    print(f"Added {particle.NAME}")
    return particle

@add_to_particle_list
class Void(Particle):
    NAME = "Void"
    def __init__(self, x: int, y: int) -> None:
        super().__init__((0,0,0), self.NAME, x, y)
@add_to_particle_list
class Sand(Particle):
    NAME = "Sand"
    
    def __init__(self, x: int, y: int) -> None:
        super().__init__((194, 178, 128), self.NAME, x, y,True,(GLOBAL_DIRECTIONS["Down"],GLOBAL_DIRECTIONS["Down_Left"],GLOBAL_DIRECTIONS["Down_Right"]))
@add_to_particle_list
class Stone(Particle):
    NAME = "Stone"
    def __init__(self, x: int, y: int) -> None:
        super().__init__((136, 140, 141), self.NAME, x, y)
@add_to_particle_list
class Wood(Particle):
    NAME = "Wood"
    def __init__(self, x: int, y: int) -> None:
        super().__init__((161, 102, 47), self.NAME, x, y)