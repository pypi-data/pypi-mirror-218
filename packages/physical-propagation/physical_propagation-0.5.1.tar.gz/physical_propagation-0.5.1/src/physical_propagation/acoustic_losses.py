import math
import cmath
import numpy as np
from PythonCoordinates.conversions.Physics import Physics
from PythonCoordinates.measurables.physical_quantities import Humidity, Temperature, Pressure, Length, Angle, Speed
from PythonCoordinates.measurables.Measurable import InvalidUnitOfMeasureException
from PythonCoordinates.coordinates.geospatial_coordinates import CartesianCoordinate


class AtmosphericAbsorption:
    """
    Thus class contains the function required to determine the atmospheric absorption attenuation as a function of
    distance, temperature, pressure, humidity, and frequency.  The equations are from research published by Bass et al.
    """
    @staticmethod
    def oxygen_relaxation_frequency(pressure, molar_concentration):
        """
        Determine the relaxation frequency of oxygen molecules

        pressure : Pressure
            the atmospheric pressure
        molar_concentration : double
            the molar concentration of water vapor

        returns : double
            the relaxation frequency for the vibration of oxygen molecules.
        """
        if isinstance(pressure, Pressure):
            fro = 4.04e4 * molar_concentration
            fro *= 0.02 + molar_concentration
            fro /= 0.391 + molar_concentration
            fro += 24
            fro *= pressure / Pressure.ref_pressure()
            return fro
        else:
            raise InvalidUnitOfMeasureException

    @staticmethod
    def nitrogen_relaxation_frequency(temperature, pressure, molar_concentration):
        """
        Determine the relaxation frequency of nitrogen molecules

        temperature : Temperature
            the temperature of the air through which the sound is propagating
        pressure : Pressure
            the atmospheric pressure
        molar_concentration : double
            the molar concentration of water vapor

        returns : double
            the relaxation frequency for the vibration of nitrogen molecules.
        """
        if isinstance(temperature, Temperature) and isinstance(pressure, Pressure):
            frn = math.exp(-4.170 * (math.pow(temperature.value / Temperature.ref_temperature().value, -1.0 / 3.0) - 1))
            frn *= 280 * molar_concentration
            frn += 9.0
            frn *= pressure / Pressure.ref_pressure()
            frn *= math.sqrt(Temperature.ref_temperature().value / temperature.value)
            return frn
        else:
            raise InvalidUnitOfMeasureException

    @staticmethod
    def alpha(temperature, pressure, humidity, frequency, s=None):
        """
        Determine the acoustic losses as a function of frequency for the propagation through a real atmosphere.  This
        amounts to a low pass filter.

        temperature : Temperature
            the temperature of the air through which the sound is propagating
        pressure : Pressure
            the atmospheric pressure
        humidity : Humidity
            the relative humidity of the atmosphere
        frequency : double
            the frequency of sound that will be calculated in Hz
        s : Pressure Saturation function that determines how to calculate the saturation of the air

        returns : double
            the atmospheric loses in dB / m
        """

        if isinstance(temperature, Temperature) and isinstance(pressure, Pressure) and isinstance(humidity, Humidity):
            if s is not None:
                molar_concentration = Physics.molar_concentration_water_vapor(pressure, humidity, temperature, s)
                fro = AtmosphericAbsorption.oxygen_relaxation_frequency(pressure, molar_concentration)
                frn = AtmosphericAbsorption.nitrogen_relaxation_frequency(temperature, pressure, molar_concentration)

                ao = fro / (fro * fro + frequency * frequency)
                an = frn / (frn * frn + frequency * frequency)

                a = 0.01275 * ao * math.exp(-2239.1 / temperature.kelvin)
                a += 0.1068 * an * math.exp(-3352.0 / temperature.kelvin)
                a *= math.pow(Temperature.ref_temperature().value / temperature.value, 5.0 / 2.0)
                a += 1.84e-11 * (Pressure.ref_pressure().value / pressure.value) * \
                     np.sqrt(temperature.value / Temperature.ref_temperature().value)
                a *= 8.686 * frequency * frequency
                return a
            else:
                if not isinstance(frequency, list):
                    return AtmosphericAbsorption.alpha(temperature, pressure, humidity, frequency,
                                                       Physics.build_psat_ratio(temperature))
                else:
                    molar_concentration = Physics.molar_concentration_water_vapor(
                        pressure, humidity, temperature, Physics.build_psat_ratio_old(temperature))
                    fro = AtmosphericAbsorption.oxygen_relaxation_frequency(pressure, molar_concentration)
                    frn = AtmosphericAbsorption.nitrogen_relaxation_frequency(
                        temperature, pressure, molar_concentration)
                    result = np.zeros((len(frequency)))
                    for index in range(0, len(frequency), 1):
                        freq = frequency[index]
                        ao = fro / (fro * fro + freq * freq)
                        an = frn / (frn * frn + freq * freq)

                        a = 0.01275 * ao * math.exp(-2239.1 / temperature.kelvin)
                        a += 0.1068 * an * math.exp(-3352.0 / temperature.kelvin)
                        a *= math.pow(Temperature.ref_temperature().value / temperature.value, 5.0 / 2.0)
                        a += 1.84e-11 * (Pressure.ref_pressure().value / pressure.value) * math.sqrt(
                            temperature.value / Temperature.ref_temperature().value)
                        a *= 8.686 * freq * freq
                        result[index] = a

                    return result


class Divergence:

    @staticmethod
    def loss(reference, distance):
        """
        This function computes the spherical spreading losses for the acoustic propagation from a reference distance to
        the specified distance.

        @author: Frank Mobley

        reference : Length
            The distance from the measurement of the sound pressure level
        distance :  Length
            The distance from the center of the sphere to the observation point
        returns: the frequency independent loss over this distance
        """

        if not (isinstance(reference, Length) and isinstance(distance, Length)):
            raise InvalidUnitOfMeasureException

        return -20 * np.log10(distance.meters / reference.meters)


class DigitalFeatureAttributeData:
    """
    To implement the calculation of the ground impedance model, the RNM 7.1 Reference and User Manual creates a chart
    that references the Digital Feature Attribute Data (DFAD). In this table they create a standardized list of the
    features within the DFAD descriptions and assign a single parameters, surface flow resisitivity. This class will
    hold a single element of this table for later use.
    """
    def __init__(self, code, flow_resistivity, description, notes):
        """
        Create the class with the information within Table 4-32.
        """

        self._code = code
        self._resistivity = flow_resistivity
        self._description = description
        self._notes = notes

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = value

    @property
    def flow_resistivity(self):
        return self._resistivity

    @flow_resistivity.setter
    def flow_resistivity(self, value):
        self._resistivity = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, value):
        self._notes = value

    @staticmethod
    def dfad_attribute_table():
        table = list()

        table.append(DigitalFeatureAttributeData(325, 225, "Athletic Field", "Grass"))
        table.append(DigitalFeatureAttributeData(334, 30000, "Artificial Mountain", "Concrete"))
        table.append(DigitalFeatureAttributeData(706, 30000, "Airport Runways", "Concrete"))
        table.append(DigitalFeatureAttributeData(707, 30000, "Aircraft Parking", "Concrete"))
        table.append(DigitalFeatureAttributeData(830, 30000, "Open Storage", "Concrete"))
        table.append(DigitalFeatureAttributeData(862, 30000, "Vehicle Storage", "Concrete"))
        table.append(DigitalFeatureAttributeData(863, 30000, "Vehicle Parking", "Concrete"))
        table.append(DigitalFeatureAttributeData(864, 650, "Aircraft Storage", "Dirt"))
        table.append(DigitalFeatureAttributeData(865, 225, "Ship Storage", "Water or Dirt"))
        table.append(DigitalFeatureAttributeData(901, 650, "Ground surface", "Dirt"))
        table.append(DigitalFeatureAttributeData(902, 650, "Soil", "Dirt"))
        table.append(DigitalFeatureAttributeData(906, 1650, "Sand/Desert", "Sand"))
        table.append(DigitalFeatureAttributeData(907, 1650, "Sand Dunes", "Sand"))
        table.append(DigitalFeatureAttributeData(908, 90000, "Marsh/Swamp", "Water/Dirt"))
        table.append(DigitalFeatureAttributeData(909, 100000, "Rice Paddies", "Water"))
        table.append(DigitalFeatureAttributeData(910, 30000, "Smooth, Solid Rock", "Rock"))
        table.append(DigitalFeatureAttributeData(911, 30000, "Boulder Field/Lava", "Rock"))
        table.append(DigitalFeatureAttributeData(912, 30000, "Rocky, Rough Surface", "Rock"))
        table.append(DigitalFeatureAttributeData(913, 5000, "Dry Lake", "Packed Dirt"))
        table.append(DigitalFeatureAttributeData(914, 90000, "Mud/Tidal Flats", "Water/Dirt"))
        table.append(DigitalFeatureAttributeData(915, 1650, "Islands", "Sand"))
        table.append(DigitalFeatureAttributeData(930, 1000000, "Salt Water", "Water"))
        table.append(DigitalFeatureAttributeData(931, 1000000, "Salt Water, Sea State", "Water"))
        table.append(DigitalFeatureAttributeData(932, 1000000, "Salt Water, Sea State, Subject to Ice", "Water"))
        table.append(DigitalFeatureAttributeData(933, 1000000, "Salt Water, Subject to Ice", "Water"))
        table.append(DigitalFeatureAttributeData(934, 100000, "Salt Pans", "Water"))
        table.append(DigitalFeatureAttributeData(940, 1000000, "Fresh Water (General)", "Water"))
        table.append(DigitalFeatureAttributeData(941, 10000000, "Fresh Water, Sea State", "Water"))
        table.append(DigitalFeatureAttributeData(942, 1000000, "Fresh Water, Sea State, Subject to Ice", "Water"))
        table.append(DigitalFeatureAttributeData(943, 1000000, "Fresh Water, Subject to Ice", "Water"))
        table.append(DigitalFeatureAttributeData(950, 40, "Vegetation (General)", "Trees"))
        table.append(DigitalFeatureAttributeData(951, 50, "Orchards/Hedgerows", "Trees"))
        table.append(DigitalFeatureAttributeData(952, 60, "Deciduous Tress", "Trees"))
        table.append(
            DigitalFeatureAttributeData(953, 60, "Evergreen Trees (Including Nipa Palm and Mangrove)", "Trees"))
        table.append(DigitalFeatureAttributeData(954, 60, "Mixed Trees (Deciduous and Evergreen)", "Trees"))
        table.append(DigitalFeatureAttributeData(955, 225, "Tundra", "Grass"))
        table.append(DigitalFeatureAttributeData(956, 200, "Vineyards ", ""))
        table.append(DigitalFeatureAttributeData(960, 20000, "Snow/Ice Areas (General)", "Packed Snow"))
        table.append(DigitalFeatureAttributeData(961, 20000, "Permanent Snow", "Packed Snow"))
        table.append(DigitalFeatureAttributeData(962, 90000, "Permanent Snow, Glacier/Ice Cap", "Ice"))
        table.append(DigitalFeatureAttributeData(963, 90000, "Pack Ice (Temporary)", "Ice or Water"))
        table.append(DigitalFeatureAttributeData(964, 90000, "Polar Ice Pack (Permanent)", "Ice"))
        table.append(DigitalFeatureAttributeData(965, 90000, "Pack Ice (Temporary)", "Ice or Water"))
        table.append(DigitalFeatureAttributeData(966, 90000, "Pack Ice (Temporary)", "Ice or Water"))
        table.append(DigitalFeatureAttributeData(967, 90000, "Pack Ice (Temporary)", "Ice or Water"))

        return table


class GroundImpedance:
    """
    This class provides the calculation of the single parameter for description of the surface reflectance of the ground
    using the method provided by Delany in Delany, M. E., & Bazley, E. N. (1970). Acoustical properties of fibrous
    absorbent materials. Applied acoustics, 3(2), 105-116 and Delany, M. E., & Bazley, E. N. (1971). A note on the
    effect of ground absorption in the measurement of aircraft noise. Journal of sound and vibration, 16(3), 315-322.
    """

    @staticmethod
    def delany_single_parameter(frequency, flow_resistivity):
        """
        The actual calculation based on the published equations.

        frequency : double
            The number of cycles per second of the sound interfacing with the ground surface
        flow_resistivity : double
            The surface flow resistivity (the single parameter) with units kPa s m^-2

        @author: Frank Mobley
        """

        x = 1 + 9.08 * (frequency / flow_resistivity) ** -0.75
        y = 11.9 * (frequency / flow_resistivity) ** -0.73

        return complex(x, y)

    @staticmethod
    def standard_flow_resisitivity():
        sigma = dict()


class ExcessGroundAttenuation:
    """
    This is a collection of functions for the purpose of calculating the acoustic loss using the grazing incidence of a
    sound wave on a pseudo-infinite semi-permeable reflective surface
    """

    @staticmethod
    def incoherent_attenuation(direct_path_length, reflected_path_length, grazing_angle, frequency, surface_impedance,
                               sound_speed, turbulence):
        """
        Calculate the coherent (without turbulent mixing of the atmosphere) excess ground attenuation loss based on the
        equations in Chessell, C. I. (1977). Propagation of noise along a finite impedance boundary. The Journal of the
        Acoustical Society of America, 62(4), 825-834..

        direct_path_length : Length
            the length of the path from the source to the receiver that is direct
        reflected_path_length : Length
            the path length from the source to the ground to the receiver
        grazing_angle : Angle
            the angle between the reflected ray and the ground on the source side of the reflection point
        frequency : double
            the sound frequency propagating through the atmosphere
        surface_impedance : double
            the single parameter required to calculate the surface reactance to the sound incident
        sound_speed : Speed
            the adiabatic speed of sound
        turbulence : double
            the turbulence factor - if turbulence = 0, this function returns the same value as the
            coherent_attenuation

        returns : double
            the excess ground attenuation based on the equations of Chessell, C. I. (1977). Propagation of noise along a
            finite impedance boundary. The Journal of the Acoustical Society of America, 62(4), 825-834. that describe
            the propagation
        """

        #   Ensure that the input arguments possess the correct units and types

        if not isinstance(direct_path_length, Length) or not isinstance(reflected_path_length, Length):
            raise InvalidUnitOfMeasureException
        if not isinstance(grazing_angle, Angle):
            raise InvalidUnitOfMeasureException
        if not isinstance(sound_speed, Speed):
            raise InvalidUnitOfMeasureException

        #   Convert to angular frequency

        w = 2 * np.pi * frequency

        #   calculate the spherical wave reflection coefficient

        q = ExcessGroundAttenuation.spherical_wave_reflection_coefficient(w, sound_speed, surface_impedance,
                                                                          grazing_angle, reflected_path_length)

        #   The path length difference

        del_r = reflected_path_length - direct_path_length

        #   the wave number

        k1 = w / sound_speed.meters_per_second

        #   Get the magnitude and phase of the spherical wave reflection coefficient

        abs_q = abs(q)
        theta = cmath.phase(q)

        #   Build the elements of the incoherent equation

        cos_angle = np.cos(k1 * del_r.meters + theta)
        r_prime = reflected_path_length / direct_path_length
        sigma_path_length = turbulence * frequency * np.sqrt(direct_path_length.meters)

        return 10 * np.log10(1 + (1/(r_prime**2)) * abs_q ** 2 +
                             (2 / r_prime) * abs_q * cos_angle * np.exp(-0.5 * sigma_path_length**2))

    @staticmethod
    def coherent_attenuation(direct_path_length, reflected_path_length, grazing_angle, frequency, surface_impedance,
                             sound_speed):
        """
        Calculate the coherent (without turbulent mixing of the atmosphere) excess ground attenuation loss based on the
        equations in Chessell, C. I. (1977). Propagation of noise along a finite impedance boundary. The Journal of the
        Acoustical Society of America, 62(4), 825-834.

        direct_path_length : Length
            the length of the path from the source to the receiver that is direct
        reflected_path_length : Length
            the path length from the source to the ground to the receiver
        grazing_angle : Angle
            the angle between the reflected ray and the ground on the source side of the reflection point
        frequency : double
            the sound frequency propagating through the atmosphere
        surface_impedance : double
            the single parameter required to calculate the surface reactance to the sound incident
        sound_speed : Speed
            the adiabatic speed of sound

        returns : double
            the excess ground attenuation based on the equations of Chessell(1971) that describe the propagation without
            wind
        """

        #   Ensure that the input arguments possess the correct units and types

        if not isinstance(direct_path_length, Length) or not isinstance(reflected_path_length, Length):
            raise InvalidUnitOfMeasureException
        if not isinstance(grazing_angle, Angle):
            raise InvalidUnitOfMeasureException
        if not isinstance(sound_speed, Speed):
            raise InvalidUnitOfMeasureException

        # convert frequency to angular frequency

        w = 2 * np.pi * frequency

        # Determine the spherical wave reflection coefficient

        q = ExcessGroundAttenuation.spherical_wave_reflection_coefficient(
            w,
            sound_speed,
            surface_impedance,
            grazing_angle,
            reflected_path_length)

        # compute the path length difference

        del_r = reflected_path_length - direct_path_length

        # The wave number

        k1 = w / sound_speed.meters_per_second

        complex_one = complex(1, 0)
        complex_imaginary_one = complex(0, 1)

        pressure = complex_one + ((direct_path_length / reflected_path_length) * q *
                                  cmath.exp(complex_imaginary_one * del_r.meters * k1))

        return 20 * np.log10(abs(pressure))

    @staticmethod
    def determine_geometry(source, receiver):
        """
        This function determines the geometry in the most efficient of the multitude of ways provided

        source : CartesianCoordinate
            The location of the source of the acoustic energy
        receiver : CartesianCoordinate
            The location of the receiver of the acoustic energy

        returns: the direct path length, reflected path length, and the angle between the reflected path and the ground
        """

        if not (isinstance(source, CartesianCoordinate) and isinstance(receiver, CartesianCoordinate)):
            raise InvalidUnitOfMeasureException

        direct_path_length = source.__sub__(receiver).length

        v1 = receiver.__sub__(source)
        v2 = receiver.__add__(source)

        reflected_path_length = Length(np.sqrt(v1.x.meters ** 2 + v1.y.meters ** 2 + v2.z.meters ** 2))

        grazing_angle = Angle(np.arctan2(source.z.meters + receiver.z.meters,
                                         np.sqrt(v1.x.meters ** 2 + v1.y.meters ** 2)),
                              Angle.Units.Radians)

        return direct_path_length, reflected_path_length, grazing_angle

    @staticmethod
    def spherical_wave_reflection_coefficient(w, c, z, grazing_angle, reflection_path_length):
        """
        Modification of the plane wave reflection coefficient that represents the more accurate spherical wavefronts.

        w : double
            the angular frequency
        c : Speed
            the sound speed
        z : complex
            the surface impedance
        grazing_angle : Angle
            the angle between the reflected ray and the ground on the source side of the geometry
        reflection_path_length : Length
            the distance from the source to the ground to the receiver

        returns : complex
            the portion of the sound energy that will be absorbed by the surface
        """
        if not isinstance(grazing_angle, Angle):
            raise InvalidUnitOfMeasureException
        if not isinstance(reflection_path_length, Length):
            raise InvalidUnitOfMeasureException
        if not isinstance(z, complex):
            raise RuntimeError
        if not isinstance(c, Speed):
            raise InvalidUnitOfMeasureException

        plane_wave_reflection = ExcessGroundAttenuation.plane_wave_reflection_coefficient(grazing_angle, z)
        numerical_distance = ExcessGroundAttenuation.numerical_distance(w, c, z, grazing_angle, reflection_path_length)
        boundary_loss = ExcessGroundAttenuation.boundary_loss_factor(numerical_distance)

        return plane_wave_reflection + boundary_loss * (1 - plane_wave_reflection)

    @staticmethod
    def plane_wave_reflection_coefficient(grazing_angle, z):
        """
        Reflection coefficients for plane waves

        grazing_angle : Angle
            the angle between the reflected ray and the ground on the source side
        z : complex
            the surface impedance

        returns : complex
            the reflected portion of the incident plane wave
        """
        if not isinstance(grazing_angle, Angle):
            raise InvalidUnitOfMeasureException

        if not isinstance(z, complex):
            raise ArithmeticError

        sin_ang = grazing_angle.sin()

        beta = 1 / z

        return (sin_ang - beta) / (sin_ang + beta)

    @staticmethod
    def boundary_loss_factor(numerical_distance):
        """
        Examine the evanescent wave that travels along the ground boundary

        numerical_distance : complex
            the calculated numerical distance

        returns : complex
            The portion of the sound energy that travels along the ground boundary
        """
        return 1 + complex(0, 1) * np.sqrt(np.pi) * numerical_distance * \
            ExcessGroundAttenuation.erfc(numerical_distance)

    @staticmethod
    def numerical_distance(w, c, z, grazing_angle, reflection_path_length):
        """
        Determine the numerical distance element of the ground reflection that is associated with the ground wave.

        w : double
            the angular frequency
        c : Speed
            the sound speed
        z : complex
            the surface impedance
        grazing_angle : Angle
            the angle between the reflected ray and the ground on the source side of the geometry
        reflection_path_length : Length
            the distance from the source to the ground to the receiver

        returns : complex
            the numerical distance that is an input to the boundary loss factor
        """

        if not isinstance(grazing_angle, Angle):
            raise InvalidUnitOfMeasureException
        if not isinstance(reflection_path_length, Length):
            raise InvalidUnitOfMeasureException
        if not isinstance(z, complex):
            raise RuntimeError
        if not isinstance(c, Speed):
            raise InvalidUnitOfMeasureException

        cos_ang = np.cos(np.pi / 2 - grazing_angle.radians)

        beta = 1 / z

        rho = cos_ang + beta

        propagation_time = reflection_path_length.meters / c.meters_per_second
        rho *= np.sqrt(propagation_time * w)
        rho *= complex(0.5, 0.5)

        return rho

    @staticmethod
    def nominal_wind_speed(source_location, receiver_location, velocity, direction):
        """
        This determines the magnitude of a vector ont he vector pointing from the source to the receiver

        source_location : CartesianCoordinate
            the location of the source
        receiver_location : CartesianCoordinate
            the location of the receiver
        velocity : Speed
            the wind speed
        direction : Angle
            the direction of the wind vector

        returns : double
            the portion of the wind speed vector that is along the propagation path
        """
        if not isinstance(source_location, CartesianCoordinate):
            raise InvalidUnitOfMeasureException
        if not isinstance(receiver_location, CartesianCoordinate):
            raise InvalidUnitOfMeasureException
        if not isinstance(velocity, Speed):
            raise InvalidUnitOfMeasureException
        if not isinstance(direction, Angle):
            raise InvalidUnitOfMeasureException

        angle = np.arctan2(receiver_location.y.meters - source_location.y.meters,
                           receiver_location.x.meters - source_location.x.meters)
        vector_angle = np.arctan2(direction.cos(), direction.sin())

        return Speed(velocity.meters_per_second * np.cos(vector_angle - angle), Speed.Units.MetersPerSecond)

    @staticmethod
    def erfc(a):
        """
        The complex error function that is required for the determination of the excess ground attenuation.

        a : complex
            the independent variable to determine the complex error function value.

        returns : complex
            the value of the complex error function at a

        Remarks:
        2022-11-29 - FSM - Running the F-35 A data suggests that there may be instances where the calculation of P2 and
        Q2 may result in Infinite/NaN values
        """
        if isinstance(a, complex):
            x = a.real
            y = a.imag
            rho2 = a ** 2
            if x > 6.0 or y > 6.0:
                return complex(0, 1) * a * (0.5124242 / (rho2 - 0.2752551) + 0.05176536 / (rho2 - 2.724745))
            else:
                if x > 3.9 or y > 3.0:
                    w = 0.4613135 / (rho2 - 0.1901635)
                    w += (0.09999216 / (rho2 - 1.7844927))
                    w += (0.002883894 / (rho2 - 5.5253437))
                    w *= (complex(0, 1) * a)
                    return w
                else:
                    h = 0.8
                    A = np.cos(2 * x * y)
                    B = np.sin(2 * x * y)
                    C = np.exp(-2 * y * np.pi / h) - np.cos(2 * x * np.pi / h)
                    D = np.sin(2 * x * np.pi / h)
                    P2 = 2.0 * np.exp(-(x * x + (2.0 * y * np.pi / h) - y * y)) * ((A * C - B * D) /
                                                                                   (C * C + D * D))
                    Q2 = 2.0 * np.exp(-(x * x + (2.0 * y * np.pi / h) - y * y)) * ((A * D + B * C) /
                                                                                   (C * C + D * D))

                    if np.isinf(P2) or np.isinf(Q2):
                        raise ValueError("There is an issue determining the correct values for the curve fit for the "
                                         "complex error function")

                    H = 0
                    K = 0
                    for n in range(1, 5):
                        H += (2.0 * y * h / np.pi) * (np.exp(-n * n * h * h) * (y * y + x * x + n * n * h * h)) / (
                                ((y * y - x * x + n * n * h * h) ** 2.0) + 4 * y * y * x * x)
                        K += (2.0 * x * h / np.pi) * (np.exp(-n * n * h * h) * (y * y + x * x - n * n * h * h)) / (
                                ((y * y - x * x + n * n * h * h) ** 2.0) + 4 * y * y * x * x)
                    H += h * y / (np.pi * (y * y + x * x))
                    K += h * x / (np.pi * (y * y + x * x))

                    if y == np.pi / h:
                        H = H + 0.5 * P2
                        K = K - 0.5 * Q2
                    elif y < (np.pi / h):
                        H = H + P2
                        K = K - Q2
                    return complex(H, K)
