# coding=utf-8
from map import Map
import pygame
from pygame.locals import *
import sys


class Drawer(object):
    """
    Draw information from Social Force Model simulator
    """

    def __init__(self, slam_map, zoom):
        """
        :type slam_map: Map
        """
        self.zoom = zoom
        self.slam_map = slam_map
        # pygame initialize
        pygame.init()
        print("drawer initialized")
        zoomed_width = int(self.zoom * slam_map.width)
        zoomed_height = int(self.zoom * slam_map.height)
        self.screen = pygame.display.set_mode((zoomed_width, zoomed_height))
        img_slam_map = pygame.image.load(slam_map.path_to_map)
        self.img_slam_map = pygame.transform.scale(img_slam_map, (zoomed_width, zoomed_height))
        pygame.display.set_caption("SFMsim")

    def draw(self, pedestrians, robots):
        """
        draw simulated pedestrians and the robot
        """
        self.screen.fill((0, 0, 0))
        self.draw_map(self.img_slam_map)
        self.draw_pedestrian(pedestrians)
        self.draw_robot(robots)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)

    def draw_map(self, img_slam_map):
        self.screen.blit(img_slam_map, (0, 0))

    def draw_pedestrian(self, pedestrians):
        for pedestrian in pedestrians:
            # screen, color, position, radius
            col, row = self.slam_map.posi_to_array(pedestrian.position[0],
                                                   pedestrian.position[1], self.zoom)
            radius = int(pedestrian.radius / self.slam_map.resolution)

            pygame.draw.circle(self.screen, pedestrian.color, (col, row), radius)

    def draw_robot(self, robots):
        # screen, color, position, radius
        for robot in robots:
            col, row = self.slam_map.posi_to_array(robot.position[0],
                                                   robot.position[1], self.zoom)
            radius = int(robot.radius / self.slam_map.resolution)

            pygame.draw.circle(self.screen, robot.color, (col, row), radius)
