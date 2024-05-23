import pygame
import random
from animal import Predator, Prey
from environment import Water, Grass
#test1
pygame.init()
clock = pygame.time.Clock()
# Ustawienia planszy
width = 1000
height = 1000
gridSize = 10
xGridSize = width // gridSize
yGridSize = height // gridSize
# ilość zwierząt i terenów
predatorsNumber = random.randint(10, 20)
preysNumber = random.randint(100, 150)
terrainNumberWater = random.randint(30, 50)
terrainNumberGrass = random.randint(100, 150)

map = pygame.display.set_mode((width, height))
pygame.display.set_caption("Symulacja Ewolucji Zwierząt")

# Funkcja rysująca siatkę kwadratów
def rysuj_siatke():
    for x in range(xGridSize):
        for y in range(yGridSize):
            rectangle = pygame.Rect(x * gridSize, y * gridSize, gridSize, gridSize)
            pygame.draw.rect(map, (192, 192, 192), rectangle, 1)

# tworzenie terenów wody
terrainsWater = []
for _ in range(terrainNumberWater):
    x = random.randint(0, xGridSize - 1)
    y = random.randint(0, yGridSize - 1)
    size = random.randint(1, 4)
    terrainsWater.append(Water(x, y, size))

# tworzenie setu okupowanych lokacji przez wodę
occupiedWater = set()
for water in terrainsWater:
    occupiedWater.update(water.occupiedCoordinates)

# tworzenie terenów trawy
terrainsGrass = []
for grass in range(terrainNumberGrass):
    while True:
        x = random.randint(0, xGridSize - 1)
        y = random.randint(0, yGridSize - 1)
        if (x, y) not in occupiedWater:
            break
    terrainsGrass.append(Grass(x,y))

# tworzenie setu okupowanych lokacji przez trawę
occupiedGrass = set()
for grass in terrainsGrass:
    occupiedGrass.update(grass.occupiedCoordinates)

# zwierzeta
predators = []
for _ in range(predatorsNumber):
    while True:
        x = random.randint(0, xGridSize - 1)
        y = random.randint(0, yGridSize - 1)
        if not any((x, y) in terrain.occupiedCoordinates for terrain in terrainsWater):
            break
    speed = 3
    hunger = random.randint(0, 100)
    hydration = random.randint(0, 100)
    vision = 7
    predators.append(Predator(x, y, speed, hunger, hydration, vision))

preys = []
for _ in range(preysNumber):
    while True:
        x = random.randint(0, xGridSize - 1)
        y = random.randint(0, yGridSize - 1)
        if not any((x, y) in terrain.occupiedCoordinates for terrain in terrainsWater):
            break
    speed = 1
    hunger = random.randint(90, 300)
    hydration = random.randint(0, 39)
    vision = 8
    preys.append(Prey(x, y, speed, hunger, hydration, vision))
def pause_resume_simulation():
    global paused
    paused = not paused

def print_animal_attributes(animals, x, y): #funkcja drukująca atrybuty obiektu
    margin = 10
    for animal in animals:
        if abs(animal.x * gridSize - x) <= margin and abs(animal.y * gridSize - y) <= margin:
            print(f"\nAnimal Attributes:")
            print(f"Type: {type(animal).__name__}")
            print(f"X: {animal.x}, Y: {animal.y}")
            print(f"Speed: {animal.speed}")
            print(f"Hunger: {animal.hunger}")
            print(f"Hydration: {animal.hydration}")
            print(f"Vision: {animal.vision}")
            print(f"Reproduction Cooldown: {animal.reproduction_cooldown}")
            return

# Główna pętla gry
running = True
paused = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                if paused:
                    print_animal_attributes(predators + preys, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pause_resume_simulation()

    if not paused: #pętla umożliwiająca pauzowanie symulacji
        map.fill((0, 0, 0))

        # rysowanie wody
        for water in terrainsWater:
            water.draw(map, gridSize)

        # rysowanie trawy
        for grass in terrainsGrass:
            grass.draw(map, gridSize, (255, 255, 0))

        # rysowanie i funkcje predatora
        predatortargets = {}
        #
        for predator in predators:
            if predator.hunger == 0 or predator.hydration == 0:
                predators.remove(predator)
                continue      
            predator.reproduce(predators)      
            #
            if predator in predatortargets and predatortargets[predator] in prey:
                prey_target = predatortargets[predator]

                if (abs(predator.x - prey_target.x) < predator.vision and
                        abs(predator.y - prey_target.y) < predator.vision):
                    predator.follow(prey_target.x, prey_target.y, terrainsWater)
                    if (predator.x, predator.y) == (prey_target.x, prey_target.y):

                        prey.remove(prey_target)
                        predatortargets.pop(predator)
                    continue
            #
            for prey in preys:
                if (abs(predator.x - prey.x) < predator.vision and
                        abs(predator.y - prey.y) < predator.vision):
                    predator.follow(prey.x, prey.y, terrainsWater)
                    if (predator.x, predator.y) == (prey.x, prey.y):
                        predator.gain_hunger()
                        predator.gain_hydration()
                        preys.remove(prey)
                        break
                    else:
                        predatortargets[predator] = prey
                        break
            #
            if predator not in predatortargets or predatortargets[predator] not in preys:
                if not predator.seek_energy(terrainsGrass, terrainsWater):
                    predator.move_randomly(xGridSize, yGridSize, occupiedWater)

            predator.cooldown()
            predator.draw(map, gridSize, (255, 0, 0))

        # rysowanie i funkcje ofiary
        for prey in preys:
            if prey.hunger == 0 or prey.hydration == 0:
                preys.remove(prey)
            prey.reproduce(preys)
            if not prey.seek_energy(terrainsGrass,  terrainsWater):
                prey.move_randomly(xGridSize, yGridSize, occupiedWater)
            prey.draw(map, gridSize, (0, 255, 0))
            prey.reproduce(preys)

    clock.tick(5)
    pygame.display.flip()

pygame.quit()
