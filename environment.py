import pygame
# klasa terenów
class Terrain:
    def init(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.occupiedCoordinates = set()
        for i in range(self.size):
            for j in range(self.size):
                self.occupiedCoordinates.add((self.x + i, self.y + j))
    def draw(self, surface, grid_size):
        for coord in self.occupiedCoordinates:
            rect = pygame.Rect(coord[0] * grid_size, coord[1] * grid_size, grid_size, grid_size)
            pygame.draw.rect(surface, self.color, rect)
            surface.fill((self.color), rect)
# klasa wody - dziedziczy po terenie
class Water(Terrain):
    def __init__(self, x, y, size):
        super().init(x, y, size, (0, 0, 255))
        for i in range(self.size):
            for j in range(self.size):
                self.occupiedCoordinates.add((self.x + i, self.y + j))
# klasa trawy - dziedziczy po terenie
class Grass:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.occupiedCoordinates = {(x, y)}
    def draw(self, surface, grid_size, color):
        rect = pygame.Rect(self.x * grid_size, self.y * grid_size, grid_size, grid_size)
        pygame.draw.arc(surface, color, rect,0,3.14)
