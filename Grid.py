from typing import List
from Particles import ParticleTypes, Particle
import math as m
class Grid:
    rows : int
    cols : int
 
    Previous_Grid : List[List[Particle | None]]
    space : List[List[Particle | None]]
    
    def __init__(self,height : int ,width : int) -> None:
        
        self.rows = m.floor(width)
        self.cols = m.floor(height)
        
        self.space = [[ParticleTypes[0] for i in range(self.cols)] for j in range(self.rows)]
        
    
        