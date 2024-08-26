# --------
# Imports:
# --------

# Third Party:
import numpy as np
from scipy.integrate import solve_ivp
from pathlib import Path
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

# First Party:
from hammer_structure import HammerStructure
from plotting.plotting import plot_mult

# ----------
# Constants:
# ----------

G_ACCEL = 9.81 # Gravitational Acceleration [m/s^2]

# -----
# Code:
# -----

class HammerSimulation:
    initial_conditions = [np.deg2rad(179), 0]
    ODE_func = None
    dt = 0.001 # s
    duration = 100 # s
    sol = None

    def __init__(self, structure_json_filename):
        json_filepath = os.path.join(os.path.dirname(__file__), structure_json_filename)
        self.hammer_structure = HammerStructure(json_filepath)
    
    def configure_ODE_func(self, ODE_func):
        self.ODE_func = ODE_func
    
    def run_sim(self):
        if self.ODE_func == None:
            print("You must configure the simulation before running it")
            return
        def event(t,y):
            return y[0];
        event.terminal = True
        self.sol = solve_ivp(self.ODE_func, [0, self.duration], (self.initial_conditions[0], self.initial_conditions[1]), t_eval = np.linspace(0, self.duration, round(self.duration/self.dt)), events=event)

    def get_t(self):
        if self.sol == None:
            print("You must run the simulation before attempting to access its parameters")
            return
        return self.sol.t
    
    def get_theta_deg(self):
        if self.sol == None:
            print("You must run the simulation before attempting to access its parameters")
            return
        return np.rad2deg(self.sol.y[0])
    
    def get_theta_dot_deg(self):
        if self.sol == None:
            print("You must run the simulation before attempting to access its parameters")
            return
        return np.rad2deg(self.sol.y[1])
    
    def get_speeds(self):
        if self.sol == None:
            print("You must run the simulation before attempting to access its parameters")
            return
        return abs(np.deg2rad(self.get_theta_dot_deg())) * self.hammer_structure.L_arm     # m/s

    def get_max_speed(self):
        if self.sol == None:
            print("You must run the simulation before attempting to access its parameters")
            return
        return max(self.get_speeds())     # m/s

    def plot_speed_and_angle(self, title):
        if self.sol == None:
            print("You must run the simulation before attempting to access its parameters")
            return
        plot_mult(self.get_t(), [self.get_theta_deg(), self.get_speeds()], "Time [s]", [r'$\theta$', r'Speed [m/s]'], title)


class SimpleHammerSimulation(HammerSimulation):
    def __init__(self,structure_json_filename):
        super().__init__(structure_json_filename)

        def hammer_ODE(t, y):
            ang_deriv = y[1]
            ang_vel_deriv = - G_ACCEL * np.sin(y[0]) / self.hammer_structure.L_arm
            return ang_deriv, ang_vel_deriv
        
        self.configure_ODE_func(hammer_ODE)

class TorsionalSpringSimulation(HammerSimulation):
    def __init__(self,structure_json_filename, max_torque, rad_range):
        super().__init__(structure_json_filename)

        def hammer_ODE(t, y):
            k_s = max_torque / rad_range #N/rad
            ang_equil = np.pi - rad_range
            ang_deriv = y[1]
            ang_vel_deriv = (-1 * k_s * (y[0] - ang_equil)) / self.hammer_structure.get_moment_of_inertia() - (G_ACCEL * np.sin(y[0]))/ self.hammer_structure.L_arm
            return ang_deriv, ang_vel_deriv

        self.configure_ODE_func(hammer_ODE)

class MotorizedHammerSimulation(HammerSimulation):
    def __init__(self,structure_json_filename, torque_func):
        super().__init__(structure_json_filename)
        
        def hammer_ODE(t, y):
            motor_torque = torque_func(y[1])
            ang_deriv = y[1]
            ang_vel_deriv = -1 * motor_torque / self.hammer_structure.get_moment_of_inertia() - (G_ACCEL * np.sin(y[0]))/ self.hammer_structure.L_arm
            return ang_deriv, ang_vel_deriv

        self.configure_ODE_func(hammer_ODE)