from setuptools import setup, find_packages

setup(
    name='selenium_simulate_ui',
    version='0.1.5',
    author='Des1r3',
    url='https://github.com/Des1r3/selenium_simulate_ui',
    description='The method to provide a simulated UI for taking screenshots with Selenium.',
    packages=find_packages(),
    install_requires=[
        'selenium',
        'pathlib',
        'attrs',
        'pillow',
        'datetime',
    ],
)