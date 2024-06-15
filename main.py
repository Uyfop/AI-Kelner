import pygame
from Components import Grid, Simulation, DecisionTree, PlateClassifier

HEIGHT = 800
WIDTH = 800
CELL_COUNT = 20
FPS = 60
BACKGROUND_COLOR = (218, 198, 169)
WALL_COLOR = (102, 51, 0)
MOVE_DELAY_MS = 600


def main():
    running = True
    paused = False
    pygame.init()
    res = (HEIGHT, WIDTH)

    surface = pygame.display.set_mode(res)
    clock = pygame.time.Clock()
    grid = Grid(CELL_COUNT)
    decision_tree = DecisionTree()
    plate_classifier = PlateClassifier()
    meal_mapping = decision_tree.initalize_tree('decision_tree_misc/data.csv')
    sim = Simulation(grid, surface, clock, FPS, (HEIGHT, WIDTH), BACKGROUND_COLOR, WALL_COLOR, decision_tree=decision_tree, meal_mapping=meal_mapping)
    sim.plate_classifier = plate_classifier

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused

        if not paused:
            sim.update()
            sim.clock.tick(sim.fps)


if __name__ == "__main__":
    main()
