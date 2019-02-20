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
        self.desired_velocity = 1.34  # [m/s]
        self.v_max = self.desired_velocity * 1.3  # [m/s]
        self.tau = 0.1  # relaxation time
        # for calc_f_wall
        self.w_Uab = 10.  # [m^2s^-2]
        self.w_R = 0.2  # [m]
        # for calc_f_pedestrian
        self.p_Vab = 2.1  # [m^2s^-2]
        self.p_sigma = 0.3  # [m]
        self.p_predict_t = 1.2  # [sec]
        self.p_phi = 100  # [degree]
        self.p_phi_cos = np.cos(np.deg2rad(self.p_phi))
        self.p_c = 0.5  # weight factor


        print('generated pedestrian')

    def set_status(self, **kwargs):
        # set_status
        if 'desired_velocity' in kwargs:
            self.desired_velocity = kwargs['desired_velocity']

        print('set -> desired_velocity:{0}'.format(self.desired_velocity))
        super(Pedestrian, self).set_status(**kwargs)

    def update_velocity(self, dt):
        # update_velocity
        # wa: preferred velocity
        wa = self.velocity + self.f_total * dt
        wa_norm = np.linalg.norm(wa)
        g_result = 1. if wa_norm <= self.v_max else self.v_max / wa_norm
        self.velocity = wa * g_result

    def update_position(self, dt):
        # update position
        #print('update vel:{0}, dt:{1}'.format(self.velocity, dt))
        self.position = self.position + (self.velocity * dt)

    def calc_f_total(self, pedestrians, slam_map):
        # get total force
        self.calc_f_wall(slam_map)
        self.calc_f_pedestrian(pedestrians)
        self.calc_f_destination()
        # print('f_wall:{0}, f_pedestrian:{1}, f_destination:{2}'.format(self.f_wall, self.f_pedestrian, self.f_destination))

        self.f_total = self.f_wall + self.f_pedestrian + self.f_destination

    def calc_f_wall(self, map):
        # calc force from wall
        self.closest_wall[0], self.closest_wall[1] = self.find_closest_wall(map)
        # self.closest_wall[0], self.closest_wall[1] = 0, 0  # for debug
        # print('closest wall:({0}, {1})'.format(self.closest_wall[0], self.closest_wall[1]))

        r_ab = self.position - self.closest_wall
        # print('r_ab:{0}'.format(r_ab))
        result, vx, vy = self.func_w_U(r_ab)
        # print('wall vx, vy:({0}, {1})'.format(vx, vy))

        self.f_wall[0] = vx
        self.f_wall[1] = vy

        return vx, vy

    def func_w_U(self, r_ab):
        # calc potential of Wall
        norm = np.linalg.norm(r_ab)
        if norm < 0.0001:
            print('pedestrian is on the wall....')
            return 0, 0, 0

        result = self.w_Uab * np.exp(-norm / self.w_R)
        # -grad(w_U)
        vx = ((self.w_Uab * r_ab[0]) / (self.w_R * norm)) * np.exp(-norm / self.w_R)
        vy = ((self.w_Uab * r_ab[1]) / (self.w_R * norm)) * np.exp(-norm / self.w_R)



        return result, vx, vy



    def find_closest_wall(self, map):
        # find nearest wall in map
        '''
        # L1 norm (guruguru)
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

        """
        # zentansaku
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
        """

        min_distance = 1000.
        for x, y in map.walls:
            distance = ((x - self.position[0]) ** 2) + ((y - self.position[1]) ** 2)
            if distance < min_distance:
                min_distance = distance
                min_x = x
                min_y = y

        return min_x, min_y




    def calc_f_pedestrian(self, pedestrians):
        print('start calc....')
        epsilon = 0.001
        f_total = np.zeros(2)
        for pedestrian in pedestrians:
            r_ab = self.position - pedestrian.position
            if 0.0001 < (r_ab[0] ** 2) + (r_ab[1] ** 2):
                # partial differential
                vx_tmp1 = - self.func_V_ab(r_ab + [epsilon, 0.], pedestrian)
                vx_tmp2 = - self.func_V_ab(r_ab - [epsilon, 0.], pedestrian)
                vy_tmp1 = - self.func_V_ab(r_ab + [0., epsilon], pedestrian)
                vy_tmp2 = - self.func_V_ab(r_ab - [0., epsilon], pedestrian)
                f_tmp = np.array([(vx_tmp1 - vx_tmp2) / (2. * epsilon), (vy_tmp1 - vy_tmp2) / (2. * epsilon)])
                f_total = f_total + (self.func_w(self.e_a, -f_tmp) * f_tmp)
                print('f_tmp:{0}'.format(f_tmp))

                # print('my_posi:{0}, b_posi:{1}, result:{2}'.format(self.position, pedestrian.position, result))
                # print('distance:{0}'.format(distance))
        self.f_pedestrian = f_total

    def func_w(self, e_a, f_ab):
        # weight function for viewing angle
        if np.dot(e_a, f_ab) >= np.linalg.norm(f_ab) * self.p_phi_cos:
            print('in viewing angle!!!')
            return 1.
        else:
            print('NOT in viewing angle!!!')
            return self.p_c

    def func_V_ab(self, r_ab, pedestrian_b):
        # calc potential of pedestrians
        norm = np.linalg.norm(r_ab)
        if norm < 0.001:
            print('error: two pedestrians are on the same position...')
            return 100.

        vb = np.linalg.norm(pedestrian_b.velocity)
        b = (((norm + np.linalg.norm(r_ab - vb * self.p_predict_t * pedestrian_b.e_a)) ** 2
              - (vb * self.p_predict_t) ** 2) ** 0.5) / 2.
        result = self.p_Vab * np.exp(-b / self.p_sigma)

        return result


    def calc_f_destination(self):
        # calc force from destination
        # unit vector for desired direction
        self.e_a = (self.subgoal - self.position) / np.linalg.norm(self.subgoal - self.position)
        f_destination = (self.desired_velocity * self.e_a - self.velocity) / self.tau
        # print('desired_vel:{0}, e_a:{1}'.format(self.desired_velocity, e_a))
        # print('f_destination:{0}'.format(f_destination))

        # exception handling when pedestrian is on his/her sub-goal
        if np.linalg.norm(self.subgoal - self.position) < 0.1:
            f_destination[0] = 0
            f_destination[1] = 0

        self.f_destination = f_destination
        return f_destination
