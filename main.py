import pygame
from Components import Grid, Simulation, DecisionTree

HEIGHT = 800
WIDTH = 800
CELL_COUNT = 20
FPS = 60
BACKGROUND_COLOR = (218, 198, 169)
WALL_COLOR = (102, 51, 0)
MOVE_DELAY_MS = 600


def main():
    running = True
    pygame.init()
    res = (HEIGHT, WIDTH)

    surface = pygame.display.set_mode(res)
    clock = pygame.time.Clock()
    grid = Grid(CELL_COUNT)
    sim = Simulation(grid, surface, clock, FPS, (HEIGHT, WIDTH), BACKGROUND_COLOR, WALL_COLOR)
    decision_tree = DecisionTree()
    decision_tree.initalize_tree('decision_tree_misc/data.csv')
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        sim.update()
        sim.clock.tick(sim.fps)


if __name__ == "__main__":
    main()
