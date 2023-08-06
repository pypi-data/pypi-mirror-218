from hawkeye.physical.geometry.CartesianCoordinate import CartesianCoordinate
from hawkeye.physical.measurables.Measurable import Speed


class Sound_Speed_Gradient:
    """
    This class houses a series of functions that will be used to determine the ray path from one point in space to
    another as defined by the CartesianCoordinates.  This is the base class and the programmer is required to implement
    their own function representation.  The code here is based on the underwater equations defined within P. A.
    Einstein, "Underwater sonic ray tracing in three dimensions", Journal of Sound and Vibration 43(4), 503-508, 1975.
    """

    def calculate_sound_speed_profile(self, x0: CartesianCoordinate):
        """
        Using the location of the start of the ray, x0, this function calculates the sound speed, and the 3-D grdients
        for the sound speed in the Cartesian coordinate directions
        """

        x = x0.x.meters
        y = x0.y.meters
        z = x0.z.meters

        c0 = Speed((1510 + 0.0135 * x - 2.2e-5 * x ** 2 + 8e-9 * x ** 3) * (1 + 2e-6 * y) *
                   (1 - 3e-6 * z + 5e-13 * z ** 2), Speed.Units.MetersPerSecond)
        dcdx = (0.0135 - 2.2e-5 * 2 * x + 8e-9 * 3 * x ** 2) * (1 + 2e-6 * y) * (1 - 3e-6 * z + 5e-13 * z ** 2)
        dcdy = (1510 + 0.0135 * x - 2.2e-5 * x ** 2 + 8e-9 * x ** 3) * 2e-6 * (1 - 3e-6 * z + 5e-13 * z ** 2)
        dcdz = (1510 + 0.0135 * x - 2.2e-5 * x ** 2 + 8e-9 * x ** 3) * (1 + 2e-6 * y) * (-3e-6 + 5e-13 * 2 * z)

        return c0, dcdx, dcdy, dcdz
