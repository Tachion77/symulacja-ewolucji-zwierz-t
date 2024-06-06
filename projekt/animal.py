def flee_from_predator(self, predators_list, terrains, x_grid_size, y_grid_size):
        closest_predator = None
        min_distance = float('inf')

        for predator in predators_list:
            distance = math.sqrt((self.x - predator.x) ** 2 + (self.y - predator.y) ** 2)
            if distance < min_distance and distance <= self.vision:
                min_distance = distance
                closest_predator = predator

        if closest_predator:
            direction_x = self.x - closest_predator.x
            direction_y = self.y - closest_predator.y

            if direction_x != 0:
                direction_x = direction_x / abs(direction_x)
            if direction_y != 0:
                direction_y = direction_y / abs(direction_y)

            for _ in range(self.speed):
                new_x = self.x + int(direction_x)
                new_y = self.y + int(direction_y)

                if not self.is_position_blocked(new_x, new_y, terrains):
                    self.x = new_x
                    self.y = new_y
                else:
                    self.move_randomly(x_grid_size, y_grid_size, [predator.get_position() for predator in predators_list])
