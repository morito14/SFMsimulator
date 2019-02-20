# coding=utf-8
from map import Map
import pygame
from pygame.locals import *
import sys
import numpy as np


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
        self.font = pygame.font.Font(None, 55)

    def draw(self, pedestrians, robots):
        """
        draw simulated pedestrians and the robot
        """
        self.screen.fill((0, 0, 0))
        self.draw_map(self.img_slam_map)
        self.draw_pedestrian_thing(pedestrians)
        self.draw_robot(robots)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)

    def draw_map(self, img_slam_map):
        self.screen.blit(img_slam_map, (0, 0))

    def draw_pedestrian_thing(self, pedestrians):
        i = 0
        for pedestrian in pedestrians:
            # screen, color, position, radius
            self.draw_pedestrian(pedestrian)
            self.draw_f_destination(pedestrian)
            self.draw_subgoal(pedestrian)
            self.draw_closest_wall(pedestrian)
            self.draw_f_wall(pedestrian)
            self.draw_velocity(pedestrian, i)
            self.draw_f_pedestrian(pedestrian)
            i += 1

    def draw_closest_wall(self, pedestrian):
        #  draw nearest wall
        x_pix, y_pix = self.slam_map.posi_to_pixel(pedestrian.closest_wall[0],
                                                   pedestrian.closest_wall[1], self.zoom)
        radius = int(0.1 / self.slam_map.resolution * self.zoom)
        pygame.draw.circle(self.screen, [255, 0, 0], (x_pix, y_pix), radius)



    def draw_pedestrian(self, pedestrian):
        x_pix, y_pix = self.slam_map.posi_to_pixel(pedestrian.position[0],
                                                   pedestrian.position[1], self.zoom)
        radius = int(pedestrian.radius / self.slam_map.resolution * self.zoom / 2.)
        pygame.draw.circle(self.screen, pedestrian.color, (x_pix, y_pix), radius)

    def draw_velocity(self, pedestrian, i):
        text = self.font.render(str(i) + '.vel:' + str(round(np.linalg.norm(pedestrian.velocity), 4)),
                           True, (0, 0, 255))  # 描画する文字列の設定
        self.screen.blit(text, [20, 100 + (50 * i)])  # 文字列の表示位置

    def draw_f_destination(self, pedestrian):
        # draw attractive force to subgoal
        x_pix, y_pix = self.slam_map.posi_to_pixel(pedestrian.position[0],
                                                   pedestrian.position[1], self.zoom)
        width = int(pedestrian.f_destination[0] * self.zoom * 3)
        height = -int(pedestrian.f_destination[1] * self.zoom * 3)
        # print('x_pix:{0}, y_pix:{1}, width:{2}, height{3}'.format(x_pix, y_pix, width, height))
        pygame.draw.line(self.screen, (0, 255, 0),
                         (x_pix, y_pix), (x_pix + width, y_pix + height), int(self.zoom))

    def draw_f_pedestrian(self, pedestrian):
        # draw attractive force to subgoal
        x_pix, y_pix = self.slam_map.posi_to_pixel(pedestrian.position[0],
                                                   pedestrian.position[1], self.zoom)
        width = int(pedestrian.f_pedestrian[0] * self.zoom * 3)
        height = -int(pedestrian.f_pedestrian[1] * self.zoom * 3)
        # print('x_pix:{0}, y_pix:{1}, width:{2}, height{3}'.format(x_pix, y_pix, width, height))
        pygame.draw.line(self.screen, (0, 0, 255),
                         (x_pix, y_pix), (x_pix + width, y_pix + height), int(self.zoom))

    def draw_f_wall(self, pedestrian):
        # draw attractive force to subgoal
        x_pix, y_pix = self.slam_map.posi_to_pixel(pedestrian.position[0],
                                                   pedestrian.position[1], self.zoom)
        width = int(pedestrian.f_wall[0] * self.zoom * 3)
        height = -int(pedestrian.f_wall[1] * self.zoom * 3)
        # print('x_pix:{0}, y_pix:{1}, width:{2}, height{3}'.format(x_pix, y_pix, width, height))
        pygame.draw.line(self.screen, (255, 0, 0),
                         (x_pix, y_pix), (x_pix + width, y_pix + height), int(self.zoom))

    def draw_subgoal(self, pedestrian):
        #draw pedestrian's subgoal
        x_pix, y_pix = self.slam_map.posi_to_pixel(pedestrian.subgoal[0],
                                                   pedestrian.subgoal[1], self.zoom)
        radius = int(pedestrian.radius / self.slam_map.resolution * self.zoom / 2.)
        draw_position = [x_pix - radius, y_pix - radius, radius, radius]
        pygame.draw.rect(self.screen, [0, 255, 0], draw_position)



    def draw_robot(self, robots):
        # screen, color, position, radius
        for robot in robots:
            x_pix, y_pix = self.slam_map.posi_to_pixel(robot.position[0],
                                                   robot.position[1], self.zoom)
            radius = int(robot.radius / self.slam_map.resolution * self.zoom / 2.)

            pygame.draw.circle(self.screen, robot.color, (x_pix, y_pix), radius)

