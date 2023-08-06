from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

    with open('HISTORY.md') as history_file:
        HISTORY = history_file.read()

        with open('LICENSE.txt') as license_file:
            LICENSE = license_file.read()

setup(
    name='physical_propagation',
    version='0.6.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY + '\n\n' + LICENSE,
    url='https://gitlab.com/physicalpropagation/physcial_propagation',
    license='MIT',
    author='Frank Mobley, Gregory Bowers, Alan T. Wall, S. Conner Campbell',
    author_email='frank.mobley.1@afrl.af.mil',
    description='A collection of code to determine how the acoustic levels propagating through the air will be altered',
    install_requires=['numpy', 'scipy', 'PythonCoordinates>=0.5.1', 'PyTimbre>=0.6.1']
)
