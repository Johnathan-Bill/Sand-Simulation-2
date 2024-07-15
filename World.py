from typing import List
from Particles import  CONSUMABLE_BY_FIRE, CONSUMABLE_BY_ICE, ICE_INTERACTION, PARTICLE_GENERATIONS, PARTICLE_LEFTOVERS, ParticleTypes, Particle, CONSUMABLE_BY_MOSS,LAVA_INTERACTION, WATER_INTERACTION
from Grid import Grid
from random import choice
from multipledispatch import dispatch
import random
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
        
        
        @dispatch(int,int)
        # deletes particle at x and y
        def delete_particle(self, x : int, y : int):
                
                particle = self._GRID.space[x][y]
                if(particle.NAME != "Void"):
                        self.Particles.remove(particle)
                        self._GRID.space[x][y] = ParticleTypes[0](particle.x,particle.y)
        
        @dispatch(Particle) #deletes specific particle                
        def delete_particle(self, particle : Particle):
                if(particle.NAME != "Void"):
                        self.Particles.remove(particle)
                        self._GRID.space[particle.x][particle.y] = ParticleTypes[0](particle.x,particle.y)
        
        #replaces specified particles
        @dispatch(Particle, str)
        def replace_particle(self, particle : Particle, name : str):
                #sets temp x and y variables
                x = particle.x
                y = particle.y
                replace_index = 0;
                #finds what the particle type it should become
                for t in range(len(ParticleTypes)):
                        if ParticleTypes[t].NAME == name:
                                replace_index = t
                if(particle.NAME != "Void"):
                        self.Particles.remove(particle)
                        self._GRID.space[x][y] = ParticleTypes[0](particle.x,particle.y)
                        self.add_particle(x,y,ParticleTypes[replace_index])
        
        def replace_with_leftover(self, particle : Particle, name : str):
                #sets temp x and y variables
                x = particle.x
                y = particle.y
                replace_index = 0;
                #finds what the particle type it should become
                for t in range(len(ParticleTypes)):
                        if ParticleTypes[t].NAME == name:
                                replace_index = t
                                
                #if the particle is not void remove it and set it to void then add the particle
                if(particle.NAME != "Void"):
                        self.Particles.remove(particle)
                        self._GRID.space[x][y] = ParticleTypes[0](particle.x,particle.y)
                        if(random.randint(0,100) <= PARTICLE_LEFTOVERS[particle.NAME][1]): 
                                self.add_particle(x,y,ParticleTypes[replace_index])
         
         #gets particle at x and y               
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
                        elif particle.canMoveDiagnoal:
                                self.particle_move_diagnoal(particle)

                        if particle.canMultiply:
                                self.multiply_particle(particle)
                        if(particle.canDissipate):
                                self.dissipate_particle(particle)
                                pass
                        if(particle.canGenerateParticle):
                                self.generateParticle(particle)
                                pass
                        
                        # unmoving particle
                        else:
                                continue
        @dispatch(Particle,dict)
        def get_specific_neighbors(self, particle : Particle, interactions : dict):
                neighbors = []
                for direction in Directions.GLOBAL_DIRECTIONS.values():
                        if(direction[0] + particle.x < self._GRID.rows and direction[0] + particle.x >= 0 #check x is in the space
                           and direction[1] + particle.y < self._GRID.cols and direction[1] + particle.y >= 0 #check if y is in the space
                           and self._GRID.space[particle.x + direction[0]][particle.y + direction[1]].NAME in interactions.keys() ): 
                               neighbors.append(self._GRID.space[particle.x + direction[0]][particle.y + direction[1]]) 
                return neighbors
        @dispatch(int,int)
        def get_specific_neighbors(self,x,y) -> Particle:
                if(x < self._GRID.rows and x >= 0 #check x is in the space
                        and y < self._GRID.cols and y >= 0 ): #check if y is in the space ): 
                               return self._GRID.space[x][y]
                return None;
        @dispatch(Particle, Particle, str, str, str, dict)
        def replace_particles(self,particle1 : Particle, particle2 : Particle, name1 : str, name2 : str, name3 : str, interactions): # replaces particles
                
                #index for what particle is generated (index 1 passed in as a literal index2 is what the particle is going to become once it is changed)
                temp_index1 = -1
                temp_index2 = -1
                for t in range(len(ParticleTypes)):
                        if ParticleTypes[t].NAME == name3:
                                temp_index1 = t
                        if ParticleTypes[t].NAME in interactions.keys():
                                for t2 in range(len(ParticleTypes)):
                                        if ParticleTypes[t2].NAME == interactions[name2]:
                                                temp_index2 = t2
                
                self._GRID.space[particle1.x][particle1.y] = ParticleTypes[temp_index1](particle1.x,particle1.y) # sets the particle at the proper location to the emitted particle
                self._GRID.space[particle2.x][particle2.y] = ParticleTypes[temp_index2](particle2.x,particle2.y) # sets the particle being changed to the result particle
                
                #sets interation
                self._GRID.space[particle1.x][particle1.y].last_update = self.current_interation
                self._GRID.space[particle2.x][particle2.y].last_update = self.current_interation
                
                #removes old particles
                self.Particles.remove(particle1)
                self.Particles.remove(particle2)
                #appends new ones
                self.Particles.append(self._GRID.space[particle1.x][particle1.y])
                self.Particles.append(self._GRID.space[particle2.x][particle2.y])
                
                
        def generateParticle(self,particle: Particle): # generates particles based on particle passed in (random chance)
                        rand = random.randint(0,100)
                        neighbor = self.get_specific_neighbors(particle.x, particle.y-1)
                        Generated_index = -1
                        if (neighbor != None and neighbor.NAME == "Void" and rand < PARTICLE_GENERATIONS[particle.NAME][1]): # only runs if valid space above it
                                for t in range(len(ParticleTypes)):
                                        if ParticleTypes[t].NAME == PARTICLE_GENERATIONS[particle.NAME][0]:
                                                Generated_index = t
                                self.add_particle(neighbor.x,neighbor.y,ParticleTypes[Generated_index])
                                
                        pass
                   
        def particle_interaction(self,particle : Particle): # determines specific interactions
                neighbors = []
                match particle.NAME:
                        case "Lava":
                                neighbors = self.get_specific_neighbors(particle,LAVA_INTERACTION) # finds all neighbors with lava interactions
                                if len(neighbors) < 1:
                                        return
                                rand = choice(neighbors)
                                self.replace_particles(particle, rand, particle.NAME, rand.NAME, "Smoke" , LAVA_INTERACTION) # replaces them with the replacement particle and generates smoke
                        case "Water":
                                neighbors = self.get_specific_neighbors(particle,WATER_INTERACTION) # finds all neighbors with water interactions
                                if len(neighbors) < 1:
                                        return
                                rand = choice(neighbors)
                                self.replace_particles(particle, rand, particle.NAME, rand.NAME, "Steam" , WATER_INTERACTION) # replaces them with the replacement particle and generates steam
                                
                        case "Ice":
                                
                                neighbors = self.get_specific_neighbors(particle,ICE_INTERACTION) # finds all neighbors with ice interactions
                                if len(neighbors) < 1:
                                        return
                                rand = choice(neighbors)
                                if(rand.NAME not in CONSUMABLE_BY_ICE): # checks if the block is consumable if it isnt it needs to multiply
                                        self.replace_particles(particle, rand, particle.NAME, rand.NAME, "Void" , ICE_INTERACTION)
                                else:
                                        self.multiply_particle(particle)
                                pass
                
                pass
        def multiply_particle(self,particle : Particle): # runs for every particle that can multiply
                match particle.NAME:
                        case "Moss":
                                neighbors = self.get_all_neighbors(particle,list(CONSUMABLE_BY_MOSS.keys())) # finds all neighbors that are consumed by moss
                                for n in neighbors:
                                        if not n.change_rate >0:
                                                self.replace_particle(n,"Moss")
                                        else:
                                                n.change_rate -= 1
                        case "Fire":
                                neighbors = self.get_all_neighbors(particle,list(CONSUMABLE_BY_FIRE.keys())) # finds all neighbors that are consumed by fire
                                for n in neighbors:
                                        
                                        if(CONSUMABLE_BY_FIRE[n.NAME]): # if a particle is guarnteed to catch fire do so (wont leave any leftovers)
                                                self.replace_with_fire(n)
                                        elif not n.change_rate >0:
                                                
                                                
                                                if(random.randint(1,5) == 1): # random chance to catch fire
                                                        self.replace_with_fire(n)
                                                else: n.change_rate = 5
                                        else:
                                                n.change_rate -= 1
                        case "Ice":
                                neighbors = self.get_all_neighbors(particle,list(CONSUMABLE_BY_ICE.keys())) # finds all neighbors that are consumed by ice
                                for n in neighbors:
                                        if not n.change_rate >0:
                                                self.replace_particle(n,"Ice")
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
        
        def replace_with_fire(self, particle : Particle): # replaces flamable particles with fire and creates smoke above it (if possible)
                temp_pointer = particle
                fire_index = -1
                smoke_index = -1
                for t in range(len(ParticleTypes)): # finds fire and smoke within the particle type list
                        if ParticleTypes[t].NAME == "Fire":
                                fire_index = t
                        if ParticleTypes[t].NAME == "Smoke":
                                smoke_index = t
                # sets particle at flamable particle location to fire and determines if it should generate a leftover block later (if the not statement on line 254 is true dont leave anything behind)                
                self._GRID.space[particle.x][particle.y] = ParticleTypes[fire_index](particle.x,particle.y)
                self._GRID.space[particle.x][particle.y].generatesLeftover = not CONSUMABLE_BY_FIRE[particle.NAME]
                self._GRID.space[particle.x][particle.y].last_update = self.current_interation
                self.Particles.remove(temp_pointer) # removes flamable particle and adds new fire
                self.Particles.append(self._GRID.space[particle.x][particle.y])
                
                neighbor = self.get_specific_neighbors(particle.x, particle.y-1) #generates smoke if possible (if there is space directly above)
                if (neighbor != None and neighbor.NAME == "Void"):
                        self.add_particle(neighbor.x,neighbor.y,ParticleTypes[smoke_index])
                        
                pass
        
        
        def dissipate_particle(self, particle : Particle): # determines if a particle should dissipate (delete itself) and leave behind a new block
                if(particle.change_rate <=0):
                        
                        
                        if(random.randint(1,5) ==1):
                                if(particle.generatesLeftover):
                                        self.replace_with_leftover(particle,PARTICLE_LEFTOVERS[particle.NAME][0])
                                else:
                                        self.delete_particle(particle)
                else:
                        particle.change_rate -=1
                        
        def particle_try_move(self,particle : Particle): #handles none ONLY horizontal movement
                neighbors = self.get_void_neighbors(particle) # gets all the neighbors that are void
                
                
                if(len(neighbors) >= 1): #choses random direction and moves to it
                        randNeighbor = choice(neighbors)
                        self.swap_particles(particle,randNeighbor) #moves particle in new direction 
                        return
                
                neighbors = self.get_neighbors(particle) #gets all neighbors of particle if there was no void neighbors
                if(len(neighbors) >= 1):
                        randNeighbor = choice(neighbors)
                        self.swap_particles(particle,randNeighbor)
                        return
                
        def particle_move_diagnoal(self, particle : Particle):
                
                

                #checks if there is a block horizontal to it and reverses direction if so
                neighbor = self.get_specific_neighbors(particle.x + particle.DIRECTIONS[0][0], particle.y)
                if(neighbor is None or neighbor.NAME != "Void"):
                        particle.DIRECTIONS = ((particle.DIRECTIONS[0][0]  *-1, particle.DIRECTIONS[0][1]),)
                        
                #checks if there is a block vertical to it and reverses direction if so
                neighbor = self.get_specific_neighbors(particle.x, particle.y  + particle.DIRECTIONS[0][1])
                if(neighbor is None or neighbor.NAME != "Void"):
                        particle.DIRECTIONS = ((particle.DIRECTIONS[0][0], particle.DIRECTIONS[0][1]  *-1),)
                
                #checks if there is a block diagnoal to it and reverses direction if so      
                neighbor = self.get_specific_neighbors(particle.x + particle.DIRECTIONS[0][0], particle.y +  particle.DIRECTIONS[0][1])
                if(neighbor is None or neighbor.NAME != "Void"):
                        particle.DIRECTIONS = ((particle.DIRECTIONS[0][0]  *-1, particle.DIRECTIONS[0][1] *-1),)
                #prevents movement if it is some how surronded by nothing (borders of screen. this is a stop gap)
                if(neighbor is not None):
                        self.particle_try_move(particle)
                pass        
                               
        def get_neighbors(self, particle : Particle):
                neighbors = []
                for direction in particle.DIRECTIONS:
                        if(direction[0] + particle.x < self._GRID.rows and direction[0] + particle.x >= 0 #check x is in the space
                           and direction[1] + particle.y < self._GRID.cols and direction[1] + particle.y >= 0 #check if y is in the space
                           and ((self._GRID.space[particle.x + direction[0]][particle.y + direction[1]].density < particle.density) or particle == -1 )#check if the density is lower
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
                #checks if the particle can move down into a void space or if needs to swap if it is higher density
                if(particle.y < self._GRID.cols-1 and 
                   (self._GRID.space[particle.x][particle.y+1].NAME == "Void" or self._GRID.space[particle.x][particle.y+1].density < particle.density)):
                        return True
                
                return False
        
        def particle_can_move_directly_up(self,particle : Particle) -> bool:
                #checks if the particle can move up into a void space or if needs to swap if it is higher density
                if(particle.y >0 and 
                   (self._GRID.space[particle.x][particle.y-1].NAME == "Void" or self._GRID.space[particle.x][particle.y-1].density < particle.density)):
                        return True
                
                return False
        
        
        def swap_particles(self, particle1: Particle, particle2 : Particle):
                #sets the new x and y of particle 1
                newX = particle2.x
                newY = particle2.y
                
                #swaps the two particles wihin _GRID.space
                self._GRID.space[newX][newY] = particle1
                self._GRID.space[particle1.x][particle1.y] = particle2
                
                #swaps the particles x and y values so the are accurate
                particle2.y = particle1.y
                particle2.x = particle1.x
                particle1.x = newX
                particle1.y = newY
                particle1.last_update = self.current_interation
                
                if(not particle2.canRise):
                        particle2.last_update = self.current_interation
                
        def particle_move(self, particle : Particle, newX : int, newY :int):
                #moves the particle to the new positions
                self._GRID.space[newX][newY] = particle
                self._GRID.space[particle.x][particle.y] = ParticleTypes[0](particle.x,particle.y)
                particle.x = particle.x + (newX - particle.x)
                particle.y = particle.y + (newY - particle.y)
        
        def reset(self):
                self._GRID = Grid(self._GRID.cols,self._GRID.rows)
                self.Particles = []