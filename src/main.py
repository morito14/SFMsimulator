# coding=utf-8
from sfm_simulator import SFMSimulator

sfm_simulator = SFMSimulator("maps/mikawalab.pgm", "maps/mikawalab.yaml",
                             zoom=3, dt=0.05, sim_speed=1.)
sfm_simulator.debug()


