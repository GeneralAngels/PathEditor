import pygame
import math


class Point(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        # The position of the point proportional to the drawing zone.
        self.pos = (x, y)
        self.heading = Arrow((x, y), 0)
        self.rect = pygame.Rect(x - 5, y - 5, 10, 10)

    def get_abs_pos(self):
        return (self.pos[0], self.pos[1] + 100)

    def get_heading(self):
        return self.heading.angle

    # pos is the position of the point relative to the drawing zone.
    def update(self, x, y):
        self.pos = (x, y)
        self.rect = pygame.Rect(x - 5, y - 5, 10, 10)
        self.heading.update(self.pos, self.heading.end)

    def draw(self, screen):
        drawing_pos = (self.pos[0], self.pos[1] + 100)
        pygame.draw.circle(screen, (0, 0, 0), drawing_pos, 3)


class Arrow(pygame.sprite.Sprite):

    global ARROW_LENGTH
    ARROW_LENGTH = 75

    def __init__(self, start, angle):

        super().__init__()
        self.start = start # The start and end points is relative to the drawing zone.
        self.angle = angle

        self.end = (self.start[0] + math.cos(math.radians(self.angle - 90)) * ARROW_LENGTH,
                    self.start[1] + math.sin(math.radians(self.angle - 90)) * ARROW_LENGTH)  # The end point is NOT relative to the drawing zone.

        # The rect is used to detect collisions with the mouse. (added 100 to the y value to account for the UI)
        self.rect = pygame.Rect(self.end[0] - 5, self.end[1] - 5, 10, 10)
        
    
    # pos is the position of the point relative to the drawing zone.
    def update(self, point_pos, mouse_pos):

        X = 0
        Y = 1

        delta_x = mouse_pos[X] - self.start[X]
        delta_y = mouse_pos[Y] - self.start[Y]

        self.angle = math.degrees(math.atan2(delta_y, delta_x)) + 90
        if (self.angle < 0):
            self.angle = self.angle + 360

        self.start = point_pos

        self.end = (self.start[0] + math.cos(math.radians(self.angle - 90)) * ARROW_LENGTH,
                    self.start[1] + math.sin(math.radians(self.angle - 90)) * ARROW_LENGTH)

        self.rect = pygame.Rect(self.end[0] - 5, self.end[1] - 5, 10, 10)

    # pos is the position of the point relative to the drawing zone.
    def update_angle(self, angle):

        # Note: This function is used to update the angle of the arrow when the user changes the angle of the point via the panel.

        self.angle = angle

        self.end = (self.start[0] + math.cos(math.radians(self.angle - 90)) * ARROW_LENGTH,
                    self.start[1] + math.sin(math.radians(self.angle - 90)) * ARROW_LENGTH) 

        self.rect = pygame.Rect(self.end[0] - 5, self.end[1] - 5, 10, 10)

    def draw(self, screen):
        drawing_base = (self.start[0], self.start[1] + 100) # Calculate the absolute start and end points for drawing.
        drawing_end = (self.end[0], self.end[1] + 100)

        pygame.draw.line(screen, (247, 121, 11), drawing_base, drawing_end, 3)
        pygame.draw.circle(screen, (247, 121, 11), drawing_end, 5)
