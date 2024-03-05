from typing import Tuple,List
import pygame
import math as Math
from World import World
from Particles import ParticleTypes
WINDOW_SIZE = (1280,720)
PIXEL_SIZE = 8
FPS = 60
world = World(WINDOW_SIZE[1]/PIXEL_SIZE,WINDOW_SIZE[0]/PIXEL_SIZE)
current_selection : int = 1
fps_clock = pygame.time.Clock()
pygame.init()
def main():
    # sets base screen
    global current_selection
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
                    if(current_selection == (len(ParticleTypes)-1)): current_selection = 1
                    else: current_selection +=1
                if event.y == -1:
                    #if the current selection is sand set to the final element in the array
                    if(current_selection -1 <= 0): current_selection = len(ParticleTypes)-1
                    else: current_selection -=1
            # checks for left mouse click and right mouse click respectively
            if pygame.mouse.get_pressed()[0]:
                Add_Event(mouse_postion)
            if pygame.mouse.get_pressed()[2]:
                Delete_Event(mouse_postion)
            if(pygame.mouse.get_pressed()[1]):
                Inspect(mouse_postion)
                
        world.PhysicsUpdate()
        render()

        fps_clock.tick(FPS)
        
    # gets the position of the world mouse and finds it corresponding array point and adds the current selected
    #particle to the world
def Add_Event(pos : Tuple[int,int]):
    x = Math.floor(pos[0])
    y = Math.floor(pos[1])
    world.add_particle(Math.floor(x),Math.floor(y),ParticleTypes[current_selection])
    #removes the corresponding mouse postion particle from the world
def Delete_Event(pos: Tuple[int,int]):
    x = Math.floor(pos[0])
    y = Math.floor(pos[1])
    world.delete_particle(x,y)
def Inspect(pos : Tuple[int,int]):
    pass
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
    mouse_x = clamp(int((mouse_pos[0] / window_size[0]) * world.width), 0, world.width - 1)
    mouse_y = clamp(int((mouse_pos[1] / window_size[1]) * world.height), 0, world.height - 1)
    return mouse_x, mouse_y


def render():
    # sets the window caption
    pygame.display.set_caption(f'Sand Simulator | FPS: {int(fps_clock.get_fps())}')

    surface = pygame.Surface((world.width, world.height))
    particle_text = pygame.font.SysFont("times new roman", 15).render(
        f'Selected Particle: {ParticleTypes[current_selection].NAME}', False, (255, 255, 255)
    )

    for particle in world.Particles:
        surface.set_at((particle.x, particle.y), particle.COLOR)

    scaled_surface = pygame.transform.scale(surface, SCREEN.get_size())
    scaled_surface.blit(particle_text, (5, 5))
    SCREEN.blit(scaled_surface, (0, 0))
    pygame.display.flip()
    
main()