import pygame
import random
from animal import Predator, Prey
from environment import Water, Grass
class Simulation:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        self.width = 1000
        self.height = 1000
        self.gridSize = 10
        self.xGridSize = self.width // self.gridSize
        self.yGridSize = self.height // self.gridSize

        self.predatorsNumber = random.randint(10, 30)
        self.preysNumber = random.randint(10, 30)
        self.terrainNumberWater = random.randint(30, 50)
        self.terrainNumberGrass = random.randint(100, 150)

        self.map = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Symulacja Ewolucji Zwierząt")

        self.paused = False
        self.running = True

        self.terrainsWater = self.create_water_terrains()
        self.occupiedWater = self.get_occupied_coordinates(self.terrainsWater)

        self.terrainsGrass = self.create_grass_terrains()
        self.occupiedGrass = self.get_occupied_coordinates(self.terrainsGrass)

        self.predators = self.create_predators()
        self.preys = self.create_preys()

    def create_water_terrains(self):
        terrainsWater = []
        for _ in range(self.terrainNumberWater):
            x = random.randint(0, self.xGridSize - 1)
            y = random.randint(0, self.yGridSize - 1)
            size = random.randint(1, 4)
            terrainsWater.append(Water(x, y, size))
        return terrainsWater

    def create_grass_terrains(self):
        terrainsGrass = []
        for _ in range(self.terrainNumberGrass):
            while True:
                x = random.randint(0, self.xGridSize - 1)
                y = random.randint(0, self.yGridSize - 1)
                if (x, y) not in self.occupiedWater:
                    break
            terrainsGrass.append(Grass(x, y))
        return terrainsGrass

    def get_occupied_coordinates(self, terrains):
        occupied = set()
        for terrain in terrains:
            occupied.update(terrain.occupiedCoordinates)
        return occupied

    def create_predators(self):
        predators = []
        for _ in range(self.predatorsNumber):
            while True:
                x = random.randint(0, self.xGridSize - 1)
                y = random.randint(0, self.yGridSize - 1)
                if not any((x, y) in terrain.occupiedCoordinates for terrain in self.terrainsWater):
                    break
            speed = 3
            hunger = random.randint(0, 100)
            hydration = random.randint(0, 100)
            vision = 7
            predators.append(Predator(x, y, speed, hunger, hydration, vision))
        return predators

    def create_preys(self):
        preys = []
        for _ in range(self.preysNumber):
            while True:
                x = random.randint(0, self.xGridSize - 1)
                y = random.randint(0, self.yGridSize - 1)
                if not any((x, y) in terrain.occupiedCoordinates for terrain in self.terrainsWater):
                    break
            speed = 1
            hunger = random.randint(90, 300)
            hydration = random.randint(0, 39)
            vision = 8
            preys.append(Prey(x, y, speed, hunger, hydration, vision))
        return preys

    def rysuj_siatke(self):
        for x in range(self.xGridSize):
            for y in range(self.yGridSize):
                rectangle = pygame.Rect(x * self.gridSize, y * self.gridSize, self.gridSize, self.gridSize)
                pygame.draw.rect(self.map, (192, 192, 192), rectangle, 1)

    def pause_resume_simulation(self):
        self.paused = not self.paused

    def print_animal_attributes(self, animals, x, y):
        margin = 10
        for animal in animals:
            if abs(animal.x * self.gridSize - x) <= margin and abs(animal.y * self.gridSize - y) <= margin:
                print(f"\nAnimal Attributes:")
                print(f"Type: {type(animal).__name__}")
                print(f"X: {animal.x}, Y: {animal.y}")
                print(f"Speed: {animal.speed}")
                print(f"Hunger: {animal.hunger}")
                print(f"Hydration: {animal.hydration}")
                print(f"Vision: {animal.vision}")
                print(f"Reproduction Cooldown: {animal.reproduction_cooldown}")
                return

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    if self.paused:
                        self.print_animal_attributes(self.predators + self.preys, mouse_x, mouse_y)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.pause_resume_simulation()

    def update_simulation(self):
        self.map.fill((0, 0, 0))

        # Rysowanie wody
        for water in self.terrainsWater:
            water.draw(self.map, self.gridSize)

        # Rysowanie trawy
        for grass in self.terrainsGrass:
            grass.draw(self.map, self.gridSize, (255, 255, 0))

        # Aktualizacja drapieżników
        predatortargets = {}
        for predator in self.predators:
            if predator.hunger == 0 or predator.hydration == 0:
                self.predators.remove(predator)
                continue
            predator.reproduce(self.predators)
            if predator in predatortargets and predatortargets[predator] in self.preys:
                prey_target = predatortargets[predator]
                if (abs(predator.x - prey_target.x) < predator.vision and
                        abs(predator.y - prey_target.y) < predator.vision):
                    predator.follow(prey_target.x, prey_target.y, self.terrainsWater)
                    if (predator.x, predator.y) == (prey_target.x, prey_target.y):
                        self.preys.remove(prey_target)
                        predatortargets.pop(predator)
                    continue
            for prey in self.preys:
                if (abs(predator.x - prey.x) < predator.vision and
                        abs(predator.y - prey.y) < predator.vision):
                    predator.follow(prey.x, prey.y, self.terrainsWater)
                    if (predator.x, predator.y) == (prey.x, prey.y):
                        predator.gain_hunger()
                        predator.gain_hydration()
                        self.preys.remove(prey)
                        break
                    else:
                        predatortargets[predator] = prey
                        break
            if predator not in predatortargets or predatortargets[predator] not in self.preys:
                if not predator.seek_energy(self.terrainsGrass, self.terrainsWater):
                    predator.move_randomly(self.xGridSize, self.yGridSize, self.occupiedWater)
            predator.cooldown()
            predator.draw(self.map, self.gridSize, (255, 0, 0))

        # Aktualizacja ofiar
        for prey in self.preys:
            if prey.hunger == 0 or prey.hydration == 0:
                self.preys.remove(prey)
            prey.reproduce(self.preys)
            prey.flee_from_predator(self.predators, self.terrainsWater, self.xGridSize,self.yGridSize)
            if not prey.seek_energy(self.terrainsGrass, self.terrainsWater):
                prey.move_randomly(self.xGridSize, self.yGridSize, self.occupiedWater)
            prey.draw(self.map, self.gridSize, (0, 255, 0))
            prey.cooldown()

    def run(self):
        while self.running:
            self.handle_events()
            if not self.paused:
                self.update_simulation()
            self.clock.tick(5)
            pygame.display.flip()
        pygame.quit()
