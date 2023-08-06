import numpy as np
import pandas as pd

from hawkeye.physical.measurables.Measurable import Length,  Angle
from hawkeye.physical.acousticlosses.propagation.sound_speed_profile import Sound_Speed_Gradient
from hawkeye.physical.geometry.CartesianCoordinate import CartesianCoordinate


class ThreeDimensionalRayTracing:
    """
    This class contains the definition for the propagation from one location through a medium using the equations and
    code contained in P. A. Einstein, "Underwater sonic ray tracing in three dimensions", Journal of Sound and Vibration
    43(4), 503-508, 1975.
    """

    def __init__(self, sound_speed: Sound_Speed_Gradient = None, x0: CartesianCoordinate = None):
        """
        The constructor that establishes the starting point for the acoustic ray and the sound speed profile for the
        ray's origin.

        :param sound_speed: Sound_Speed_Gradient - the class that defines the sound speed gradient calculation class
        :param x0: CartesianCoordinate - this is the starting point for the ray
        """

        self.sound_speed = sound_speed
        self.ray_start = x0

    @property
    def ray_start_position(self):
        return self.ray_start

    @ray_start_position.setter
    def ray_start_position(self, value: CartesianCoordinate):
        self.ray_start = value

    @property
    def sound_speed_gradient_calculator(self):
        return self.sound_speed

    @sound_speed_gradient_calculator.setter
    def sound_speed_gradient_calculator(self, value: Sound_Speed_Gradient):
        self.sound_speed = value

    def propagate(self, a0: Angle, b0: Angle, c0: Angle, maximum_ray_length: Length, count: int = 900):
        """
        This function moves through the medium's profile in the initial direction using the starting position and the
        sound speed profile class that was previously specified.

        :param a0: Angle - the initial direction cosine for the X-direction
        :param b0: Angle - the initial direction cosine for the Y-direction
        :param c0: Angle - the initial direction cosine for the Z-direction
        :param maximum_ray_length: Length - the maximum length before terminating the algorithm
        :param count: int - the maximum number of segments in the array before terminating the algorithm
        """

        a1 = a0.cos()
        b1 = b0.cos()
        c1 = c0.cos()
        t = 0
        s1 = maximum_ray_length / count

        data = pd.DataFrame(columns=['index', 'time', 'x', 'y', 'z', 'c0', 'dcdx', 'dcdy', 'dcdz'])

        location = self.ray_start
        for i in range(count):
            #   Get the velocity and gradients

            v, g1, g2, g3 = self.sound_speed.calculate_sound_speed_profile(location)

            data = data.append({'index': i,
                                'time': t,
                                'x': location.x.meters,
                                'y': location.y.meters,
                                'z': location.z.meters,
                                'c0': c0,
                                'dcdx': g1,
                                'dcdy': g2,
                                'dcdz': g3},
                               ignore_index=True)

            #   Calculate the resultant vector for the gradient components

            g4 = np.sqrt(g1 ** 2 + g2 ** 2 + g3 ** 2)

            #   Recalculate the direction cosines

            a2 = g1 / g4
            b2 = g2 / g4
            c2 = g3 / g4

            w1 = a1 * a2 + b1 * b2 + c1 * c2

            #   Increment the time

            t += (s1 / v).total_seconds()

            #   Determine the differential length along the ray

            l2 = s1.meters ** 2 * g4 / 2 / v.meters_per_second
            p2 = np.sqrt(s1.meters ** 2 + l2 ** 2 + 2 * s1.meters * l2 * w1)
            x1 = p2 * a1 - l2 * a2
            y1 = p2 * b1 - l2 * b2
            z1 = p2 * c1 - l2 * c2

            q1 = np.sqrt(x1 ** 2 + y1 ** 2 + z1 ** 2)

            r = v / g4 / (np.sqrt(1 - w1 ** 2) + 0.000001)

            t2 = (s1 / 2 / r).total_seconds()
            t1 = q1 / 2 / np.cos(t2)

            x3 = location.x.meters + t1 * a1
            y3 = location.y.meters + t1 * b1
            z3 = location.z.meters + t1 * c1

            location.x += Length(x1)
            location.y += Length(y1)
            location.z += Length(z1)

            #   Calculate the new direction cosines

            a1 = (location.x.meters - x3) / t1
            b1 = (location.y.meters - y3) / t1
            c1 = (location.z.meters - z3) / t1

            #   Check for reflections at the surface

            if location.x.meters < 0:
                a1 *= -1
                location.x *= -1

        return data
