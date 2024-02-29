from typing import Tuple,Type,List


class Particle:
    COLOR : Tuple
    NAME : str
    x : int
    y : int
    def __init__(self, color: Tuple, name : str, x : int, y : int) -> None:
        self.COLOR = color
        self.NAME = name
        self.x = x
        self.y = y
        pass
    
    
ParticleTypes: List[Type[Particle]] = []
def add_to_particle_list(particle : Type[Particle]) -> Type[Particle]:
    ParticleTypes.append(particle)
    print(f"Added tile {particle.NAME}")
    return particle

@add_to_particle_list
class Void(Particle):
    NAME = "Void"
    def __init__(self, name: str, x: int, y: int) -> None:
        super().__init__((0,0,0), self.NAME, x, y)
    pass
@add_to_particle_list
class Sand(Particle):
    NAME = "Sand"
    def __init__(self, x: int, y: int) -> None:
        super().__init__((194, 178, 128), self.NAME, x, y)
    pass