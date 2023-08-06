import numpy as np
from .acoustic_losses import Divergence, AtmosphericAbsorption, GroundImpedance, \
    ExcessGroundAttenuation
from PythonCoordinates.measurables.physical_quantities import Temperature, Pressure, Humidity, Length, Angle, Speed
from PythonCoordinates.measurables.physical_quantities import InvalidUnitOfMeasureException
from PythonCoordinates.coordinates.geospatial_coordinates import SourcePoint, GeospatialCoordinate
from pytimbre.spectral.fractional_octave_band import FractionalOctaveBandTools as fob


def propagate(source_point, receiver_location, field_temperature, field_pressure, field_humidity,
              surface_flow_resistivity, normalized_distance, normalized_temperature, normalized_pressure,
              normalized_humidity, frequencies=fob.tob_frequencies()):
    """
    This function determines the propagation losses using acoustic spreading, atmospheric absorption, and excess
    ground reflection to determine what level the source would be reduced by during travel through the atmosphere.

    This function is modeled after the MATLAB propagate script

    :param source_point - SourcePoint
        The location and attitude of the source of the acoustic signal
    :param receiver_location - CartesianCoordinate
        The location of the receiver based on geo-referenced models
    :param field_pressure - Pressure
        The measured atmospheric pressure at the time of the acoustic measurement
    :param field_temperature - Temperature
        The measured atmospheric temperature at the time of the acoustic measurement
    :param field_humidity - Humidity
        The measured relative humidity at the time of the acoustic measurement
    :param surface_flow_resistivity - double
        The signal parameter that defines the surface structure of the ground
    :param normalized_humidity - Humidity
        The desired normalized atmospheric relative humidity for the source description
    :param normalized_distance - Length
        The desired normalized radius for the source description
    :param normalized_pressure - Pressure
        The desired normalized atmospheric pressure for the source description
    :param normalized_temperature - Temperature
        The desired normalized atmospheric temperature for the source description
    :param frequencies - ndarrdy

    :returns dict
        The dictionary will contain the arrival time, the acoustic losses, and the spherical locations of the emissions
    """

    if (not isinstance(source_point, SourcePoint) or not isinstance(receiver_location, GeospatialCoordinate) or
            not isinstance(field_pressure, Pressure) or not isinstance(field_humidity, Humidity) or
            not isinstance(field_temperature, Temperature) or not isinstance(surface_flow_resistivity, float) or
            not isinstance(normalized_distance, Length) or not isinstance(normalized_pressure, Pressure) or
            not isinstance(normalized_humidity, Humidity) or not isinstance(normalized_temperature, Temperature)):
        InvalidUnitOfMeasureException("One or more of the inputs were not correctly formatted")

    #   Determine the geometry of the vector pointing from the source to the receiver as a function of the source index

    v = (receiver_location - source_point).to_body_reference()

    if isinstance(source_point, SourcePoint):
        v.orient_vector(source_point.heading, source_point.pitch, source_point.roll)

    v_sp = v.to_spherical()

    c = Speed.adiabatic_speed_of_sound(field_temperature)

    #   Determine the divergence loss

    sigma_div = Divergence.loss(normalized_distance, v_sp.r)

    r1, r2, psi = ExcessGroundAttenuation.determine_geometry(source_point, receiver_location)

    spl = np.zeros((len(frequencies),))
    for i in range(len(spl)):
        sigma_alpha = AtmosphericAbsorption.alpha(field_temperature, field_pressure, field_humidity,
                                                  frequencies[i]) * v_sp.r.meters

        sigma_normal_alpha = AtmosphericAbsorption.alpha(normalized_temperature, normalized_pressure,
                                                         normalized_humidity,
                                                         frequencies[i]) * normalized_distance.meters

        sigma_ega = ExcessGroundAttenuation.coherent_attenuation(r1,
                                                                 r2,
                                                                 psi,
                                                                 frequencies[i],
                                                                 GroundImpedance.delany_single_parameter(
                                                                     frequencies[i],
                                                                     surface_flow_resistivity),
                                                                 c)

        spl[i] = (sigma_normal_alpha - sigma_alpha) + sigma_div + sigma_ega

    return {"propagation_time": (v_sp.r / Speed.adiabatic_speed_of_sound(field_temperature)).total_seconds(),
            "polar": v_sp.polar,
            "azimuthal": v_sp.azimuthal,
            "distance": v_sp.r,
            "losses": spl}


def directivity_angle(tcp_alt: Length, tcp_offset: Length, aircraft_speed: Speed, field_temperature: Temperature,
                      time_closest_approach: float, time_max_noisiness: float):
    """
    This function calculations the directivity angle for the normalization procedure used to create the NOISEFILE
    sources.

    Parameters
    ----------
    tcp_alt: Length - the altitude at the time of closest approach of the aircraft to the measurement site
    tcp_offset: Length - the ground range from the aircraft to the source at the time of closest approach
    aircraft_speed: Speed - the velocity of the aircraft
    field_temperature: Temperature - the temperature at the time of the measurement, which is used to determine the
        speed of sound during the measurement
    time_closest_approach: float - the time in seconds past midnight of the time of closest approach
    time_max_noisiness: float - the time of the maximum noisiness spectrum

    Returns
    -------
    Angle - the angle of the maximum directivity from the nose of the aircraft.
    """

    #   Determine the slant propagation distance
    slant_distance = Length(np.sqrt(tcp_alt.meters ** 2 + tcp_offset.meters ** 2))

    #   Determine the time delta
    duration = time_closest_approach - time_max_noisiness

    #   Calculate the adiabatic speed of sound
    c0 = Speed.adiabatic_speed_of_sound(field_temperature)

    #   Determine the distance correction for elements approaching mach 1
    distance_correction = 1 - (aircraft_speed.meters_per_second / c0.meters_per_second) ** 2

    #   Build the argument of the arcsine function
    numerator = distance_correction * slant_distance.meters ** 2
    denominator = numerator**2 / distance_correction
    denominator += (aircraft_speed.meters_per_second * duration)**2
    denominator = np.sqrt(denominator)
    denominator -= (duration * aircraft_speed.meters_per_second **2) / c0.meters_per_second

    argument = numerator / denominator

    if duration > (slant_distance / c0).total_seconds():
        return Angle(180) - Angle.acos(argument)
    else:
        return Angle(np.arcsin(argument), Angle.Units.Radians)


def normalize_sound_pressure_level(closet_approach_height: Length,
                                   closet_approach_offset: Length,
                                   time_closest_approach: float,
                                   time_max_noisiness: float,
                                   spl: np.ndarray,
                                   frequency: np.ndarray,
                                   temperature: Temperature,
                                   pressure: Pressure,
                                   humidity: Humidity,
                                   velocity: Speed,
                                   reference_distance: Length = Length(1000, Length.Units.Feet),
                                   reference_temperature: Temperature = Temperature.ref_temperature(),
                                   reference_pressure: Pressure = Pressure.ref_pressure(),
                                   reference_humidity: Humidity = Humidity.std_humidity(),
                                   reference_speed: Speed = Speed(125, Speed.Units.Knots)):
    """
    This function calculate the normalization of the maximum perceived noise level spectrum using the field and
    reference conditions for the atmosphere and propagation distances. This function also determines various other
    normalization parameters required for the generation of the Omega 10 input dataset.

    This code is adapted from a Matlab conversion of a C++ code written in VS2008 to normalize the community noise
    datasets.

    Author: Dr. Frank Mobley

    Parameters
    ----------
    closet_approach_height: Length - the height of the aircraft above the measurement site at the time of closest
        approach
    closet_approach_offset: Length - the ground offset from the aircraft at the time of closest approach
    time_closest_approach: float - the time in seconds past midnight of the closet approach of the aircraft
    time_max_noisiness: float - the time of the maximum noisiness of the over-flight time history
    spl: np.ndarray - the array of sound pressure level values that are normalized
    frequency: np.ndarray - the collection of frequencies that we want to process the sound pressure level at
    temperature: Temperature - the temperature average around the time of closet approach
    pressure: Pressure - the pressure average around the time of closest approach
    humidity: Humidity - the average humidity around the time of the closest approach
    velocity: Speed - the average speed of the aircraft around the time of closest approach
    reference_distance: Length - the distance to normalize the sound pressure level to
    reference_temperature: Temperature - the normalization temperature
    reference_pressure: Pressure - the normalization pressure
    reference_humidity: Humidity - the normalization humidity
    reference_speed: Speed - the normalization speed

    Returns
    -------
    dictionary with:
    normal_spl: np.ndarray - the normalized sound pressure levels
    atmos_spl: np.ndarray - the atmospheric absorption spectrum
    div_spl: np.ndarray - the array of spherical spreading
    d2: float - the speed correction
    """
    from .acoustic_losses import Divergence, AtmosphericAbsorption

    #   Calculate the directivity angle
    theta = directivity_angle(closet_approach_height,
                              closet_approach_offset,
                              velocity,
                              temperature,
                              time_closest_approach,
                              time_max_noisiness)

    #   Calculate the slant distance from the aircraft to the microphone
    slant_distance = Length(np.sqrt(closet_approach_offset.meters**2 + closet_approach_height.meters**2),
                            Length.Units.Meters)
    d5 = Divergence.loss(reference_distance, slant_distance)

    #   Calculate the speed correction
    d2 = -0.3 * d5 * 10.0 * np.log10(velocity.meters_per_second / reference_speed.meters_per_second)

    #   Calculate the atmospheric absorption correction spectrum
    alpha_field = AtmosphericAbsorption.alpha(temperature, pressure, humidity, frequency)
    alpha_ref = AtmosphericAbsorption.alpha(reference_temperature, reference_pressure, reference_humidity, frequency)
    atmos_spl = (slant_distance.meters * alpha_field - reference_distance.meters * alpha_ref)/theta.sin()

    normal_spl = spl + atmos_spl + d5

    return {'normal_spl': normal_spl, 'atmos_spl': atmos_spl, 'div_spl': d5, 'd2': d2, 'directivity': theta}
