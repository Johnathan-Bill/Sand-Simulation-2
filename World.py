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
            
         # using the x and y postions add the element to the partcles list and space list   
        def AddParticle(self, x:int , y:int, particle_type : type):
            if(self._GRID.space[x][y].NAME == "Void"):
                new_particle : Particle = particle_type(x,y)
                self._GRID.space[x][y] = new_particle
                self.Particles.append(new_particle)
        pass
        
        # given a particle check if its neighbors and corners to see if i can move
        def Valid_Directions(self, particle : Particle) -> List[List[int]]:
                valid = []
                # for d in particle.DIRECTIONS:  
                #         if(particle.x + d[0] < self._GRID.rows and particle.y + d[1] < self._GRID.cols 
                #            and particle.x + d[0] >= 0 and particle.y + d[1] >0):
                #                 if(self._GRID.space[particle.x+d[0]][particle.y+d[1]].density < particle.density 
                #                    and self._GRID.space[particle.x+d[0]][particle.y].NAME == "Void"):
                #                         valid.append(d)
                
                for d in particle.DIRECTIONS:
                        if(particle.x + d[0] < self._GRID.rows and particle.y + d[1] < self._GRID.cols 
                            and particle.x + d[0] >= 0 and particle.y + d[1] >=0):
                                if(self._GRID.space[particle.x+d[0]][particle.y+d[1]].density < particle.density
                                        and self._GRID.space[particle.x+d[0]][particle.y].density < particle.density):
                                        valid.append(d)
                        pass
                
                return valid
        #if the particle can fall and not at the bottom of the array and not above any particle that is void move it
        def PhysicsUpdate(self):
                for particle in self.Particles:
                        if((not particle.canFall and not particle.canRise) or particle.updated) : 
                                particle.updated = False
                                continue
                        elif(particle.y+1 == self._GRID.cols or particle.y-1 < 0 and (particle.canFall or particle.canRise)):
                                d = self.Valid_Directions(particle)
                                if(len(d) < 1) : continue
                                r = choice(d)
                                particle.x += r[0]
                                particle.y += r[1]
                                self._GRID.space[particle.x - r[0]][particle.y - r[1]] = ParticleTypes[0](particle.x - r[0],particle.y-r[1])
                                self._GRID.space[particle.x ][particle.y] = particle
                                continue
                        if(self._GRID.space[particle.x][particle.y+1].density < particle.density and self._GRID.space[particle.x][particle.y+1].NAME != "Void" and particle.canFall):
                                self.Swap_Particles(particle,self._GRID.space[particle.x][particle.y+1])
                        elif(self._GRID.space[particle.x][particle.y+1].NAME != "Void" and particle.canFall):
                                d = self.Valid_Directions(particle)
                                if(len(d) < 1) : continue
                                r = choice(d)
                                
                                if(self._GRID.space[particle.x + r[0]][particle.y + r[1]].NAME != "Void"):
                                        if(self.Can_Push_Up(particle.x + r[0],particle.y + r[1])):          
                                                particle.x += r[0]
                                                particle.y += r[1]
                                                self.Push_Up(particle,r)
                                                self._GRID.space[particle.x - r[0]][particle.y - r[1]] = ParticleTypes[0](particle.x - r[0],particle.y-r[1])
                                                self._GRID.space[particle.x ][particle.y] = particle
                                        pass
                                else:
                                        particle.x += r[0]
                                        particle.y += r[1]
                                        self._GRID.space[particle.x - r[0]][particle.y - r[1]] = ParticleTypes[0](particle.x - r[0],particle.y-r[1])
                                        self._GRID.space[particle.x ][particle.y] = particle
                                
                        elif(self._GRID.space[particle.x][particle.y+1].NAME == "Void" and particle.canFall):
                                particle.y += 1
                        # print(d)
                        #replaces the partical current position to a void particle then sets the new postion with the .space
                                self._GRID.space[particle.x][particle.y-1] = ParticleTypes[0](particle.x,particle.y-1)
                                self._GRID.space[particle.x][particle.y] = particle
                        elif(self._GRID.space[particle.x][particle.y-1].NAME != "Void" and particle.canRise):
                                d = self.Valid_Directions(particle)
                                if(len(d) < 1) : continue
                                r = choice(d)
                                
                                particle.x += r[0]
                                particle.y += r[1]
                                self._GRID.space[particle.x - r[0]][particle.y - r[1]] = ParticleTypes[0](particle.x - r[0],particle.y-r[1])
                                self._GRID.space[particle.x ][particle.y] = particle
                                pass
                        elif(self._GRID.space[particle.x][particle.y-1].NAME == "Void" and particle.canRise):
                                particle.y -= 1
                                self._GRID.space[particle.x][particle.y+1] = ParticleTypes[0](particle.x,particle.y+1)
                                self._GRID.space[particle.x][particle.y] = particle
                        
                        
                pass
        # deletes particle at x and y
        def Delete_Particle(self, x : int, y : int):
                
                particle = self._GRID.space[x][y]
                if(particle.NAME != "Void"):
                        self.Particles.remove(particle)
                        self._GRID.space[x][y] = ParticleTypes[0](particle.x,particle.y)
        def Swap_Particles(self, particle1: Particle, particle2 : Particle):
                self._GRID.space[particle1.x][particle1.y+1] = particle1
                self._GRID.space[particle1.x][particle1.y] = particle2
                particle2.updated = True
                particle1.y +=1
                particle2.y -=1
                pass
        def Can_Push_Up(self, x,y) -> bool:
                for i in range(y,1,-1):
                        if(self._GRID.space[x][i].density > self._GRID.space[x][y].density):
                                return False
                        if(self._GRID.space[x][i].NAME == "Void"):
                                return True
                # if(self._GRID.space[x][0].NAME != "Void"):
                #         return False
                
                
                return True
        def Push_Up(self,particle:Particle,r):
                first_non_void = -1
                for i in range(particle.y,1,-1):
                        if(self._GRID.space[particle.x+r[0]][i].NAME != "Void"):
                                first_non_void = i
                                break;
                i = first_non_void          
                while(i < particle.y+r[1]):
                        particle2 =  self._GRID.space[particle.x][i]
                        particle2.y -=1
                        self._GRID.space[particle2.x][particle2.y] = particle2
                        if(particle.NAME == "Stone"):
                                print("wtf")
                        
                        i +=1