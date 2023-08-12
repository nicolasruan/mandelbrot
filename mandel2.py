import numpy as np
import pygame
import sys

import time

def point_in_rect(point, x_min, y_min, x_width, y_width):
    x_max=x_min+x_width
    y_max=y_min+y_width
    x,y=point
    return x_min <= x <= x_max and y_min <= y <= y_max

def pixel_grid(n_rows, n_cols, x_bounds, y_bounds):
    real_axis = np.linspace(x_bounds[0], x_bounds[1], num=n_cols)
    imaginary_axis = np.linspace(y_bounds[1], y_bounds[0], num=n_rows)
    n_rows, n_cols = n_rows, n_cols
    complex_grid = np.zeros((n_rows, n_cols), dtype=np.complex)
    real, imag = np.meshgrid(real_axis, imaginary_axis)
    complex_grid.real = real
    complex_grid.imag = imag
    pixel_grid = np.zeros((n_rows,n_cols),dtype=np.uint8)

    z_grid = np.zeros_like(complex_grid)
    elements_todo = np.ones((n_rows, n_cols), dtype=bool)
    for iteration in range(255):
        z_grid[elements_todo] = z_grid[elements_todo]**2 + complex_grid[elements_todo]
        mask = np.logical_and(np.absolute(z_grid) > 2, elements_todo)
        pixel_grid[mask] = iteration
        elements_todo = np.logical_and(elements_todo, np.logical_not(mask))

    return pixel_grid



pygame.init()

grid_size = 100
square_size = 6
width = grid_size * square_size
height = grid_size * square_size

center = [-1.787941304730,0]
x_bounds = [center[0]-2, center[0]+2]
y_bounds = [center[1]-2, center[1]+2]

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Mandelbrot")

def draw_mandel():
    p_grid = pixel_grid(grid_size, grid_size, x_bounds, y_bounds)
    for y in range(grid_size):
        for x in range(grid_size):
            a = x_bounds[0] + (x_bounds[1]-x_bounds[0])*x/(grid_size)
            b = y_bounds[0] + (y_bounds[1]-y_bounds[0])*y/(grid_size)
            val = p_grid[x,y]
            pygame.draw.rect(screen, (val, val, val), (x * square_size, y * square_size, square_size, square_size))
    

zoom = 1
on=0
zoom_dir = 1
move_xdir = 0
move_ydir = 0

# Main loop
running = True
while running:
    screen.fill((0, 0, 0))

    draw_mandel()

    w = x_bounds[1]-x_bounds[0]
    h = y_bounds[1]-y_bounds[0]
    x_bounds = [center[0]-w/(2*zoom), center[0]+w/(2*zoom)]
    y_bounds = [center[1]-w/(2*zoom), center[1]+w/(2*zoom)]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_xdir=1
            elif event.key == pygame.K_RIGHT:
                move_xdir=-1
            elif event.key == pygame.K_UP:
                move_ydir=-1
            elif event.key == pygame.K_DOWN:
                move_ydir=1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                move_xdir=0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                move_ydir=0
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  
                if point_in_rect(event.pos, 50,50,35,35):
                    on=1
                    zoom_dir=1
                elif point_in_rect(event.pos, 50,90,35,35):
                    on=1
                    zoom_dir=-1
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: 
                on=0
                print(center)


    pygame.draw.rect(screen, (100,100+100*on*zoom_dir,255), (50,50,35,35))
    pygame.draw.rect(screen, (100,100+50*on*(1-zoom_dir),255), (50,90,35,35))
                
    zoom = 1 + 0.08*zoom_dir*on
    center = [center[0]+move_ydir*0.01*w, center[1]+move_xdir*0.01*h]
    pygame.display.flip()
    time.sleep(0.005)

# Quit pygame
pygame.quit()
sys.exit()
