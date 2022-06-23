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

    def appear(self, win):
        pygame.draw.circle(win, BLUE, (self.x, self.y), 2)

    def update(self):
        pass

class Cell:
    def __init__(self, x, y, hungry):
        self.x = x
        self.y = y
        self.hungry = hungry
        self.speed = 4


    def move(self, win, food_list):

        # Поиск пути к ближайшей еде
        closest = [0, 9999999]
        for name in food_list:
            distance = (name.x - self.x) ** 2 + (name.y - self.y) ** 2
            if closest[1] > distance:
                closest[1] = distance
                closest[0] = name
        if self.x < closest[0].x:
            self.x = self.x + self.speed
        elif self.x > closest[0].x:
            self.x = self.x - self.speed
        else:
            self.x = self.x + 0
        if self.y < closest[0].y:
            self.y = self.y + self.speed
        elif self.y > closest[0].y:
            self.y = self.y - self.speed
        else:
            self.y = self.y + 0

        # Проверка на границы
        if self.x <= 20:
            self.x = self.x + 10
        elif self.y <= 20:
            self.y = self.y + 10
        elif self.x >= 680:
            self.x = self.x - 10
        elif self.y >= 680:
            self.y = self.y - 10

        # Прорисовка клетки
        pygame.draw.circle(win, RED, (self.x, self.y), 10)
        hungry_text = FONT.render(f'{self.hungry}', 1, BLUE)
        win.blit(hungry_text, (self.x+8, self.y+8))

    def status_update(self, list, name):
        self.hungry = self.hungry + randint(-30, -10)
        if self.hungry <= 0:
            list.remove(name)
        if self.hungry >= 70:
            list.append(Cell(self.x, self.y, 50))
            self.hungry = self.hungry - 50

    def eat(self, cell, list_food):
        for name in list_food:
            # print(name.x, cell.x)
            hypotenous = 100 - (name.x - cell.x)** 2
            if  hypotenous >= (name.y - cell.y) ** 2:
                self.hungry = self.hungry + 20
                list_food.remove(name)
                return 1



def main():
    run = True
    clock = pygame.time.Clock()

    time = 0
    seconds = 0

    cells = []
    cells.append(Cell(350, 350, 100))

    food = []

    i = 0

    while run:
        time = time + 1
        if time%60 == 0:
            seconds = seconds + 1

        clock.tick(180)
        WIN.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if len(food) < 50:
            imp_number = randint(40, 660)
            imp2_number = randint(40, 660)
            food.append(Food(imp_number, imp2_number))


        if len(cells) == 0:
            cells.append(Cell(350, 350, 100))

        for name in cells:
            name.move(WIN, food)
            name.eat(name, food)
            if len(food) < 50:
                i = i + 1
            if seconds % 2 == 0 and time % 60 == 0:
                name.status_update(cells, name)

        for name in food:
            name.appear(WIN)

        WIN.blit(FONT.render(f'{seconds} seconds, {len(cells)} creatures, {len(food)} food, {i-49}', 1, (0, 0, 0)), (50, 650))
        pygame.display.update()

    pygame.quit()

main()
