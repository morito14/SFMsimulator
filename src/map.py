# coding=utf-8
from PIL import Image
import numpy as np
import yaml


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
         self.resolution,
         self.origin,
         self.height,
         self.width) = self.load_map(path_to_map, path_to_yaml)

    @staticmethod
    def load_map(path_to_map, path_to_yaml):
        """
        load map (.pgm)
        :param path_to_map: String
        :param path_to_yaml: String
        :return: Boolean
        """
        img = Image.open(path_to_map).convert('L')
        img_np = np.array(img)  # ndarray
        # binarization
        img_np = np.where(img_np < 250, 0, 255)
        img_pillow = Image.fromarray(np.uint8(img_np))

        # open .yaml
        with open(path_to_yaml, "r") as yf:
            data = yaml.load(yf)
            print(data)
            resolution = data['resolution']
            origin = data['origin']

        height, width = img_pillow.size

        return (img_pillow, img_np,
                resolution, origin, height, width)

    def get_status(self):
        # get loaded map
        return (self.img_pillow, self.img_np,
                self.resolution, self.origin, self.width, self.resolution,
                self.path_to_map)

    def posi_to_pixel(self, x_m, y_m, zoom):
        # /map
        x_pix = ((x_m - self.origin[0]) / self.resolution) * zoom
        y_pix = (self.height - int((y_m - self.origin[1]) / self.resolution)) * zoom

        return int(x_pix), int(y_pix)

    def posi_to_matrix(self, x_m, y_m):
        # /map
        row = int((y_m - self.origin[0]) / self.resolution)
        col = int((x_m - self.origin[1]) / self.resolution)

        return row, col
