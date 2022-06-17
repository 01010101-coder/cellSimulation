import pygame
from random import randint
pygame.init()

WIDTH, HEIGHT = 700, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Darvin logic')


FONT = pygame.font.SysFont('conicsans', 16)

BG_COLOR = (255, 255, 255)
BLUE = (0, 0, 255)


def main():
    run = True
    clock = pygame.time.Clock()

    time = 0
    seconds = 0

    cells = []
    cells.append([350, 350])

    while run:
        time = time + 1
        if time%60 == 0:
            seconds = seconds + 1

        clock.tick(180)
        WIN.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


        for cell in range(len(cells)):
            x = randint(-4, 4)
            y = randint(-4, 4)
            cells[cell] = [cells[cell][0] + x, cells[cell][1] + y]
            pygame.draw.circle(WIN, BLUE, (cells[cell][0], cells[cell][1]), 2)



        if seconds%2 == 0 and time%60 == 0:
            for i in range(len(cells)):
                cells.append(cells[i])

        WIN.blit(FONT.render(f'{seconds} seconds, {len(cells)} creatures', 1, (0, 0, 0)), (50, 650))
        pygame.display.update()

    pygame.quit()

main()
