from typing import List
from Particles import ParticleTypes, Particle
from Grid import Grid
class World:
        DIRECTIONS = {
                "Left":(-1,0),
                "Still" :(0,0),
                "Right":(1,0),
                "Up_Left":(-1,-1),
                "Up":(-1,0),
                "Up_Right":(-1,1),
                "Down_Left":(1,-1),
                "Down":(1,0),
                "Down_Right":(1,1)
    }
        _GRID :Grid
        Particles : List[Particle] = []
        width : int
        height : int
        def __init__(self, height : int, width :int) -> None:
                self._GRID = Grid(height,width)
                self.width = width
                self.height = height
                pass
            
            
        def AddParticle(self, x:int , y:int, particle_type : type):
            if(self._GRID.space[x][y].NAME == "Void"):
                new_particle : Particle = particle_type(x,y)
                self._GRID.space[x][y] = new_particle
                self.Particles.append(new_particle)
        pass
        
        def PhysicsUpdate(self):
                for particle in self.Particles:
                        if(not particle.canFall or particle.y+1 == self._GRID.cols or self._GRID.space[particle.x][particle.y+1].NAME != "Void") : continue
                        particle.y += 1
                        
                        #replaces the partical current position to a void particle then sets the new postion with the .space
                        self._GRID.space[particle.x][particle.y-1] = ParticleTypes[0](particle.x,particle.y-1)
                        self._GRID.space[particle.x][particle.y] = particle
                        
                pass
        def Delete_Particle(self, x : int, y : int):
                
                particle = self._GRID.space[x][y]
                if(particle.NAME != "Void"):
                        self.Particles.remove(particle)
                        self._GRID.space[x][y] = ParticleTypes[0](particle.x,particle.y)