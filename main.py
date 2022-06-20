import pygame
from random import randint
pygame.init()

WIDTH, HEIGHT = 700, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Darvin logic')


FONT = pygame.font.SysFont('conicsans', 16)

BG_COLOR = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

random = 0
cell_number = 0



class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, win):
        pygame.draw.circle(win, BLUE, (self.x, self.y), 2)

    def update(self):
        pass

class Cell:
    def __init__(self, x, y, hungry):
        self.x = x
        self.y = y
        self.hungry = hungry

    def move(self, win):
        random = randint(-4, 4)
        self.x = self.x + random
        random = randint(-4, 4)
        self.y = self.y + random
        pygame.draw.circle(win, RED, (self.x, self.y), 10)
        hungry_text = FONT.render(f'{self.hungry}', 1, BLUE)
        win.blit(hungry_text, (self.x+8, self.y+8))

    def status_update(self, list, name):
        self.hungry = self.hungry + randint(-30, -10)
        if self.hungry <= 0:
            list.remove(name)


def main():
    run = True
    clock = pygame.time.Clock()

    time = 0
    seconds = 0

    cells = []
    cells.append(Cell(350, 350, 100))

    while run:
        time = time + 1
        if time%60 == 0:
            seconds = seconds + 1

        clock.tick(180)
        WIN.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


        if seconds%1 == 0 and time%60 == 0:
            imp_number = len(cells)
            imp2_number = 0
            for name in cells:
                if imp2_number == imp_number:
                    break
                else:
                    cells.append(Cell(name.x, name.y, 100))
                imp2_number = imp2_number + 1
        for name in cells:
            name.move(WIN)
            if seconds % 2 == 0 and time % 60 == 0:
                name.status_update(cells, name)


        WIN.blit(FONT.render(f'{seconds} seconds, {len(cells)} creatures', 1, (0, 0, 0)), (50, 650))
        pygame.display.update()

    pygame.quit()

main()
