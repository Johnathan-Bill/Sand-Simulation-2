from typing import List
from Particles import ParticleTypes, Particle
from Grid import Grid
from random import choice
class World:
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
        
        def Valid_Directions(self, particle : Particle) -> List[List[int]]:
                valid = []
                for d in particle.DIRECTIONS:  
                        if(particle.x + d[0] < self._GRID.rows and particle.y + d[1] < self._GRID.cols 
                           and particle.x + d[0] >= 0 and particle.y + d[1] >0):
                                if(self._GRID.space[particle.x+d[0]][particle.y+d[1]].NAME == "Void" 
                                   and self._GRID.space[particle.x+d[0]][particle.y].NAME == "Void"):
                                        valid.append(d)
                                
                return valid
        def PhysicsUpdate(self):
                for particle in self.Particles:
                        if(not particle.canFall or particle.y+1 == self._GRID.cols) : continue
                        if(self._GRID.space[particle.x][particle.y+1].NAME != "Void"):
                                d = self.Valid_Directions(particle)
                                if(len(d) < 1) : continue
                                r = choice(d)
                                particle.x += r[0]
                                particle.y += r[1]
                                self._GRID.space[particle.x - r[0]][particle.y - r[1]] = ParticleTypes[0](particle.x - r[0],particle.y-r[1])
                                self._GRID.space[particle.x ][particle.y] = particle
                        else:
                                particle.y += 1
                        # print(d)
                        #replaces the partical current position to a void particle then sets the new postion with the .space
                                self._GRID.space[particle.x][particle.y-1] = ParticleTypes[0](particle.x,particle.y-1)
                                self._GRID.space[particle.x][particle.y] = particle
                        
                        
                        
                pass
        def Delete_Particle(self, x : int, y : int):
                
                particle = self._GRID.space[x][y]
                if(particle.NAME != "Void"):
                        self.Particles.remove(particle)
                        self._GRID.space[x][y] = ParticleTypes[0](particle.x,particle.y)
        