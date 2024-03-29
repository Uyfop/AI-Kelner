import pygame
from Components import Grid, Simulation

HEIGHT = 800
WIDTH = 800
CELL_COUNT = 20
FPS = 60
BACKGROUND_COLOR = (218, 198, 169)
WALL_COLOR = (102, 51, 0)


def main():
    running = True
    pygame.init()
    res = (HEIGHT, WIDTH)

    surface = pygame.display.set_mode(res)
    clock = pygame.time.Clock()

    grid = Grid(CELL_COUNT)
    sim = Simulation(grid, surface, clock, FPS, (HEIGHT, WIDTH), BACKGROUND_COLOR, WALL_COLOR)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        sim.update()
        sim.clock.tick(sim.fps)


if __name__ == "__main__":
    main()
