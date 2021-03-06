import pygame
from random import randint, random
pygame.init()

WIDTH, HEIGHT = 1200, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Darvin logic')


FONT = pygame.font.SysFont('conicsans', 16)

BG_COLOR = (255, 255, 255)
BLUE = (0, 0, 255)
GREY = (255, 10, 150)
GREEN = (0, 255, 0)

randomNum = 0
cell_number = 0

food_number = 0



def color_check(color, firstWay, secondWay):
    if firstWay:
        r = color[1] + randint(1, 10)
        if r > 255:
            r = r - 255
        elif r < 0:
            r = 255 - r
        else:
            r = r
        return (150, r, 150)
    elif secondWay:
        r = color[1] + randint(1, 10)
        if r > 255:
            r = r - 255
        elif r < 0:
            r = 255 - r
        else:
            r = r
        return (r, 150, 150)

def borders_check(x, y):
    global x_dif, y_dif
    if x <= 20:
        x_dif = x + 10
    elif y <= 20:
        y_dif = y + 10
    elif x >= WIDTH-20:
        x_dif = x - 10
    elif y >= HEIGHT-20:
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
    def __init__(self, x, y, hungry, health, speed, color, evolutionWay):
        self.x = x
        self.y = y
        self.hungry = hungry
        self.health = health
        self.speed = speed
        self.color = color



        if evolutionWay == 0:
            self.speedEvolutionWay = False
            self.healthEvolutionWay = False
        elif evolutionWay == 1:
            self.speedEvolutionWay = True
            self.healthEvolutionWay = False
        elif evolutionWay == 2:
            self.healthEvolutionWay = True
            self.speedEvolutionWay = False

        self.way = evolutionWay


        self.healthNextGeneration = health
        self.speedNextGeneration = speed
        self.colorNextGeneration = color
        self.mutation = False


    def move(self, win, food_list):
        # ?????????? ???????? ?? ?????????????????? ??????
        find_way(self.x, self.y, self.speed, food_list)
        self.x = x_dif
        self.y = y_dif
        # ???????????????? ???? ??????????????
        borders_check(self.x, self.y)
        self.x = x_dif
        self.y = y_dif
        # ???????????????????? ????????????
        pygame.draw.circle(win, self.color, (self.x, self.y), 10)
        hungry_text = FONT.render(f'{self.health}/{round(self.speed, 1)}', 1, BLUE)
        debug_text = FONT.render(f'{self.healthEvolutionWay, self.speedEvolutionWay}/{round(self.speed, 1)}', 1, BLUE)
        win.blit(hungry_text, (self.x+8, self.y+8))

    def status_update(self, list, name, list2):
        self.hungry = self.hungry - 1.5
        if self.hungry <= 0:
            self.health = self.health - 1
            if self.health <= 0:
                list2.append(Food(self.x, self.y))
                list.remove(name)
        if self.hungry >= 70:
            randomNum = random()
            if randomNum > 0.5:
                list.append(Cell(self.x, self.y, 50, self.healthNextGeneration, self.speedNextGeneration, self.colorNextGeneration, self.way))
                self.hungry = self.hungry - 40
            elif randomNum < 0.2 and self.mutation == False:
                if self.speedEvolutionWay:
                    self.speedNextGeneration = self.speedNextGeneration + 0.1
                    self.colorNextGeneration = color_check(self.color, self.speedEvolutionWay, self.healthEvolutionWay)
                    self.hungry = self.hungry - 40
                    self.mutation = True
                    self.way = 1
                elif self.healthEvolutionWay:
                    self.healthNextGeneration = self.healthNextGeneration + 5
                    self.colorNextGeneration = color_check(self.color, self.speedEvolutionWay, self.healthEvolutionWay)
                    self.hungry = self.hungry - 40
                    self.mutation = True
                    self.way = 2
                else:
                    randomNum = random()
                    if randomNum >= 0.7:
                        self.healthEvolutionWay = True
                    else:
                        self.speedEvolutionWay = True


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
    pause = False
    clock = pygame.time.Clock()

    time = 0
    seconds = 0

    cells = []
    food = []

    i = 0

    food_number = 500

    while run:
        while not pause and run:
            fps = 1000

            time = time + 1
            if time%60 == 0:
                seconds = seconds + 1

            clock.tick(fps)

            WIN.fill(BG_COLOR)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pause = True
                    if event.key == pygame.K_ESCAPE:
                        cells.append(Cell(WIDTH/2, HEIGHT/2, 100, 100, 2, GREY, 0))


            if len(food) < food_number:
                imp_number = randint(40, WIDTH-40)
                imp2_number = randint(40, HEIGHT-40)
                food.append(Food(imp_number, imp2_number))

            for name in cells:
                name.move(WIN, food)
                name.eat(name, food)
                name.status_update(cells, name, food)


            for name in food:
                name.appear(WIN)

            WIN.blit(FONT.render(f'{seconds} seconds, {len(cells)} creatures, {len(food)} food', 1, (0, 0, 0)), (30, HEIGHT-50))
            pygame.display.update()




        while pause and run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pause = False
                    if event.key == pygame.K_ESCAPE:
                        cells.append(Cell(WIDTH/2, HEIGHT/2, 100, 2, GREY))

            pygame.display.update()

            for name in cells:
                pygame.draw.circle(WIN, name.color, (name.x, name.y), 10)



    pygame.quit()

main()
