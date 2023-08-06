# ![Image](./Ghosteye.png "GhostEye") 
# Physical Propagation

For simplistic geometric acoustics we can use the information regarding the atmosphere and ground to determine nominal 
acoustic losses that a spherical wave would experience as the signal moves through the atmosphere. This code originated
in the calculation of equivalent sources that were created as part of the Acoustic Repropagation Technique [ART](https://pubs.aip.org/asa/jasa/article/127/3_Supplement/1834/683047/Acoustic-repropagation-technique-and-practical) that 
was developed as part of the Rotorcraft Noise Model. The same de-propagation methods were employed by the Swiss Federal 
Laboratories when they created a series of sources using [spherical harmonics](https://www.ingentaconnect.com/content/dav/aaua/2003/00000089/00000002/art00010).

The author of this package took these elements, originating with a variety of ANSI standards and Acoustical Society of 
America papers, and created a series of C++, Matlab, and C# codes to determine the nominal losses. These culminated in 
the author's [dissertation](https://www.proquest.com/openview/710a6e22398b280d3f900fbdf9b965e3/1?pq-origsite=gscholar&cbl=18750) regarding the de-propagation of measurements on a UH-1J (Huey).

This package contains acoustic losses for:
- Spherical spreading (divergence) of spherical waves
- [Atmospheric absorption](https://pubs.aip.org/asa/jasa/article-abstract/97/1/680/835919/Atmospheric-absorption-of-sound-Further?redirectedFrom=PDF)
- [Ground reflection](https://pubs.aip.org/asa/jasa/article-abstract/62/4/825/988530/Propagation-of-noise-along-a-finite-impedance)

An additional code is available to trace the [acoustic ray](https://www.sciencedirect.com/science/article/abs/pii/0022460X75902801#preview-section-cited-by) through a media defined by a series of horizontal and vertical
temperature & wind speed gradients.

This code is part of a series of packages that were developed from the C# codes for the purpose of providing a code 
base for continued creation of acoustic propagation and perception.

This code requires [PythonCoordinates](https://pypi.org/project/pythoncoordinates), a package with measurable objects to assist in the calculation of the physical 
losses and the location within the world and relative coordinates of the various objects.

