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
    pygame.display.set_caption('Sand Simulation  - JBill')
    global SCREEN
    SCREEN = pygame.display.set_mode(WINDOW_SIZE)
    SCREEN.fill((0,0,0))
    
    running = True
    while running:
        mouse_postion = get_mouse_world_position()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if pygame.mouse.get_pressed()[0]:
                Click_Event(mouse_postion)
        render()
        fpsClock.tick(FPS)
        
        
def Click_Event(pos : Tuple[int,int]):
    x = Math.floor(pos[0])
    y = Math.floor(pos[1])
    WORLD.AddParticle(Math.floor(x),Math.floor(y),ParticleTypes[Current_Selection])



def clamp(n, smallest, largest) -> int:
    ll: List[int] = [smallest, n, largest]
    ll.sort()
    return ll[1]
def get_mouse_world_position() -> Tuple[int, int]:
    window_size = SCREEN.get_size()
    mouse_pos = pygame.mouse.get_pos()
    mouse_x = clamp(int((mouse_pos[0] / window_size[0]) * WORLD.width), 0, WORLD.width - 1)
    mouse_y = clamp(int((mouse_pos[1] / window_size[1]) * WORLD.height), 0, WORLD.height - 1)
    return mouse_x, mouse_y


def render():
    pygame.display.set_caption(f'Sand Simulator | FPS: {int(fpsClock.get_fps())}')
    surface = pygame.Surface((WORLD.width, WORLD.height))
    
    for particle in WORLD.Particles:
        surface.set_at((particle.x,particle.y),particle.COLOR)
    
    scaled_surface = pygame.transform.scale(surface, SCREEN.get_size())
    SCREEN.blit(scaled_surface,(0,0))
    pygame.display.flip()
    
main()