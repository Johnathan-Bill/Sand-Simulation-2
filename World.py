from typing import List
from Particles import ParticleTypes, Particle, CONSUMABLE_BY_MOSS,LAVA_INTERACTION
from Grid import Grid
from random import choice
import Directions
class World:
        _GRID :Grid
        Particles : List[Particle] = []
        width : int
        height : int
        current_interation = 0
        
        def __init__(self, height : int, width :int) -> None:
                self._GRID = Grid(height,width)
                self.width = width
                self.height = height
                pass
            
         # using the x and y postions add the element to the partcles list and space list   
        def add_particle(self, x:int , y:int, particle_type : type):
            if(self._GRID.space[x][y].NAME == "Void"):
                new_particle : Particle = particle_type(x,y)
                self._GRID.space[x][y] = new_particle
                self.Particles.append(new_particle)
        
        # deletes particle at x and y
        def delete_particle(self, x : int, y : int):
                
                particle = self._GRID.space[x][y]
                if(particle.NAME != "Void"):
                        self.Particles.remove(particle)
                        self._GRID.space[x][y] = ParticleTypes[0](particle.x,particle.y)
                        
        def get_particle(self, x : int, y : int) -> Particle:
                return self._GRID.space[x][y]
                   
        def PhysicsUpdate(self):
                self.current_interation += 1
                if(self.current_interation >1000):
                        self.current_interation = 0
                for particle in self.Particles:
                        if(self.current_interation == particle.last_update): continue
                        
                        if particle.special_interaction:
                                self.particle_interaction(particle)
                                if(not particle in self.Particles):
                                        continue
                        
                        if particle.canFall:
                                if self.particle_can_move_directly_down(particle):
                                        self.swap_particles(particle,self._GRID.space[particle.x][particle.y+1])
                                else:
                                        self.particle_try_move(particle)
                                        
                                
                        elif particle.canRise:
                                if self.particle_can_move_directly_up(particle):
                                        self.swap_particles(particle,self._GRID.space[particle.x][particle.y-1])
                                else:
                                        self.particle_try_move(particle)

                        elif particle.canMultiply:
                                self.multiply_particle(particle)
                        
                        
                        # unmoving particle
                        else:
                                continue
        
        def get_specific_neighbors(self, particle : Particle, interactions : dict):
                neighbors = []
                for direction in particle.DIRECTIONS:
                        if(direction[0] + particle.x < self._GRID.rows and direction[0] + particle.x >= 0 #check x is in the space
                           and direction[1] + particle.y < self._GRID.cols and direction[1] + particle.y >= 0 #check if y is in the space
                           and self._GRID.space[particle.x + direction[0]][particle.y + direction[1]].NAME in interactions.keys() ): 
                               neighbors.append(self._GRID.space[particle.x + direction[0]][particle.y + direction[1]]) 
                return neighbors
        
        
        def replace_particles(self,particle1 : Particle, particle2 : Particle, name1 : str, name2 : str, name3 : str, interactions):
                temp_index1 = -1
                temp_index2 = -1
                for t in range(len(ParticleTypes)):
                        if ParticleTypes[t].NAME == name3:
                                temp_index1 = t
                        if ParticleTypes[t].NAME in interactions.keys():
                                for t2 in range(len(ParticleTypes)):
                                        if ParticleTypes[t2].NAME == interactions[name2]:
                                                temp_index2 = t2
                
                self._GRID.space[particle1.x][particle1.y] = ParticleTypes[temp_index1](particle1.x,particle1.y)
                self._GRID.space[particle2.x][particle2.y] = ParticleTypes[temp_index2](particle2.x,particle2.y)
                
                self._GRID.space[particle1.x][particle1.y].last_update = self.current_interation
                self._GRID.space[particle2.x][particle2.y].last_update = self.current_interation
                
                self.Particles.remove(particle1)
                self.Particles.remove(particle2)
                
                self.Particles.append(self._GRID.space[particle1.x][particle1.y])
                self.Particles.append(self._GRID.space[particle2.x][particle2.y])
               
        def particle_interaction(self,particle : Particle):
                neighbors = []
                match particle.NAME:
                        case "Lava":
                                neighbors = self.get_specific_neighbors(particle,LAVA_INTERACTION)
                                if len(neighbors) < 1:
                                        return
                                rand = choice(neighbors)
                                self.replace_particles(particle, rand, particle.NAME, rand.NAME, "Smoke" , LAVA_INTERACTION)
                                pass
                
                pass
        def multiply_particle(self,particle : Particle):
                match particle.NAME:
                        case "Moss":
                                neighbors = self.get_all_neighbors(particle,CONSUMABLE_BY_MOSS)
                                for n in neighbors:
                                        if not n.change_rate >0:
                                                self.replace_with_moss(n)
                                        else:
                                                n.change_rate -= 1
                        case _:
                                pass
        def get_all_neighbors(self,particle : Particle, interaction_array) -> List[Particle]:
                neighbors = []
                for direction in Directions.GLOBAL_DIRECTIONS.values():
                     if(direction[0] + particle.x < self._GRID.rows and direction[0] + particle.x >= 0 #check x is in the space
                           and direction[1] + particle.y < self._GRID.cols and direction[1] + particle.y >= 0 #check if y is in the space
                           and self._GRID.space[particle.x + direction[0]][particle.y + direction[1]].NAME in interaction_array): # check if it can be consumed
                             neighbors.append(self._GRID.space[particle.x + direction[0]][particle.y + direction[1]]) 
                return neighbors
        def replace_with_moss(self, particle : Particle):
                temp_pointer = particle
                moss_index = -1
                for t in range(len(ParticleTypes)):
                        if ParticleTypes[t].NAME == "Moss":
                                moss_index = t
                                
                self._GRID.space[particle.x][particle.y] = ParticleTypes[moss_index](particle.x,particle.y)
                self._GRID.space[particle.x][particle.y].last_update = self.current_interation
                self.Particles.remove(temp_pointer)
                self.Particles.append(self._GRID.space[particle.x][particle.y])
                
                pass
        def particle_try_move(self,particle : Particle):
                neighbors = self.get_void_neighbors(particle)
                
                
                if(len(neighbors) >= 1):
                        randNeighbor = choice(neighbors)
                        self.swap_particles(particle,randNeighbor)
                        return
                
                neighbors = self.get_neighbors(particle)
                if(len(neighbors) >= 1):
                        randNeighbor = choice(neighbors)
                        self.swap_particles(particle,randNeighbor)
                        return
                
                
                               
        def get_neighbors(self, particle : Particle):
                neighbors = []
                for direction in particle.DIRECTIONS:
                        if(direction[0] + particle.x < self._GRID.rows and direction[0] + particle.x >= 0 #check x is in the space
                           and direction[1] + particle.y < self._GRID.cols and direction[1] + particle.y >= 0 #check if y is in the space
                           and self._GRID.space[particle.x + direction[0]][particle.y + direction[1]].density < particle.density #check if the density is lower
                           and self._GRID.space[particle.x + direction[0]][particle.y + direction[1]].NAME !="Void"): 
                               neighbors.append(self._GRID.space[particle.x + direction[0]][particle.y + direction[1]]) 
                return neighbors
        
        def get_void_neighbors(self, particle : Particle) -> List[Particle]:
                neighbors = []
                for direction in particle.DIRECTIONS:
                        if(direction[0] + particle.x < self._GRID.rows and direction[0] + particle.x >= 0 #check x is in the space
                           and direction[1] + particle.y < self._GRID.cols and direction[1] + particle.y >= 0 #check if y is in the space
                           and self._GRID.space[particle.x + direction[0]][particle.y].NAME == "Void" #check if it can actually move to the left/right logically (needs empty space next to it)
                           and self._GRID.space[particle.x + direction[0]][particle.y + direction[1]].NAME =="Void"): # check if the neighbor is void
                                neighbors.append(self._GRID.space[particle.x + direction[0]][particle.y + direction[1]])
                return neighbors
        
        def particle_can_move_directly_down(self,particle : Particle) -> bool:
                if(particle.y < self._GRID.cols-1 and 
                   (self._GRID.space[particle.x][particle.y+1].NAME == "Void" or self._GRID.space[particle.x][particle.y+1].density < particle.density)):
                        return True
                
                return False
        def particle_can_move_directly_up(self,particle : Particle) -> bool:
                if(particle.y >0 and 
                   (self._GRID.space[particle.x][particle.y-1].NAME == "Void" or self._GRID.space[particle.x][particle.y-1].density < particle.density)):
                        return True
                
                return False
        
        
        def swap_particles(self, particle1: Particle, particle2 : Particle):
                newX = particle2.x
                newY = particle2.y
                self._GRID.space[newX][newY] = particle1
                self._GRID.space[particle1.x][particle1.y] = particle2
                particle2.y = particle1.y
                particle2.x = particle1.x
                particle1.x = newX
                particle1.y = newY
                particle1.last_update = self.current_interation
                
                if(not particle2.canRise):
                        particle2.last_update = self.current_interation
                
        def particle_move(self, particle : Particle, newX : int, newY :int):
                self._GRID.space[newX][newY] = particle
                self._GRID.space[particle.x][particle.y] = ParticleTypes[0](particle.x,particle.y)
                particle.x = particle.x + (newX - particle.x)
                particle.y = particle.y + (newY - particle.y)
        
        def reset(self):
                self._GRID = Grid(self._GRID.cols,self._GRID.rows)
                self.Particles = []