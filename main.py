import pygame
from random import randint, random
pygame.init()

WIDTH, HEIGHT = 700, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Darvin logic')


FONT = pygame.font.SysFont('conicsans', 16)

BG_COLOR = (255, 255, 255)
BLUE = (0, 0, 255)
GREY = (255, 10, 10)
GREEN = (0, 255, 0)

randomNum = 0
cell_number = 0



def color_check(color):
    listColorNextGeneration = []
    for i in range(2):
        r = color[i] + randint(1, 10)
        if r > 255:
            listColorNextGeneration.append(r - 255)
            print(listColorNextGeneration)
        elif r < 0:
            listColorNextGeneration.append(255 - r)
            print(listColorNextGeneration)
        else:
            listColorNextGeneration.append(r)

    print(listColorNextGeneration)
    return (listColorNextGeneration[0], listColorNextGeneration[1], 150)

def borders_check(x, y):
    global x_dif, y_dif
    if x <= 20:
        x_dif = x + 10
    elif y <= 20:
        y_dif = y + 10
    elif x >= 680:
        x_dif = x - 10
    elif y >= 680:
        y_dif = y - 10

def find_way(x, y, speed, food_list):
    global x_dif, y_dif
    closest = [0, 9999999]
    for name in food_list:
        distance = (name.x - x) ** 2 + (name.y - y) ** 2
        if closest[1] > distance:
            closest[1] = distance
            closest[0] = name
    if x < closest[0].x:
        x_dif = x + speed
    elif x > closest[0].x:
        x_dif = x - speed
    else:
        x_dif = x + 0
    if y < closest[0].y:
        y_dif = y + speed
    elif y > closest[0].y:
        y_dif = y - speed
    else:
        y_dif = y + 0

class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def appear(self, win):
        pygame.draw.circle(win, BLUE, (self.x, self.y), 2)

    def update(self):
        pass

class Cell:
    def __init__(self, x, y, hungry, speed, color):
        self.x = x
        self.y = y
        self.hungry = hungry
        self.speed = speed
        self.color = color

        self.speedNextGeneration = speed
        self.colorNextGeneration = color
        self.mutation = False
        print(self.color)
        print(self.colorNextGeneration)


    def move(self, win, food_list):
        # Поиск пути к ближайшей еде
        find_way(self.x, self.y, self.speed, food_list)
        self.x = x_dif
        self.y = y_dif
        # Проверка на границы
        borders_check(self.x, self.y)
        self.x = x_dif
        self.y = y_dif
        print(self.color)
        print(self.colorNextGeneration)

        # Прорисовка клетки
        pygame.draw.circle(win, self.color, (self.x, self.y), 10)
        hungry_text = FONT.render(f'{self.hungry}', 1, BLUE)
        win.blit(hungry_text, (self.x+8, self.y+8))

    def status_update(self, list, name):
        self.hungry = self.hungry - 1.5
        if self.hungry <= 0:
            list.remove(name)
        if self.hungry >= 70:
            randomNum = random()
            if randomNum > 0.5:
                list.append(Cell(self.x, self.y, 50, self.speedNextGeneration, self.colorNextGeneration))
                self.hungry = self.hungry - 40
            elif randomNum < 0.2 and self.mutation == False:
                self.speedNextGeneration = self.speedNextGeneration + 0.1
                self.colorNextGeneration = color_check(self.color)
                self.hungry = self.hungry - 20
                self.mutation = True


    def eat(self, cell, list_food):
        for name in list_food:
            # print(name.x, cell.x)
            hypotenous = 100 - (name.x - cell.x) ** 2
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
    food = []

    i = 0

    while run:
        time = time + 1
        if time%60 == 0:
            seconds = seconds + 1

        clock.tick(60)
        WIN.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if len(food) < 200:
            imp_number = randint(40, 660)
            imp2_number = randint(40, 660)
            food.append(Food(imp_number, imp2_number))


        if len(cells) == 0:
            cells.append(Cell(350, 350, 100, 2, GREY))

        for name in cells:
            name.move(WIN, food)
            name.eat(name, food)
            name.status_update(cells, name)
            if len(food) < 200:
                i = i + 1


        for name in food:
            name.appear(WIN)

        WIN.blit(FONT.render(f'{seconds} seconds, {len(cells)} creatures, {len(food)} food, {i-199}', 1, (0, 0, 0)), (50, 650))
        pygame.display.update()

    pygame.quit()

main()
