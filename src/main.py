# coding=utf-8
from sfm_simulator import SFMSimulator

sfm_simulator = SFMSimulator("maps/mikawalab.pgm", "maps/mikawalab.yaml",
                             zoom=2, dt=0.05, sim_speed=0.2)
sfm_simulator.debug()

