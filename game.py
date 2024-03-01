from typing import Tuple,List
import pygame
import math as Math
from World import World
from Particles import ParticleTypes
WINDOW_SIZE = (1280,720)
PIXEL_SIZE = 8
FPS = 60
WORLD = World(WINDOW_SIZE[1]/PIXEL_SIZE,WINDOW_SIZE[0]/PIXEL_SIZE)
Current_Selection : int = 1
fpsClock = pygame.time.Clock()
pygame.init()
def main():
    # sets base screen
    global Current_Selection
    pygame.display.set_caption('Sand Simulation  - JBill')
    global SCREEN
    SCREEN = pygame.display.set_mode(WINDOW_SIZE)
    SCREEN.fill((0,0,0))
    
    #basic pygame loop
    running = True
    while running:
        #converts mouse_position to a world postion based of size of the screen and size of the pixels
        mouse_postion = get_mouse_world_position()
        for event in pygame.event.get():
            #runs if the exit buttong is clicked
            if event.type == pygame.QUIT:
                running = False
                # veiws mouse wheel changes
            if event.type == pygame.MOUSEWHEEL:
                if event.y == 1:
                    #if the current selection is the final element in the array reset to sand
                    if(Current_Selection == (len(ParticleTypes)-1)): Current_Selection = 1
                    else: Current_Selection +=1
                if event.y == -1:
                    #if the current selection is sand set to the final element in the array
                    if(Current_Selection -1 <= 0): Current_Selection = len(ParticleTypes)-1
                    else: Current_Selection -=1
            # checks for left mouse click and right mouse click respectively
            if pygame.mouse.get_pressed()[0]:
                Add_Event(mouse_postion)
            if pygame.mouse.get_pressed()[2]:
                Delete_Event(mouse_postion)
                
        WORLD.PhysicsUpdate()
        render()

        fpsClock.tick(FPS)
        
    # gets the position of the world mouse and finds it corresponding array point and adds the current selected
    #particle to the world
def Add_Event(pos : Tuple[int,int]):
    x = Math.floor(pos[0])
    y = Math.floor(pos[1])
    WORLD.AddParticle(Math.floor(x),Math.floor(y),ParticleTypes[Current_Selection])
    #removes the corresponding mouse postion particle from the world
def Delete_Event(pos: Tuple[int,int]):
    x = Math.floor(pos[0])
    y = Math.floor(pos[1])
    WORLD.Delete_Particle(x,y)

# returns the middle value
def clamp(n, smallest, largest) -> int:
    ll: List[int] = [smallest, n, largest]
    ll.sort()
    return ll[1]

#
def get_mouse_world_position() -> Tuple[int, int]:
    window_size = SCREEN.get_size()
    mouse_pos = pygame.mouse.get_pos()
    # Calculate the normalized mouse position in the world for both x and y coordinates
    mouse_x = clamp(int((mouse_pos[0] / window_size[0]) * WORLD.width), 0, WORLD.width - 1)
    mouse_y = clamp(int((mouse_pos[1] / window_size[1]) * WORLD.height), 0, WORLD.height - 1)
    return mouse_x, mouse_y


def render():
    # sets the window caption
    pygame.display.set_caption(f'Sand Simulator | FPS: {int(fpsClock.get_fps())}')
    #sets the surface
    surface = pygame.Surface((WORLD.width, WORLD.height))
    
    #for each particle draw it on the surface as a pixel
    for particle in WORLD.Particles:
        surface.set_at((particle.x,particle.y),particle.COLOR)
    
    #scales the surface so the pixels are n * normal size where n is PIXEL_SIZE
    scaled_surface = pygame.transform.scale(surface, SCREEN.get_size())
    
    #applies it to the screen and updates the render
    SCREEN.blit(scaled_surface,(0,0))
    pygame.display.flip()
    
main()