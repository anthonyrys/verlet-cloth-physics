import pygame
import math

class VerletCloth(object):
    @staticmethod
    def get_distance(p1, p2):
        rx = abs(p1[0][0] - p2[0][0])
        ry = abs(p1[1][0] - p2[1][0])

        return math.sqrt(((rx **2) + (ry **2)))  

    @staticmethod
    def point(x, y, m, r):
        return [[x, x], [y, y], m, r]
    
    @staticmethod
    def constraint(p1, p2, l):
        return [p1, p2, l]
        
    def __init__(self):
        self.offset = [400, 100]
        self.scale = 20

        self.points = []
        self.polygon_points = []
        self.constraints = []
        
        self.create_points()
        self.create_constraints()

        self.gravity = .05
        self.flex = 1

        self.mode = 0

    def create_points(self):
        for x in range(5):
            for y in range(15 - x):          
                r = False if y != 0 else x
                if x == 0 and y == 0:
                    r = 'center'

                self.points.append(self.point(x, y, 1, r))
                if x != 0:
                    self.points.append(self.point(-x, y, 1, -r))

    def create_constraints(self): 
        for p1 in self.points:
            bottom = False

            for p2 in self.points:
                if p1 == p2:
                    continue

                if p1[0][0] + 1 == p2[0][0] and p1[1][0] == p2[1][0]:
                    self.constraints.append(self.constraint(p1, p2, self.get_distance(p1, p2)))

                elif p1[1][0] + 1 == p2[1][0] and p1[0][0] == p2[0][0]:
                    self.constraints.append(self.constraint(p1, p2, self.get_distance(p1, p2)))
                    bottom = True

            if not bottom:
                for p2 in self.points:
                    if p1[0][0] + 1 == p2[0][0] and p1[1][0] + 1 == p2[1][0]:
                        self.constraints.append(self.constraint(p1, p2, self.get_distance(p1, p2)))

                    elif p1[0][0] - 1 == p2[0][0] and p1[1][0] + 1 == p2[1][0]:
                        self.constraints.append(self.constraint(p1, p2, self.get_distance(p1, p2)))
                    
    def update(self):
        for point in self.points:
            if point[3]:
                offset = 0 if point[3] == 'center' else point[3]
                point[0][0] = (pygame.mouse.get_pos()[0] - self.offset[0] + (self.scale * offset)) / self.scale
                point[1][0] = (pygame.mouse.get_pos()[1] - self.offset[1]) / self.scale

            else:
                p = [point[0][0], point[1][0]]
                g = self.gravity / point[2] if not point[3] else 0

                point[0][0] = 2 * point[0][0] - point[0][1]
                point[1][0] = 2 * point[1][0] - point[1][1] + g

                point[0][1] = p[0]
                point[1][1] = p[1]

        for constraint in self.constraints:
            d = self.get_distance(constraint[0], constraint[1])
            r = (constraint[2] - d) / d * .5

            x = constraint[0][0][0] - constraint[1][0][0] 
            y = constraint[0][1][0] - constraint[1][1][0] 

            if not constraint[0][3]:
                constraint[0][0][0] += x * r * self.flex
                constraint[0][1][0] += y * r * self.flex
            
            if not constraint[1][3]:
                constraint[1][0][0] -= x * r * self.flex
                constraint[1][1][0] -= y * r * self.flex

    def render(self, screen):
        self.update()
    
        for constraint in self.constraints:
            start_p = [constraint[0][0][0] * self.scale + self.offset[0], constraint[0][1][0] * self.scale + self.offset[1]]
            end_p = [constraint[1][0][0] * self.scale + self.offset[0], constraint[1][1][0] * self.scale + self.offset[1]]
            
            pygame.draw.line(screen, (255, 255, 255), start_p, end_p)

        for point in self.points:
            p = [point[0][0] * self.scale + self.offset[0], point[1][0] * self.scale + self.offset[1]]
            pygame.draw.circle(screen, (255, 255, 255), p, 3)
