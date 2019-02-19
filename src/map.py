# coding=utf-8
from PIL import Image
import numpy as np
import yaml
import itertools


class Map(object):
    """
    serve map to SFM-simulator
    """

    def __init__(self, path_to_map, path_to_yaml):
        """
        :type path_to_map: String
        """
        self.path_to_map = path_to_map
        (self.img_pillow,
         self.img_np,
         self.img_bool,
         self.resolution,
         self.origin,
         self.height,
         self.width) = self.load_map(path_to_map, path_to_yaml)
        self.walls = []
        self.make_walls_array()

    def load_map(self, path_to_map, path_to_yaml):
        """
        load map (.pgm)
        :param path_to_map: String
        :param path_to_yaml: String
        :return: Boolean
        """
        img = Image.open(path_to_map).convert('L')
        img_np = np.array(img)  # ndarray
        # binarization
        img_np = np.where(img_np < 40, 0, 255)
        img_bool = np.where(img_np < 40, True, False)
        img_pillow = Image.fromarray(np.uint8(img_np))

        # open .yaml
        with open(path_to_yaml, "r") as yf:
            data = yaml.load(yf)
            print(data)
            resolution = data['resolution']
            origin = data['origin']

        height, width = img_pillow.size

        return (img_pillow, img_np, img_bool,
                resolution, origin, height, width)

    def make_walls_array(self):
        # for finding nearest wall
        for row, col in itertools.product(range(self.height), range(self.width)):
            if self.img_bool[row][col]:
                x, y = self.matrix_to_posi(row, col)
                self.walls.append([x, y])

    def get_status(self):
        # get loaded map
        return (self.img_pillow, self.img_np,
                self.resolution, self.origin, self.width, self.resolution,
                self.path_to_map)

    def posi_to_pixel(self, x_m, y_m, zoom):
        # /map
        x_pix = ((x_m - self.origin[0]) / self.resolution) * zoom
        print('ym:{0}, origin:{1}, res:{2}'.format(y_m, self.origin, self.resolution))
        y_pix = (self.height - int((y_m - self.origin[1]) / self.resolution)) * zoom

        return int(x_pix), int(y_pix)

    def posi_to_matrix(self, x_m, y_m):
        # /map
        row = self.height - int((y_m - self.origin[1]) / self.resolution)
        col = int((x_m - self.origin[1]) / self.resolution)

        # for debug (mark the position of pedestrian)
        print('row:{0}, col{1}'.format(row, col))
        for i, j in itertools.product(range(-4, 4), range(-4, 4)):
            self.img_np[row + i][col + j] = 120

        return row, col

    def matrix_to_posi(self, row, col):
        # /map
        x_m = (self.resolution * col) + self.origin[0]
        y_m = (self.resolution * (self.height - row)) + self.origin[1]

        return x_m, y_m

    def show_ndarray(self):
        # show ndarray matrix
        img_pillow = Image.fromarray(np.uint8(self.img_np))
        img_pillow.show()

'''
    def make_grid(self):
        # grid
'''