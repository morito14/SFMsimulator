from moving_object import MovingObject
import numpy as np
import itertools


class Pedestrian(MovingObject, object):
    '''robot, pedestrian'''

    def __init__(self):
        # initialize
        super(Pedestrian, self).__init__()
        self.radius = 0.3  # [m]
        self.color = [0, 0, 255]
        self.desired_velocity = 1.08  # [m/s]
        self.tau = 0.1  # relaxation time
        # for calc_f_wall
        self.w_Uab = 10.  # [m^2s^-2]
        self.w_R = 0.2  # [m]

        print('generated pedestrian')

    def set_status(self, **kwargs):
        # set_status
        if 'desired_velocity' in kwargs:
            self.desired_velocity = kwargs['desired_velocity']

        print('set -> desired_velocity:{0}'.format(self.desired_velocity))
        super(Pedestrian, self).set_status(**kwargs)

    def calc_f_total(self, pedestrians, slam_map):
        # get total force
        self.f_wall = self.calc_f_wall(slam_map)
        self.f_pedestrian = self.calc_f_pedestrian(pedestrians)
        self.calc_f_destination()

        return self.f_wall + self.f_pedestrian + self.f_destination

    def calc_f_wall(self, map):
        # calc force from wall
        self.closest_wall[0], self.closest_wall[1] = self.find_closest_wall(map)
        print('closest wall:({0}, {1})'.format(self.closest_wall[0], self.closest_wall[1]))

        r_ab = self.position - self.closest_wall
        result = self.func_w_U(r_ab)

        return 0, 0

    def func_w_U(self, r_ab):
        # calc potential of Wall
        norm = np.linalg.norm(r_ab)
        return self.w_Uab * np.exp(-norm / self.w_R)


    def find_closest_wall(self, map):
        # find nearest wall in map
        '''
        # L1 norm (uzumaki)
        row_origin, col_origin = map.posi_to_matrix(self.position[0], self.position[1])
        r = 1
        while (r < 100):
            row = row_origin - r
            col = col_origin - r
            for num in range(r * 2):  # right
                col+= 1
                if map.img_bool[row][col]:
                    print('find!!:{0}, {1}'.format(row, col))
                    return map.matrix_to_posi(row, col)
            for num in range(r * 2):  # down
                row+= 1
                if map.img_bool[row][col]:
                    print('find!!:{0}, {1}'.format(row, col))
                    return map.matrix_to_posi(row, col)
            for num in range(r * 2):  # left
                col-= 1
                if map.img_bool[row][col]:
                    print('find!!:{0}, {1}'.format(row, col))
                    return map.matrix_to_posi(row, col)
            for num in range(r * 2 + 1):  # up
                row-= 1
                if map.img_bool[row][col]:
                    print('find!!:{0}, {1}'.format(row, col))
                    return map.matrix_to_posi(row, col)
            r+= 1

            print('error, any obsutacle around the pedestrian not find....')
            '''

        min_distance = 1000.
        for row, col in itertools.product(range(map.height), range(map.width)):
            if map.img_bool[row][col]:
                map_x, map_y = map.matrix_to_posi(row, col)
                distance = np.linalg.norm([map_x - self.position[0], map_y - self.position[1]])
                if distance < min_distance:
                    min_distance = distance
                    min_row = row
                    min_col = col

        if min_distance > 999:
            print('error: no neighborhood pixel found')

        return map.matrix_to_posi(min_row, min_col)



    def calc_f_pedestrian(self, pedestrians):
        for pedestrian in pedestrians:
            distance = np.linalg.norm(self.position - pedestrian.position)
            print('distance:{0}'.format(distance))

        # calc force from the other pedestrians
        return [0, 0]

    def calc_f_destination(self):
        # calc force from destination
        # unit vector for desired direction
        e_a = (self.subgoal - self.position) / np.linalg.norm(self.subgoal - self.position)
        f_destination = (self.desired_velocity * e_a - self.velocity) / self.tau
        # print('desired_vel:{0}, e_a:{1}'.format(self.desired_velocity, e_a))
        print('f_destination:{0}'.format(f_destination))

        self.f_destination = f_destination
        return f_destination
