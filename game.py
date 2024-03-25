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
inspect = False
pause = False
pygame.init()
def main():
    # sets base screen
    global current_selection
    pygame.display.set_caption('Sand Simulation  - JBill')
    global SCREEN,pause
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
            
            if(event.type == pygame.KEYUP):
                if(event.key == pygame.K_c):
                    world.reset()
                elif(event.key == pygame.K_p):
                    pause = not pause
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
                add_particle_event(mouse_postion)
            if pygame.mouse.get_pressed()[2]:
                delete_particle_event(mouse_postion)
            if(pygame.mouse.get_pressed()[1]):
                enable_inspect()
        if(not pause):        
            world.PhysicsUpdate()
        render()

        fps_clock.tick(FPS)
        
    # gets the position of the world mouse and finds it corresponding array point and adds the current selected
    #particle to the world
def add_particle_event(pos : Tuple[int,int]):
    x = Math.floor(pos[0])
    y = Math.floor(pos[1])
    world.add_particle(Math.floor(x),Math.floor(y),ParticleTypes[current_selection])
    #removes the corresponding mouse postion particle from the world
def delete_particle_event(pos: Tuple[int,int]):
    x = Math.floor(pos[0])
    y = Math.floor(pos[1])
    world.delete_particle(x,y)
    
    
def enable_inspect():
    global inspect
    
    inspect = not inspect
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


def get_opposite_side(mouse_postion) -> List[int]:
    x = 0
    y = 0
    x_offset = 15
    y_offset = 30
    if mouse_postion[0] >= WINDOW_SIZE[0]/2:
        x = x_offset * -1
    else: x = x_offset
    
    if mouse_postion[1] >= WINDOW_SIZE[1]/2:
        y = y_offset * -1
    else: y = y_offset 
    
    
    
    return x,y 

def render():
    # sets the window caption
    pygame.display.set_caption(f'Sand Simulator | FPS: {int(fps_clock.get_fps())}')

    surface = pygame.Surface((world.width, world.height))
    particle_text = pygame.font.SysFont("times new roman", 15).render(
        f'Selected Particle: {ParticleTypes[current_selection].NAME}', False, (255, 255, 255)
    )
    inspect_text  = pygame.font.SysFont("times new roman", 15).render(
        f'Inspect: {"Enabled" if inspect else "Disabled"}', False, (255, 255, 255)
        
    )
    pause_label  = pygame.font.SysFont("times new roman", 15).render(
        f'{"Paused" if pause else ""}', False, (255, 255, 255)
        
    )
    clear_text  = pygame.font.SysFont("times new roman", 15).render(
        f'Press C to clear the world', False, (255, 255, 255)
    )
    pause_text  = pygame.font.SysFont("times new roman", 15).render(
        f'Press P to pause physics', False, (255, 255, 255)
    )
    left_click_text  = pygame.font.SysFont("times new roman", 15).render(
        f'Left Click to place particle', False, (255, 255, 255)
    )
    right_click_text  = pygame.font.SysFont("times new roman", 15).render(
        f'Right Click to delete particle', False, (255, 255, 255)
    )
    scroll_click_text  = pygame.font.SysFont("times new roman", 15).render(
        f'Click Scroll Wheel to enable Inspect', False, (255, 255, 255)
    )
    scroll_cycle_text  = pygame.font.SysFont("times new roman", 15).render(
        f'Use Scroll wheel to cycle through particles', False, (255, 255, 255)
    )
    

    for particle in world.Particles:
        surface.set_at((particle.x, particle.y), particle.COLOR)

    scaled_surface = pygame.transform.scale(surface, SCREEN.get_size())
    
    if inspect:
        mouse_position = pygame.mouse.get_pos()
        global_mouse_position = get_mouse_world_position()
        coords = get_opposite_side(mouse_position)
        particle = world.get_particle(global_mouse_position[0],global_mouse_position[1])
        if particle.NAME != "Void":
            inspect_text_name  = pygame.font.SysFont("times new roman", 13).render(
                f'{particle.NAME}', False, (255, 255, 255))
            
            inspect_text_coords  = pygame.font.SysFont("times new roman", 13).render(
                f'{particle.x},{particle.y}', False, (255, 255, 255))
        
            scaled_surface.blit(inspect_text_name, (mouse_position[0] + coords[0], mouse_position[1] + coords[1]))
            scaled_surface.blit(inspect_text_coords, (mouse_position[0] + coords[0], mouse_position[1] + coords[1]  + 18))
            
            
    scaled_surface.blit(particle_text, (5, 5))
    scaled_surface.blit(inspect_text, (5, 25))
    scaled_surface.blit(pause_label, (5, 45))
    scaled_surface.blit(left_click_text, (WINDOW_SIZE[0] - left_click_text.get_width() - 10, 5))
    scaled_surface.blit(right_click_text, (WINDOW_SIZE[0] - right_click_text.get_width() - 10, 25))
    scaled_surface.blit(scroll_cycle_text, (WINDOW_SIZE[0] - scroll_cycle_text.get_width() - 10, 65))
    scaled_surface.blit(scroll_click_text, (WINDOW_SIZE[0] - scroll_click_text.get_width() - 10, 45))
    scaled_surface.blit(clear_text, (WINDOW_SIZE[0] - clear_text.get_width() - 10, 85))
    scaled_surface.blit(pause_text, (WINDOW_SIZE[0] - pause_text.get_width() - 10, 105))
    SCREEN.blit(scaled_surface, (0, 0))
    pygame.display.flip()

main()